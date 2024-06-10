import ast

def generate_final_code(optimized_code):
    # Implementação da geração de código final
    final_code = []
    lines = optimized_code.split('\n')
    
    # Exemplo simples de geração de código final
    for line in lines:
        if line.startswith("DECLARE"):
            var_name = line.split()[1]
            symbol_type = check_symbol_type(var_name)
            if symbol_type == 'inteiro':
                var_type = 'int'
            elif symbol_type == 'decimal':
                var_type = 'double'
            elif symbol_type == 'texto':
                var_type = 'String'
            final_code.append(f"{var_type} {var_name};")
        elif ":=" in line:
            var, expr = line.split(":=")
            var = var.strip()
            expr = expr.strip()
            final_code.append(f"{var} = {expr};")
        elif line.startswith("ESCREVA"):
            args = line[len("ESCREVA "):]
            final_code.append(f"System.out.println({args});")
        elif line.startswith("LEIA"):
            var_name = line.split()[1]
            var_type = check_symbol_type(var_name)
            if var_type == 'inteiro':
                final_code.append(f"{var_name} = scanner.nextInt();")
            elif var_type == 'decimal':
                final_code.append(f"{var_name} = scanner.nextDouble();")
            elif var_type in 'texto':
                final_code.append(f"{var_name} = scanner.nextLine();")
        elif line == "INICIO_PROGRAMA":
            final_code.append("public class Main { public static void main(String[] args) {")
            for l in lines:
                if l.startswith("LEIA"):
                    final_code.insert(0, f"import java.util.Scanner;")
                    final_code.append(f"Scanner scanner = new Scanner(System.in);")
                    break
            # final_code.append("def main():")
        elif line == "FIM_PROGRAMA":
            final_code.append("}}")
            # final_code.append("//fim do programa")
            # final_code.append("if __name__ == '__main__':\n    main()")
        elif line.startswith("IF"):
            partes = line.split()
            final_code.append(f"if ({partes[1]} {partes[2]} {partes[3]})" + " {")
            # final_code.append("if:")
        elif line == "ELSE":
            final_code.append("} else {")
            # final_code.append("else:")
        elif line == "ENDIF":
            final_code.append("}")
        elif line.startswith("WHILE"):
            partes = line.split()
            final_code.append(f"while ({partes[1]} {partes[2]} {partes[3]})" + " {")
        elif line == "ENDWHILE":
            final_code.append("}")
        # elif line == "ARRUMAR":
        #     arg = line[len("ARRUMAR "):]
        #     final_code.append(f"Math.round({arg})")
        else:
            final_code.append(line)

    return "\n".join(final_code)

def check_symbol_type(var_name):
    return symbol_table[var_name]

if __name__ == "__main__":
    with open('./tabela_simbolos.txt', 'r', encoding='utf-8') as f:
        symbol_table = f.read()

    symbol_table = ast.literal_eval(symbol_table)

    with open('./codigo_intermediario.txt', 'r', encoding='utf-8') as f:
        optimized_code = f.read()
    final_code = generate_final_code(optimized_code)
    
    with open('./codigo_objeto.java', 'w', encoding='utf-8') as f:
        f.write(final_code)

    print('Código objeto gerado.')

    # print("Saída:")
    # print(final_code)
    # print()