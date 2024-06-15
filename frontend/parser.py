from analisador_semantico import AnalisadorSemantico

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0
        self.analisador_semantico = AnalisadorSemantico()

    def token_atual(self):
        return self.tokens[self.posicao] if self.posicao < len(self.tokens) else None

    def consumir(self, tipo_esperado=None, valor_esperado=None):
        token = self.token_atual()
        if token and (tipo_esperado is None or token[1] == tipo_esperado) and (valor_esperado is None or token[0] == valor_esperado):
            self.posicao += 1
            return token
        else:
            token_esperado = f"{tipo_esperado} {valor_esperado}".strip()
            raise SyntaxError(f"Esperado {token_esperado}, mas obteve {token[0] if token else None}")

    def analisar(self):
        return self.programa()

    def programa(self):
        self.consumir('PALAVRA_CHAVE', 'programa')
        corpo = self.corpo()
        self.consumir('PALAVRA_CHAVE', 'fimprog')
        return ('programa', corpo)

    def corpo(self):
        instrucoes = []
        while self.token_atual() and self.token_atual()[0] != 'fimprog':
            if self.token_atual()[0] in ['inteiro', 'decimal', 'texto']:
                instrucoes.append(self.declaracao())
            else:
                instrucoes.append(self.comando())
        return instrucoes

    def declaracao(self):
        tipo = self.tipo()
        var_list = self.var_list()
        self.consumir('DELIMITADOR', ';')
        for var in var_list:
            self.analisador_semantico.declarar_variavel(var[0], tipo)
        return ('declaracao', tipo, var_list)

    def tipo(self):
        token = self.consumir('PALAVRA_CHAVE')
        if token[0] not in ['inteiro', 'decimal', 'texto']:
            raise SyntaxError(f"Tipo inválido: {token[0]}")
        return token[0]

    def var_list(self):
        variables = [self.consumir('ID')]
        while self.token_atual() and self.token_atual()[0] == ',':
            self.consumir('DELIMITADOR', ',')
            variables.append(self.consumir('ID'))
        return variables

    def comando(self):
        if self.token_atual()[0] == 'escreva':
            return self.escreva()
        elif self.token_atual()[0] == 'leia':
            return self.leia()
        elif self.token_atual()[0] == 'se':
            return self.condicional()
        elif self.token_atual()[0] == 'enquanto':
            return self.repeticao_enquanto()
        elif self.token_atual()[0] == 'para':
            return self.repeticao_para()
        elif self.token_atual()[0] == '{':
            return self.bloco()
        elif self.token_atual()[1] == 'ID':
            return self.atribuicao()
        else:
            raise SyntaxError(f"Comando inválido: {self.token_atual()}")

    def escreva(self):
        self.consumir('PALAVRA_CHAVE', 'escreva')
        self.consumir('DELIMITADOR', '(')
        argumentos = self.argumento_list()
        for arg in argumentos:
            if arg[1] == 'ID':
                self.analisador_semantico.check_variavel(arg[0])
        self.consumir('DELIMITADOR', ')')
        self.consumir('DELIMITADOR', ';')
        return ('escreva', argumentos)

    def leia(self):
        self.consumir('PALAVRA_CHAVE', 'leia')
        self.consumir('DELIMITADOR', '(')
        id_token = self.consumir('ID')
        self.analisador_semantico.check_variavel(id_token[0])  # Verifica se a variável foi declarada
        self.consumir('DELIMITADOR', ')')
        self.consumir('DELIMITADOR', ';')
        return ('leia', id_token)

    def condicional(self):
        self.consumir('PALAVRA_CHAVE', 'se')
        self.consumir('DELIMITADOR', '(')
        expressao = self.expressao()
        self.consumir('DELIMITADOR', ')')
        bloco = self.bloco()
        if self.token_atual() and self.token_atual()[0] == 'senao':
            self.consumir('PALAVRA_CHAVE', 'senao')
            else_bloco = self.bloco()
            return ('if_else', expressao, bloco, else_bloco)
        return ('se', expressao, bloco)

    def repeticao_enquanto(self):
        self.consumir('PALAVRA_CHAVE', 'enquanto')
        self.consumir('DELIMITADOR', '(')
        expressao = self.expressao()
        self.consumir('DELIMITADOR', ')')
        bloco = self.bloco()
        return ('enquanto', expressao, bloco)

    def repeticao_para(self):
        self.consumir('PALAVRA_CHAVE', 'para')
        self.consumir('DELIMITADOR', '(')
        atribuicao = self.atribuicao()
        expressao = self.expressao()
        self.consumir('DELIMITADOR', ';')
        expressao2 = self.expressao()
        self.consumir('DELIMITADOR', ')')
        bloco = self.bloco()
        return ('para', atribuicao, expressao, expressao2, bloco)

    def bloco(self):
        self.consumir('DELIMITADOR', '{')
        comandos = []
        while self.token_atual() and self.token_atual()[0] != '}':
            comandos.append(self.comando())
        self.consumir('DELIMITADOR', '}')
        return ('bloco', comandos)

    def expressao(self):
        left = self.termo()
        while self.token_atual() and self.token_atual()[1] == 'OPERADOR' and self.token_atual()[0] not in [':=', '=']:
            operador = self.consumir('OPERADOR')
            right = self.termo()
            # Verificação de tipos (por simplicidade, supondo que termos são variáveis ou números)
            if left[1] == 'ID':
                left_type = self.analisador_semantico.check_variavel(left[0])
            elif left[1] == 'NUMERO':
                left_type = 'inteiro'
            elif left[1] == 'DECIMAL':
                left_type = 'decimal'
            elif left[1] == 'TEXTO':
                left_type = 'texto'
            if right[1] == 'ID':
                right_type = self.analisador_semantico.check_variavel(right[0])
            elif right[1] == 'NUMERO':
                right_type = 'inteiro'
            elif right[1] == 'DECIMAL':
                right_type = 'decimal'
            elif right[1] == 'TEXTO':
                right_type = 'texto'

            if operador[0] != '+' and left_type != right_type or (left_type != 'inteiro' and left_type != 'decimal' and left_type != 'texto'):
                raise TypeError(f"Operação inválida entre tipos '{left_type}' e '{right_type}'")
            
            left = ('binop', operador, left, right)
        return left

    def termo(self):
        token = self.token_atual()
        if token[1] == 'ID':
            return self.consumir('ID')
        elif token[1] == 'NUMERO':
            return self.consumir('NUMERO')
        elif token[1] == 'DECIMAL':
            return self.consumir('DECIMAL')
        elif token[1] == 'TEXTO':
            return self.consumir('TEXTO')
        elif token[0] == '(':
            self.consumir('DELIMITADOR', '(')
            expressao = self.expressao()
            self.consumir('DELIMITADOR', ')')
            return expressao
        else:
            raise SyntaxError(f"Termo inválido: {token}")

    def argumento_list(self):
        argumentos = [self.argumento()]
        while self.token_atual() and self.token_atual()[0] in [',', '+']:
            self.consumir(self.token_atual()[1], self.token_atual()[0])
            argumentos.append(self.argumento())
        return argumentos

    def argumento(self):
        token = self.token_atual()
        if token[1] == 'ID':
            if self.analisador_semantico.check_variavel(token[0]):
                return self.consumir()
            else:
                raise SyntaxError(f"Argumento inválido: {token[0]}")
        else:
            return self.consumir()

    def atribuicao(self):
        id_token = self.consumir('ID')
        self.analisador_semantico.check_variavel(id_token[0])  # Verifica se a variável foi declarada
        operador = self.consumir('OPERADOR', ':=')
        expressao = self.expressao()
        self.consumir('DELIMITADOR', ';')
        return ('atribuicao', id_token, operador, expressao)
    
tokens = []

# Teste do parser com análise semântica
with open('./tokens.txt', 'r', encoding='utf-8') as arquivo:
  linhas = arquivo.readlines()

for linha in linhas:
  linha = linha.strip().strip("()").replace("'", "")
  token, tipo = linha.split(', ')
  tokens.append((token, tipo))

try:
    parser = Parser(tokens)
    ast = parser.analisar()
    with open('arvore_sintatica_abstrata.txt', 'w', encoding='utf-8') as f:
        f.write(str(ast) + '\n')

    print('Árvore de sintaxe abstrata gerada.')

    with open('tabela_simbolos.txt', 'w', encoding='utf-8') as f:
        f.write(str(parser.analisador_semantico.tabela_simbolos) + '\n')

    print('Tabela de símbolos gerada.')

except SyntaxError as e:
    print(f"Erro sintático: {e}")