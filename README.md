# Simulador de Máquina de Turing

Este projeto é uma implementação de um **Simulador de Máquina de Turing** em Python, com uma interface gráfica (GUI) desenvolvida em **Tkinter**. O simulador permite visualizar a fita, o estado atual, as transições e o movimento do cabeçote passo a passo.

##  Funcionalidades

* **Interface Gráfica:** Visualização clara da fita e da posição do cabeçote.
* **Carregamento Dinâmico:** Leitura de definições da máquina (estados, transições, fita inicial) a partir de arquivos `.txt`.
* **Controles de Execução:**
    * ▶ **Próximo Passo:** Executa uma transição por vez.
    * ⏩ **Executar Tudo:** Executa automaticamente com controle de velocidade.
    * ⟲ **Reiniciar:** Restaura a máquina para o estado inicial.
* **Logs Detalhados:** Mostra o histórico de leituras, escritas e mudanças de estado.
* **Feedback Visual:** Indica claramente se a palavra foi **ACEITA** ou **REJEITADA** (ou se a máquina travou).

## Estrutura do Projeto

* `Interface.py`: Arquivo principal. Gerencia a GUI e o loop de eventos.
* `Machine.py`: O "motor" do simulador. Gerencia a fita, o cabeçote e a lógica de execução.
* `TuringLoader.py`: Responsável por ler o arquivo `.txt` (input) e construir os objetos da máquina.
* `State.py`: Representa um estado da máquina e armazena suas transições.
* `Transition.py` & `Edge.py`: Definem as regras de mudança (o que ler, o que escrever, para onde mover).

## Como Executar

### Pré-requisitos
* Python 3.x instalado.
* Biblioteca `tkinter` (geralmente já vem instalada com o Python).

### Passo a Passo
1. Clone este repositório ou baixe os arquivos.
2. Abra o terminal na pasta do projeto.
3. Execute o arquivo da interface:

```bash
python Interface.py
````

4.  Na janela que abrir, clique em **📂 Carregar input.txt** e selecione um arquivo de configuração válido.

## Formato do Arquivo de Entrada (.txt)

Para testar suas próprias Máquinas de Turing, crie um arquivo `.txt` seguindo a sintaxe abaixo. O `TuringLoader` interpreta linhas de comando e transições.

### Comandos Especiais

  * `init <nome_estado>`: Define o estado inicial.
  * `accept <estado1,estado2...>`: Define o(s) estado(s) de aceitação.
  * `fita <conteudo_inicial>`: Define a palavra de entrada na fita.

### Transições

O formato da transição é:
`origem, leu, destino, escreveu, direcao`

  * **origem:** Nome do estado atual.
  * **leu:** Caractere lido na fita (use `_` para representar o símbolo branco/vazio).
  * **destino:** Nome do próximo estado.
  * **escreveu:** Caractere a ser escrito na fita (use `_` para apagar/deixar vazio).
  * **direcao:** Para onde o cabeçote vai:
      * `<` : Esquerda
      * `>` : Direita

### Exemplo de Arquivo (`exemplo.txt`)

Abaixo, um exemplo de máquina que inverte bits (0 vira 1, 1 vira 0):

```text
# Definição da fita inicial
fita 10110

# Estado inicial
init q0

# Estados de aceitação
accept qfim

# Transições (origem, leu, destino, escreveu, direção)
q0, 0, q0, 1, >
q0, 1, q0, 0, >
q0, _, qfim, _, <
```

## Detalhes Técnicos

  * **Fita Infinita:** A fita é implementada como uma lista dinâmica que cresce conforme a necessidade (`_range` inicial de 50 células).
  * **Tratamento de Erros:** O simulador detecta loops infinitos simples (por estouro de memória/tempo) ou travamentos quando não há transição definida para o símbolo lido.

Desenvolvido para fins educacionais.



