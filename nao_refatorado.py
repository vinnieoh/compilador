from enum import Enum
import re

class TokenClass(Enum):
    PALAVRA_RESERVADA = r"\b(CONST|VAR|PROCEDURE|BEGIN|END|CALL|IF|THEN|WHILE|DO|PRINT|ODD|EVEN|NOT)\b"
    OPERADOR = r"(<-|\+|\-|\*|\/|=|#|<|<=|>|>=|/\?|\?)"
    DELIMITADOR = r"(,|;|\(|\)|\.)"
    IDENT = r"\b[a-zA-Z][a-zA-Z0-9]*\b"
    NUMERO = r"\b\d+(\.\d+)?\b"
    COMENTARIO = r"\{[^}]*\}"
    ESPACO_EM_BRANCO = r"\s+"

class Token:
    def __init__(self, token_class, token_value, line, column):
        self.token_class = token_class
        self.token_value = token_value
        self.line = line
        self.column = column

    def __str__(self):
        return f'Classe do Token: {self.token_class}, Valor: {self.token_value}, Linha: {self.line}, Coluna: {self.column}'

def analisado_lexico(code):
    global tokens
    code = re.sub(TokenClass.COMENTARIO.value, "", code)
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
                raise SyntaxError(f"Erro léxico na linha {line_num}, coluna {column}: caractere inesperado: {line[0]!r}")

        line_num += 1
    return tokens

# Funções auxiliares
def erro(mensagem, token=None):
    if token is None:
        token_atual = tokens[indice_token] if indice_token < len(tokens) else "Fim de arquivo"
        raise SyntaxError(f"Erro Sintático: {mensagem} | Token Atual: {token_atual}")
    else:
        raise SyntaxError(f"Erro Sintático: {mensagem} | Token: {token}")


def fim_de_arquivo():
    return indice_token >= len(tokens)

def verificar(classe_esperada, valor_esperado=None):
    if not fim_de_arquivo():
        token = tokens[indice_token]
        if token.token_class == classe_esperada and (valor_esperado is None or token.token_value == valor_esperado):
            return True
    return False

def check(classe_token_esperada, valor_token_esperado=None):
    global indice_token
    if not verificar(classe_token_esperada, valor_token_esperado):
        token_atual = tokens[indice_token] if indice_token < len(tokens) else None
        erro(f"Esperado {classe_token_esperada.name}, encontrado {token_atual.token_class.name if token_atual else 'None'}")
    else:
        indice_token += 1

def proximo_token():
    global indice_token
    indice_token += 1
    if indice_token < len(tokens):
        return tokens[indice_token]
    else:
        return Token(TokenClass.ESPACO_EM_BRANCO, "", -1, -1)

# Funções de análise sintática com tradução para Python
def analisar_programa():
    block_code = analisar_block()
    check(TokenClass.DELIMITADOR, ".")  # Verifica se o próximo token é o ponto final
    return block_code


def analisar_block():
    block_code = ""
    if verificar(TokenClass.PALAVRA_RESERVADA, "CONST"):
        block_code += analisar_constants()
    if verificar(TokenClass.PALAVRA_RESERVADA, "VAR"):
        block_code += analisar_variables()
    while verificar(TokenClass.PALAVRA_RESERVADA, "PROCEDURE"):
        block_code += analisar_procedures()
    block_code += analisar_statement()
    return block_code

def analisar_constants():
    check(TokenClass.PALAVRA_RESERVADA, "CONST")
    constants_code = ""
    while True:
        constants_code += analisar_constdef() + "\n"
        if verificar(TokenClass.DELIMITADOR, ";"):
            proximo_token()
            break
        check(TokenClass.DELIMITADOR, ",")
    return constants_code

def analisar_constdef():
    check(TokenClass.IDENT)
    const_name = tokens[indice_token - 1].token_value
    check(TokenClass.OPERADOR, "=")
    check(TokenClass.NUMERO)
    const_value = tokens[indice_token - 1].token_value
    return f"{const_name} = {const_value}"

def analisar_variables():
    check(TokenClass.PALAVRA_RESERVADA, "VAR")
    vars_code = ""
    while True:
        check(TokenClass.IDENT)
        var_name = tokens[indice_token - 1].token_value
        vars_code += f"{var_name} = None\n"
        if verificar(TokenClass.DELIMITADOR, ";"):
            proximo_token()
            break
        check(TokenClass.DELIMITADOR, ",")
    return vars_code

def analisar_procedures():
    procedures_code = ""
    while verificar(TokenClass.PALAVRA_RESERVADA, "PROCEDURE"):
        check(TokenClass.PALAVRA_RESERVADA, "PROCEDURE")
        check(TokenClass.IDENT)
        proc_name = tokens[indice_token - 1].token_value
        check(TokenClass.DELIMITADOR, ";")
        proc_body = analisar_block()
        check(TokenClass.DELIMITADOR, ";")
        # Corrigir a indentação do código do procedimento
        proc_body_indented = '\n'.join(['    ' + line for line in proc_body.split('\n')])
        procedures_code += f"def {proc_name}():\n{proc_body_indented}\n\n"
    return procedures_code


def analisar_statement():
    statement_code = ""
    if verificar(TokenClass.IDENT):
        statement_code = analisar_assignment()
    elif verificar(TokenClass.PALAVRA_RESERVADA, "CALL"):
        statement_code = analisar_call()
    elif verificar(TokenClass.PALAVRA_RESERVADA, "BEGIN"):
        statement_code = analisar_begin_end()
    elif verificar(TokenClass.PALAVRA_RESERVADA, "IF"):
        statement_code = analisar_if()
    elif verificar(TokenClass.PALAVRA_RESERVADA, "WHILE"):
        statement_code = analisar_while()
    elif verificar(TokenClass.PALAVRA_RESERVADA, "PRINT"):
        statement_code = analisar_print()
    return statement_code

def analisar_assignment():
    check(TokenClass.IDENT)
    var_name = tokens[indice_token - 1].token_value
    check(TokenClass.OPERADOR, "<-")
    return f"{var_name} = {analisar_expression()}\n"

def analisar_call():
    check(TokenClass.PALAVRA_RESERVADA, "CALL")
    check(TokenClass.IDENT)
    return f"{tokens[indice_token - 1].token_value}()\n"

def analisar_begin_end():
    check(TokenClass.PALAVRA_RESERVADA, "BEGIN")
    compound_statements = []
    while not verificar(TokenClass.PALAVRA_RESERVADA, "END"):
        compound_statements.append(analisar_statement())
        if verificar(TokenClass.DELIMITADOR, ";"):
            proximo_token()
    check(TokenClass.PALAVRA_RESERVADA, "END")
    return "\n".join(compound_statements) + "\n"

def analisar_if():
    check(TokenClass.PALAVRA_RESERVADA, "IF")
    condition_code = analisar_condition()
    check(TokenClass.PALAVRA_RESERVADA, "THEN")
    return f"if {condition_code}:\n    {analisar_statement()}"

def analisar_while():
    check(TokenClass.PALAVRA_RESERVADA, "WHILE")
    condition_code = analisar_condition()
    check(TokenClass.PALAVRA_RESERVADA, "DO")
    return f"while {condition_code}:\n    {analisar_statement()}"

def analisar_print():
    check(TokenClass.PALAVRA_RESERVADA, "PRINT")
    return f"print({analisar_expression()})\n"

def analisar_expression():
    expression_code = ""
    if verificar(TokenClass.OPERADOR, "+") or verificar(TokenClass.OPERADOR, "-"):
        expression_code += tokens[indice_token].token_value
        proximo_token()
    expression_code += analisar_term()
    while verificar(TokenClass.OPERADOR, "+") or verificar(TokenClass.OPERADOR, "-"):
        expression_code += f" {tokens[indice_token].token_value} "
        proximo_token()
        expression_code += analisar_term()
    return expression_code

# Continuação das funções de análise sintática

def analisar_term():
    term_code = analisar_factor()
    while verificar(TokenClass.OPERADOR, "*") or verificar(TokenClass.OPERADOR, "/"):
        operador = tokens[indice_token].token_value
        proximo_token()
        term_code += f" {operador} {analisar_factor()}"
    return term_code

def analisar_expression():
    expr_code = analisar_term()
    while verificar(TokenClass.OPERADOR, "+") or verificar(TokenClass.OPERADOR, "-"):
        operador = tokens[indice_token].token_value
        proximo_token()
        expr_code += f" {operador} {analisar_term()}"
    return expr_code

def analisar_factor():
    if verificar(TokenClass.IDENT) or verificar(TokenClass.NUMERO):
        factor_code = tokens[indice_token].token_value
        proximo_token()
        return factor_code
    elif verificar(TokenClass.DELIMITADOR, "("):
        proximo_token()
        factor_code = f"({analisar_expression()})"
        check(TokenClass.DELIMITADOR, ")")
        return factor_code
    else:
        token_atual = tokens[indice_token] if indice_token < len(tokens) else "Fim de arquivo"
        erro(f"Esperado IDENT, NUMERO ou (, encontrado: {token_atual}")
        return ""  # Retorna string vazia em caso de erro

def analisar_condition():
    left_expr = analisar_expression()  # Analisa o lado esquerdo da condição

    # Mapeia operadores PL/0 para operadores Python, se necessário
    operators_map = {"=": "==", "#": "!=", "/?": "%"}

    if verificar(TokenClass.OPERADOR):
        op = tokens[indice_token].token_value
        proximo_token()

        # Trata operadores especiais como "/?"
        if op in operators_map:
            op = operators_map[op]

        # Trata operadores compostos como "<="
        if (op in ["<", ">"] and verificar(TokenClass.OPERADOR, "=")) or (op == "/" and verificar(TokenClass.OPERADOR, "?")):
            op += tokens[indice_token].token_value
            proximo_token()

        right_expr = analisar_expression()  # Analisa o lado direito da condição
        return f"{left_expr} {op} {right_expr}"
    else:
        erro("Operador de relação esperado")
        return ""

# Tradução do código da linguagem PL/0 para Python
def analisar_sintaxe(codigo_pl0):
    global tokens, indice_token
    indice_token = 0
    tokens = analisado_lexico(codigo_pl0)
    codigo_python = analisar_programa()
    print(codigo_python)
    if not fim_de_arquivo():
        erro("Código após o final do programa")

