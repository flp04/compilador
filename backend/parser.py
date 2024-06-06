from semantic_analyzer import SemanticAnalyzer

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.semantic_analyzer = SemanticAnalyzer()

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
        for var in var_list:
            self.semantic_analyzer.declare_variable(var[0], tipo)
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
        for arg in argumentos:
            if arg[1] == 'ID':
                self.semantic_analyzer.check_variable(arg[0])
        self.consume('DELIMITADOR', ')')
        self.consume('DELIMITADOR', ';')
        return ('escreva', argumentos)

    def leia(self):
        self.consume('PALAVRA_CHAVE', 'leia')
        self.consume('DELIMITADOR', '(')
        id_token = self.consume('ID')
        self.semantic_analyzer.check_variable(id_token[0])  # Verifica se a variável foi declarada
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
            # Verificação de tipos (por simplicidade, supondo que termos são variáveis ou números)
            if left[1] == 'ID':
                left_type = self.semantic_analyzer.check_variable(left[0])
            elif left[1] == 'NUMERO':
                left_type = 'inteiro'
            elif left[1] == 'DECIMAL':
                left_type = 'decimal'
            
            if right[1] == 'ID':
                right_type = self.semantic_analyzer.check_variable(right[0])
            elif right[1] == 'NUMERO':
                right_type = 'inteiro'
            elif right[1] == 'DECIMAL':
                right_type = 'decimal'
            
            if left_type != right_type or left_type != 'inteiro' and left_type != 'decimal':
                raise TypeError(f"Operação inválida entre tipos '{left_type}' e '{right_type}'")
            
            left = ('binop', operador, left, right)
        return left

    def termo(self):
        token = self.current_token()
        if token[1] == 'ID':
            return self.consume('ID')
        elif token[1] == 'NUMERO':
            return self.consume('NUMERO')
        elif token[1] == 'DECIMAL':
            return self.consume('DECIMAL')
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
        if token[1] in ['TEXTO', 'ID', 'NUMERO', 'DECIMAL']:
            return self.consume()
        else:
            raise SyntaxError(f"Argumento inválido: {token}")

    def atribuicao(self):
        id_token = self.consume('ID')
        self.semantic_analyzer.check_variable(id_token[0])  # Verifica se a variável foi declarada
        operador = self.consume('OPERADOR', ':=')
        expr = self.expr()
        self.consume('DELIMITADOR', ';')
        return ('atribuicao', id_token, operador, expr)
    
tokens = []

# Teste do lexer e parser com análise semântica
with open('tokens.txt', 'r', encoding='utf-8') as arquivo:
  linhas = arquivo.readlines()

for linha in linhas:
  linha = linha.strip().strip("()").replace("'", "")
  token, tipo = linha.split(', ')
  tokens.append((token, tipo))

# print(tokens.split('\n'))

# print(tokens)

# i=1
# for token in tokens:
#   print(i)
#   print(token)
#   i += 1

parser = Parser(tokens)
ast = parser.parse()

print("\nAST:")
print(ast)

with open('semantic_analysis.txt', 'w', encoding='utf-8') as f:
  f.write(str(ast) + '\n')