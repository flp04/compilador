# Biblioteca importada para validarmos os tokens com expressões
import re

TIPOS_TOKEN = {
    'PALAVRA_CHAVE': 'PALAVRA_CHAVE',
    'ID': 'ID',
    'NUMERO': 'NUMERO',
    'DECIMAL': 'DECIMAL',
    'OPERADOR': 'OPERADOR',
    'DELIMITADOR': 'DELIMITADOR',
    'TEXTO': 'TEXTO'
}

# Palavras-chave da linguagem
PALAVRAS_CHAVE = ['programa', 'fimprog', 'inteiro', 'decimal', 'texto', 'leia', 'escreva', 'se', 'senao', 'enquanto', 'para']

# Operadores aritméticos, de relação e atribuição
OPERADORES = ['+', '-', '*', '/', '<', '>', '<=', '>=', '!=', '==', ':=', '=']
DELIMITADORES = ['(', ')', '{', '}', ',', ';']

def lexer(codigo):
    tokens = []

    #Remover quebras de linha e comentarios
    padrao_comentarios = r'\*(.|[\n])*?\*|//.*[\n]'
    codigo = re.sub(padrao_comentarios, '', codigo)

    while codigo:
        match = re.match(r'\s*(\b(?:' + '|'.join(PALAVRAS_CHAVE) + r')\b|' # Verifica palavras-chave
            r'^[a-z_][a-zA-Z0-9_]*' # Verifica identificadores válidos
            r'|\d+(\.\d*)?(?![a-zA-Z_á-úÁ-Ú])' # Verifica números inteiros e decimais
            r'|\+|\-|\*|\/|<=|>=|<|>|!=|==|:=|=' # Verifica operadores
            r'|\(|\)|\{|\}|,|;' # Verifica delimitadores
            r'|"([^"\\]*(?:\\.[^"\\]*)*)")\s*', codigo) # Verifica texto entre aspas
        
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
            elif re.match(r'\d+(\.\d*)?', valor):
                tipo_token = TIPOS_TOKEN['DECIMAL']
            elif re.match(r'^[a-z_][a-zA-Z0-9_]*', valor[0]):
                tipo_token = TIPOS_TOKEN['ID']
            elif re.match(r'^"([^"\\]*(?:\\.[^"\\]*)*)"', valor):
                tipo_token = TIPOS_TOKEN['TEXTO']
                valor = valor[1:-1]  # Remover aspas do texto
            else:
                raise ValueError('Token inválido: ' + valor)
            tokens.append((valor, tipo_token))
        elif codigo[0] == ' ':
            codigo = codigo[1:]  # Ignorar espaços em branco
        else:
            raise ValueError('Token inválido: ' + codigo.split()[0])
    return tokens

try:
    # Pegar o código fonte na pasta raiz
    with open('codigo_fonte.txt', 'r', encoding='utf-8') as f:
        codigo_teste = f.read()

    # Testar o código no analisador lexer
    tokens = lexer(codigo_teste)

    # Salvar sequência de tokens em um arquivo texto
    with open('./tokens.txt', 'w', encoding='utf-8') as f:
        for token in tokens:
            f.write(str(token) + '\n')
    print('Sequência de tokens gerada.')
except ValueError as e:
    print(f"{e}")
