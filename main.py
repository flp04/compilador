import os

def main():
    print("Iniciando processo de tradução...")
    print()

    os.system('python frontend/lexer.py')
    print("Realizada análise léxica.")

    os.system('python frontend/parser.py')
    print("Realizada análise sintática e semântica.")

    os.system('python backend/intermediate_code.py')
    print("Gerado código intermediário.")

    os.system('python backend/code_generator.py')
    print("Gerado código objeto.")

    print()
    print("Execução de fases do compilador concluída.")
    print()

    print("Saída:")
    with open('codigo_objeto.java', 'r', encoding='utf-8') as f:
        print(f.read())


if __name__ == "__main__":
    main()