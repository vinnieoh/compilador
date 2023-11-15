import re

from analisado_sintatico import analisar_sintaxe
#from analisado_lexico import tokenize_code


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
            raise "Valor Nao Encontrado!"


    with open(caminho, 'r', encoding='utf-8') as f:
        code = f.read()
        
    #cleaned_code = re.sub(r'/\*[\s\S]*?\*/|//.*', '', code, flags=re.DOTALL)
    
    return code
   


def main():
    
    prints()
    num = int(input('Digite o numuro do arquivo: '))
    
    code = leitura_arquivos(num)
    

    analisar_sintaxe(code)
    
    
    

if __name__ == "__main__":
    main()