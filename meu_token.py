from enum import Enum

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

