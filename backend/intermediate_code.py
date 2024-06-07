def generate_intermediate_code(ast):
    # Implementação da geração de código intermediário
    intermediate_code = []

    def traverse(node):
        if not node:
            return
        
        if node[0] == 'programa':
            intermediate_code.append("INICIO_PROGRAMA")
            for stmt in node[1]:
                traverse(stmt)
            intermediate_code.append("FIM_PROGRAMA")
        
        elif node[0] == 'declaracao':
            var_type = node[1]
            for var in node[2]:
                intermediate_code.append(f"DECLARE {var[0]} {var_type}")
        
        elif node[0] == 'atribuicao':
            var_name = node[1][0]
            expr = generate_expression_code(node[3])
            intermediate_code.append(f"{var_name} := {expr}")
        
        elif node[0] == 'leia':
            var_name = node[1][0]
            intermediate_code.append(f"LEIA {var_name}")
        
        elif node[0] == 'escreva':
            args = ", ".join(arg[0] if arg[1] != 'TEXTO' else f'"{arg[0]}"' for arg in node[1])
            intermediate_code.append(f"ESCREVA {args}")
        
        elif node[0] == 'if' or node[0] == 'if_else':
            expr = generate_expression_code(node[1])
            intermediate_code.append(f"IF {expr} THEN")
            traverse(node[2])
            if node[0] == 'if_else':
                intermediate_code.append("ELSE")
                traverse(node[3])
            intermediate_code.append("ENDIF")
        
        elif node[0] == 'bloco':
            for cmd in node[1]:
                traverse(cmd)
        
        elif node[0] == 'binop':
            left = generate_expression_code(node[2])
            right = generate_expression_code(node[3])
            intermediate_code.append(f"{left} {node[1][0]} {right}")

    def generate_expression_code(node):
        if node[1] == 'NUMERO':
            return node[0]
        if node[1] == 'DECIMAL':
            return node[0]
        elif node[1] == 'ID':
            return node[0]
        elif node[0] == 'binop':
            left = generate_expression_code(node[2])
            right = generate_expression_code(node[3])
            return f"{left} {node[1][0]} {right}"
        else:
            raise ValueError("Tipo de expressão desconhecido")

    traverse(ast)
    return "\n".join(intermediate_code)

if __name__ == "__main__":
    with open('./semantic_analysis.txt', 'r', encoding='utf-8') as f:
        ast = eval(f.read())
    intermediate_code = generate_intermediate_code(ast)
    with open('./intermediate_code.txt', 'w', encoding='utf-8') as f:
        f.write(intermediate_code)

    # print("Código Intermediário:")
    # print(intermediate_code)
    # print()
