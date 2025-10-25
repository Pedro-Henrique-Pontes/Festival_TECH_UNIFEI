# roteiro.py
import os
from pilha import criar_pilha, push, pop, vazia

def _join(caminho_atual, novo_caminho):
    if novo_caminho.startswith('/'):
        return os.path.normpath(novo_caminho)
    else:
        return os.path.normpath(os.path.join(caminho_atual, novo_caminho))

def ir(atual, voltar, avancar, destino):
    push(voltar, atual) #empilha para saber a orientação de onde eu vou e volto 
    avancar.clear()
    destino = os.path.normpath(destino)
    print(f"OK: {destino}")
    novo_local = _join(atual, destino) #junta para ficar certinho /tal/tal
    return novo_local

def voltar(atual, voltar, avancar):
    if atual == os.path.normpath('/') and vazia(voltar):
        print("ERRO: Nenhum local anterior.")
        return atual
    push(avancar, atual)# mesma coisa, empilha para saber a orientação de onde eu vou e volto
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
