# Biblioteca importada para realizar conversão de str em dicionário
import ast

def gerar_codigo_saida(codigo_intermediario):
    codigo_saida = []
    # Divide o código intermediário em linhas
    linhas = codigo_intermediario.split('\n')

    # Itera o código intermediário linha a a linha verificando as palavras-chave
    for linha in linhas:
        # Ao identificar a palavra-chave traduz conforme a sintaxe da linguagem de destino
        if linha.startswith("DECLARE"):
            variavel_id = linha.split()[1]
            variavel_tipo = check_tabela_simbolos(variavel_id)
            if variavel_tipo == 'inteiro':
                variavel_tipo_traduzido = 'int'
            elif variavel_tipo == 'decimal':
                variavel_tipo_traduzido = 'double'
            elif variavel_tipo == 'texto':
                variavel_tipo_traduzido = 'String'
            codigo_saida.append(f"{variavel_tipo_traduzido} {variavel_id};")
        elif ":=" in linha and "FOR" not in linha:
            variavel, expressao = linha.split(":=")
            variavel = variavel.strip()
            expressao = expressao.strip()
            codigo_saida.append(f"{variavel} = {expressao};")
        elif linha.startswith("ESCREVA"):
            argumentos = linha[len("ESCREVA "):]
            codigo_saida.append(f"System.out.println({argumentos});")
        elif linha.startswith("LEIA"):
            variavel_id = linha.split()[1]
            variavel_tipo = check_tabela_simbolos(variavel_id)
            if variavel_tipo == 'inteiro':
                codigo_saida.append(f"{variavel_id} = scanner.nextInt();")
            elif variavel_tipo == 'decimal':
                codigo_saida.append(f"{variavel_id} = scanner.nextDouble();")
            elif variavel_tipo in 'texto':
                codigo_saida.append(f"{variavel_id} = scanner.nextLine();")
        elif linha == "INICIO_PROGRAMA":
            codigo_saida.append("public class Main { public static void main(String[] args) {")
            for l in linhas:
                if l.startswith("LEIA"):
                    codigo_saida.insert(0, f"import java.util.Scanner;")
                    codigo_saida.append(f"Scanner scanner = new Scanner(System.in);")
                    break
        elif linha == "FIM_PROGRAMA":
            codigo_saida.append("}}")
        elif linha.startswith("IF"):
            partes = linha.split()
            codigo_saida.append(f"if ({partes[1]} {partes[2]} {partes[3]})" + " {")
        elif linha == "ELSE":
            codigo_saida.append("} else {")
        elif linha == "ENDIF":
            codigo_saida.append("}")
        elif linha.startswith("WHILE"):
            partes = linha.split()
            codigo_saida.append(f"while ({partes[1]} {partes[2]} {partes[3]})" + " {")
        elif linha == "ENDWHILE":
            codigo_saida.append("}")
        elif linha.startswith("FOR"):
            partes = linha.replace(' ', ';')
            partes = partes.split(';')
            # partes[0].replace(':=', '=')
            print(partes)
            codigo_saida.append(f"for ({partes[1]} = {partes[3]}; {partes[4]} {partes[5]} {partes[6]}; {partes[7]} {partes[8]}= {partes[9]})" + " {")
        elif linha == "ENDFOR":
            codigo_saida.append("}")
        else:
            codigo_saida.append(linha)

    # retorna o código de saida contendo um script em java correspondente ao código fonte 
    return "\n".join(codigo_saida)

def check_tabela_simbolos(variavel_id):
    return tabela_simbolos[variavel_id]

if __name__ == "__main__":
    # Carrega o arquivo de texto com a tabela de símbolos gerada no frontend
    with open('./tabela_simbolos.txt', 'r', encoding='utf-8') as f:
        tabela_simbolos = f.read()

    # Transforma o arquivo de texto em um dicionário
    tabela_simbolos = ast.literal_eval(tabela_simbolos)

    # Carrega o código intermediário gerado através da árvore sintátic abstrata
    with open('./codigo_intermediario.txt', 'r', encoding='utf-8') as f:
        codigo_intermediario = f.read()
    codigo_saida = gerar_codigo_saida(codigo_intermediario)
    
    with open('./codigo_saida.java', 'w', encoding='utf-8') as f:
        f.write(codigo_saida)

    print('Código de saída gerado.')