from tokens.tokens_sintatico import TokenSintatico, TokenClassSintatico
import re


def analisar(codigo):
    padroes = '|'.join(f'(?P<{t}> {p})' for t, p in TokenClassSintatico.__members__.items())
    regex = re.compile(padroes)
    tokens = [TokenSintatico(TokenClassSintatico[t.lastgroup], t.group(t.lastgroup)) for t in regex.finditer(codigo)]
    return tokens

def analisar_sintaxe(codigo):
    global indice_token, tokens
    indice_token = 0
    tokens = analisar(codigo)

    def analisar_parte_constantes():
        check(TokenClassSintatico.PALAVRA_RESERVADA, "CONST", "analisar_parte_constantes")
        while verificar(TokenClassSintatico.IDENT):
            identificador = proximo_token()
            check(TokenClassSintatico.OPERADOR, "=")
            valor = proximo_token()
            check(TokenClassSintatico.DELIMITADOR, ";")
            print(f"Constante: {identificador.valor} = {valor.valor}")

    def analisar_parte_variaveis():
        check(TokenClassSintatico.PALAVRA_RESERVADA, "VAR", "analisar_parte_variaveis")
        while verificar(TokenClassSintatico.IDENT):
            identificadores = [proximo_token()]
            while verificar(TokenClassSintatico.DELIMITADOR, ","):
                check(TokenClassSintatico.DELIMITADOR, ",")
                identificadores.append(proximo_token())
            check(TokenClassSintatico.DELIMITADOR, ";")
            for identificador in identificadores:
                print(f"Variável: {identificador.valor}")

    def analisar_parte_procedimentos():
        check(TokenClassSintatico.PALAVRA_RESERVADA, "PROCEDURE", "analisar_parte_procedimentos")
        while verificar(TokenClassSintatico.IDENT):
            identificador = proximo_token()
            check(TokenClassSintatico.DELIMITADOR, ";")
            print(f"Procedimento: {identificador.valor}")

    def analisar_parte_instrucao():
        check(TokenClassSintatico.PALAVRA_RESERVADA, "BEGIN", "analisar_parte_instrucao")
        while not verificar(TokenClassSintatico.PALAVRA_RESERVADA, "END") and not fim_de_arquivo():
            # Implemente aqui a lógica para analisar as instruções dentro do bloco BEGIN...END
            proximo_token()
        check(TokenClassSintatico.PALAVRA_RESERVADA, "END")
        print("Análise da parte de instrução concluída.")

    def analisar_programa():
        check(TokenClassSintatico.PALAVRA_RESERVADA, "CONST", "analisar_programa")
        analisar_parte_constantes()
        check(TokenClassSintatico.PALAVRA_RESERVADA, "VAR", "analisar_programa")
        analisar_parte_variaveis()
        check(TokenClassSintatico.PALAVRA_RESERVADA, "PROCEDURE", "analisar_programa")
        analisar_parte_procedimentos()
        check(TokenClassSintatico.PALAVRA_RESERVADA, "BEGIN", "analisar_programa")
        analisar_parte_instrucao()
        check(TokenClassSintatico.PALAVRA_RESERVADA, "END")
        check(TokenClassSintatico.DELIMITADOR, ".")

    analisar_programa()

# FUNÇÕES AUXILIARES 

def erro(mensagem, token=None):
    if token is None:
        raise SyntaxError(f"Erro Sintático: {mensagem}")
    else:
        raise SyntaxError(f"Erro Sintático: {mensagem}\nToken: {token}")

def fim_de_arquivo():
    global tokens, indice_token
    return indice_token >= len(tokens)

def verificar(classe_esperada, valor_esperado=None):
    global tokens, indice_token
    if not fim_de_arquivo():
        token = tokens[indice_token]
        if token.classe == classe_esperada and (valor_esperado is None or token.valor == valor_esperado):
            return True
    return False

def check(classe_token_esperada, valor_token_esperado=None, nome_funcao=None):
    global token_anterior
    if not verificar(classe_token_esperada, valor_token_esperado):
        token = None if fim_de_arquivo() else tokens[indice_token]
        if token is not None:
            valor_esperado_str = valor_token_esperado if valor_token_esperado is not None else "None"
            classe_encontrada_str = token.classe.name if token is not None else "None"
            lexema_encontrado_str = token.valor if token is not None else "None"
            nome_funcao_str = f" na função {nome_funcao}" if nome_funcao is not None else ""
            mensagem_erro = f"Esperado {classe_token_esperada.name} {valor_esperado_str}, encontrado {classe_encontrada_str} {lexema_encontrado_str}{nome_funcao_str}"
            erro(mensagem_erro, token)
    else:
        token_anterior = tokens[indice_token]
        proximo_token()


def proximo_token():
    global indice_token, tokens
    if not fim_de_arquivo():
        token = tokens[indice_token]
        print(f"Token atual: {token}")
        indice_token += 1
        return token
    else:
        return None

def token_anterior():
    global indice_token, token_anterior
    if indice_token > 0:
        indice_token -= 1
        token_anterior = tokens[indice_token]
        return tokens[indice_token]

