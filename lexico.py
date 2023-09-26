from typing import List
from tokens import Token, TokenClass
import re

def tokenize_code(code: str) -> List[Token]:
    
    tokens = []

    for line_num, line in enumerate(code.split('\n'), start=1):
        line = re.sub(r'\s+', ' ', line.strip())

        while line:
            match = None
            for token_class in TokenClass:
                regex = token_class.value
                match = re.match(regex, line)
                if match:
                    break
            if match:
                lexema = match.group(0)
                token = Token(token_class, lexema)
                tokens.append(token)
                line = line[len(lexema):].lstrip()
            else:
                raise ValueError(f"Erro léxico na linha {line_num}: caractere inesperado: {line[0]!r}")
    return tokens