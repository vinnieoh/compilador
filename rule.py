import re
from tokens import tokenClass, Token


class RulesInterface:
    def regex_rules(self) -> list[str]:
        pass
    
    def extract_token(self, match: str) -> Token:
        pass
    
    def check_match(self, content: str) -> re.Match:
        for rule in self.regex_rules():
            match = re.match('^' + rule, content)
            if match:
                return match
            
        return None
    
    

class PalavrasReservadasRule(RulesInterface):
    def regex_rules(self) -> list[str]:
        return tokenClass.PALAVRA_RESERVADA
    
    def extract_token(self, match: str) -> Token:
        return (tokenClass.PALAVRA_RESERVADA, match)


class OperadorRule(RulesInterface):
    def regex_rules(self) -> list[str]:
        return tokenClass.OPERADOR
    
    def extract_token(self, match: str) -> Token:
        return (tokenClass.OPERADOR, match)


class DelimitadorRole(RulesInterface):
    def regex_rules(self) -> list[str]:
        return tokenClass.DELIMITADOR
    
    def extract_token(self, match: str) -> Token:
        return (tokenClass.DELIMITADOR, match)
    

class ConstateTextoRule(RulesInterface):
    def regex_rules(self) -> list[str]:
        return tokenClass.CONSTANTE_TEXTO
    
    def extract_token(self, match: str) -> Token:
        return (tokenClass.CONSTANTE_INTEIRA, match)


class PontoFlutuanteRule(RulesInterface):
    def regex_rules(self) -> list[str]:
        return tokenClass.PONTO_FLUTUANTE
    
    def extract_token(self, match: str) -> Token:
        return (tokenClass.PONTO_FLUTUANTE, float(match))
    

class ConstanteInteiraRule(RulesInterface):
    def regex_rules(self) -> list[str]:
        return tokenClass.CONSTANTE_INTEIRA
    
    def extract_token(self, match: str) -> Token:
        return (tokenClass.CONSTANTE_INTEIRA, int(match))


class IdentificadorRule(RulesInterface):
    def regex_rules(self) -> list[str]:
        return tokenClass.IDENTIFICADOR
    
    def extract_token(self, match: str) -> Token:
        return (tokenClass.IDENTIFICADOR, match)

