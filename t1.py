from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import binascii
import os
import re

def is_valid_hex(hex_string):
    return bool(re.match(r'^[0-9A-Fa-f]+$', hex_string))

def pad(data):
    pad_length = 16 - (len(data) % 16)
    return data + bytes([pad_length] * pad_length)

def unpad(data):
    pad_length = data[-1]
    return data[:-pad_length]

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def decrypt_dlms_packet(block_cipher_key, dlms_packet):
    # Convert hex to bytes
    block_cipher_key_bytes = binascii.unhexlify(block_cipher_key)
    dlms_packet_bytes = binascii.unhexlify(dlms_packet)

    # Pad the packet to make it a multiple of the block size
    dlms_packet_bytes = pad(dlms_packet_bytes)

    cipher = Cipher(algorithms.AES(block_cipher_key_bytes), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(dlms_packet_bytes) + decryptor.finalize()

    decrypted_data = unpad(decrypted_data)

    return decrypted_data

def main():
    password = input("Enter your password: ")
    block_cipher_key = input("Enter the Block Cipher Key (hex): ")
    auth_key = input("Enter the Authentication Key (hex): ")

    if not (is_valid_hex(block_cipher_key) and is_valid_hex(auth_key)):
        print("Error: Please enter valid hexadecimal strings for the keys.")
        return

    dlms_packet = input("Enter the DLMS Packet (hex): ")

    if not is_valid_hex(dlms_packet):
        print("Error: Please enter a valid hexadecimal DLMS packet.")
        return

    salt = os.urandom(16)  # Salt for key derivation
    derived_key = derive_key(password, salt)
    print("Derived Key (for reference, do not use directly):", binascii.hexlify(derived_key).decode())

    decrypted_packet = decrypt_dlms_packet(block_cipher_key, dlms_packet)

    # Output the decrypted data in both hex and ASCII
    print("Decrypted DLMS Packet (Hex):", decrypted_packet.hex())
    try:
        print("Decrypted DLMS Packet (ASCII):", decrypted_packet.decode('ascii', errors='ignore'))
    except Exception as e:
        print("Error decoding to ASCII:", e)

if __name__ == "__main__":
    main()
