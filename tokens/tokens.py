from enum import Enum


class TokenClass(Enum):
    PALAVRA_RESERVADA = r"(struct\b|if\b|int\b|else\b|while\b|do\b|for\b|\bfloat\b|double\b|char\b|long\b|short\b|break\b|continue\b|case\b|switch\b|default\b|void\b|return)"
    OPERADOR = r"(==|!=|<=|>=|\|\||&&|\+=|-=|\*=|\=|--|\+\+|\+|\/|->|\*|\-|\||!|&|%|<|>)"
    DELIMITADOR = r"\[|\]|\(|\)|\{|\}|\;|\,|\:"
    CONSTANTE_TEXTO = r'\".*?\"'
    PONTO_FLUTUANTE = r'(\d+\.\d+)'
    CONSTANTE_INTEIRA = r"(\d+)(?![a-zA-Z])"
    IDENTIFICADOR = r"([a-zA-Z_][a-zA-Z0-9_]*|main|printf)"
    
    
class Token:
    def __init__(self, token_class: TokenClass, token_value) -> None:
        self.token_class = token_class
        self.token_value = token_value
        
    def __str__(self) -> str:
        return f'Token Class: {self.token_class.name}, Value: {self.token_value}'

#################################################################################################################################################################

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