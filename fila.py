# fila.py
from pilha import criar_pilha, push, pop, vazia, tamanho

def criar_fila():
    return []

def enfileirar(fila, item):
    fila.append(item)

def desenfileirar(fila):
    if not fila:
        raise IndexError("Fila vazia")
    return fila.pop(0)

def frente(fila):
    if not fila:
        raise IndexError("Fila vazia")
    return fila[0]

def criar_fila_prioridade():
    return {
        "VIP": criar_fila(),
        "INTEIRA": criar_fila(),
        "MEIA": criar_fila()
    }

def enfileirar_prioridade(fila_dict, pessoa):
    cat = pessoa["Categoria"]
    if cat in fila_dict:
        enfileirar(fila_dict[cat], pessoa)
    else:
        raise ValueError("Categoria inválida")

def desenfileirar_prioridade(fila_dict):
    for cat in ["VIP", "INTEIRA", "MEIA"]:
        if not vazia(fila_dict[cat]):
            return desenfileirar(fila_dict[cat])
    raise IndexError("Todas as filas estão vazias")