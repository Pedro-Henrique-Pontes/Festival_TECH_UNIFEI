# ingressos.py

_proximo_id = 1

def criar_ingresso():
    global _proximo_id
    id_atual = _proximo_id
    _proximo_id += 1
    return id_atual