class LinearBuffer():

    def __init__(self, size : int):
        self.__max_size = size
        self.__alloc_size = 0
        self.__buffer = bytearray(size)

    def __del__(self):
        pass

    def append(self, buffer):
        size = len(buffer)
        if (self.__alloc_size + size > self.__max_size):
            return False
        self.__memcpy(self.__buffer, self.__alloc_size,
                      buffer, size)
        self.__alloc_size += size
        return True

    def append_byte(self, byte):
        size = 1
        if (self.__alloc_size + size > self.__max_size):
            return False
        self.__buffer[self.__alloc_size] = byte
        self.__alloc_size += size
        return True

    def clear(self):
        for i in range(0, self.__max_size):
            self.__buffer[i] = 0x00
        self.__alloc_size = 0

    def reset(self):
        self.__alloc_size = 0
        
    def get(self):
        return memoryview(self.__buffer)

    def get_null_terminated(self):
        for i in range(0, self.__max_size):
            if (self.__buffer[i] == 0x00):
                return memoryview(self.__buffer[0:i])
        return memoryview(self.__buffer)

    def size(self):
        return self.__alloc_size

    def max_size(self):
        return self.__max_size

    def __memcpy(self, dest, dest_idx, source, size):
        for i in range(0, size):
            dest[dest_idx + i] = source[i]
