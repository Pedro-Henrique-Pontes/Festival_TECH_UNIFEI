from fila import*
from ingressos import*

def bilheteria_portaria():
    portaria = criar_fila()

    while True:

        a = input().strip()
        partes = a.split()

        cmd = partes[0].upper()
        if cmd == "AJUDA" and len(partes) == 1:
            print("Comandos: COMPRAR/ENTRAR/ESPIAR/CANCELAR/LISTAR/ESTATISTICAS/MODO/IR/VOLTAR/AVANCAR/ONDE/DESFAZER/REFAZER/SALVAR/CARREGAR/SAIR")
        
        # MODO PADRAO/PRIORIDADE
        elif cmd == "MODO" and len(partes) == 2:
            modo = partes[1].upper()
            if modo in ("PADRAO", "PRIORIDADE"):
                tipo_fila = modo
                if tipo_fila == "PADRAO":
                    portaria = criar_fila()
                else:
                    portaria = criar_fila_prioridade()
                print("OK")
            else:
                print("Comando inválido. Uso correto: MODO PADRAO/PRIORIDADE")

        # COMPRAR
        elif cmd == "COMPRAR" and len(partes) >= 3:
            categoria = partes[-1].upper()
            nome = " ".join(partes[1:-1]).strip()
            ingresso = criar_ingresso()

            pessoa = {
                "ID": ingresso,
                "Nome": nome,
                "Categoria": categoria
            }

            if tipo_fila == "PRIORIDADE":
                enfileirar_prioridade(portaria, pessoa)
            else:
                enfileirar(portaria, pessoa)

        elif cmd == "ENTRAR" and len(partes) == 1:

        elif cmd == "ESPIAR" and len(partes) == 1: 

        elif cmd == "CANCELAR" and len(partes) == 1: 
            try:
                id_cancelar = int(partes[1])
            except ValueError:
                print("ID inválido.")
                continue

            removido = False  

            if tipo_fila == "PADRAO":
                nova_fila = criar_fila()
                while not vazia(portaria):  # percorre a fila atual
                    pessoa = desenfileirar(portaria)
                    if pessoa["ID"] == id_cancelar:
                        print(f"Ingresso Nº {id_cancelar} removido da fila.")
                        removido = True
                    else:
                        enfileirar(nova_fila, pessoa)
                portaria = nova_fila  

            else:  # MODO PRIORIDADE
                for categoria in ["VIP", "INTEIRA", "MEIA"]: #percorrer cadauma das 3 filas
                    if categoria in portaria:
                        nova_fila = criar_fila()
                        while not vazia(portaria[categoria]): #achar o id que quero cancelar
                            pessoa = desenfileirar(portaria[categoria])
                            if pessoa["ID"] == id_cancelar:
                                print(f"Ingresso Nº {id_cancelar} removido da fila ({categoria}).")
                                removido = True
                            else:
                                enfileirar(nova_fila, pessoa)
                        portaria[categoria] = nova_fila

            if not removido:
                print(f"Ingresso Nº {id_cancelar} não encontrado.")

        elif cmd == "LISTAR" and len(partes) == 1: 
            print(portaria)
        elif cmd == "ENTRAR" and len(partes) == 1: 

        else:
            print("Comando inválido. Digite AJUDA para ver os comandos disponíveis.")

def main():
    bilheteria_portaria()
main()