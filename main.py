import re
from analisado_lexico import tokenize_code


def prints():
    print("Test: 1")
    print("Test: 2")
    print("Test: 3")
    print("Test: 4")
    print("Test: 5")
    print("Test: 6")
    print("Test: 7")
    print("Test: 8")
    print("Test-Erro 1: 9")
    print("Test-Erro 2: 10")
    

def leitura_arquivos(code_test):
    
    match code_test:
        case 1:
            caminho = './test_code/teste1.c'
        case 2: 
           caminho = './test_code/teste2.c'
        case 3: 
            caminho = './test_code/teste3.c'
        case 4:
            caminho = './test_code/teste4.c'
        case 5:
            caminho = './test_code/teste5.c'
        case 6:
            caminho = './test_code/teste6.c'
        case 7:
            caminho = './test_code/teste7.c'
        case 8:
            caminho = './test_code/teste8.c'
        case 9:
            caminho = './test_code/teste-erro1.c'
        case 10:
            caminho = './test_code/teste-erro2.c'
        case _:
            raise "Valor Nao Encontrado!"


    with open(caminho, 'r', encoding='utf-8') as f:
        code = f.read()
        
    cleaned_code = re.sub(r'/\*[\s\S]*?\*/|//.*', '', code, flags=re.DOTALL)
    
    return cleaned_code
   


def main():
    
    prints()
    num = int(input('Digite o numuro do arquivo: '))
    
    content = leitura_arquivos(num)
    
    values = tokenize_code(content)

    for token in values:
        print(token)
    

if __name__ == "__main__":
    main()