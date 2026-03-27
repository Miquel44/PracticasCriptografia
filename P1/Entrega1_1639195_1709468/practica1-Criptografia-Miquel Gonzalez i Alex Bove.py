#PRACTICA 1 - CRIPTOGRAFIA I SEGURETAT
# Miquel Gonzalez i Alex Bové

import os
import random
from collections import Counter
import matplotlib.pyplot as plt
from scipy.stats import chisquare

# Taula de substitució S-Box
SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

# Constants de ronda (Rcon)
RCON = [
    [0x00, 0x00, 0x00, 0x00],
    [0x01, 0x00, 0x00, 0x00],
    [0x02, 0x00, 0x00, 0x00],
    [0x04, 0x00, 0x00, 0x00],
    [0x08, 0x00, 0x00, 0x00],
    [0x10, 0x00, 0x00, 0x00],
    [0x20, 0x00, 0x00, 0x00],
    [0x40, 0x00, 0x00, 0x00],
    [0x80, 0x00, 0x00, 0x00],
    [0x1b, 0x00, 0x00, 0x00],
    [0x36, 0x00, 0x00, 0x00]
]

def sub_word(word):
    return [SBOX[b] for b in word]

def rot_word(word):
    return word[1:] + word[:1]

def key_expansion(key):
    w = [[key[4*i + j] for j in range(4)] for i in range(4)]
    for i in range(4, 44):
        temp = w[i-1]
        if i % 4 == 0:
            temp = [a ^ b for a, b in zip(sub_word(rot_word(temp)), RCON[i//4])]
        w.append([a ^ b for a, b in zip(w[i-4], temp)])
    return w

def bytes2matrix(text):
    return [[text[i + 4*j] for j in range(4)] for i in range(4)]

def matrix2bytes(matrix):
    return bytes([matrix[i][j] for j in range(4) for i in range(4)])

def print_matrix(titol, matriu):
    print(titol)
    for r in range(4):
        fila_hex = ["{:02x}".format(matriu[r][c]) for c in range(4)]
        print("  [{}]".format(", ".join(fila_hex)))
    print("")

def add_round_key(state, key_schedule, round_num):
    for c in range(4):
        k_word = key_schedule[round_num * 4 + c]
        for r in range(4):
            state[r][c] ^= k_word[r]
    return state

def sub_bytes(state):
    for r in range(4):
        for c in range(4):
            state[r][c] = SBOX[state[r][c]]
    return state

def shift_rows(state):
    state[1][0], state[1][1], state[1][2], state[1][3] = state[1][1], state[1][2], state[1][3], state[1][0]
    state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = state[3][3], state[3][0], state[3][1], state[3][2]
    return state

def xtime(a):
    return (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

def mix_single_column(a):
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)

def mix_columns(state):
    for c in range(4):
        col = [state[0][c], state[1][c], state[2][c], state[3][c]]
        mix_single_column(col)
        for r in range(4):
            state[r][c] = col[r]
    return state

def aes_encrypt_block(m, k, debug=False):
    state = bytes2matrix(m)
    key_schedule = key_expansion(k)

    if debug:
        print("\n=== EXTRACCIÓ DE MATRIUS PER A L'INFORME ===")
        print_matrix("Codificació de m (Matriu d'Entrada Inicial):", state)
        print_matrix("Codificació de k (Matriu de la Clau Inicial):", bytes2matrix(k))
        print_matrix("Entrada AddRoundKey (Ronda 0):", state)

    state = add_round_key(state, key_schedule, 0)
    
    if debug:
        print_matrix("Sortida AddRoundKey (Ronda 0) / Entrada SubBytes (Ronda 1):", state)

    for round_num in range(1, 10):
        state = sub_bytes(state)
        if debug and round_num == 1:
            print_matrix("Sortida SubBytes (Ronda 1) / Entrada ShiftRows:", state)
            
        state = shift_rows(state)
        if debug and round_num == 1:
            print_matrix("Sortida ShiftRows (Ronda 1) / Entrada MixColumns:", state)
            
        state = mix_columns(state)
        if debug and round_num == 1:
            print_matrix("Sortida MixColumns (Ronda 1):", state)
            
        state = add_round_key(state, key_schedule, round_num)
        
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, key_schedule, 10)
    
    return matrix2bytes(state)

# EXERCICI 1: Procés de xifrat
print("--- EXERCICI 1: Xifratge AES ---")
nom = b"Miquel i Alex   "
m = nom.ljust(16, b' ') 

k = os.urandom(16)

c = aes_encrypt_block(m, k, debug=True)

print("Missatge en clar (m): {}".format(m))
print("Clau (k): {}".format(k.hex()))
print("Text xifrat final (c): {}\n".format(c.hex()))


# EXERCICI 2: Desxifrat sense llibreries externes de Python
print("--- EXERCICI 2: Desxifrat (Eina Externa) ---")
print("Per comprovar el desxifratge sense llibreries externes, utilitza CyberChef:")
print("1. Ves a https://gchq.github.io/CyberChef/")
print("2. Busca i afegeix la recepta 'AES Decrypt'")
print("3. Introdueix la següent clau (Key) en format Hex: {}".format(k.hex()))
print("4. Selecciona el mode 'ECB'")
print("5. Introdueix el següent text xifrat a l'Input en format Hex:\n{}".format(c.hex()))
print(">> El resultat a l'Output hauria de ser exactament el missatge original.\n")


# EXERCICI 3: Efecte allau 
print("--- EXERCICI 3: Efecte allau (Això trigarà uns segons...) ---")

num_experiments = 100000
distancies = []

c_original = aes_encrypt_block(m, k, debug=False)

for _ in range(num_experiments):
    byte_idx = random.randint(0, 15)
    bit_idx = random.randint(0, 7)
    
    m_prime = bytearray(m)
    m_prime[byte_idx] ^= (1 << bit_idx)
    
    c_prime = aes_encrypt_block(bytes(m_prime), k, debug=False)
    
    distancia = sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(c_original, c_prime))
    distancies.append(distancia)

mitjana_bits = sum(distancies) / num_experiments
print("Mitjana de bits modificats: {:.2f}".format(mitjana_bits))
print("Valor teòric esperat: 64.0 (la meitat dels 128 bits)")

plt.hist(distancies, bins=range(min(distancies), max(distancies) + 2), edgecolor='black', alpha=0.7)
plt.title("Distribució de la distància de Hamming (Efecte Allau)")
plt.xlabel("Distància de Hamming (bits diferents)")
plt.ylabel("Freqüència")
plt.axvline(mitjana_bits, color='r', linestyle='dashed', linewidth=2, label='Mitjana: {:.2f}'.format(mitjana_bits))
plt.legend()
plt.show()


# EXERCICI 4: Anàlisi estadística del text xifrat 
print("\n--- EXERCICI 4: Anàlisi estadística (Això pot trigar un parell de minuts...) ---")

num_blocs = 100000
freq_bytes = Counter()

for _ in range(num_blocs):
    bloc_aleatori = os.urandom(16)
    bloc_xifrat = aes_encrypt_block(bloc_aleatori, k, debug=False)
    freq_bytes.update(bloc_xifrat)

valors_observats = [freq_bytes.get(i, 0) for i in range(256)]
total_bytes = num_blocs * 16
valor_esperat_uniforme = total_bytes / 256
valors_esperats = [valor_esperat_uniforme] * 256

chi2_stat, p_valor = chisquare(f_obs=valors_observats, f_exp=valors_esperats)

print("Estadístic de la prova \u03c72: {:.4f}".format(chi2_stat))
print("P-valor: {:.4f}".format(p_valor))
if p_valor > 0.05:
    print("La distribució dels bytes és compatible amb una distribució uniforme (P-valor > 0.05).")
else:
    print("S'han trobat diferències significatives amb la distribució uniforme.")

plt.bar(range(256), valors_observats, color='blue', alpha=0.7)
plt.axhline(valor_esperat_uniforme, color='r', linestyle='dashed', linewidth=2, label='Freqüència esperada')
plt.title("Distribució dels valors dels bytes al text xifrat")
plt.xlabel("Valor del byte (0-255)")
plt.ylabel("Freqüència d'aparició")
plt.legend()
plt.show()