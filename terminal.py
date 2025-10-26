# terminal.py

from fila import *
from ingressos import *
from roteiro import *
from pilha import criar_pilha, push, pop, vazia

def copiar_estado(fila_padrao, fila_prioridade, atendidos, tempo_logico, tipo_fila):
    from copy import deepcopy
    return {
        "fila_padrao": deepcopy(fila_padrao),
        "fila_prioridade": deepcopy(fila_prioridade),
        "atendidos": deepcopy(atendidos),
        "tempo_logico": tempo_logico,
        "tipo_fila": tipo_fila
    }

#Fiz diferente do que foi pedido para deixar mais bonitinho o menu
def cmd_ajuda():
    print("=" * 60)
    print("                   COMANDOS DISPONÍVEIS   ")
    print("=" * 60)
    print(f"{'COMANDO':<15} | {'DESCRIÇÃO'}")
    print("-" * 60)
    print(f"{'COMPRAR':<15} | Comprar <nome> <categoria: VIP/INTEIRA/MEIA>")
    print(f"{'ENTRAR':<15} | Permite entrada do próximo da fila")
    print(f"{'ESPIAR':<15} | Mostra próximo sem remover")
    print(f"{'CANCELAR':<15} | Cancela ingresso por ID")
    print(f"{'LISTAR':<15} | Lista todos na fila atual")
    print(f"{'ESTATISTICAS':<15} | Mostra estatísticas")
    print(f"{'MODO':<15} | MODO PADRAO / PRIORIDADE")
    print(f"{'IR':<15} | Salva estado e avança (ex: IR confirmar)")
    print(f"{'VOLTAR':<15} | Retorna ao estado anterior")
    print(f"{'AVANCAR':<15} | Refaz um estado desfeito")
    print(f"{'ONDE':<15} | Mostra descrição do estado atual")
    print(f"{'SAIR':<15} | Encerra o sistema")
    print("=" * 60)
    
def bilheteria_portaria():
    fila_padrao = criar_fila()
    fila_prioridade = criar_fila_prioridade()
    tempo_logico = 0
    tipo_fila = "PADRAO"
    atendidos = []

    # criei aqui as pilhas pra ir salvando cada comando, pra poder desfazer e refazer depois
    historico_desfazer = criar_pilha()
    historico_refazer = criar_pilha()

    # criei aqui as pilhas para ir e voltar nos "stands de navegação"
    local_atual = "/"
    pilha_voltar = criar_pilha()
    pilha_avancar = criar_pilha()

    #aqui começa o loop 
    while True:
        try:
            entrada = input("> ").strip()
        except EOFError:
            print("\nEncerrando o sistema.")
            break
        if not entrada:
            continue
        partes = entrada.split()
        cmd = partes[0].upper()

        # =============== Comandos de navegação (locais) ===============
        #puxei todos os comando abaixo do arquivo roteiro

        if cmd == "IR":
            if len(partes) < 2 or not partes[1].strip():
                print("Uso: IR <caminho>")
                continue
            destino = partes[1].strip()
            local_atual = ir(local_atual, pilha_voltar, pilha_avancar, destino)

        elif cmd == "VOLTAR":
            local_atual = voltar(local_atual, pilha_voltar, pilha_avancar)

        elif cmd == "AVANCAR":
            local_atual = avancar(local_atual, pilha_voltar, pilha_avancar)

        elif cmd == "ONDE":
            onde(local_atual)

        # =============== Comandos da bilheteria ===============
        elif cmd == "AJUDA":
            cmd_ajuda()

        elif cmd == "MODO":
            if len(partes) != 2:
                print("Comando inválido. Uso: MODO PADRAO/PRIORIDADE")
                continue
            novo_modo = partes[1].upper()
            if novo_modo not in ["PADRAO", "PRIORIDADE"]:
                print("Modo inválido.")
                continue

            if novo_modo == tipo_fila:
                print("OK")  # já está nesse modo
                continue

            # Salvar estado ANTES da conversão, com descrição da ação
            acao_descr = f"MODO {tipo_fila}->{novo_modo}"
            push(historico_desfazer, {"estado": copiar_estado(fila_padrao, fila_prioridade, atendidos, tempo_logico, tipo_fila), "acao": acao_descr})
            historico_refazer.clear()

            # Converter filas conforme o novo modo
            if tipo_fila == "PADRAO" and novo_modo == "PRIORIDADE":
                # Converter fila_padrao → fila_prioridade
                nova_fila_prioridade = criar_fila_prioridade()
                while not vazia(fila_padrao):
                    pessoa = desenfileirar(fila_padrao)
                    enfileirar_prioridade(nova_fila_prioridade, pessoa)
                fila_prioridade = nova_fila_prioridade

            elif tipo_fila == "PRIORIDADE" and novo_modo == "PADRAO":
                # Converter fila_prioridade → fila_padrao
                nova_fila_padrao = criar_fila()
                # Ordem de prioridade: VIP, INTEIRA, MEIA
                for cat in ["VIP", "INTEIRA", "MEIA"]:
                    while not vazia(fila_prioridade[cat]):
                        pessoa = desenfileirar(fila_prioridade[cat])
                        enfileirar(nova_fila_padrao, pessoa)
                fila_padrao = nova_fila_padrao

            tipo_fila = novo_modo
            print("OK")
            
        elif cmd == "COMPRAR":
            if len(partes) < 3:
                print("Uso: COMPRAR <nome> <categoria>")
                continue
            nome = " ".join(partes[1:-1]).strip()
            categoria = partes[-1].upper()
            if categoria not in ("VIP", "INTEIRA", "MEIA"):
                print("Categoria inválida. Use: VIP, INTEIRA ou MEIA.")
                continue

            # Salvar estado antes, com descrição da ação (sem ID, pois ID é gerado depois)
            acao_descr = f"COMPRAR {nome} ({categoria})"
            push(historico_desfazer, {"estado": copiar_estado(fila_padrao, fila_prioridade, atendidos, tempo_logico, tipo_fila), "acao": acao_descr})
            historico_refazer.clear()

            ingresso = criar_ingresso()
            pessoa = {
                "ID": ingresso,
                "Nome": nome,
                "Categoria": categoria,
                "Chegada": tempo_logico,
                "Atendido": False
            }

            if tipo_fila == "PRIORIDADE":
                enfileirar_prioridade(fila_prioridade, pessoa)
            else:
                enfileirar(fila_padrao, pessoa)

            print(f"OK: ingresso {ingresso}")

        elif cmd == "ENTRAR":
            # Primeiro espiar quem será atendido para guardar descrição da ação
            try:
                if tipo_fila == "PRIORIDADE":
                    # encontra a primeira categoria não vazia
                    p_peek = None
                    for cat in ["VIP", "INTEIRA", "MEIA"]:
                        if not vazia(fila_prioridade[cat]):
                            p_peek = frente(fila_prioridade[cat])
                            break
                else:
                    p_peek = frente(fila_padrao) if not vazia(fila_padrao) else None

                if p_peek is None:
                    print("Nenhuma pessoa na fila.")
                    continue

                acao_descr = f"ENTRAR [{p_peek['ID']}] {p_peek['Nome']} ({p_peek['Categoria']})"

                # Salvar estado antes
                push(historico_desfazer, {"estado": copiar_estado(fila_padrao, fila_prioridade, atendidos, tempo_logico, tipo_fila), "acao": acao_descr})
                historico_refazer.clear()

                tempo_logico += 1
                if tipo_fila == "PRIORIDADE":
                    pessoa = desenfileirar_prioridade(fila_prioridade)
                else:
                    pessoa = desenfileirar(fila_padrao)
                pessoa["Atendido"] = True
                pessoa["Atendimento"] = tempo_logico
                atendidos.append(pessoa)
                print(f"Entrada: [{pessoa['ID']}] {pessoa['Nome']} ({pessoa['Categoria']})")
            except (IndexError, ValueError):
                print("Nenhuma pessoa na fila.")
                # Reverter o tempo_logico? Opcional. Vamos manter como está.

        elif cmd == "ESTATISTICAS":
            pendentes = sum(tamanho(fila_prioridade[c]) for c in ["VIP", "INTEIRA", "MEIA"]) if tipo_fila == "PRIORIDADE" else tamanho(fila_padrao)
            total_atendidos = len(atendidos)
            categorias = {"VIP": 0, "INTEIRA": 0, "MEIA": 0}
            for p in atendidos:
                cat = p["Categoria"]
                if cat in categorias:
                    categorias[cat] += 1
            tempos = [p["Atendimento"] - p["Chegada"] for p in atendidos if "Atendimento" in p]
            media = sum(tempos) / len(tempos) if tempos else 0.0
            print(f"pendentes={pendentes}, atendidos={total_atendidos}, por_categoria={categorias}, espera_media={media:.1f}")

        elif cmd == "ESPIAR":
            if tipo_fila == "PADRAO":
                if not vazia(fila_padrao):
                    p = frente(fila_padrao)
                    print(f"Próximo: [{p['ID']}] {p['Nome']} ({p['Categoria']})")
                else:
                    print("Fila vazia.")
            else:
                for cat in ["VIP", "INTEIRA", "MEIA"]:
                    if not vazia(fila_prioridade[cat]):
                        p = frente(fila_prioridade[cat])
                        print(f"Próximo ({cat}): [{p['ID']}] {p['Nome']} ({p['Categoria']})")
                        break
                else:
                    print("Fila vazia.")

        elif cmd == "LISTAR":
            if tipo_fila == "PADRAO":
                if vazia(fila_padrao):
                    print("Fila vazia.")
                else:
                    for p in fila_padrao:
                        print(f"[{p['ID']}] {p['Nome']} ({p['Categoria']})")
            else:
                vazio = True
                for cat in ["VIP", "INTEIRA", "MEIA"]:
                    if not vazia(fila_prioridade[cat]):
                        vazio = False
                        for p in fila_prioridade[cat]:
                            print(f"[{p['ID']}] {p['Nome']} ({p['Categoria']}) ({cat})")
                if vazio:
                    print("Fila vazia.")

        elif cmd == "CANCELAR":
            if len(partes) != 2:
                print("Uso: CANCELAR <ID>")
                continue
            try:
                id_cancelar = int(partes[1])
            except ValueError:
                print("ID inválido.")
                continue

            # Antes de modificar, procurar a pessoa para montar descrição da ação
            removido = False
            info_nome = None
            info_categoria = None
            if tipo_fila == "PADRAO":
                for p in fila_padrao:
                    if p["ID"] == id_cancelar:
                        removido = True
                        info_nome = p["Nome"]
                        info_categoria = p["Categoria"]
                        break
            else:
                for cat in ["VIP", "INTEIRA", "MEIA"]:
                    for p in fila_prioridade[cat]:
                        if p["ID"] == id_cancelar:
                            removido = True
                            info_nome = p["Nome"]
                            info_categoria = p["Categoria"]
                            break
                    if removido:
                        break

            if not removido:
                print(f"Erro: ingresso {id_cancelar} não encontrado.")
                continue

            acao_descr = f"CANCELAR [{id_cancelar}] {info_nome} ({info_categoria})"

            # Salvar estado antes
            push(historico_desfazer, {"estado": copiar_estado(fila_padrao, fila_prioridade, atendidos, tempo_logico, tipo_fila), "acao": acao_descr})
            historico_refazer.clear()

            # Executar remoção
            if tipo_fila == "PADRAO":
                nova_fila = criar_fila()
                while not vazia(fila_padrao):
                    p = desenfileirar(fila_padrao)
                    if p["ID"] == id_cancelar:
                        removido = True
                    else:
                        enfileirar(nova_fila, p)
                fila_padrao = nova_fila
            else:
                for cat in ["VIP", "INTEIRA", "MEIA"]:
                    nova_fila = criar_fila()
                    while not vazia(fila_prioridade[cat]):
                        p = desenfileirar(fila_prioridade[cat])
                        if p["ID"] == id_cancelar:
                            removido = True
                        else:
                            enfileirar(nova_fila, p)
                    fila_prioridade[cat] = nova_fila

            if removido:
                print(f"OK: ingresso {id_cancelar} cancelado")
            else:
                print(f"Erro: ingresso {id_cancelar} não encontrado.")

        elif cmd == "DESFAZER":
            if vazia(historico_desfazer):
                print("Nada para desfazer.")
            else:
                # Pegar o snapshot que representa o estado ANTES da ação que queremos desfazer
                snapshot = pop(historico_desfazer)
                # salvar estado atual no histórico de refazer, associando a mesma descrição de ação
                push(historico_refazer, {"estado": copiar_estado(fila_padrao, fila_prioridade, atendidos, tempo_logico, tipo_fila), "acao": snapshot["acao"]})
                # restaurar o estado salvo (o 'estado' dentro do snapshot)
                estado = snapshot["estado"]
                fila_padrao = estado["fila_padrao"]
                fila_prioridade = estado["fila_prioridade"]
                atendidos = estado["atendidos"]
                tempo_logico = estado["tempo_logico"]
                tipo_fila = estado["tipo_fila"]
                print(f"OK: Desfeito: {snapshot['acao']}")

        elif cmd == "REFAZER":
            if vazia(historico_refazer):
                print("Nada para refazer.")
            else:
                snapshot = pop(historico_refazer)
                # salvar estado atual no histórico de desfazer, associando a mesma descrição de ação
                push(historico_desfazer, {"estado": copiar_estado(fila_padrao, fila_prioridade, atendidos, tempo_logico, tipo_fila), "acao": snapshot["acao"]})
                estado = snapshot["estado"]
                fila_padrao = estado["fila_padrao"]
                fila_prioridade = estado["fila_prioridade"]
                atendidos = estado["atendidos"]
                tempo_logico = estado["tempo_logico"]
                tipo_fila = estado["tipo_fila"]
                print(f"OK: Refeito: {snapshot['acao']}")

        elif cmd == "SALVAR":
            if len(partes) != 2:
                print("Uso: SALVAR <arquivo.csv>")
                continue
            arquivo = partes[1].strip()
            try:
                with open(arquivo, 'w') as f:
                    f.write("ID,Nome,Categoria,Chegada,Atendido,Atendimento\n")
                    for p in atendidos:
                        atend = p.get("Atendimento", "")
                        f.write("\n" + "-" * 40 + "\n")
                        f.write(f"Ingresso nº {p['ID']}\n")
                        f.write(f"Nome: {p['Nome']}\n")
                        f.write(f"Categoria: {p['Categoria']}\n")
                        f.write(f"Horário de Chegada: {p['Chegada']}\n")
                        f.write(f"Atendido: {p['Atendido']}\n")
                        f.write(f"Tempo de Atendimento: {atend}\n")
                        f.write("-" * 40 + "\n")
                print("OK")
            except Exception as e:
                print(f"Erro ao salvar: {e}")

        elif cmd == "CARREGAR":
            print("CARREGAR não implementado.")  # opcional

        elif cmd == "SAIR":
            print("Encerrando o sistema.")
            break

        else:
            print("Comando inválido.")

def main():
    bilheteria_portaria()

if __name__ == "__main__":
    main()
