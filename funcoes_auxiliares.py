def erro(mensagem, token_atual):
    raise SyntaxError(f"Erro Sintático: {mensagem} | Token Atual: {token_atual}")

def fim_de_arquivo(tokens, indice_token):
    return indice_token >= len(tokens)

def verificar(tokens, indice_token, classe_esperada, valor_esperado=None):
    if not fim_de_arquivo(tokens, indice_token):
        token = tokens[indice_token]
        if token.token_class == classe_esperada and (valor_esperado is None or token.token_value == valor_esperado):
            return True
    return False

def check(tokens, indice_token, classe_token_esperada, valor_token_esperado=None):
    if not verificar(tokens, indice_token, classe_token_esperada, valor_token_esperado):
        token_atual = tokens[indice_token] if indice_token < len(tokens) else None
        erro(f"Esperado {classe_token_esperada.name}, encontrado {token_atual.token_class.name if token_atual else 'None'}", token_atual)
    else:
        indice_token += 1
    return indice_token

def proximo_token(tokens, indice_token):
    # Incrementa o indice_token para avançar para o próximo token
    return indice_token + 1