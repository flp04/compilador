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

# Teste do lexer
codigo_teste = """
programa
decimal notaA1, notaA2, notaA3, media;
escreva("PROGRAMA PARA CALCULAR MÉDIA E APROVAÇÃO SEMESTRAL DO ALUNO");
escreva("Digite a nota da A1");
leia(notaA1);
escreva("Digite a nota da A2");
leia(notaA2);
escreva("Digite a nota da A3");
leia(notaA3);
if (x > 0) {
    y := x * 2;
    escreva("O dobro de ", x, " é ", y);
} else {
    escreva("O valor de x é negativo");
}
fimprog
"""

tokens = lexer(codigo_teste)
for token in tokens:
    print(token)

tokens = lexer(codigo_teste)
with open('tokens.txt', 'w', encoding='utf-8') as f:
    for token in tokens:
        f.write(str(token) + '\n')
