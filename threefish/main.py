from threefish import Threefish
from datetime import datetime
import skein 

def small_data_test(threefish, plaintext):
    start = datetime.now()
    result = threefish.encrypt_block(plaintext)
    end = datetime.now()
    td = (end - start).total_seconds() * 1000
    print(f"encrypt: {result.hex()}")
    print(f"Time: {td:.03f}ms")

    start = datetime.now()
    result = threefish.decrypt_block(result)
    end = datetime.now()
    td = (end - start).total_seconds() * 1000
    print(f"decrypt: {result}")
    print(f"Time: {td:.03f}ms\n")

def test_small_data():
    print("Test: small data")
    key = b"key of 32,64 or 128 bytes length"
    tweak = b"tweak: 16 bytes "
    plaintext = b"block of data,same length as key"
    print("Plaintext")
    print(f"{plaintext}\n")

    implemented_threefish = Threefish(key, tweak)
    lib_threefish = skein.threefish(key, tweak)

    print("Implemented threefish")
    small_data_test(implemented_threefish, plaintext)
    print("Lib threefish")
    small_data_test(lib_threefish, plaintext)

    
def large_data_test(threefish, input_filename, encrypt_filename, decrypt_filename):
    start = datetime.now()
    with open(input_filename, "rb") as input_file, open(encrypt_filename, "wb") as encrypt_output, open(decrypt_filename,"wb") as decrypt_output:
        while True:
            plaintext = input_file.read(128)
            if not plaintext or len(plaintext) != 128:
                break
            result = threefish.encrypt_block(plaintext)
            encrypt_output.write(result)
            decrypt_output.write(threefish.decrypt_block(result))
    end = datetime.now()
    td = (end - start).total_seconds() * 1000
    print(f"Time: {td:.03f}ms\n")

def test_large_data():
    print("Test: large data\n")
    key = bytes("k" * 128, "utf-8")
    tweak = bytes("t" * 16, "utf-8")

    implemented_threefish = skein.threefish(key, tweak)
    lib_threefish = skein.threefish(key, tweak)

    print("Implemented threefish")
    large_data_test(implemented_threefish,"1MB.txt", "encrypt.txt", "decrypt.txt")
    print("Lib threefish")
    large_data_test(lib_threefish,"1MB.txt", "encrypt_lib.txt", "decrypt_lib.txt")

def pad(data:bytearray):
    data.extend(bytes([0b10000000]))
    if (len(data)%128 != 128):
        data.extend([0]*((-len(data))%128))
    
def remove_pad(data:bytearray):
    i = 127
    print(data)
    while data[i] != 0b10000000:
        i = i - 1
    result = data[:i]
    return result
    
def test_encrypt(threefish, input_filename, output_filename):
    plaintext = None
    with open(input_filename, "rb") as input_file, open(output_filename, "wb") as output_file:
        while True:
            plaintext = input_file.read(128)
            if not plaintext or len(plaintext) != 128:
                break
            result = threefish.encrypt_block(plaintext)
            print(type(result))
            output_file.write(result)
        
        plaintext = bytearray(plaintext)
        pad(plaintext)
        print(len(plaintext))
        result = threefish.encrypt_block(plaintext)
        output_file.write(result)


def test_decrypt(threefish, input_filename, output_filename):
    chipertext = ''
    chipertext_next = ''
    result = bytes()
    with open(input_filename, "rb") as input_file, open(output_filename, "wb") as output_file:
        chipertext_next = input_file.read(128)
        while True:
            chipertext = chipertext_next
            chipertext_next = input_file.read(128)
            if not chipertext or len(chipertext_next) != 128:
                break
            result = threefish.decrypt_block(chipertext)
            output_file.write(result)
        
        result = threefish.decrypt_block(chipertext)
        result = remove_pad(result)
        output_file.write(result)

def test_with_padding():
    print("Test: with padding\n")
    key = bytes("k" * 128, "utf-8")
    tweak = bytes("t" * 16, "utf-8")

    implemented_threefish = skein.threefish(key, tweak)
    test_encrypt(implemented_threefish, "some_text.txt", "some_text_encrypted.bin")
    test_decrypt(implemented_threefish, "some_text_encrypted.bin", "some_text_decrypted.txt")

if __name__ == '__main__':
    #test_small_data()
    #print('===============================================')
    #test_large_data()
    test_with_padding()