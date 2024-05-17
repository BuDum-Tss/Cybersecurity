from datetime import datetime

import rsa
import myrsa


def generate_keys_test(nbits):
    # создание ключей
    start = datetime.now()
    (public_key, private_key) = rsa.newkeys(nbits)
    end = datetime.now()
    td = (end - start).total_seconds() * 1000
    print(f"Public Key by lib: \n{(public_key.e, public_key.n)}\n"
          f"Private Key by lib:\n{(private_key.d, private_key.n)}")
    print(f"Time: {td:.03f}ms\n")
    start = datetime.now()
    (my_public_key, my_private_key) = myrsa.newkeys(nbits)
    end = datetime.now()
    td = (end - start).total_seconds() * 1000
    print(f"Public Key by myrsa: \n{my_public_key}\n"
          f"Private Key by myrsa:\n{my_private_key}")
    print(f"Time: {td:.03f}ms\n")
    return my_private_key, my_public_key, private_key, public_key


def encrypt_data_test(message, my_public_key, public_key):
    # Шифрование сообщения
    start = datetime.now()
    encrypted_message = rsa.encrypt(message, public_key)
    end = datetime.now()
    td = (end - start).total_seconds() * 1000
    print("Encrypted message by lib:\n", encrypted_message)
    print(f"Time: {td:.03f}ms\n")
    start = datetime.now()
    my_encrypted_message = myrsa.encrypt(message, my_public_key)
    end = datetime.now()
    td = (end - start).total_seconds() * 1000
    print("Encrypted message by myrsa:\n", my_encrypted_message)
    print(f"Time: {td:.03f}ms\n")
    return encrypted_message, my_encrypted_message


def decrypt_data_test(encrypted_message, my_encrypted_message, my_private_key, private_key):
    # Дешифрование сообщения
    start = datetime.now()
    decrypted_message = rsa.decrypt(encrypted_message, private_key)
    end = datetime.now()
    td = (end - start).total_seconds() * 1000
    print("Decrypted Message by lib:\n", decrypted_message)
    print(f"Time: {td:.03f}ms\n")
    start = datetime.now()
    my_decrypted_message = myrsa.decrypt(my_encrypted_message, my_private_key)
    end = datetime.now()
    td = (end - start).total_seconds() * 1000
    print("Decrypted Message by myrsa:\n", my_decrypted_message)
    print(f"Time: {td:.03f}ms\n")


def my_rsa_test(message: bytes, nbits: int):
    print("RSA test")
    my_private_key, my_public_key, private_key, public_key = generate_keys_test(nbits)
    encrypted_message, my_encrypted_message = encrypt_data_test(message, my_public_key, public_key)
    decrypt_data_test(encrypted_message, my_encrypted_message, my_private_key, private_key)


def digital_signature_small_test():
    print("Digital signature small test")
    (public_key, private_key) = myrsa.newkeys(2048)

    # Сообщение для подписи
    message = b"Hello, world!"

    # Подпись сообщения приватным ключом
    start = datetime.now()
    signature = myrsa.sign(message, private_key, 'SHA3-256')
    end = datetime.now()
    td = (end - start).total_seconds() * 1000
    print("Message is signed")
    print(f"Time: {td:.03f}ms\n")

    # Проверка подписи публичным ключом
    start = datetime.now()
    if myrsa.verify(message, signature, public_key, 'SHA3-256'):
        print("Signature is valid.")
    else:
        print("Signature is invalid.")
    end = datetime.now()
    td = (end - start).total_seconds() * 1000
    print(f"Time: {td:.03f}ms\n")


def digital_signature_large_test():
    print("Digital signature large test")
    (my_public_key, my_private_key) = myrsa.newkeys(2048)
    (public_key, private_key) = myrsa.newkeys(2048)

    # Подпись сообщения приватным ключом
    start = datetime.now()
    signature = myrsa.sign_file("1MB.txt", my_private_key, 'SHA3-256')
    end = datetime.now()
    td = (end - start).total_seconds() * 1000
    print("File is signed")
    print(f"Time: {td:.03f}ms\n")

    file_encrypted =

    # Проверка подписи публичным ключом
    start = datetime.now()
    if myrsa.verify_file("1MB.txt", signature, my_public_key, 'SHA3-256'):
        print("Signature is valid.")
    else:
        print("Signature is invalid.")
    end = datetime.now()
    td = (end - start).total_seconds() * 1000
    print(f"Time: {td:.03f}ms\n")


def main():
    my_rsa_test(b"Hello, RSA!!!", 256)
    digital_signature_small_test()
    digital_signature_large_test()


if __name__ == '__main__':
    main()
