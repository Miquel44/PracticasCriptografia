import hashlib
import itertools
import time
import string


def crack_md5_num(hashes_obj, max_len=6):
    """Fuerza bruta contínua para contraseñas de solo dígitos (MD5)."""
    encontrados = {}
    print(f"[*] Iniciando fuerza bruta (dígitos) hasta longitud {max_len}...")
    inicio = time.time()

    # 0 al 9
    caracteres = string.digits
    for i in range(1, max_len + 1):
        for intento in itertools.product(caracteres, repeat=i):
            pwd = ''.join(intento)
            hash_calc = hashlib.md5(pwd.encode()).hexdigest()
            if hash_calc in hashes_obj:
                encontrados[hash_calc] = pwd
                print(f"  [+] Encontrado: {pwd} -> {hash_calc}")
                if len(encontrados) == len(hashes_obj):
                    break
        if len(encontrados) == len(hashes_obj):
            break

    print(f"[*] Tiempo invertido: {time.time() - inicio:.2f} segundos\n")
    return encontrados


def benchmark_sha1():
    """Calcula cuántos hashes SHA-1 por segundo puede hacer esta máquina en Python."""
    print("[*] Ejecutando benchmark SHA-1 (Python)...")
    inicio = time.time()
    iteraciones = 1_000_000
    for _ in range(iteraciones):
        hashlib.sha1(b"test").hexdigest()
    tiempo = time.time() - inicio
    tasa = iteraciones / tiempo
    print(f"  [+] Rendimiento aproximado: {tasa:.2f} hashes SHA-1 / segundo\n")
    return tasa


def calcular_espacio_claves(longitud, tasa_hash):
    """Calcula combinaciones y tiempo estimado."""
    num_combinaciones = 10 ** longitud
    alfa_combinaciones = 62 ** longitud  # Letras (mayús/minús) + dígitos

    print(f"[*] Para longitud {longitud}:")
    print(f"  - Solo números (10^L): {num_combinaciones} combinaciones ({(num_combinaciones / tasa_hash):.5f} seg)")
    print(f"  - Alfanumérico (62^L): {alfa_combinaciones} combinaciones ({(alfa_combinaciones / tasa_hash):.5f} seg)\n")


def generar_diccionarios_contextuales():
    """Genera diccionarios basados en contexto (Ej 11 y 12)."""
    print("[*] Generando diccionarios basados en contexto (Ej 11)...")

    # Marta (Ciudades)
    ciudades = ["barcelona", "bcn", "madrid", "valencia", "sevilla", "girona", "tarragona", "lleida"]
    with open("dict_marta.txt", "w") as f:
        for c in ciudades:
            f.write(f"{c}\n{c.capitalize()}\n{c}123\n")

    # John Smith (Deportes)
    deportes = ["cricket", "rugby", "tennis", "golf", "baseball", "basketball", "soccer", "football"]
    with open("dict_john.txt", "w") as f:
        for d in deportes:
            f.write(f"{d}\n{d}2023\n{d}2024\n")

    # Marc (Profesor)
    educacion = ["mestre", "escola", "oposicions", "profesor", "educacio", "magisteri", "infantil", "primaria"]
    with open("dict_marc.txt", "w") as f:
        for e in educacion:
            f.write(f"{e}\n{e}123\n")

    print("  [+] Diccionarios dict_marta.txt, dict_john.txt y dict_marc.txt generados.\n")


if __name__ == "__main__":
    print("=== Ejercicio 7: Ataque de fuerza bruta (Dígitos) ===")
    hashes_ej7 = [
        "6ea9ab1baa0efb9e19094440c317e21b", "8e296a067a37563370ded05f5a3bf3ec",
        "54fe976ba170c19ebae453679b362263", "6562c5c1f33db6e05a082a88cddab5ea",
        "7c590f287acefdd3ea84a7678f1e907b", "6593a1651adf82783394195112e73aac",
        "a388742c988cb1b8d9a304db528cf71d", "047d8415eec2dcec989c77d531535531",
        "b87262873e28e7589c15c5e467e9c39a", "42005f9a3f3a28aabe4883bb7a60ec0a",
        "1f99c8a687de5b829addfce79383827a", "1d1803570245aa620446518b2154f324"
    ]
    # Comandos para John the Ripper equivalentes:
    # john --format=raw-md5 --incremental=digits hashes_ej7.txt
    crack_md5_num(hashes_ej7, max_len=6)  # Ajusta max_len si no encuentra todos

    print("=== Ejercicio 8: Espacio de claves y Benchmark ===")
    tasa = benchmark_sha1()
    calcular_espacio_claves(6, tasa)
    calcular_espacio_claves(8, tasa)

    print("=== Ejercicios 9, 10, 11 y 12: Comandos y diccionarios ===")
    print("Para los ataques de diccionarios, utiliza John the Ripper. Ejemplos de comandos:")
    print(" Ej 9 : john --format=raw-md5 --wordlist=rockyou.txt hashes_ej9.txt")
    print(" Ej 10: john --format=md5crypt --wordlist=rockyou.txt hashes_ej10.txt")

    generar_diccionarios_contextuales()

    print("Para aplicar alteraciones (Ej 12) usa las reglas de John The Ripper:")
    print(" john --wordlist=dict_john.txt --rules=Jumbo hashes_ej12.txt")
    print(" (O define reglas Leetspeak personalizadas en john.conf y llama a --rules=KoreLogic)")
