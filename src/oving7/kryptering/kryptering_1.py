import binascii
import uuid


def to_hex(word):
    return int(str(binascii.hexlify(bytes(word, encoding='ascii')), 'ascii'), 16)


def to_string(word):
    return str(binascii.unhexlify(hex(word)[2:]), 'ascii')


def encrypt(message, key):
    hex_msg = to_hex(message)
    hex_key = to_hex(key)

    return hex_msg ^ hex_key


def decrypt(encrypted, key):
    hex_key = to_hex(key)
    return to_string(encrypted ^ hex_key)


def main():
    msg = input("Message: ")
    key = str(uuid.uuid1())
    print(f"Using key {key}")

    encrypted = encrypt(msg, key)
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypt(encrypted, key)}")