def generate_final_code(optimized_code):
    # Implementação da geração de código final
    final_code = []
    lines = optimized_code.split('\n')
    
    # Exemplo simples de geração de código final
    for line in lines:
        if line.startswith("DECLARE"):
            var_type = "let" if "inteiro" in line else "float"
            var_name = line.split()[1]
            final_code.append(f"{var_type} {var_name};")
        elif ":=" in line:
            var, expr = line.split(":=")
            var = var.strip()
            expr = expr.strip()
            final_code.append(f"{var} = {expr};")
        elif line.startswith("ESCREVA"):
            args = line[len("ESCREVA "):]
            final_code.append(f"console.log({args});")
        elif line.startswith("LEIA"):
            var_name = line.split()[1]
            final_code.append(f"{var_name} = prompt('Digite');")
        elif line == "INICIO_PROGRAMA":
            final_code.append("// inicio do programa")
            # final_code.append("def main():")
        elif line == "FIM_PROGRAMA":
            final_code.append("//fim do programa")
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
            # final_code.append("# End if")
        else:
            final_code.append(line)

    return "\n".join(final_code)

if __name__ == "__main__":
    with open('optimized_code.txt', 'r') as f:
        optimized_code = f.read()
    final_code = generate_final_code(optimized_code)
    with open('final_code.js', 'w') as f:
        f.write(final_code)

    print("Código Final:")
    print(final_code)