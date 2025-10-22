
def criar_ingresso(pessoa, fila, contador):

    """ cria o ingresso da pessoa"""
    categoria = pessoa["Categoria"].upper()
    ingresso = { 
        "id": contador, 
        "nome": pessoa["Nome"], 
        "prioridade": categoria
    }
    
    """colocar contador na main"""
    contador += 1
    
    """enfileira a pessoa na fila"""
    enfileirar_prioridade(fila,pessoa )
    
    return ingresso, contador
