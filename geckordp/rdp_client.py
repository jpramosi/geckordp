import asyncio
import socket
from enum import Enum
from threading import Thread, Lock, get_ident
from collections import defaultdict
import json
import concurrent.futures
from typing import List, Dict
from concurrent.futures import Future, ThreadPoolExecutor
from jmespath import search as get_nested_value
from geckordp.settings import GECKORDP
from geckordp.logger import log, dlog, elog
from geckordp.buffers import LinearBuffer
from geckordp.actors.events import Events
from geckordp.utils import ExpireAt


class RDPClient():

    __ENCODING = "utf-8"
    __READ_SINGLE_DIGITS = 10
    __MAX_READ_SIZE = 65536
    __NUMBER_LUT = bytes([0x30, 0x31, 0x32, 0x33, 0x34,
                          0x35, 0x36, 0x37, 0x38, 0x39])

    class _HandlerEntry():

        def __init__(self, handler, is_async: bool):
            self.handler = handler
            self.is_async = is_async

    def __init__(
            self,
            timeout_sec=3,
            max_buffer_size=33554432,
            executor_workers=3):
        """ Initializes an instance of the remote debug protocol client.

        Args:
            timeout_sec (int, optional): The timeout for a response in seconds. Defaults to 3.
            max_buffer_size (int, optional): The maximum size of the read buffer. 
                                             High values are only required for large data 
                                             such as screenshots or raw html. Defaults to ~33mb.
            executor_workers (int, optional): The amount of executor workers which are used for event handling. Defaults to 3.
        """
        self.__timeout_sec = timeout_sec
        self.__mtx = Lock()
        self.__connect_mtx = Lock()
        self.__loop = asyncio.new_event_loop()
        self.__loop_thread = None
        self.__thread_id = 0
        self.__reader = None
        self.__writer = None
        self.__connected = False
        self.__dc_fut = None
        self.__read_task = None
        self.__cached_response = ""
        self.__cached_buffer_read = 0
        self.__cached_total_size = 0
        self.__current_handler = None
        self.__digits_buffer = LinearBuffer(RDPClient.__READ_SINGLE_DIGITS)
        self.__read_buffer = LinearBuffer(max_buffer_size)
        self.__registered_events = set()
        self.__await_request_fut = Future()
        self.__await_request_id = ""
        self.__workers = ThreadPoolExecutor(executor_workers)

        self.__event_handlers_mtx = Lock()
        self.__event_handlers: Dict[str, Dict[str, List[RDPClient._HandlerEntry]]] = defaultdict(
            lambda: defaultdict(list))

        self.__actor_handlers_mtx = Lock()
        self.__actor_handlers: Dict[str, List[RDPClient._HandlerEntry]] = defaultdict(
            list)

        self.__register_events()

    def __del__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @property
    def timeout_sec(self) -> int:
        """ Returns the timeout in seconds.

        Returns:
            int: The timeout.
        """
        return self.__timeout_sec

    def add_actor_listener(self, actor_id: str, handler) -> bool:
        """ Appends a listener for a specific actor.
        Multiple handlers can be added for each event type.

        .. warning::
            Called functions within manually registered **async** handlers on RDPClient
            can not call functions which emits :func:`~geckordp.rdp_client.RDPClient.request_response` later in its execution path
            (instead use non-async handlers in this case)

        Args:
            actor_id (str): The actor ID.
            handler (any): The handler to call on match. 
                           Can be either async (executed with coroutine)
                           or a common function (queued to executor).

        Returns:
            bool: True: Handler registered; False: Handler already registered
        """
        with self.__actor_handlers_mtx:
            return self.__add_actor_listener(actor_id, handler)

    def __add_actor_listener(self, actor_id: str, handler) -> bool:
        handler_entries = self.__actor_handlers[actor_id]
        for handler_entry in handler_entries:
            if (handler_entry.handler == handler):
                return False
        handler_entries.append(
            RDPClient._HandlerEntry(handler, asyncio.iscoroutinefunction(handler)))
        return True

    def remove_actor_listener(self, actor_id: str, handler):
        """ Removes a listener with the specified actor ID.

        Args:
            actor_id (str): The ID to find.
            handler ([type]): The handler to remove.
        """
        with self.__actor_handlers_mtx:
            self.__remove_actor_listener(actor_id, handler)

    def __remove_actor_listener(self, actor_id: str, handler):
        if (not actor_id in self.__actor_handlers):
            return
        for entry in self.__actor_handlers[actor_id]:
            if (entry.handler == handler):
                self.__actor_handlers[actor_id].remove(entry)
                return

    def add_event_listener(self, actor_id: str, event, handler) -> bool:
        """ Appends a listener for a specific actor and event.
        Multiple handlers can be added for each event type.

        .. warning::
            Called functions within manually registered **async** handlers on RDPClient
            can not call functions which emits :func:`~geckordp.rdp_client.RDPClient.request_response` later in its execution path
            (instead use non-async handlers in this case)

        Args:
            actor_id (str): The actor ID.
            event_type (Enum/str): The event type. See /actors/events.py
            handler (any): The handler to call on match. 
                           Can be either async (executed with coroutine)
                           or a common function (queued to executor).

        Returns:
            bool: True: Handler registered; False: Handler already registered
        """
        with self.__event_handlers_mtx:
            return self.__add_event_listener(actor_id, event, handler)

    def __add_event_listener(self, actor_id: str, event, handler) -> bool:
        event_name = event
        if (isinstance(event, Enum)):
            event_name = event.value

        handler_entries = self.__event_handlers[event_name][actor_id]
        for handler_entry in handler_entries:
            if (handler_entry.handler == handler):
                return False

        handler_entries.append(
            RDPClient._HandlerEntry(handler, asyncio.iscoroutinefunction(handler)))
        if (GECKORDP.DEBUG_EVENTS):
            self.__print_event_handlers("__add_event_listener")
        return True

    def remove_event_listener(self, actor_id: str, event, handler):
        """ Removes a listener with the specified actor ID and event.

        Args:
            actor_id (str): The actor ID.
            event_type (Enum/str): The event type. See /actors/events.py
            handler (any): The handler to remove.
        """
        with self.__event_handlers_mtx:
            self.__remove_event_listener(actor_id, event, handler)

    def __remove_event_listener(self, actor_id: str, event, handler):
        event_name = event
        if (isinstance(event, Enum)):
            event_name = event.value

        actors = self.__event_handlers.get(event_name, None)
        if (actors == None):
            return

        handler_entries = actors.get(actor_id, None)
        if (handler_entries == None):
            return

        for entry in handler_entries:
            if (entry.handler == handler):
                handler_entries.remove(entry)
                break

        if (len(handler_entries) == 0):
            actors.pop(actor_id, None)

        if (GECKORDP.DEBUG_EVENTS):
            self.__print_event_handlers("__remove_event_listener")

    def remove_event_listeners_by_id(self, actor_id: str):
        """ Removes all callback handlers by actor ID.

        Args:
            actor_id (Enum/str): The actor ID.
        """
        with self.__event_handlers_mtx:
            for _event_name, handler_entries in self.__event_handlers.items():
                try:
                    handler_entries.pop(actor_id, None)
                    dlog(f"actor '{actor_id}' removed with its handlers")
                except KeyError:
                    pass
            if (GECKORDP.DEBUG_EVENTS):
                self.__print_event_handlers("remove_event_listeners_by_id")

    def connected(self) -> bool:
        """ Check whether the client is currently connected to the server.

        Returns:
            bool: True: Connected; False: Disconnected
        """
        with self.__mtx:
            return self.__connected

    def connect(self, host: str, port: int) -> dict:
        """ Connects to the firefox debug server.

        Args:
            host (str): The host to connect to, usually 'localhost'
            port (int): The port to use, default '6000'

        Returns:
            dict/None: The server response on successful established connection.
        """
        with self.__mtx:
            if (self.__connected):
                return None
            dlog("")
            self.__await_request_id = "root"
            self.__await_request_fut = Future()
            self.__loop_thread = Thread(
                target=self.__connect, args=[host, port])
            self.__loop_thread.start()
            try:
                return self.__await_request_fut.result(self.__timeout_sec)
            except:
                dlog("Timeout")
                if (len(asyncio.all_tasks(self.__loop)) > 0):
                    dlog("Cancel read")
                    self.__loop.call_soon_threadsafe(
                        asyncio.ensure_future, self.__disconnect())
            return None

    def __connect(self, host: str, port: int):
        if (self.__loop.is_running()):
            log("Queue is already running")
            return
        dlog("Queue read task")
        self.__read_task = self.__loop.create_task(
            self.__open_connection(host, port))
        self.__read_task.add_done_callback(self.__on_close_connection)
        try:
            dlog("Run IO loop")
            self.__loop.run_until_complete(self.__read_task)
        except socket.gaierror as e:
            elog(f"{e}")
        except concurrent.futures._base.CancelledError:
            dlog("Read task cancelled: futures")
        except asyncio.exceptions.CancelledError:
            dlog("Read task cancelled: asyncio")

    async def __open_connection(self, host: str, port: int):
        dlog("Try to open connection")
        try:
            self.__reader = asyncio.StreamReader(
                limit=RDPClient.__MAX_READ_SIZE, loop=self.__loop)
            protocol = asyncio.StreamReaderProtocol(
                self.__reader, loop=self.__loop)
            transport, _ = await self.__loop.create_connection(
                lambda: protocol, host, port)
            self.__writer = asyncio.StreamWriter(
                transport, protocol, self.__reader, self.__loop)
        except ConnectionRefusedError as e:
            elog(e)
            return
        dlog("Start listening")
        self.__connected = True
        self.__thread_id = get_ident()
        await self.__read_loop()

    def __on_close_connection(self, _future):
        try:
            dlog("Stop listening")
            self.__connected = False
            self.__dc_fut.set_result(1)
        except:
            pass

    def disconnect(self):
        """ Disconnects from the debug server.
        """
        with self.__mtx:
            if (not self.__connected):
                return
            dlog("")
            self.__dc_fut = Future()
            self.__loop.call_soon_threadsafe(
                asyncio.ensure_future, self.__disconnect())
            try:
                self.__dc_fut.result(0.2)
                return
            except:
                dlog("Timeout")
            return

    async def __disconnect(self):
        dlog(self.__connected)
        self.__read_task.cancel()

    def request(self,  msg: dict):
        """ Starts sending a request without waiting for a response.
            The dict message will be transformed to a utf-8 json string.

        Args:
            msg (dict): The message to send.

        """
        with self.__mtx:
            if (not self.__connected):
                elog(f"Not connected on request:\n{msg}")
                return False
            dlog("")
            if (not "to" in msg):
                raise ValueError("parameter 'msg' must contain 'to' field")
            if (get_ident() == self.__thread_id):
                return self.__async_request(msg)
            return self.__sync_request(msg)

    async def __async_request(self,  msg: dict) -> dict:
        dlog("")
        return await self.__request(msg)

    def __sync_request(self,  msg: dict) -> dict:
        dlog("")
        self.__loop.call_soon_threadsafe(
            asyncio.ensure_future, self.__request(msg))
        return True

    def request_response(self,  msg: dict, extract_expression=""):
        """ Starts sending a request and waiting for a response.
            The dictionary message will be transformed to a utf-8 json string.
            The timeout can be specified in the class its constructor.

        Args:
            msg (dict): The message to send.

        Returns:
            dict/None/coroutine: The response from the server.
        """
        with self.__mtx:
            if (not self.__connected):
                elog(f"Not connected on request:\n{msg}")
                return None
            if (not "to" in msg):
                raise ValueError("parameter 'msg' must contain 'to' field")
            if (get_ident() == self.__thread_id):
                return self.__async_request_response(msg, extract_expression)
            return self.__sync_request_response(msg, extract_expression)

    async def __async_request_response(self,  msg: dict, extract_expression: str):
        dlog("")
        fut = Future()
        await self.__request(msg, fut)

        # read in loop to allow other messages to pass
        exp = ExpireAt(self.__timeout_sec)
        while exp:
            timeout_sec = self.__timeout_sec - exp.expired_time()
            if (timeout_sec <= 0):
                break
            try:
                await asyncio.wait_for(
                    self.__loop.create_task(self.__read(False)),
                    timeout_sec,
                    loop=self.__loop)
            except:
                break
            if (fut.done()):
                break

        # get response
        if (fut.done()):
            try:
                response = fut.result(0)
                if ("error" in response):
                    elog(
                        f"Error on request:\n{msg}\n{json.dumps(response, indent=2)}")
                if (extract_expression == ""):
                    return response
                extracted = get_nested_value(extract_expression, response)
                if (extracted == None):
                    return response
                return extracted
            except:
                elog(f"No response on request:\n{msg}")
                return None
        else:
            elog(f"Timeout on request:\n{msg}")
            return None

    def __sync_request_response(self,  msg: dict, extract_expression: str) -> dict:
        dlog("")
        fut = Future()
        self.__loop.call_soon_threadsafe(
            asyncio.ensure_future, self.__request(msg, fut))
        try:
            response = fut.result(
                self.__timeout_sec)
            if ("error" in response):
                elog(
                    f"Error on request:\n{msg}\n{json.dumps(response, indent=2)}")
            if (extract_expression == ""):
                return response
            extracted = get_nested_value(extract_expression, response)
            if (extracted == None):
                return response
            return extracted
        except:
            elog(f"Timeout on request:\n{msg}")
            return None

    async def __request(self, msg: dict, fut=None):
        self.__await_request_id = msg["to"]
        if (fut != None):
            self.__await_request_fut = fut
        msg = json.dumps(msg, separators=(',', ':'))
        if (GECKORDP.DEBUG_REQUEST):
            log(f"REQUEST->\n{len(msg)}:{msg}")
        self.__writer.write(
            bytes(f"{len(msg)}:{msg}", encoding=RDPClient.__ENCODING))
        await self.__writer.drain()

    async def __read_loop(self):
        while True:
            if (not await self.__read(True)):
                break

    async def __read(self, lock: bool):
        # read a few single digits to get the actual size of the response:
        # at the beginning of every server message there is a size indicator
        # it does look like this:
        # 196:{"x":"y"}
        payload_size = 0
        self.__digits_buffer.clear()
        for _ in range(0, RDPClient.__READ_SINGLE_DIGITS):
            # read just a byte, this will "block" until a message arrives
            byte = (await self.__reader.read(1))
            if (len(byte) <= 0):
                elog(
                    f"No bytes read, connection is probably closed")
                return False
            # if byte is a digit, store it for later usage
            byte = byte[0]
            if (self.__is_numeric(byte)):
                self.__digits_buffer.append_byte(byte)
                continue
            # if byte is a colon, the payload size string is finished
            if (byte == 0x3a):  # ":"
                self.__digits_buffer.append_byte(byte)
                payload_size = int(self.__digits_buffer.get(
                ).tobytes().decode(encoding="utf-8").split(':', 1)[0])
                break
            # if execution flow arrives here, it means there's no size indicator
            # and the message probably may have a very large size
            read_size_str = self.__digits_buffer.get(
            ).tobytes().decode(encoding="utf-8")
            elog(f"invalid size indicator starts with '{read_size_str}'")
            break

        # this shouldn't happen except the size inidcator exceeds __READ_SINGLE_DIGITS
        if (payload_size == 0):
            elog(
                f"could not read size indicator, probably too large")
            return False

        # after payload is received, read the remaining message
        bytes_read = 0
        self.__read_buffer.reset()
        while bytes_read < payload_size:

            # truncate read size, else it will leak into the next message
            trunc_read_size = payload_size - bytes_read
            # the passed max limit to streamreader doesn't seem to take effect here
            if (trunc_read_size > RDPClient.__MAX_READ_SIZE):
                trunc_read_size = RDPClient.__MAX_READ_SIZE

            read_bytes = (await self.__reader.read(trunc_read_size))
            read_bytes_size = len(read_bytes)
            if (read_bytes_size == 0):
                elog(f"EOF remote host probably closed")
                return False

            bytes_read += read_bytes_size
            if (not self.__read_buffer.append(read_bytes)):
                elog(
                    f"""
                    buffer overflow while appending response: buffer is too small\n
                    buffer:{self.__read_buffer.size()}\nresponse:{read_bytes_size}
                    """)
                return False

            if (bytes_read < payload_size):
                dlog(f"read more data ({bytes_read} < {payload_size})")
            elif (bytes_read == payload_size):
                dlog(f"message complete ({bytes_read} == {payload_size})")
            elif (bytes_read > payload_size):
                dlog(f"message corrupted ({bytes_read} > {payload_size})")

        # add null termination else 'get_null_terminated()' won't work correctly
        if (not self.__read_buffer.append_byte(0x00)):
            elog(f"buffer overflow while appending null termination")
            return False

        # get string representation of bytes
        json_response = self.__read_buffer.get_null_terminated(
        ).tobytes().decode(encoding="utf-8")

        # load json string to dictionary
        response = None
        try:
            response = json.loads(json_response, strict=False)
        except:
            elog(
                f"couldn't load json response as dictionary:\n'{json_response}'")
            return True
        if (GECKORDP.DEBUG_RESPONSE):
            log(f"RESPONSE<-\n{json.dumps(response, indent=2)}")

        # check required response fields
        from_actor = response.get("from", None)
        if (not from_actor):
            elog(
                f"'from' field doesn't exist in response:\n{json.dumps(response, indent=2)}")
            return True

        # handle actor handlers
        await self.__handle_actors(response, from_actor, lock)

        # check if listener event
        if (await self.__handle_events(response, from_actor, lock)):
            return True

        # handle single request
        self.__handle_single_request(response, from_actor)

        return True

    async def __handle_actors(self, response: dict, from_actor: str, lock: bool):
        if (lock):
            self.__actor_handlers_mtx.acquire()
        try:
            entries = self.__actor_handlers.get(from_actor, None)
            if (entries == None):
                return
            await self.__process_callback_handlers(response, entries)
        finally:
            if (lock):
                self.__actor_handlers_mtx.release()

    async def __handle_events(self, response: dict, from_actor: str, lock: bool):
        event_type = response.get("type", None)
        if (event_type == None):
            return False
        if (GECKORDP.DEBUG_EVENTS):
            log(f"EVENT:\n{json.dumps(response, indent=2)}")
        if (lock):
            self.__event_handlers_mtx.acquire()
        try:
            actors = self.__event_handlers.get(event_type, None)
            if (actors):
                entries = actors.get(from_actor, None)
                if (entries):
                    await self.__process_callback_handlers(response, entries)
                    dlog(f"[{from_actor}][{event_type}] handled")
                return True
        finally:
            if (lock):
                self.__event_handlers_mtx.release()

        if (event_type in self.__registered_events):
            dlog(f"unhandled event received")
            return True
        return False

    async def __process_callback_handlers(self, response: dict, entries):
        for entry in entries:
            if (not entry.handler):
                continue
            if (entry.is_async):
                if (self.__current_handler != None):
                    dlog("break recursion")
                    continue
                self.__current_handler = entry.handler
                await entry.handler(response)
                self.__current_handler = None
            else:
                self.__loop.run_in_executor(
                    self.__workers, entry.handler, response)

    def __handle_single_request(self, response: dict, from_actor: str):
        if (self.__await_request_fut == None or from_actor != self.__await_request_id):
            return
        try:
            dlog("response valid, set result")
            self.__await_request_fut.set_result(response)
        except:
            pass

    def __register_events(self):
        for name, value in Events.__dict__.items():
            if ("enum" in str(value)):
                event_type = getattr(Events, name)
                for event in event_type:
                    self.__registered_events.add(event.value)

    def __is_numeric(self, byte):
        return byte in RDPClient.__NUMBER_LUT

    def __print_event_handlers(self, name: str):
        log(f"____________________________{name}")
        for event_name, handler_entries in self.__event_handlers.items():
            log(f"event:{event_name}:")
            for actor, handler in handler_entries.items():
                log(f"\tactor:{actor} handlers:{len(handler)}")
