#Proyecto final Teoría de la Computación
#José Antonio Castro Mariscal

# Autómata finito (modelo matricial) para validar contraseñas:
# Reglas:
# 1) Debe iniciar con letra
# 2) Debe contener al menos un número
# 3) Debe contener al menos un carácter especial @ # $ % &
# 4) Debe tener mínimo 8 caracteres
# 5) Debe contener al menos una letra mayúscula

from typing import Dict, List, Tuple

#Parámetros / categorías 
SPECIALS = set("@#$%&")
CATEGORIES = ["LOWER", "UPPER", "DIGIT", "SPECIAL", "OTHER"]

# --- Mapeo de estados ---
# state 0 = q0 (antes de leer)
# states 1..64 = producto (length_index 1..8) x (D,S,U) bits
# state 65 = q_dead

N_LENGTH = 8  # 1..7, 8 => 8 or more
FLAGS_COMBINATIONS = 8  # 2^3
Q0 = 0
FIRST_PRODUCT_STATE = 1
DEAD = 65
TOTAL_STATES = 66

def flags_to_index(D: int, S: int, U: int) -> int:
    return D*4 + S*2 + U*1  # 0..7

def product_state_index(length_index: int, D: int, S: int, U: int) -> int:
    # length_index in 1..8
    return FIRST_PRODUCT_STATE + (length_index - 1)*FLAGS_COMBINATIONS + flags_to_index(D, S, U)

def decode_product_state(idx: int) -> Tuple[int,int,int,int]:
    # returns (length_index, D, S, U)
    off = idx - FIRST_PRODUCT_STATE
    length_index = off // FLAGS_COMBINATIONS + 1
    flags = off % FLAGS_COMBINATIONS
    D = (flags >> 2) & 1
    S = (flags >> 1) & 1
    U = flags & 1
    return length_index, D, S, U

# --- Construcción de la tabla de transición: lista de dicts ---
def categorize(ch: str) -> str:
    if ch.islower(): return "LOWER"
    if ch.isupper(): return "UPPER"
    if ch.isdigit(): return "DIGIT"
    if ch in SPECIALS: return "SPECIAL"
    return "OTHER"

# Inicializa la tabla con DEAD por defecto
transition: List[Dict[str,int]] = [ {cat: DEAD for cat in CATEGORIES} for _ in range(TOTAL_STATES) ]

# Desde DEAD permaneces DEAD
for cat in CATEGORIES:
    transition[DEAD][cat] = DEAD

# Desde q0 (estado 0): solo letras (lower o upper) aceptables
for cat in CATEGORIES:
    if cat == "LOWER":
        # length=1, U=0, D=0, S=0
        transition[Q0][cat] = product_state_index(1, 0, 0, 0)
    elif cat == "UPPER":
        # length=1, U=1
        transition[Q0][cat] = product_state_index(1, 0, 0, 1)
    else:
        transition[Q0][cat] = DEAD

# Rellenar el bloque de 64 estados producto
for length_index in range(1, N_LENGTH+1):  # 1..8 (8 significa 8+)
    for flags in range(FLAGS_COMBINATIONS):  # 0..7
        D = (flags >> 2) & 1
        S = (flags >> 1) & 1
        U = flags & 1
        state_idx = product_state_index(length_index, D, S, U)
        # para cada categoría calculamos next state
        for cat in CATEGORIES:
            if cat == "OTHER":
                transition[state_idx][cat] = DEAD
                continue
            # longitud siguiente
            next_len = length_index + 1 if length_index < N_LENGTH else N_LENGTH
            next_D = D or (cat == "DIGIT")
            next_S = S or (cat == "SPECIAL")
            next_U = U or (cat == "UPPER")
            next_state = product_state_index(next_len, int(next_D), int(next_S), int(next_U))
            transition[state_idx][cat] = next_state

#Funciones auxiliares 
def is_accepting(state_idx: int) -> bool:
    if state_idx < FIRST_PRODUCT_STATE or state_idx == DEAD:
        return False
    length_index, D, S, U = decode_product_state(state_idx)
    return (length_index == N_LENGTH) and (D == 1) and (S == 1) and (U == 1)

# Mostrar estado en forma legible
def state_str(idx: int) -> str:
    if idx == Q0: return "q0"
    if idx == DEAD: return "q_dead"
    l, D, S, U = decode_product_state(idx)
    return f"q_len{l}_D{D}S{S}U{U}"

#Simulación con mensajes paso a paso 
def simulate_with_messages(password: str):
    state = Q0
    # estados previos de flags para detectar cambios
    prev_D = prev_S = prev_U = 0
    prev_len = 0
    print("Iniciando simulación del AF para validar contraseña...")
    for i, ch in enumerate(password, start=1):
        cat = categorize(ch)
        next_state = transition[state].get(cat, DEAD)
        print(f"\nPaso {i}: leído '{ch}' (categoría {cat})")
        if next_state == DEAD:
            if state == Q0 and cat != "LOWER" and cat != "UPPER":
                print("Primer carácter no es letra. Condición 'inicia con letra' fallida. TERMINADO.")
            else:
                print("Símbolo inválido detectado (no permitido). CONTRASEÑA RECHAZADA. TERMINADO.")
            return False
        # decodificar estado siguiente para ver cambios en flags / longitud
        length_index, D, S, U = decode_product_state(next_state)
        # mensaje cuando una condición pasa a cumplida
        if prev_len < 8 and length_index == N_LENGTH:
            print("Condición de longitud mínima (>=8) ahora cumplida (se alcanzó 8 caracteres).")
        if prev_D == 0 and D == 1:
            print("Condición 'al menos un número' cumplida (se leyó un dígito).")
        if prev_S == 0 and S == 1:
            print("Condición 'al menos un caracter especial' cumplida (se leyó @/#/$/%/&).")
        if prev_U == 0 and U == 1:
            print("Condición 'al menos una mayúscula' cumplida (se leyó una letra mayúscula).")
        # avanzar
        state = next_state
        prev_len, prev_D, prev_S, prev_U = length_index, D, S, U
        print(f"→ Estado actual: {state_str(state)}")

    # terminado de leer toda la cadena: evaluar aceptación final
    if is_accepting(state):
        print("\nRESULTADO: CONTRASEÑA ACEPTADA (todas las condiciones cumplidas).")
        return True
    else:
        print("\nRESULTADO: CONTRASEÑA RECHAZADA.")
        # indicar qué condiciones faltaron
        length_index, D, S, U = decode_product_state(state) if state not in (Q0, DEAD) else (0,0,0,0)
        if length_index < N_LENGTH:
            print(f" - Longitud insuficiente: {length_index} caracteres (se requieren >= {N_LENGTH}).")
        if D == 0:
            print(" - Falta al menos un número.")
        if S == 0:
            print(" - Falta al menos un carácter especial (@ # $ % &).")
        if U == 0:
            print(" - Falta al menos una letra mayúscula.")
        if state == Q0:
            print(" - No se leyó ningún carácter (la contraseña está vacía).")
        return False

# ---- Modo consola ----
if __name__ == "__main__":
    pwd = input("Ingresa la contraseña a validar: ").strip()
    simulate_with_messages(pwd)
