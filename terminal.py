from fila import *
from ingressos import *

def bilheteria_portaria():

    fila_padrao = criar_fila()
    fila_prioridade = criar_fila_prioridade()

    tempo_logico = 0

    tipo_fila = "PADRAO"  # por definição a fila é modo padrao

    atendidos = []

    while True:
        a = input().strip()
        partes = a.split()

        if not partes:
            continue

        cmd = partes[0].upper()

        if cmd == "AJUDA" and len(partes) == 1: #Já que é para ajudar, fiz uma tabela completona
            print("=" * 60)
            print("                   COMANDOS DISPONÍVEIS   ")
            print("=" * 60)
            print(f"{'COMANDO':<15} | {'DESCRIÇÃO'}")
            print("-" * 60)
            print(f"{'COMPRAR':<15} | Comprar <nome da pessoa> <categoria: VIP/INTEIRA/MEIA>")
            print(f"{'ENTRAR':<15} | Permite a entrada do próximo da fila")
            print(f"{'ESPIAR':<15} | Mostra quem é o próximo sem retirar da fila")
            print(f"{'CANCELAR':<15} | Cancela <ID do ingresso> e removê-lo da fila")
            print(f"{'LISTAR':<15} | Exibe todos os ingressos na fila atual")
            print(f"{'ESTATISTICAS':<15} | Mostra dados gerais sobre os ingressos vendidos")
            print(f"{'MODO':<15} | Mudar o tipo de fila: MODO PADRAO ou MODO PRIORIDADE")
            print(f"{'IR':<15} | Avança para o próximo estado salvo (em desenvolvimento)")
            print(f"{'VOLTAR':<15} | Retorna ao estado anterior (em desenvolvimento)")
            print(f"{'AVANCAR':<15} | Similar ao comando IR (em desenvolvimento)")
            print(f"{'ONDE':<15} | Mostra o estado atual do sistema")
            print(f"{'DESFAZER':<15} | Desfaz a última ação realizada (em desenvolvimento)")
            print(f"{'REFAZER':<15} | Refaz uma ação desfeita (em desenvolvimento)")
            print(f"{'SALVAR':<15} | Salva o estado atual da fila em arquivo")
            print(f"{'CARREGAR':<15} | Carrega uma fila salva anteriormente")
            print(f"{'SAIR':<15} | Encerra o sistema")
            print("=" * 60)
                
        # ===== MODO PADRAO/PRIORIDADE =====
        elif cmd == "MODO" and len(partes) == 2:
            modo = partes[1].upper()
            if modo in ["PADRAO", "PRIORIDADE"]:
                tipo_fila = modo
                print("OK")
            else:
                print("Comando inválido. Uso correto: MODO PADRAO/PRIORIDADE")

        # ===== COMPRAR =====
        elif cmd == "COMPRAR" and len(partes) >= 3:
            nome = " ".join(partes[1:-1]).strip()
            categoria = partes[-1].upper()
            ingresso = criar_ingresso()

            pessoa = {
                "ID": ingresso,
                "Nome": nome,
                "Categoria": categoria,
                "Chegada": tempo_logico,
                "Atendido": False
            }

            if tipo_fila == "PRIORIDADE":
                if categoria not in ("VIP", "INTEIRA", "MEIA"):
                    print("Categoria inválida. Use: VIP, INTEIRA ou MEIA.")
                    continue
                enfileirar_prioridade(fila_prioridade, pessoa)
            else:
                enfileirar(fila_padrao, pessoa)

            print(f"OK, ingresso Nº {ingresso} criado para {nome} ({categoria})")

        # ===== ENTRAR =====
        elif cmd == "ENTRAR" and len(partes) == 1:
            tempo_logico += 1
            try:
                if tipo_fila == "PRIORIDADE":
                    pessoa = desenfileirar_prioridade(fila_prioridade)
                else:
                    pessoa = desenfileirar(fila_padrao)
                
                pessoa["Atendido"] = True
                pessoa["Atendimento"] = tempo_logico
                atendidos.append(pessoa)
                print(f"Entrada: [{pessoa['ID']}] {pessoa['Nome']} ({pessoa['Categoria']})")
            except IndexError:
                print("Nenhuma pessoa na fila.")

        # ===== ESTATISTICAS =====
        elif cmd == "ESTATISTICAS" and len(partes) == 1:
            pendentes = 0
            if tipo_fila == "PRIORIDADE":
                pendentes = sum(tamanho(fila_prioridade[c]) for c in ["VIP", "INTEIRA", "MEIA"])
            else:
                pendentes = tamanho(fila_padrao)

            total_atendidos = len(atendidos)

            # contagem por categoria
            categorias = {"VIP": 0, "INTEIRA": 0, "MEIA": 0}
            for p in atendidos:
                cat = p["Categoria"].upper()
                if cat in categorias:
                    categorias[cat] += 1

            # tempo médio de espera
            tempos = []
            for p in atendidos:
                if "Atendimento" in p:
                    espera = p["Atendimento"] - p["Chegada"]
                    tempos.append(espera)
            media = sum(tempos) / len(tempos) if tempos else 0

            print("===== ESTATÍSTICAS =====")
            print(f"Total pendente:  {pendentes}")
            print(f"Total atendido:  {total_atendidos}")
            print(f"VIP: {categorias['VIP']}  |  INTEIRA: {categorias['INTEIRA']}  |  MEIA: {categorias['MEIA']}")
            print(f"Tempo médio de espera: {media:.2f} minutos")
            print("========================")
        # ===== CANCELAR =====
        elif cmd == "CANCELAR" and len(partes) == 2:
            try:
                id_cancelar = int(partes[1])
            except ValueError:
                print("ID inválido.")
                continue

            removido = False

            if tipo_fila == "PADRAO":
                nova_fila = criar_fila()
                while not vazia(fila_padrao):
                    pessoa = desenfileirar(fila_padrao)
                    if pessoa["ID"] == id_cancelar:
                        print(f"Ingresso Nº {id_cancelar} removido da fila.")
                        removido = True
                    else:
                        enfileirar(nova_fila, pessoa)
                fila_padrao = nova_fila
            else:
                for categoria in ["VIP", "INTEIRA", "MEIA"]:
                    nova_fila = criar_fila()
                    while not vazia(fila_prioridade[categoria]):
                        pessoa = desenfileirar(fila_prioridade[categoria])
                        if pessoa["ID"] == id_cancelar:
                            print(f"Ingresso Nº {id_cancelar} removido da fila ({categoria}).")
                            removido = True
                        else:
                            enfileirar(nova_fila, pessoa)
                    fila_prioridade[categoria] = nova_fila

            if not removido:
                print(f"Ingresso Nº {id_cancelar} não encontrado.")

        # ===== ESPIAR =====
        elif cmd == "ESPIAR" and len(partes) == 1:
            if tipo_fila == "PADRAO":
                if not vazia(fila_padrao):
                    print("Próximo da fila:", frente(fila_padrao))
                else:
                    print("Fila vazia.")
            else:
                for categoria in ["VIP", "INTEIRA", "MEIA"]:
                    if not vazia(fila_prioridade[categoria]):
                        print(f"Próximo ({categoria}):", frente(fila_prioridade[categoria]))
                        break
                else:
                    print("Nenhum cliente nas filas de prioridade.")

        # ===== LISTAR =====
        elif cmd == "LISTAR" and len(partes) == 1:
            if tipo_fila == "PADRAO":
                print(list(fila_padrao))
            else:
                for categoria in ["VIP", "INTEIRA", "MEIA"]:
                    print(f"{categoria}: {list(fila_prioridade[categoria])}")

        elif cmd == "SAIR":
            print("Encerrando o sistema.")
            break

        else:
            print("Comando inválido. Digite AJUDA para ver os comandos disponíveis.")


def main():
    bilheteria_portaria()

main()


