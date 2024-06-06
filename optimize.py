def optimize_code(intermediate_code):
    # Implementação da otimização de código
    optimized_code = []
    lines = intermediate_code.split('\n')
    
    # Exemplo simples de otimização: remover declarações de variáveis não usadas
    declared_vars = set()
    used_vars = set()
    for line in lines:
        if line.startswith("DECLARE"):
            declared_vars.add(line.split()[1])
        elif ":=" in line:
            var = line.split(":=")[0].strip()
            used_vars.add(var)
        elif any(op in line for op in ["ESCREVA", "LEIA"]):
            vars_in_line = [word.strip() for word in line.split() if word.isidentifier()]
            used_vars.update(vars_in_line)
    
    for line in lines:
        if line.startswith("DECLARE"):
            var = line.split()[1]
            if var in used_vars:
                optimized_code.append(line)
        else:
            optimized_code.append(line)
    
    return "\n".join(optimized_code)

if __name__ == "__main__":
    with open('intermediate_code.txt', 'r') as f:
        intermediate_code = f.read()
    optimized_code = optimize_code(intermediate_code)
    with open('optimized_code.txt', 'w') as f:
        f.write(optimized_code)

    print("Código Otimizado:")
    print(optimized_code)