# roteiro.py
import os
from pilha import criar_pilha, push, pop, vazia

def _join(caminho_atual, novo_caminho):
    # usar isabs para portabilidade (Windows também)
    if os.path.isabs(novo_caminho):
        return os.path.normpath(novo_caminho)
    else:
        return os.path.normpath(os.path.join(caminho_atual, novo_caminho))

def _topo(pilha):
    """Retorna o elemento do topo sem alterar a pilha (usa pop+push)."""
    if vazia(pilha):
        return None
    item = pop(pilha)
    push(pilha, item)
    return item

def ir(atual, voltar, avancar, destino):
    # não empilha o atual se ele já estiver no topo da pilha 'voltar'
    if _topo(voltar) != atual:
        push(voltar, atual)  # empilha o local atual
    avancar.clear()
    destino = os.path.normpath(destino)
    print(f"OK: {destino}")
    novo_local = _join(atual, destino)  # junta para ficar certinho /tal/tal

    # Se o destino é absoluto, empilha os pais do destino para que
    # voltar aconteça passo-a-passo pelos ancestrais, evitando duplicatas.
    if os.path.isabs(novo_local):
        parents = []
        parent = os.path.dirname(novo_local)
        while parent and parent != os.path.sep:
            parents.append(parent)
            parent = os.path.dirname(parent)
        for p in reversed(parents):
            if _topo(voltar) != p:
                push(voltar, p)

    return novo_local

def voltar(atual, voltar, avancar):
    if atual == os.path.normpath('/') and vazia(voltar):
        print("ERRO: Nenhum local anterior.")
        return atual
    push(avancar, atual)  # empilha para poder avançar depois
    anterior = pop(voltar)
    print(f"OK: {anterior}")
    # Ao voltar tudo, defini um local vazio \, como se fosse o ponto inicial onde a partir dele você vai pros locais
    return anterior

def avancar(atual, voltar, avancar):
    if vazia(avancar):
        print("ERRO: Nenhum local para avançar.")
        return atual
    push(voltar, atual)
    proximo = pop(avancar)
    print(f"OK: {proximo}")
    return proximo

def onde(atual):
    print(atual)
    print(atual)
