class AnalisadorSemantico:
    def __init__(self):
        self.tabela_simbolos = {}

    def declarar_variavel(self, variavel_id, variavel_tipo):
        try:
            if variavel_id in self.tabela_simbolos:
                raise ValueError(f"Erro Semântico: Variável '{variavel_id}' já declarada.")
            self.tabela_simbolos[variavel_id] = variavel_tipo
        except ValueError as e:
            print(e)

    def check_variavel(self, variavel_id):
        try:
            if variavel_id not in self.tabela_simbolos:
                raise ValueError(f"Erro Semântico: Variável '{variavel_id}' não declarada.")
            return self.tabela_simbolos[variavel_id]
        except ValueError as e:
            print(e)

    def check_tipo(self, variavel_id, tipo_esperado):
        try:
            variavel_tipo = self.check_variavel(variavel_id)
            if variavel_tipo != tipo_esperado:
                raise TypeError(f"Erro Semântico: Tipo incompatível: variável '{variavel_id}' é do tipo '{variavel_tipo}', esperado '{tipo_esperado}'.")
        except TypeError as e:
            print(e)