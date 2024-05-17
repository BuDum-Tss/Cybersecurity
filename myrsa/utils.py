import math
from random import getrandbits
from sympy import isprime


def generate_odd_number(length: int) -> int:
    p = getrandbits(length)
    p |= (1 << length - 1) | 1
    return p


def generate_prime_number(number: int):
    x = 4
    while not isprime(x):
        x = generate_odd_number(number)
    return x


def bytes_to_blocks(raw_bytes: bytes, block_length: int) -> list[int]:
    return [int.from_bytes(raw_bytes[i: i + block_length], 'little') for i in range(0, len(raw_bytes), block_length)]


def blocks_to_bytes(blocks: list[int]) -> bytes:
    array = bytearray()
    for block in blocks:
        array.extend(block.to_bytes(math.ceil(block.bit_length() / 8), 'little'))
    return bytes(array)


def split_to_blocks(message: bytes, block_size: int) -> [bytes]:
    return [message[i:i + block_size] for i in range(0, len(message), block_size)]
