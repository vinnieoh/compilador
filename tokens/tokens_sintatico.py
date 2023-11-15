from enum import Enum

class TokenClassSintatico(Enum):
    PALAVRA_RESERVADA = "(CONST|VAR|PROCEDURE|BEGIN|END|CALL|IF|THEN|WHILE|DO|PRINT|ODD|EVEN)"
    OPERADOR = "(\+|-|\*|/|=|#|<|<=|>|>=|/\?)"
    DELIMITADOR = "(,|;|\(|\))"
    IDENT = "[a-zA-Z][a-zA-Z0-9]*"
    NUMERO = "\d+"
    ESPACO_EM_BRANCO = "\s+"

class TokenSintatico:
    def __init__(self, token_class: TokenClassSintatico, token_value) -> None:
        self.token_class = token_class
        self.token_value = token_value

    def __str__(self) -> str:
        return f'Classe do Token: {self.token_class.name}, Valor: {self.token_value}'