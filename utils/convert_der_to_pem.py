from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
import os


def convert_der_to_pem(der_key_path, pem_key_path, password):
    # Leer el archivo .key en formato DER
    with open(der_key_path, "rb") as key_file:
        der_data = key_file.read()

    # Convertir clave privada DER a PEM
    private_key = serialization.load_der_private_key(
        der_data,
        password=password.encode(),  # La contraseña debe ser bytes
        backend=default_backend()
    )

    # Encriptar la clave privada con una contraseña (si deseas cifrarla)
    encrypted_pem_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(password.encode())  # Cifrado con AES
    )

    # Guardar clave privada en formato PEM cifrada
    with open(pem_key_path, "wb") as pem_file:
        pem_file.write(encrypted_pem_key)

    return pem_key_path