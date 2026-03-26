# Actividad4.py
import os
import matplotlib.pyplot as plt
from scipy.stats import chisquare
from collections import Counter
from P1_AES import AES128

if __name__ == "__main__":
    clave = b"ClaveSecreta1234"
    aes = AES128(clave)

    byte_counts = Counter()

    # Generar y cifrar 100,000 bloques aleatorios
    for _ in range(100000):
        plaintext = os.urandom(16)
        ciphertext = aes.encrypt_block(plaintext)
        byte_counts.update(ciphertext)

    # Extraer frecuencias
    observed_frequencies = [byte_counts[i] for i in range(256)]
    expected_frequency = sum(observed_frequencies) / 256

    chi_stat, p_value = chisquare(f_obs=observed_frequencies)

    print(f"Test Chi-cuadrado:")
    print(f"Estadístico: {chi_stat:.2f}")
    print(f"p-valor: {p_value:.4f}")

    plt.bar(range(256), observed_frequencies, color='steelblue')
    plt.axhline(expected_frequency, color='red', linestyle='dashed', linewidth=1, label='Frecuencia esperada')
    plt.title('Distribución de valores de bytes en el texto cifrado')
    plt.xlabel('Valor del byte (0-255)')
    plt.ylabel('Frecuencia')
    plt.legend()
    plt.show()
