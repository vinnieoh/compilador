from enum import Enum
import re

class TokenClass(Enum):
    PALAVRA_RESERVADA = r"\b(CONST|VAR|PROCEDURE|BEGIN|END|CALL|IF|THEN|WHILE|DO|PRINT|ODD|EVEN)\b"
    OPERADOR = r"(\+|-|\*|/|=|#|<|<=|>|>=|\?)"
    DELIMITADOR = r"(,|;|\(|\)|\.)"
    IDENT = r"\b[a-zA-Z][a-zA-Z0-9]*\b"
    NUMERO = r"\b\d+(\?\d*)?(\.\d+(\d*)?)?|#"
    ESPACO_EM_BRANCO = r"\s+"

class Token:
    def __init__(self, token_class, token_value, line, column) -> None:
        self.token_class = token_class
        self.token_value = token_value
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f'Classe do Token: {self.token_class}, Valor: {self.token_value}, Linha: {self.line}, Coluna: {self.column}'

def parse_code(code):
    global tokens
    lines = code.split('\n')
    tokens = []
    line_num = 1

    for line in lines:
        line = re.sub(r'\s+', ' ', line.strip())
        column = 1

        while line:
            match = None
            for token_class in TokenClass:
                regex = token_class.value
                match = re.match(regex, line)
                if match:
                    lexeme = match.group(0)
                    token = Token(token_class, lexeme, line_num, column)
                    tokens.append(token)
                    line = line[len(lexeme):].lstrip()
                    column += len(lexeme)
                    break

            if match is None:
                raise SyntaxError(
                    f"Erro léxico na linha {line_num}, coluna {column}: caractere inesperado: {line[0]!r}")

        line_num += 1
    return tokens

def analisar_sintaxe(codigo):
    indice_token = 0
    parse_code(codigo)
    print(tokens)

    def analisar_programa():
        analisar_block()
        check(TokenClass.DELIMITADOR, ".")

    def analisar_block():
        analisar_constants()
        analisar_variables()
        analisar_procedures()
        analisar_statement()

    def analisar_constants():
        if verificar(TokenClass.PALAVRA_RESERVADA, "CONST"):
            proximo_token()
            analisar_constdecl()
            check(TokenClass.DELIMITADOR, ";")

    def analisar_constdecl():
        analisar_constdef()
        while verificar(TokenClass.DELIMITADOR, ","):
            proximo_token()
            analisar_constdef()

    def analisar_constdef():
        check(TokenClass.IDENT)
        proximo_token()
        check(TokenClass.OPERADOR, "=")
        proximo_token()
        check(TokenClass.NUMERO)

    def analisar_variables():
        if verificar(TokenClass.PALAVRA_RESERVADA, "VAR"):
            proximo_token()
            analisar_vardecl()
            check(TokenClass.DELIMITADOR, ";")

    def analisar_vardecl():
        analisar_ident()
        while verificar(TokenClass.DELIMITADOR, ","):
            proximo_token()
            analisar_ident()

    def analisar_procedures():
        while verificar(TokenClass.PALAVRA_RESERVADA, "PROCEDURE"):
            proximo_token()
            check(TokenClass.IDENT)
            proximo_token()
            check(TokenClass.DELIMITADOR, ";")
            analisar_block()
            check(TokenClass.DELIMITADOR, ";")

    def analisar_statement():
        if verificar(TokenClass.IDENT):
            analisar_assignment()
        elif verificar(TokenClass.PALAVRA_RESERVADA, "CALL"):
            analisar_call()
        elif verificar(TokenClass.PALAVRA_RESERVADA, "BEGIN"):
            analisar_begin_end()
        elif verificar(TokenClass.PALAVRA_RESERVADA, "IF"):
            analisar_if()
        elif verificar(TokenClass.PALAVRA_RESERVADA, "WHILE"):
            analisar_while()
        elif verificar(TokenClass.PALAVRA_RESERVADA, "PRINT"):
            analisar_print()
        elif verificar(TokenClass.ESPACO_EM_BRANCO):  # Trata o final do arquivo
            return
        else:
            erro("Comando desconhecido")

    def analisar_assignment():
        analisar_ident()
        check(TokenClass.OPERADOR, "<-")
        analisar_expression()

    def analisar_call():
        check(TokenClass.PALAVRA_RESERVADA, "CALL")
        analisar_ident()

    def analisar_begin_end():
        check(TokenClass.PALAVRA_RESERVADA, "BEGIN")
        while not verificar(TokenClass.PALAVRA_RESERVADA, "END"):
            analisar_statement()
            check(TokenClass.DELIMITADOR, ";")
        check(TokenClass.PALAVRA_RESERVADA, "END")

    def analisar_if():
        check(TokenClass.PALAVRA_RESERVADA, "IF")
        analisar_condition()
        check(TokenClass.PALAVRA_RESERVADA, "THEN")
        analisar_statement()

    def analisar_while():
        check(TokenClass.PALAVRA_RESERVADA, "WHILE")
        analisar_condition()
        check(TokenClass.PALAVRA_RESERVADA, "DO")
        analisar_statement()

    def analisar_print():
        check(TokenClass.PALAVRA_RESERVADA, "PRINT")
        analisar_expression()

    def analisar_condition():
        if verificar(TokenClass.PALAVRA_RESERVADA, "ODD") or verificar(TokenClass.PALAVRA_RESERVADA, "EVEN"):
            proximo_token()
            analisar_expression()
        else:
            analisar_expression()
            analisar_relation()
            analisar_expression()

    def analisar_relation():
        check(TokenClass.OPERADOR, "=")
        proximo_token()

    def analisar_expression():
        if verificar(TokenClass.OPERADOR, "+") or verificar(TokenClass.OPERADOR, "-"):
            proximo_token()
        analisar_term()
        while verificar(TokenClass.OPERADOR, "+") or verificar(TokenClass.OPERADOR, "-"):
            proximo_token()
            analisar_term()

    def analisar_term():
        analisar_factor()
        while verificar(TokenClass.OPERADOR, "*") or verificar(TokenClass.OPERADOR, "/"):
            proximo_token()
            analisar_factor()

    def analisar_factor():
        if verificar(TokenClass.IDENT):
            analisar_ident()
        elif verificar(TokenClass.NUMERO):
            proximo_token()
        elif verificar(TokenClass.DELIMITADOR, "("):
            proximo_token()
            analisar_expression()
            check(TokenClass.DELIMITADOR, ")")
            proximo_token()
        else:
            erro("Esperado IDENT, NUMERO ou (")

    def analisar_ident():
        check(TokenClass.IDENT)
        proximo_token()

    def erro(mensagem, token=None):
        if token is None:
            raise SyntaxError(f"Erro Sintático: {mensagem}")
        else:
            raise SyntaxError(f"Erro Sintático: {mensagem}\nToken: {token}")

    def fim_de_arquivo():
        return indice_token >= len(tokens)

    def verificar(classe_esperada, valor_esperado=None):
        if not fim_de_arquivo():
            token = tokens[indice_token]
            if token.token_class == classe_esperada and (valor_esperado is None or token.token_value == valor_esperado):
                return True
        return False

    def check(classe_token_esperada, valor_token_esperado=None):
        if not verificar(classe_token_esperada, valor_token_esperado):
            token = None if fim_de_arquivo() else tokens[indice_token]
            if token is not None:
                valor_esperado_str = valor_token_esperado if valor_token_esperado is not None else "None"
                classe_encontrada_str = token.token_class.name if token is not None else "None"
                lexema_encontrado_str = token.token_value if token is not None else "None"
                mensagem_erro = f"Esperado {classe_token_esperada.name} {valor_esperado_str}, encontrado {classe_encontrada_str} {lexema_encontrado_str}"
                erro(mensagem_erro, token)
        else:
            proximo_token()

    def proximo_token():
        nonlocal indice_token
        if not fim_de_arquivo():
            token = tokens[indice_token]
            print(f"Token atual: {token}")
            indice_token += 1
            return token
        else:
            # Retorna um token especial para indicar o final do arquivo
            return Token(TokenClass.ESPACO_EM_BRANCO, "", -1, -1)

    analisar_programa()

# Teste do código
codigo_teste_1 = """
VAR n, f;
BEGIN
  n <- 0;
  f <- 1;
  WHILE n # 16 DO
  BEGIN
    n <- n + 1;
    f <- f * n;
  END;
END.
"""

codigo_teste_2 = """
VAR x, squ;

PROCEDURE square;
BEGIN
  squ <- x * x;
END;

BEGIN
  x <- 1;
  WHILE x <= 10 DO
  BEGIN
    CALL square;
    PRINT squ;
    x <- x + 1;
  END;
END.
"""

codigo_teste_3 = """
CONST max = 100;
VAR arg, ret;

PROCEDURE checkprime;
VAR i;
BEGIN
  ret <- 1;
  i <- 2;
  WHILE i < arg DO
  BEGIN
    IF arg /? i THEN
    BEGIN
      ret <- 0;
      i <- arg;
    END;
    i <- i + 1;
  END;
END;

PROCEDURE primes;
BEGIN
  arg <- 2;
  WHILE arg < max DO
  BEGIN
    CALL checkprime;
    IF ret = 1 THEN PRINT arg;
    arg <- arg + 1;
  END;
END;

CALL primes.
"""

analisar_sintaxe(codigo_teste_2)
