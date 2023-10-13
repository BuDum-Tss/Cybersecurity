import numpy as np
from state import State

class Sha3():
    RC = [
    bytearray(b'\x01\x00\x00\x00\x00\x00\x00\x00'),
    bytearray(b'\x82\x80\x00\x00\x00\x00\x00\x00'),
    bytearray(b'\x8a\x80\x00\x00\x00\x00\x00\x80'),
    bytearray(b'\x00\x80\x00\x80\x00\x00\x00\x80'),
    bytearray(b'\x8b\x80\x00\x00\x00\x00\x00\x00'),
    bytearray(b'\x01\x00\x00\x80\x00\x00\x00\x00'),
    bytearray(b'\x81\x80\x00\x80\x00\x00\x00\x80'),
    bytearray(b'\t\x80\x00\x00\x00\x00\x00\x80'),
    bytearray(b'\x8a\x00\x00\x00\x00\x00\x00\x00'),
    bytearray(b'\x88\x00\x00\x00\x00\x00\x00\x00'),
    bytearray(b'\t\x80\x00\x80\x00\x00\x00\x00'),
    bytearray(b'\n\x00\x00\x80\x00\x00\x00\x00'),
    bytearray(b'\x8b\x80\x00\x80\x00\x00\x00\x00'),
    bytearray(b'\x8b\x00\x00\x00\x00\x00\x00\x80'),
    bytearray(b'\x89\x80\x00\x00\x00\x00\x00\x80'),
    bytearray(b'\x03\x80\x00\x00\x00\x00\x00\x80'),
    bytearray(b'\x02\x80\x00\x00\x00\x00\x00\x80'),
    bytearray(b'\x80\x00\x00\x00\x00\x00\x00\x80'),
    bytearray(b'\n\x80\x00\x00\x00\x00\x00\x00'),
    bytearray(b'\n\x00\x00\x80\x00\x00\x00\x80'),
    bytearray(b'\x81\x80\x00\x80\x00\x00\x00\x80'),
    bytearray(b'\x80\x80\x00\x00\x00\x00\x00\x80'),
    bytearray(b'\x01\x00\x00\x80\x00\x00\x00\x00'),
    bytearray(b'\x08\x80\x00\x80\x00\x00\x00\x80')]
    
    def __init__(self, output_length, rate, capacity) -> None:
        self.output_length = output_length
        self.rate = rate
        self.capacity = capacity

    def hash(self, data): 
        return self.sponge_construction(data).squeeze(self.output_length//8)
    
    def sponge_construction(self, data:bytearray):
        state = State()
        self.pad(data)
        for block in self.split_into_blocks(data, 136):
            state.xor(block)
            state = self.permutation_function(state)
        return state
    
    def split_into_blocks(self, data:bytearray, size:int):
        return [data[i:i + size] for i in range(0, len(data), size)]
    
    def permutation_function(self, state:State):
        for round in range(24):
            state = self.theta(state)
            state = self.rho(state)
            state = self.pi(state)
            state = self.chi(state)
            state = self.iota(state, self.RC[round])
        return state
    
    def pad(self, data:bytearray):
        if (len(data)%136==135): #136 * 8 = 1088
            data.extend(bytes([0b10000110]))
        else:
            data.extend(bytes([0b00000110]))
            data.extend([0]*((-len(data)-1)%136))
            data.extend(bytes([0b10000000]))

    def theta(self, state:State):
        A_prime = State()
        C = np.zeros((5, 64), dtype=np.uint8)
        for x in range(5):
            for z in range(64):
                for y in range(5):
                    C[x][z] ^= state.get_bit(x, y, z)

        for x in range(5):
            for z in range(64):
                D = C[(x-1) % 5][z] ^ C[(x+1) % 5][(z-1) % 64]
                for y in range(5):
                    new_bit = state.get_bit(x, y, z) ^ D
                    A_prime.set_bit(x, y, z, new_bit)
        return A_prime
          
    def rho(self, state:State):
        A_prime = State()
        
        for z in range(64):
            A_prime.set_bit(0, 0, z, state.get_bit(0, 0, z))
        x, y = 1, 0

        for t in range(24):
            for z in range(64):
                new_z = (z - ((t + 1) * (t + 2) // 2)) % 64
                A_prime.set_bit(x, y, z, state.get_bit(x, y, new_z))
            x, y = y, ((2 * x + 3 * y) % 5)
            
        return A_prime
    
    def pi(self, state:State):
        A_prime = State()

        for x in range(5):
            for y in range(5):
                new_x = (x + 3 * y) % 5
                for z in range(64):    
                    A_prime.set_bit(x, y, z, state.get_bit(new_x, x, z))
        return A_prime

    def chi(self, state:State):
        A_prime = State()

        for x in range(5):
            for y in range(5):
                for z in range(64):
                    A_prime.set_bit(x, y, z, state.get_bit(x, y, z) ^ ((state.get_bit((x + 1) % 5, y, z) ^ 1) & state.get_bit((x + 2) % 5, y, z)))

        return A_prime
    
    def iota(self, state:State, round_constant:bytearray):
        state_prime = state

        for z in range(64):
            byte_index = z // 8
            bit_index = z % 8
            rc_bit = (round_constant[byte_index] >> bit_index) & 1
            state_prime.set_bit(0, 0, z, state_prime.get_bit(0, 0, z) ^ rc_bit)

        return state_prime