# pylint: disable=unused-import
import pytest
import tests.helpers.utils as utils
import tests.helpers.constants as constants
from geckordp.buffers import LinearBuffer


def append(buffer):
    bytes0 = bytes([0x68])           # h
    assert buffer.append(bytes0)

    bytes0 = bytes([0xc3, 0x88])     # È
    assert buffer.append(bytes0)

    bytes0 = bytearray(1)            # l
    bytes0[0] = 0x6c
    assert buffer.append(bytes0)

    assert buffer.append_byte(0x6c)  # l

    bytes0 = bytes([0x6f])           # o
    assert buffer.append(bytes0)

    bytes0 = bytes([0x00])           # \0
    assert buffer.append(bytes0)

    bytes0 = bytes([0x78])           # x
    assert buffer.append(bytes0)


def test_linear_buffer_append_get():
    buffer = LinearBuffer(11)
    append(buffer)
    # note: decode doesn't handle null termination
    string = buffer.get().tobytes().decode(
        encoding="utf-8").split('\0', 1)[0]
    assert string == "hÈllo"


def test_linear_buffer_append_get_null_terminated():
    buffer = LinearBuffer(11)
    append(buffer)
    string = buffer.get_null_terminated().tobytes().decode(
        encoding="utf-8")
    assert string == "hÈllo"


def test_linear_buffer_reappend_address():
    buffer = LinearBuffer(11)
    append(buffer)
    address1 = hex(id(buffer.get()[5]))  # o
    buffer.clear()
    append(buffer)
    address2 = hex(id(buffer.get()[5]))  # o
    assert address1 == address2


def test_linear_buffer_max_size():
    buffer = LinearBuffer(11)
    assert buffer.max_size() == 11


def test_linear_buffer_size():
    buffer = LinearBuffer(11)

    assert buffer.size() == 0
    append(buffer)
    assert buffer.size() == 8
    buffer.clear()
    assert buffer.size() == 0


def test_linear_buffer_clear():
    buffer = LinearBuffer(11)
    append(buffer)
    buffer.clear()

    data = buffer.get()
    size = buffer.max_size()
    for i in range(0, size):
        assert data[i] == 0


def test_linear_buffer_reset():
    buffer = LinearBuffer(11)

    append(buffer)
    assert buffer.size() == 8
    buffer.reset()
    assert buffer.size() == 0

    # note: alloc pointer is just set to zero = no data wipe,
    # however the data is not valid anymore at this point
    data = buffer.get()
    size = buffer.max_size()

    # note: decode doesn't handle null termination
    string = data.tobytes().decode(
        encoding="utf-8").split('\0', 1)[0]

    assert string == "hÈllo"

    for i in range(8, size):
        assert data[i] == 0
