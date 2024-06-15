import os

def main():
    print("Iniciando processo de tradução...")
    print()
    try:
        print("Executando análise léxica...")
        os.system('python frontend/lexer.py')

        print("Executando análise sintática e semântica...")
        os.system('python frontend/parser.py')

        print("Geradando código intermediário...")
        os.system('python backend/otimizador.py')

        print("Geradando código de saída...")
        os.system('python backend/gerador_codigo.py')

        print()
        print("Execução de fases do compilador concluída.")
        print()

        print("Saída:")
        with open('codigo_saida.java', 'r', encoding='utf-8') as f:
            print(f.read())
    except KeyError as e:
        print(e)

if __name__ == "__main__":
    main()