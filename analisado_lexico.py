import re
from meu_token import TokenClass, Token

def analisado_lexico(code):
    tokens = []
    lines = code.split('\n')
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
