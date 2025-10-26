# Festival_TECH_UNIFEI
Trabalho referente à disciplina de Python, Estrutura de dados e Orientação a Objetos

Integrantes
Pedro Henrique Pontes
Matrícula: 

Thalytta Fernandes Damiani
Matrícula:2025004602

# Sistema de Terminal Interativo do Festival Universitário

O projeto utiliza a linguagem Python para criar um terminal de comandos interativo, que simula as operações da bilheteria e portaria, em conjunto também o roteiro de visitantes de um festival universitário.

O terminal faz uso de estruturas de dados como filas e pilhas para implementar uma variedade de comandos que controlam o fluxo de visitantes, o registro de entradas e saídas, além de funcionalidades de navegação entre locais do evento.

### Estruturas de dados
    ```bash
    ┣  terminal.py             # Execução da main e estrturação dos comando
    ┣  pilha.py                # Implementação da pilha
    ┣  fila.py                 # Implementação da fila
    ┣  ingressos.py            # Criação dos ingressos
    ┣  roteiro.py              # Funções de movimentação
    ┗  README.md               # Documentação do projeto
    
### Pré-requisitos
- **Python 3.12** ou superior instalado no sistema.  
- Um terminal (Prompt de Comando, PowerShell, ou o terminal do VSCode).  
### Passos para execução

1. **Baixe ou clone este repositório** em seu computador:  
   ```bash
   https://github.com/Pedro-Henrique-Pontes/Festival_TECH_UNIFEI.git
2. **Acesse a pasta do projeto:**
   ```bash
   cd Festival_TECH_UNIFEI
3. **Execute o programa principal:**
   ```bash
   python terminal.py
4. **O terminal vai aguardar que algum dos comandos sejam executados**
    ```bash
    EXEMPLO DE EXECUÇÃO:
    >ajuda
    ============================================================
                   COMANDOS DISPONÍVEIS   
    ============================================================
    COMANDO         | DESCRIÇÃO
    ------------------------------------------------------------
    COMPRAR         | Comprar <nome> <categoria: VIP/INTEIRA/MEIA>
    ENTRAR          | Permite entrada do próximo da fila
    ESPIAR          | Mostra próximo sem remover
    CANCELAR        | Cancela ingresso por ID
    LISTAR          | Lista todos na fila atual
    ESTATISTICAS    | Mostra estatísticas
    MODO            | MODO PADRAO / PRIORIDADE
    IR              | Salva estado e avança (ex: IR confirmar)
    VOLTAR          | Retorna ao estado anterior
    AVANCAR         | Refaz um estado desfeito
    ONDE            | Mostra descrição do estado atual
    SAIR            | Encerra o sistema
    ============================================================
    >comprar Gabi meia
    OK: ingresso 1
    
    >comprar Pedro vip
    OK: ingresso 2
    
    >comprar Nicole inteira
    OK: ingresso 3
    
    > listar
    [1] Gabi (MEIA)
    [2] Pedro (VIP)
    [3] Nicole (INTEIRA)
    
    >modo prioridade
    
    >entrar
    Entrada: [2] Pedro (VIP)
    
    > estatisticas
    pendentes=2, atendidos=1, por_categoria={'VIP': 1, 'INTEIRA': 0, 'MEIA': 0}, espera_media=1.0
    
    >modo padrao
    
    >entrar
    Entrada: [1] Gabi (Meia)
    
    >desfazer
    OK: Desfeito: ENTRAR [1] gabi (MEIA)
    
    >espiar
    Próximo: [1] gabi (Meia)
    
    >refazer
    OK: Refeito: ENTRAR [1] gabi (VIP)

    >cancelar 3
    OK: ingresso 3 cancelado
    ir \lago
    OK: \lago
    
    > ir \palco\vip
    OK: \palco\vip
    
    > voltar
    OK: \palco
    
    > avancar
    OK: \palco\vip
    
    > onde
    \palco\vip

    >sair
    Encerrando o sistema.
    
# Decisões de implementação
    
