# Gera o código intermediário estruturado para geração do código de saída
def gerar_codigo_intermediario(arvore_sintatica_abstrata):
    codigo_intermediario = []

    # Função recursiva para percorrer cada nó da árvore até que não haja mais nós
    def percorrer(no):
        if not no:
            return
        
        if no[0] == 'programa':
            codigo_intermediario.append("INICIO_PROGRAMA")
            for declaracao in no[1]:
                percorrer(declaracao)
            codigo_intermediario.append("FIM_PROGRAMA")
        
        elif no[0] == 'declaracao':
            variavel_tipo = no[1]
            # Itera o segundo elemento do nó pois pode ser declarada mais de uma variável
            for variavel_identificador in no[2]:
                codigo_intermediario.append(f"DECLARE {variavel_identificador[0]} {variavel_tipo}")
        
        elif no[0] == 'atribuicao':
            variavel_id = no[1][0]
            expressao = gerar_codigo(no[3])
            codigo_intermediario.append(f"{variavel_id} := {expressao}")
        
        elif no[0] == 'leia':
            variavel_id = no[1][0]
            codigo_intermediario.append(f"LEIA {variavel_id}")
        
        elif no[0] == 'escreva':
            argumentos = " + ".join(arg[0] if arg[1] != 'TEXTO' else f'"{arg[0]}"' for arg in no[1])
            codigo_intermediario.append(f"ESCREVA {argumentos}")
        
        elif no[0] == 'se' or no[0] == 'if_else':
            expressao = gerar_codigo(no[1])
            codigo_intermediario.append(f"IF {expressao} THEN")
            percorrer(no[2])
            if no[0] == 'if_else':
                codigo_intermediario.append("ELSE")
                percorrer(no[3])
            codigo_intermediario.append("ENDIF")

        elif no[0] == 'enquanto':
            expressao = gerar_codigo(no[1])
            codigo_intermediario.append(f"WHILE {expressao} DO")
            percorrer(no[2])
            codigo_intermediario.append("ENDWHILE")

        elif no[0] == 'para':
            # atribuicao = gerar_codigo(no[1])
            atribuicao = f"{no[1][1][0]} {no[1][2][0]} {no[1][3][0]}"
            expressao = gerar_codigo(no[2])
            expressao2 = gerar_codigo(no[3])
            codigo_intermediario.append(f"FOR {atribuicao};{expressao};{expressao2}; DO")
            percorrer(no[4])
            codigo_intermediario.append("ENDFOR")
        
        elif no[0] == 'bloco':
            for comando in no[1]:
                percorrer(comando)
        
        elif no[0] == 'binop':
            operador = no[1][0]
            operando_esquerda = gerar_codigo(no[2])
            operando_direita = gerar_codigo(no[3])
            codigo_intermediario.append(f"{operando_esquerda} {operador} {operando_direita}")
            
    def gerar_codigo(no):
        if no[1] == 'NUMERO':
            return no[0]
        if no[1] == 'DECIMAL':
            return no[0]
        if no[1] == 'TEXTO':
            return f'"{no[0]}"'
        elif no[1] == 'ID':
            return no[0]
        elif no[0] == 'binop':
            esquerda = gerar_codigo(no[2])
            direita = gerar_codigo(no[3])
            return f"{esquerda} {no[1][0]} {direita}"

        else:
            print(no)
            raise ValueError("Tipo de expressão desconhecido")

    percorrer(arvore_sintatica_abstrata)
    return "\n".join(codigo_intermediario)

if __name__ == "__main__":
    with open('./arvore_sintatica_abstrata.txt', 'r', encoding='utf-8') as f:
        arvore_sintatica_abstrata = eval(f.read())

    codigo_intermediario = gerar_codigo_intermediario(arvore_sintatica_abstrata)

    with open('./codigo_intermediario.txt', 'w', encoding='utf-8') as f:
        f.write(codigo_intermediario)

    print('Código intermediário gerado.')