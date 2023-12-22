from analisado_lexico import analisado_lexico
from meu_token import TokenClass
from funcoes_auxiliares import erro, verificar, check, proximo_token, fim_de_arquivo
from contexto_analisador import tokens, indice_token

# Funções de análise sintática e tradução
def analisar_programa(tokens, indice_token):
    indice_token, block_code = analisar_block(tokens, indice_token)
    indice_token = check(tokens, indice_token, TokenClass.DELIMITADOR, ".")
    return indice_token, block_code

def analisar_block(tokens, indice_token):
    block_code = ""
    if verificar(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "CONST"):
        indice_token, constants_code = analisar_constants(tokens, indice_token)
        block_code += constants_code
    if verificar(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "VAR"):
        indice_token, vars_code = analisar_variables(tokens, indice_token)
        block_code += vars_code
    while verificar(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "PROCEDURE"):
        indice_token, procedures_code = analisar_procedures(tokens, indice_token)
        block_code += procedures_code
    indice_token, statement_code = analisar_statement(tokens, indice_token)
    block_code += statement_code
    return indice_token, block_code

def analisar_constants(tokens, indice_token):
    indice_token = check(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "CONST")
    constants_code = ""

    while True:
        indice_token, const_def_code = analisar_constdef(tokens, indice_token)
        constants_code += const_def_code + "\n"

        if verificar(tokens, indice_token, TokenClass.DELIMITADOR, ";"):
            indice_token = proximo_token(tokens, indice_token)
            break
        indice_token = check(tokens, indice_token, TokenClass.DELIMITADOR, ",")

    return indice_token, constants_code

def analisar_constdef(tokens, indice_token):
    indice_token = check(tokens, indice_token, TokenClass.IDENT)
    const_name = tokens[indice_token - 1].token_value
    indice_token = check(tokens, indice_token, TokenClass.OPERADOR, "=")
    indice_token = check(tokens, indice_token, TokenClass.NUMERO)
    const_value = tokens[indice_token - 1].token_value
    return indice_token, f"{const_name} = {const_value}"

def analisar_variables(tokens, indice_token):
    # Verifica se o próximo token é a palavra reservada "VAR"
    indice_token = check(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "VAR")
    vars_code = ""

    while True:
        # O nome da variável é o valor do token atual
        var_name = tokens[indice_token].token_value

        # Avança para o próximo token após o identificador
        indice_token = check(tokens, indice_token, TokenClass.IDENT)
        vars_code += f"{var_name} = None\n"

        # Verifica se o próximo token é um ponto e vírgula ou uma vírgula
        if verificar(tokens, indice_token, TokenClass.DELIMITADOR, ";"):
            indice_token = proximo_token(tokens, indice_token)
            break
        indice_token = check(tokens, indice_token, TokenClass.DELIMITADOR, ",")

    return indice_token, vars_code

def analisar_procedures(tokens, indice_token):
    procedures_code = ""
    while verificar(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "PROCEDURE"):
        indice_token = check(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "PROCEDURE")
        indice_token = check(tokens, indice_token, TokenClass.IDENT)
        proc_name = tokens[indice_token - 1].token_value
        indice_token = check(tokens, indice_token, TokenClass.DELIMITADOR, ";")
        
        indice_token, proc_body = analisar_block(tokens, indice_token)
        
        indice_token = check(tokens, indice_token, TokenClass.DELIMITADOR, ";")
        
        proc_body_indented = '\n'.join(['    ' + line for line in proc_body.split('\n')])
        procedures_code += f"def {proc_name}():\n{proc_body_indented}\n\n"
    
    return indice_token, procedures_code


def analisar_statement(tokens, indice_token):
    statement_code = ""
    if verificar(tokens, indice_token, TokenClass.IDENT):
        indice_token, assignment_code = analisar_assignment(tokens, indice_token)
        statement_code += assignment_code
    elif verificar(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "CALL"):
        indice_token, call_code = analisar_call(tokens, indice_token)
        statement_code += call_code
    elif verificar(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "BEGIN"):
        indice_token, begin_end_code = analisar_begin_end(tokens, indice_token)
        statement_code += begin_end_code
    elif verificar(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "IF"):
        indice_token, if_code = analisar_if(tokens, indice_token)
        statement_code += if_code
    elif verificar(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "WHILE"):
        indice_token, while_code = analisar_while(tokens, indice_token)
        statement_code += while_code
    elif verificar(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "PRINT"):
        indice_token, print_code = analisar_print(tokens, indice_token)
        statement_code += print_code
    
    return indice_token, statement_code


# Continuação das funções de análise sintática
def analisar_assignment(tokens, indice_token):
    indice_token = check(tokens, indice_token, TokenClass.IDENT)
    var_name = tokens[indice_token - 1].token_value
    indice_token = check(tokens, indice_token, TokenClass.OPERADOR, "<-")
    indice_token, expr_code = analisar_expression(tokens, indice_token)
    return indice_token, f"{var_name} = {expr_code}\n"

def analisar_call(tokens, indice_token):
    indice_token = check(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "CALL")
    indice_token = check(tokens, indice_token, TokenClass.IDENT)
    proc_name = tokens[indice_token - 1].token_value
    return indice_token, f"{proc_name}()\n"

def analisar_begin_end(tokens, indice_token):
    indice_token = check(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "BEGIN")
    compound_statements = []
    while not verificar(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "END"):
        indice_token, statement_code = analisar_statement(tokens, indice_token)
        compound_statements.append(statement_code)
        if verificar(tokens, indice_token, TokenClass.DELIMITADOR, ";"):
            indice_token = proximo_token(tokens, indice_token)
    indice_token = check(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "END")
    return indice_token, "\n".join(compound_statements) + "\n"

def analisar_if(tokens, indice_token):
    indice_token = check(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "IF")
    indice_token, condition_code = analisar_condition(tokens, indice_token)
    indice_token = check(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "THEN")
    indice_token, statement_code = analisar_statement(tokens, indice_token)
    return indice_token, f"if {condition_code}:\n    {statement_code}"

def analisar_while(tokens, indice_token):
    indice_token = check(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "WHILE")
    indice_token, condition_code = analisar_condition(tokens, indice_token)
    indice_token = check(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "DO")
    indice_token, statement_code = analisar_statement(tokens, indice_token)
    return indice_token, f"while {condition_code}:\n    {statement_code}"

def analisar_print(tokens, indice_token):
    indice_token = check(tokens, indice_token, TokenClass.PALAVRA_RESERVADA, "PRINT")
    indice_token, expr_code = analisar_expression(tokens, indice_token)
    return indice_token, f"print({expr_code})\n"

def analisar_expression(tokens, indice_token):
    expression_code = ""
    if verificar(tokens, indice_token, TokenClass.OPERADOR, "+") or verificar(tokens, indice_token, TokenClass.OPERADOR, "-"):
        expression_code += tokens[indice_token].token_value
        indice_token = proximo_token(tokens, indice_token)
    indice_token, term_code = analisar_term(tokens, indice_token)
    expression_code += term_code
    while verificar(tokens, indice_token, TokenClass.OPERADOR, "+") or verificar(tokens, indice_token, TokenClass.OPERADOR, "-"):
        expression_code += f" {tokens[indice_token].token_value} "
        indice_token = proximo_token(tokens, indice_token)
        indice_token, additional_term_code = analisar_term(tokens, indice_token)
        expression_code += additional_term_code
    return indice_token, expression_code

def analisar_term(tokens, indice_token):
    indice_token, factor_code = analisar_factor(tokens, indice_token)
    term_code = factor_code
    while verificar(tokens, indice_token, TokenClass.OPERADOR, "*") or verificar(tokens, indice_token, TokenClass.OPERADOR, "/"):
        operador = tokens[indice_token].token_value
        indice_token = proximo_token(tokens, indice_token)
        indice_token, additional_factor_code = analisar_factor(tokens, indice_token)
        term_code += f" {operador} {additional_factor_code}"
    return indice_token, term_code

def analisar_factor(tokens, indice_token):
    if verificar(tokens, indice_token, TokenClass.IDENT):
        # Trata IDENT
        factor_code = tokens[indice_token].token_value
        indice_token = proximo_token(tokens, indice_token)
    elif verificar(tokens, indice_token, TokenClass.NUMERO):
        # Trata NUMERO
        factor_code = tokens[indice_token].token_value
        indice_token = proximo_token(tokens, indice_token)
    elif verificar(tokens, indice_token, TokenClass.DELIMITADOR, "("):
        # Trata expressão entre parênteses
        indice_token = proximo_token(tokens, indice_token)
        indice_token, expr_code = analisar_expression(tokens, indice_token)
        factor_code = f"({expr_code})"
        indice_token = check(tokens, indice_token, TokenClass.DELIMITADOR, ")")
    else:
        # Erro: token inesperado
        token_atual = tokens[indice_token]
        erro(f"Esperado IDENT, NUMERO ou (, encontrado: {token_atual}", token_atual)
        return indice_token, ""

    return indice_token, factor_code


def analisar_condition(tokens, indice_token):
    operators_map = {"=": "==", "#": "!=", "/?": "%"}

    indice_token, left_expr = analisar_expression(tokens, indice_token)  # Analisa o lado esquerdo da condição

    if verificar(tokens, indice_token, TokenClass.OPERADOR):
        op = tokens[indice_token].token_value
        indice_token = proximo_token(tokens, indice_token)

        # Trata operadores especiais e compostos
        if op in operators_map:
            op = operators_map[op]
        elif op in ["<", ">"] and verificar(tokens, indice_token, TokenClass.OPERADOR, "="):
            op += "="
            indice_token = proximo_token(tokens, indice_token)
        elif op == "/" and verificar(tokens, indice_token, TokenClass.OPERADOR, "?"):
            op = "%"
            indice_token = proximo_token(tokens, indice_token)

        indice_token, right_expr = analisar_expression(tokens, indice_token)  # Analisa o lado direito da condição
        return indice_token, f"{left_expr} {op} {right_expr}"
    else:
        erro("Operador de relação esperado", tokens[indice_token])
        return indice_token, ""

def analisar_sintaxe(codigo_pl0):
    tokens = analisado_lexico(codigo_pl0)
    indice_token = 0
    
    indice_token, codigo_python = analisar_programa(tokens, indice_token)
    #print(codigo_python)
    if not fim_de_arquivo(tokens, indice_token):
        erro("Código após o final do programa", tokens[indice_token])
    return codigo_python

