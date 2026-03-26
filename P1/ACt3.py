# Actividad3.py
import random
import matplotlib.pyplot as plt
from P1_AES import AES128


def hamming_distance(b1: bytes, b2: bytes) -> int:
    return sum(bin(x ^ y).count('1') for x, y in zip(b1, b2))


def flip_random_bit(data: bytes) -> bytes:
    mutable_data = bytearray(data)
    byte_idx = random.randint(0, 15)
    bit_idx = random.randint(0, 7)
    mutable_data[byte_idx] ^= (1 << bit_idx)
    return bytes(mutable_data)


if __name__ == "__main__":
    mensaje = b"MiquelNombre123!"
    clave = b"ClaveSecreta1234"
    aes = AES128(clave)

    c = aes.encrypt_block(mensaje)
    distances = []

    for _ in range(100000):
        mensaje_m = flip_random_bit(mensaje)
        c_m = aes.encrypt_block(mensaje_m)
        dist = hamming_distance(c, c_m)
        distances.append(dist)

    avg_dist = sum(distances) / len(distances)
    print(f"Media de bits modificados: {avg_dist:.2f} (Esperado: ~64)")

    plt.hist(distances, bins=range(min(distances), max(distances) + 1), edgecolor='black')
    plt.title('Distribución de Distancias de Hamming (Efecto Avalancha)')
    plt.xlabel('Bits modificados')
    plt.ylabel('Frecuencia')
    plt.show()
