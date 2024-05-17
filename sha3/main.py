from sha3 import Sha3
from datetime import datetime
import hashlib


def get_my_hash(data):
    return Sha3(256, 1088, 512).hash(bytearray(data)).hex()


def get_lib_hash(data):
    sha3_256_hash = hashlib.sha3_256()
    sha3_256_hash.update(data)
    return sha3_256_hash.hexdigest()


def test(byte_data: bytearray):
    print("Text:", byte_data)
    start = datetime.now()
    my_result = get_my_hash(byte_data)
    end = datetime.now()
    print("My  result:", my_result)
    td = (end - start).total_seconds() * 1000
    print(f"Time: {td:.03f}ms")

    lib_result = get_lib_hash(byte_data)
    print("Lib result:", lib_result)
    if my_result != lib_result:
        print("Bad result")


def main():
    # Test from file
    file = open("test.txt", "rb")
    byte_data = file.read()
    file.close()
    test(byte_data)

    # Empty test
    # 0b (241.511ms)
    # test(bytes())

    # Small test
    # 13b (264.873ms)
    # test("Hello, world!".encode('utf-8'))

    # Middle test
    # 10Kb (19566.594ms)
    # from_string = bytes("".join(random.choice(ascii_lowercase) for _ in range(10240)).encode())
    # test(from_string)

    # Large test
    # >1Mb (2165394.512ms)
    # from_string = bytes("".join(random.choice(ascii_lowercase) for _ in range(550000)).encode())
    # test(from_string)


if __name__ == '__main__':
    main()
