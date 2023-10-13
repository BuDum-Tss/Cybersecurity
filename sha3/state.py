
class State:
    def __init__(self):
        self.state = bytearray(5*5*8)

    def get_bit(self, x, y, z):
        index = (x + y * 5) * 64 + z
        byte_index = index // 8
        bit_index = index % 8
        return (self.state[byte_index] >> bit_index) & 1

    def set_bit(self, x, y, z, value):
        index = (x + y * 5) * 64 + z
        byte_index = index // 8
        bit_index = index % 8
        if value:
            self.state[byte_index] |= (1 << bit_index)
        else:
            self.state[byte_index] &= ~(1 << bit_index)

    def print(self, text):
        print(text + self.state.hex())

    def xor(self, data:bytearray):
        for i in range(len(data)):
            self.state[i] ^= data[i]

    def squeeze(self, n):
        return self.state[:n]