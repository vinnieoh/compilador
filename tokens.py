
class TokenClass:
    PALAVRA_RESERVADA = 0
    OPERADOR = 0
    DELIMITADOR = 0
    CONSTANTE_TEXTO = 0
    PONTO_FLUTUANTE = 0
    CONSTANTE_INTEIRA = 0
    IDENTIFICADOR = 0
    

tokenClass: TokenClass = TokenClass()
    
    
class Token:
    def __init__(self, token_class: TokenClass, token_value) -> None:
        self.token_class = token_class
        self.token_value = token_value
        
    def __str__(self) -> str:
        return f'<Token class: {self.token_class}, value: {self.token_value}>'
    