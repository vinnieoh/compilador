# compilador:  Trabalho desenvolvido na matéria de compiladores na Universidade Federal do Tocantins, curso ciências da computação 

## Descrição

O compilador foi desenvolvido como parte de um projeto educativo para entender os princípios da compilação de linguagens de programação. Ele analisa código PL/0, realiza a análise léxica e sintática, e gera um código equivalente em Python.

## Estrutura do Projeto

Este projeto é organizado da seguinte maneira:

- `main.py`: Ponto de entrada do compilador. Este script executa o processo de compilação.
- `analisador_lexico.py`: Módulo responsável pela análise léxica, onde o código PL/0 é quebrado em tokens.
- `analisador_sintatico.py`: Módulo que realiza a análise sintática e a tradução do código PL/0 para Python.
- `funcoes_auxiliares.py`: Conjunto de funções auxiliares usadas nos processos de análise léxica e sintática.
- `gramatica/`: Diretório contendo exemplos de códigos PL/0 para teste e a gramatica da linguagem.
- `codigo_traduzido/`: Diretório onde os códigos traduzidos para Python são salvos automaticamente.
- `Dockerfile`: Arquivo para criação de um container Docker, garantindo um ambiente consistente para a execução do compilador.
- `README.md`: Documentação do projeto.

## Pré-requisitos

- Python 3.11+
- Docker (opcional para execução via container)

## Instalação e Execução

1. **Clone o Repositório**: [git clone](https://github.com/vinnieoh/compilador.git)


2. **Navegue até a pasta do projeto**: cd ./compilador/


3. **Execução do Compilador**: python main.py


4. **Uso com Docker** (opcional):
docker build -t nome-do-compilador,
docker run nome-do-compilador


Após executar `main.py`, o programa solicitará que você escolha um arquivo PL/0 para compilar. O código Python resultante será automaticamente salvo no diretório `codigo_traduzido/`.

## Agradecimentos

- Agradecimentos a colaboradores, professores, etc.

---

Desenvolvido com 💻 e ☕ por [Vinicius de Oliveira](https://github.com/vinnieoh)
