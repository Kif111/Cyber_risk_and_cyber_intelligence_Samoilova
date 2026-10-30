# ============================================================
# Задание 1 (Финальная версия): Хеш-функция SHA-3 (Keccak)
# Архитектура: Губка (Sponge) + Перестановка Keccak-f[1600]
# ============================================================

# ------------------------------------------------------------
# 1. Вспомогательные функции (работа с 64-битными словами)
# ------------------------------------------------------------
def rotl64(x, n):
    """Циклический сдвиг 64-битного числа влево на n бит."""
    n %= 64
    return ((x << n) | (x >> (64 - n))) & 0xFFFFFFFFFFFFFFFF

def bytes_to_lanes(b):
    """Превращает массив байт в список из 25 64-битных слов (lanes)."""
    lanes = []
    for i in range(0, len(b), 8):
        # Берем 8 байт, переводим в число (Little-Endian)
        lanes.append(int.from_bytes(b[i:i+8], 'little'))
    return lanes

def lanes_to_bytes(lanes):
    """Превращает 25 слов обратно в массив байт."""
    b = bytearray()
    for lane in lanes:
        b.extend(lane.to_bytes(8, 'little'))
    return bytes(b)

# ------------------------------------------------------------
# 2. Константы раундов (шаг Iota) и сдвиги (шаг Rho)
# ------------------------------------------------------------
# Константы раундов (RC) для 24 раундов
RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
    0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
    0x8000000080008081, 0x8000000000008009, 0x000000000000008A,
    0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
    0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
    0x000000000000800A, 0x800000008000000A, 0x8000000080008081,
    0x8000000000008080, 0x0000000080000001, 0x8000000080008008
]

# Таблица сдвигов для шага Rho (r[x][y])
RHO_OFFSETS = [
    [0, 36, 3, 41, 18],
    [1, 44, 10, 45, 2],
    [62, 6, 43, 15, 61],
    [28, 55, 25, 21, 56],
    [27, 20, 39, 8, 14]
]

# ------------------------------------------------------------
# 3. Перестановка Keccak-f[1600]
# ------------------------------------------------------------
def keccak_f(state):
    """
    Применяет перестановку Keccak-f к состоянию (список из 25 64-битных слов).
    24 раунда, в каждом 5 шагов: Theta, Rho, Pi, Chi, Iota.
    """
    # state — это список длиной 25. Индексы от 0 до 24.
    # Для удобства будем воспринимать его как матрицу 5x5: A[x][y] = state[x + 5*y]
    
    for rnd in range(24):
        # --- Шаг 1: Theta (θ) ---
        C = [state[x] ^ state[x+5] ^ state[x+10] ^ state[x+15] ^ state[x+20] for x in range(5)]
        D = [C[(x-1)%5] ^ rotl64(C[(x+1)%5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                state[x + 5*y] ^= D[x]
                
        # --- Шаг 2 & 3: Rho (ρ) и Pi (π) ---
        # Мы совмещаем их для эффективности: переставляем и сдвигаем
        new_state = [0] * 25
        for x in range(5):
            for y in range(5):
                # Pi переставляет координаты: B[y][2x + 3y] = rot(A[x][y])
                new_x = y
                new_y = (2*x + 3*y) % 5
                new_state[new_x + 5*new_y] = rotl64(state[x + 5*y], RHO_OFFSETS[x][y])
        state = new_state
        
        # --- Шаг 4: Chi (χ) ---
        for y in range(5):
            row = [state[x + 5*y] for x in range(5)]
            for x in range(5):
                # A[x][y] = A[x][y] XOR ((NOT A[x+1][y]) AND A[x+2][y])
                state[x + 5*y] = row[x] ^ ((~row[(x+1)%5]) & row[(x+2)%5])
                
        # --- Шаг 5: Iota (ι) ---
        state[0] ^= RC[rnd]
        
    return state
# ------------------------------------------------------------
# 4. Губка (Sponge) и паддинг SHA-3
# ------------------------------------------------------------
# Параметры для SHA3-256:
# Состояние = 1600 бит (200 байт)
# Capacity (c) = 512 бит (64 байта)
# Rate (r) = 1600 - 512 = 1088 бит (136 байт)

RATE_BYTES = 136
CAPACITY_BYTES = 64

def sponge_absorb_squeeze(message_bytes):
    # 1. Инициализация (нули)
    state = [0] * 25
    
    # 2. Паддинг pad10*1
    # Добавляем 0x06 (биты 011) и 0x80 в конец, чтобы получить 1...1
    padded = bytearray(message_bytes)
    padded.append(0x06) 
    
    # Дополняем нулями до кратности RATE_BYTES
    while len(padded) % RATE_BYTES != 0:
        padded.append(0x00)
        
    # Меняем последний байт на 0x80 (добавляем старший бит 1)
    padded[-1] ^= 0x80 
    
    # 3. Фаза Absorb (Впитывание)
    for i in range(0, len(padded), RATE_BYTES):
        block = padded[i:i+RATE_BYTES]
        # XOR блока с началом состояния (первые 136 байт = 17 lanes)
        for j in range(RATE_BYTES // 8):
            lane_bytes = block[j*8:(j+1)*8]
            state[j] ^= int.from_bytes(lane_bytes, 'little')
        # Перестановка
        state = keccak_f(state)
        
    # 4. Фаза Squeeze (Выжимание) — нам нужно 256 бит = 32 байта
    output = bytearray()
    while len(output) < 32:
        # Берем первые RATE_BYTES (или сколько нужно) из состояния
        for j in range(RATE_BYTES // 8):
            if len(output) >= 32:
                break
            lane_bytes = state[j].to_bytes(8, 'little')
            output.extend(lane_bytes)
            
        # Если нужно больше — снова перестановка
        if len(output) < 32:
            state = keccak_f(state)
            
    return bytes(output[:32])

# ------------------------------------------------------------
# 5. Утилиты и Интерфейс
# ------------------------------------------------------------
def bin_to_bytes(bin_str):
    """Дополняет BIN слева нулями до кратности 8 и переводит в байты."""
    if len(bin_str) % 8 != 0:
        bin_str = bin_str.zfill(len(bin_str) + (8 - len(bin_str) % 8))
    return bytes(int(bin_str[i:i+8], 2) for i in range(0, len(bin_str), 8))

def bytes_to_bin(b):
    """Переводит байты в BIN-строку."""
    return "".join(format(x, "08b") for x in b)

def hash_sha3_256(message_bin):
    """Главная функция: BIN на входе -> 256-битный хеш BIN на выходе."""
    msg_bytes = bin_to_bytes(message_bin)
    hash_bytes = sponge_absorb_squeeze(msg_bytes)
    return bytes_to_bin(hash_bytes)

def input_bits(prompt):
    while True:
        v = input(prompt).replace(" ", "").replace("\n", "")
        if not v:
            continue
        if any(c not in "01" for c in v):
            print("Ошибка: только 0 и 1.")
            continue
        return v

def main():
    while True:
        print("\n" + "=" * 60)
        print("     ХЕШ-ФУНКЦИЯ SHA-3 (Keccak Sponge)")
        print("=" * 60)
        print("1. Вычислить хеш (SHA3-256)")
        print("2. Выйти")
        choice = input("Выбор: ").strip()

        if choice == "1":
            msg = input_bits("Сообщение (BIN, любой длины):\n")
            if not msg:
                continue
                
            print("\nВычисляем хеш...")
            h = hash_sha3_256(msg)
            
            print("\n" + "=" * 60)
            print("РЕЗУЛЬТАТ (256 бит)")
            print("=" * 60)
            print("ХЕШ (BIN):", h)
            print("Длина:", len(h), "бит")
            print("=" * 60)
            
        elif choice == "2":
            print("Выход.")
            break

if __name__ == "__main__":
    main()
