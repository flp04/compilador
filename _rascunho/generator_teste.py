def generate_final_code(optimized_code):
    final_code = []
    lines = optimized_code.split('\n')

    def translate_expression(expr):
        # Transforma expressões do formato intermediário para o formato C
        return expr.replace(' := ', ' = ').replace('LEIA', 'scanf').replace('ESCREVA', 'printf')

    for line in lines:
        if line.startswith("DECLARE"):
            var_type = "int" if "inteiro" in line else "float"
            var_name = line.split()[1]
            final_code.append(f"{var_type} {var_name};")
        elif ":=" in line:
            var, expr = line.split(":=")
            var = var.strip()
            expr = expr.strip()
            final_code.append(f"{var} = {expr};")
        elif line.startswith("ESCREVA"):
            args = line[len("ESCREVA "):]
            args = args.split(", ")
            format_string = ""
            variables = []
            for arg in args:
                if arg.startswith('"') and arg.endswith('"'):
                    format_string += arg[1:-1]
                else:
                    format_string += " %d"
                    variables.append(arg)
            format_string += "\\n"
            final_code.append(f'printf("{format_string}"' + ''.join([f", {var}" for var in variables]) + ');')
        elif line.startswith("LEIA"):
            var_name = line.split()[1]
            final_code.append(f"scanf(\"%d\", &{var_name});")
        elif line == "INICIO_PROGRAMA":
            final_code.append("#include <stdio.h>\nint main() {")
        elif line == "FIM_PROGRAMA":
            final_code.append("return 0;\n}")
        elif line.startswith("IF"):
            expr = line[len("IF "):].strip().replace(" THEN", "")
            final_code.append(f"if ({translate_expression(expr)}) {{")
        elif line == "ELSE":
            final_code.append("} else {")
        elif line == "ENDIF":
            final_code.append("}")
        else:
            final_code.append(line)

    return "\n".join(final_code)

if __name__ == "__main__":
    with open('optimized_code.txt', 'r') as f:
        optimized_code = f.read()
    final_code = generate_final_code(optimized_code)
    with open('final_code.txt', 'w') as f:
        f.write(final_code)

    print("Código Final:")
    print(final_code)