#from nao_refatorado import analisar_sintaxe
from analisado_sintatico import analisar_sintaxe
import datetime

def prints():
    print("Test: 1")
    print("Test: 2")
    print("Test: 3")

def leitura_arquivos(code_test):
    match code_test:
        case 1:
            caminho = './gramatica/ex1.pl0mod.txt'
        case 2: 
           caminho = './gramatica/ex2.pl0mod.txt'
        case 3: 
            caminho = './gramatica/ex3.pl0mod.txt'
        case _:
            raise Exception("Valor Nao Encontrado!")

    with open(caminho, 'r', encoding='utf-8') as f:
        code = f.read()
    
    return code

def salvar_codigo(codigo_py):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"./codigo_tradutor/codigo_{timestamp}.py"
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(codigo_py)
    print(f"Código salvo em: {nome_arquivo}")

def main():
    prints()
    num = int(input('Digite o número do arquivo: '))
    
    code = leitura_arquivos(num)

    codigo_py = analisar_sintaxe(code)
    
    print(codigo_py)

    salvar_codigo(codigo_py)

if __name__ == "__main__":
    main()
