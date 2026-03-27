# Actividad2.py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from P1_AES import AES128

if __name__ == "__main__":
    mensaje = b"MiquelNombre123!"
    clave = b"ClaveSecreta1234"

    # 1. Cifrar usando P1_AES.py
    aes_propio = AES128(clave)
    texto_cifrado = aes_propio.encrypt_block(mensaje)

    print(f"Mensaje original: {mensaje}")
    print(f"Texto cifrado (Hex): {texto_cifrado.hex()}")

    # 2. Descifrar el texto cifrado usando una librería externa
    backend = default_backend()
    cipher_externo = Cipher(algorithms.AES(clave), modes.ECB(), backend=backend)
    decryptor = cipher_externo.decryptor()

    texto_descifrado = decryptor.update(texto_cifrado) + decryptor.finalize()

    print(f"Texto descifrado con la biblioteca cryptography: {texto_descifrado}")

    if texto_descifrado == mensaje:
        print("\nCoincide")
    else:
        print("\nno coincide")
