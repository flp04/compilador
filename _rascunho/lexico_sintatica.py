import re

# Definição dos tipos de token
TIPOS_TOKEN = {
    'PALAVRA_CHAVE': 'PALAVRA_CHAVE',
    'ID': 'ID',
    'NUMERO': 'NUMERO',
    'OPERADOR': 'OPERADOR',
    'DELIMITADOR': 'DELIMITADOR',
    'TEXTO': 'TEXTO'
}

# Palavras-chave da linguagem
PALAVRAS_CHAVE = ['programa', 'fimprog', 'inteiro', 'decimal', 'leia', 'escreva', 'if', 'else']

# Operadores e delimitadores
OPERADORES = ['+', '-', '*', '/', '<', '>', '<=', '>=', '!=', '==', ':=', '=']
DELIMITADORES = ['(', ')', '{', '}', ',', ';']

def lexer(codigo):
    tokens = []
    codigo = codigo.replace('\n', ' ')  # Remover quebras de linha
    while codigo:
        # Verificar palavras-chave, identificadores, números, operadores, delimitadores e texto
        match = re.match(r'\s*(\b(?:' + '|'.join(PALAVRAS_CHAVE) + r')\b|[a-zA-Z_á-úÁ-Ú][a-zA-Z0-9_á-úÁ-Ú]*|\d+|'
                         r'\+|\-|\*|\/|<|>|<=|>=|!=|==|:=|=|\(|\)|\{|\}|,|;|"([^"\\]*(?:\\.[^"\\]*)*)")\s*', codigo)
        if match:
            valor = match.group(1)
            codigo = codigo[len(match.group(0)):]
            if valor in PALAVRAS_CHAVE:
                tipo_token = TIPOS_TOKEN['PALAVRA_CHAVE']
            elif valor in OPERADORES:
                tipo_token = TIPOS_TOKEN['OPERADOR']
            elif valor in DELIMITADORES:
                tipo_token = TIPOS_TOKEN['DELIMITADOR']
            elif valor.isdigit():
                tipo_token = TIPOS_TOKEN['NUMERO']
            elif valor[0].isalpha():
                tipo_token = TIPOS_TOKEN['ID']
            else:
                tipo_token = TIPOS_TOKEN['TEXTO']
                valor = valor[1:-1]  # Remover aspas do texto
            tokens.append((valor, tipo_token))
        elif codigo[0] == ' ':
            codigo = codigo[1:]  # Ignorar espaços em branco
        else:
            raise ValueError('Token inválido: ' + codigo)
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type=None, expected_value=None):
        token = self.current_token()
        if token and (expected_type is None or token[1] == expected_type) and (expected_value is None or token[0] == expected_value):
            self.pos += 1
            return token
        else:
            expected = f"{expected_type} {expected_value}".strip()
            raise SyntaxError(f"Expected {expected} but got {token}")

    def parse(self):
        return self.programa()

    def programa(self):
        self.consume('PALAVRA_CHAVE', 'programa')
        corpo = self.corpo()
        self.consume('PALAVRA_CHAVE', 'fimprog')
        return ('programa', corpo)

    def corpo(self):
        statements = []
        while self.current_token() and self.current_token()[0] != 'fimprog':
            if self.current_token()[0] in ['inteiro', 'decimal']:
                statements.append(self.declaracao())
            else:
                statements.append(self.comando())
        return statements

    def declaracao(self):
        tipo = self.tipo()
        var_list = self.var_list()
        self.consume('DELIMITADOR', ';')
        return ('declaracao', tipo, var_list)

    def tipo(self):
        token = self.consume('PALAVRA_CHAVE')
        if token[0] not in ['inteiro', 'decimal']:
            raise SyntaxError(f"Tipo inválido: {token[0]}")
        return token[0]

    def var_list(self):
        variables = [self.consume('ID')]
        while self.current_token() and self.current_token()[0] == ',':
            self.consume('DELIMITADOR', ',')
            variables.append(self.consume('ID'))
        return variables

    def comando(self):
        if self.current_token()[0] == 'escreva':
            return self.escreva()
        elif self.current_token()[0] == 'leia':
            return self.leia()
        elif self.current_token()[0] == 'if':
            return self.condicional()
        elif self.current_token()[0] == '{':
            return self.bloco()
        elif self.current_token()[1] == 'ID':
            return self.atribuicao()
        else:
            raise SyntaxError(f"Comando inválido: {self.current_token()}")

    def escreva(self):
        self.consume('PALAVRA_CHAVE', 'escreva')
        self.consume('DELIMITADOR', '(')
        argumentos = self.argumento_list()
        self.consume('DELIMITADOR', ')')
        self.consume('DELIMITADOR', ';')
        return ('escreva', argumentos)

    def leia(self):
        self.consume('PALAVRA_CHAVE', 'leia')
        self.consume('DELIMITADOR', '(')
        id_token = self.consume('ID')
        self.consume('DELIMITADOR', ')')
        self.consume('DELIMITADOR', ';')
        return ('leia', id_token)

    def condicional(self):
        self.consume('PALAVRA_CHAVE', 'if')
        self.consume('DELIMITADOR', '(')
        expr = self.expr()
        self.consume('DELIMITADOR', ')')
        bloco = self.bloco()
        if self.current_token() and self.current_token()[0] == 'else':
            self.consume('PALAVRA_CHAVE', 'else')
            else_bloco = self.bloco()
            return ('if_else', expr, bloco, else_bloco)
        return ('if', expr, bloco)

    def bloco(self):
        self.consume('DELIMITADOR', '{')
        comandos = []
        while self.current_token() and self.current_token()[0] != '}':
            comandos.append(self.comando())
        self.consume('DELIMITADOR', '}')
        return ('bloco', comandos)

    def expr(self):
        left = self.termo()
        while self.current_token() and self.current_token()[1] == 'OPERADOR' and self.current_token()[0] not in [':=', '=']:
            operador = self.consume('OPERADOR')
            right = self.termo()
            left = ('binop', operador, left, right)
        return left

    def termo(self):
        token = self.current_token()
        if token[1] == 'ID':
            return self.consume('ID')
        elif token[1] == 'NUMERO':
            return self.consume('NUMERO')
        elif token[0] == '(':
            self.consume('DELIMITADOR', '(')
            expr = self.expr()
            self.consume('DELIMITADOR', ')')
            return expr
        else:
            raise SyntaxError(f"Termo inválido: {token}")

    def argumento_list(self):
        argumentos = [self.argumento()]
        while self.current_token() and self.current_token()[0] == ',':
            self.consume('DELIMITADOR', ',')
            argumentos.append(self.argumento())
        return argumentos

    def argumento(self):
        token = self.current_token()
        if token[1] in ['TEXTO', 'ID', 'NUMERO']:
            return self.consume()
        else:
            raise SyntaxError(f"Argumento inválido: {token}")

    def atribuicao(self):
        id_token = self.consume('ID')
        operador = self.consume('OPERADOR', ':=')
        expr = self.expr()
        self.consume('DELIMITADOR', ';')
        return ('atribuicao', id_token, operador, expr)

# Teste do lexer e parser
codigo_teste = """
programa
inteiro x, y;
escreva("Olá, mundo!");
leia(x);
if (x > 0) {
    y := x * 2;
    escreva("O dobro de ", x, " é ", y);
} else {
    escreva("O valor de x é negativo");
}
fimprog
"""

tokens = lexer(codigo_teste)
print("Tokens:")
for token in tokens:
    print(token)

parser = Parser(tokens)
ast = parser.parse()
# ast = parser(tokens)
with open('ast.txt', 'w') as f:
    f.write(str(ast) + '\n')
