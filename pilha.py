# pilha.py

def criar_pilha():
    return []

def push(pilha, item):
    pilha.append(item)

def pop(pilha):
    if not pilha:
        raise IndexError("Pilha vazia")
    return pilha.pop()

def vazia(pilha):
    return len(pilha) == 0

def tamanho(pilha):
    return len(pilha)