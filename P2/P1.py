import hashlib
import math
import pickle
import time
import sys
import random
import string
import os

class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bytearray(math.ceil(size / 8))

    def _get_hashes(self, item):
        hashes = []
        for i in range(self.hash_count):
            h = hashlib.md5(f"{i}:{item}".encode('utf-8')).hexdigest()
            hashes.append(int(h, 16) % self.size)
        return hashes

    def add(self, item):
        for position in self._get_hashes(item):
            byte_index = position // 8
            bit_index = position % 8
            self.bit_array[byte_index] |= (1 << bit_index)

    def check(self, item):
        for position in self._get_hashes(item):
            byte_index = position // 8
            bit_index = position % 8
            if not (self.bit_array[byte_index] & (1 << bit_index)):
                return False
        return True

    def save(self, filename):
        with open(filename, 'wb') as f:
            data = {'size': self.size, 'hash_count': self.hash_count, 'bit_array': self.bit_array}
            pickle.dump(data, f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        instance = cls(data['size'], data['hash_count'])
        instance.bit_array = data['bit_array']
        return instance


class BloomFilterDoubleHashing(BloomFilter):
    def _get_hashes(self, item):
        item_bytes = str(item).encode('utf-8')
        h1 = int(hashlib.md5(item_bytes).hexdigest(), 16)
        h2 = int(hashlib.sha1(item_bytes).hexdigest(), 16)

        hashes = []
        for i in range(self.hash_count):
            pos = (h1 + i * h2) % self.size
            hashes.append(pos)
        return hashes


# --- Ejercicio 2: Selección óptima de parámetros ---
def calcular_parametros_optimos(n, p):
    m = math.ceil(-(n * math.log(p)) / (math.log(2) ** 2))
    k = round((m / n) * math.log(2))
    return m, k


def generar_datos_prueba(cantidad):
    """Genera contraseñas aleatorias para las pruebas."""
    return [''.join(random.choices(string.ascii_letters + string.digits, k=8)) for _ in range(cantidad)]


def evaluar_estructura(estructura, datos_insercion, datos_comprobacion, es_filtro=False):
    """Evalúa tiempos, tamaño y falsos positivos de una estructura de datos."""
    # 1. Tiempo de inserción
    inicio = time.time()
    for item in datos_insercion:
        estructura.add(item)
    tiempo_insercion = time.time() - inicio

    # 2. Tamaño en memoria
    if es_filtro:
        tamano = sys.getsizeof(estructura) + sys.getsizeof(estructura.bit_array)
    else:
        tamano = sys.getsizeof(estructura)

    # 3. Tiempo de comprobación y falsos positivos
    falsos_positivos = 0
    inicio = time.time()
    for item in datos_comprobacion:
        encontrado = item in estructura if not es_filtro else estructura.check(item)
        if encontrado and item not in datos_insercion:
            falsos_positivos += 1
    tiempo_comprobacion = time.time() - inicio

    tasa_fp = falsos_positivos / len(datos_comprobacion) if datos_comprobacion else 0

    return {
        "insercion_s": tiempo_insercion,
        "comprobacion_s": tiempo_comprobacion,
        "tamano_bytes": tamano,
        "tasa_fp": tasa_fp
    }


if __name__ == "__main__":
    print("=== Ejercicio 1: Pruebas Básicas del Filtro de Bloom ===")
    filtro_test = BloomFilter(1000, 5)
    pwds_ejemplo = ["123456", "password123", "qwerty"]
    print("Añadiendo contraseñas: ", pwds_ejemplo)
    for p in pwds_ejemplo:
        filtro_test.add(p)

    print("Comprobando contraseñas añadidas (Esperado: True):")
    for p in pwds_ejemplo:
        print(f" - '{p}': {filtro_test.check(p)}")

    print("Comprobando contraseñas no añadidas (Esperado: False):")
    for p in ["segura1!", "otraClave"]:
        print(f" - '{p}': {filtro_test.check(p)}")

    fichero_test = "test_bloom.bin"
    filtro_test.save(fichero_test)
    print(f"Filtro guardado en '{fichero_test}'.")
    filtro_recuperado = BloomFilter.load(fichero_test)
    print(f"Filtro cargado. ¿Detecta 'password123'?: {filtro_recuperado.check('password123')}")
    if os.path.exists(fichero_test):
        os.remove(fichero_test)

    print("\n=== Ejercicios 3 y 5: Comparativa de estructuras ===")
    tasa_fp_deseada = 0.05
    tamanos_dataset = [1000, 10000, 100000]  # Subconjuntos de prueba

    for n in tamanos_dataset:
        print(f"\n--- Evaluando dataset de {n} elementos ---")
        datos = generar_datos_prueba(n)
        datos_prueba_fp = generar_datos_prueba(n // 10)

        m_opt, k_opt = calcular_parametros_optimos(n, tasa_fp_deseada)

        conjunto = set()
        res_set = evaluar_estructura(conjunto, datos, datos_prueba_fp, es_filtro=False)

        filtro_orig = BloomFilter(m_opt, k_opt)
        res_orig = evaluar_estructura(filtro_orig, datos, datos_prueba_fp, es_filtro=True)

        filtro_dh = BloomFilterDoubleHashing(m_opt, k_opt)
        res_dh = evaluar_estructura(filtro_dh, datos, datos_prueba_fp, es_filtro=True)

        print(
            f"SET      - Ins: {res_set['insercion_s']:.4f}s, Comp: {res_set['comprobacion_s']:.4f}s, Tamaño: {res_set['tamano_bytes']}B, FP: {res_set['tasa_fp']:.2%}")
        print(
            f"BF ORIG  - Ins: {res_orig['insercion_s']:.4f}s, Comp: {res_orig['comprobacion_s']:.4f}s, Tamaño: {res_orig['tamano_bytes']}B, FP: {res_orig['tasa_fp']:.2%}")
        print(
            f"BF DOBLE - Ins: {res_dh['insercion_s']:.4f}s, Comp: {res_dh['comprobacion_s']:.4f}s, Tamaño: {res_dh['tamano_bytes']}B, FP: {res_dh['tasa_fp']:.2%}")

    print("\n=== Ejercicio 6: Filtro de Bloom para el dataset REAL ===")
    n_total = 1400000000  # 1400 millones
    tasa_fp_deseada = 0.05
    m_total, k_total = calcular_parametros_optimos(n_total, tasa_fp_deseada)

    print(f"Creando filtro real con m={m_total}, k={k_total}...")
    filtro_real = BloomFilterDoubleHashing(m_total, k_total)

    directorios_datos = [os.path.join('data', 'data'), os.path.join('data', '__data')]

    elementos_anadidos = 0
    inicio_carga = time.time()

    # Procesamiento real de los ficheros
    for directorio in directorios_datos:
        if not os.path.exists(directorio):
            print(f"Omitiendo {directorio} (no encontrado).")
            continue

        print(f"Procesando archivos continuamente en {directorio}...")
        # Usamos os.walk para recorrer todas las subcarpetas y archivos
        for root, _, files in os.walk(directorio):
            for filename in files:
                filepath = os.path.join(root, filename)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        try:
                            # Formato correo:password - ajusta esto según cómo vengan tus datos
                            if ':' in line:
                                _, pwd = line.strip().split(':', 1)
                            else:
                                pwd = line.strip()  # Por si en data/data vienen contraseñas solas

                            filtro_real.add(pwd)
                            elementos_anadidos += 1
                        except ValueError:
                            pass  # Ignorar líneas mal formadas

    tiempo_total = time.time() - inicio_carga
    print(f"\nSe han añadido {elementos_anadidos} elementos.")
    print(f"Tiempo total de inserción: {tiempo_total:.2f} segundos.")

    # Opcional: Guardar el filtro real para no tener que volver a procesar 41GB
    # filtro_real.save('filtro_dataset_completo.bin')

    print("\nComprobando las contraseñas del enunciado contra el dataset REAL:")
    contrasenas_test = [
        "hola", "1234", "iloveyou", "Awesome1", "mmmmmmm",
        "367026606991464", "supertrooper2002", "SpRyhdjd2002",
        "593b04318425a33190ceaabab648376c", "bnbd246GbB"
    ]

    for pwd in contrasenas_test:
        print(f" '{pwd}': {'Filtrada (True)' if filtro_real.check(pwd) else 'No filtrada (False)'}")