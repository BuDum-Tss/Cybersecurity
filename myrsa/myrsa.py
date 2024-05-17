import hashlib
import math
import random

import utils

DEFAULT_EXPONENT = math.e

Key = (int, int)
PublicKey = Key
PrivateKey = Key


def newkeys(nbits: int) -> tuple[PublicKey, PrivateKey]:
    p = utils.generate_prime_number(nbits // 2)
    q = utils.generate_prime_number(nbits // 2)
    while p == q:
        q = utils.generate_prime_number(nbits // 2)

    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = random.randint(2, phi_n - 1)

    while math.gcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)

    d = pow(e, -1, phi_n)
    return (e, n), (d, n)


def encrypt(message: bytes, public_key: PublicKey):
    e, n = public_key
    block_length = (n.bit_length() - 1) // 8
    numbers = utils.bytes_to_blocks(message, block_length)
    output = []
    for number in numbers:
        r = pow(number, e, n)
        output.append(r)
    return utils.blocks_to_bytes(output)


def decrypt(encrypted_message: bytes, private_key: PrivateKey):
    d, n = private_key
    block_length = (n.bit_length() - 1) // 8 + 1
    numbers = utils.bytes_to_blocks(encrypted_message, block_length)
    output = []
    for number in numbers:
        r = pow(number, d, n)
        output.append(r)
    return utils.blocks_to_bytes(output)


HASH_METHODS = {
    'MD5': hashlib.md5,
    'SHA3-256': hashlib.sha3_256,
    'SHA3-512': hashlib.sha3_512,
    'BLAKE2b': hashlib.blake2b,
    'BLAKE2s': hashlib.blake2s,
}


def hash_message(message: bytes, hash_method: str) -> bytes:
    hash_method = HASH_METHODS[hash_method]
    hasher = hash_method()
    blocks = utils.split_to_blocks(message, hasher.block_size)
    for block in blocks:
        hasher.update(block)
    return hasher.digest()


def sign(message: bytes, private_key: PrivateKey, hash_method: str):
    return encrypt(hash_message(message, hash_method), private_key)


def verify(message: bytes, signature: bytes, public_key: PublicKey, hash_method: str):
    _hash = hash_message(message, hash_method)
    _decrypt = decrypt(signature, public_key)
    return _hash == _decrypt


def hash_file(file_name: str, hash_method) -> bytes:
    hash_method = HASH_METHODS[hash_method]
    hasher = hash_method()
    with open(file_name, "rb") as file:
        while True:
            data = file.read(hasher.block_size)
            hasher.update(bytes(data))
            if not data:
                break
    return hasher.digest()


def sign_file(file_name: str, private_key: PrivateKey, hash_method: str):
    return encrypt(hash_file(file_name, hash_method), private_key)


def verify_file(file_name: str, signature: bytes, public_key: PublicKey, hash_method: str):
    _hash = hash_file(file_name, hash_method)
    _decrypt = decrypt(signature, public_key)
    return _hash == _decrypt
