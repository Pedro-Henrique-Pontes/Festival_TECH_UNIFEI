#----Funções genéricas de fila normal----#
from collections import deque

def criar_fila():
    return deque()
def vazia(fila):
    return len(fila) == 0

def enfileirar(fila, x):
    fila.append(x) 

def desenfileirar(fila):
    if vazia(fila):
        raise IndexError("fila vazia")
    return fila.popleft() 

def tamanho(fila):
    return len(fila)

def frente(fila):
    if vazia(fila):
        raise IndexError("fila vazia")
    return fila[0]

# ---- Fila com prioridade ---- #
def criar_fila_prioridade():
    
    return {
        "VIP": criar_fila(),
        "INTEIRA": criar_fila(),
        "MEIA": criar_fila()
    }

def enfileirar_prioridade(filas, pessoa):
    """Enfileira na fila correspondente à categoria da pessoa"""
    categoria = pessoa["Categoria"].upper()
    if categoria not in filas:
        raise ValueError("Categoria inválida. Use: VIP, INTEIRA ou MEIA.")
    enfileirar(filas[categoria], pessoa)

def desenfileirar_prioridade(filas):
    """Desenfileira respeitando a prioridade: VIP → INTEIRA → MEIA"""
    if not vazia(filas["VIP"]):
        return desenfileirar(filas["VIP"])
    elif not vazia(filas["INTEIRA"]):
        return desenfileirar(filas["INTEIRA"])
    elif not vazia(filas["MEIA"]):
        return desenfileirar(filas["MEIA"])
    else:
        raise IndexError("Todas as filas estão vazias")

def vazia_prioridade(filas):
    """Verifica se todas as filas estão vazias"""
    return all(vazia(fila) for fila in filas.values())

