#Funções genéricas de pilha
def criar_pilha():
    return []

def vazia(p):
    return len(p) == 0

def empilhar(p, x):
    p.append(x)  # topo = fim da lista

def desempilhar(p):
    if vazia(p):
        return None
    return p.pop()

def topo(p):
    if vazia(p):
        return None
    return p[-1]

def tamanho(p):
    return len(p)

def imprime_pilha(p):
    print("Pilha:", p)
