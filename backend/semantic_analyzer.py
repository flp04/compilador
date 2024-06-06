class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def declare_variable(self, var_name, var_type):
        if var_name in self.symbol_table:
            raise ValueError(f"Variável '{var_name}' já declarada.")
        self.symbol_table[var_name] = var_type

    def check_variable(self, var_name):
        if var_name not in self.symbol_table:
            raise ValueError(f"Variável '{var_name}' não declarada.")
        return self.symbol_table[var_name]

    def check_type(self, var_name, expected_type):
        var_type = self.check_variable(var_name)
        if var_type != expected_type:
            raise TypeError(f"Tipo incompatível: variável '{var_name}' é do tipo '{var_type}', esperado '{expected_type}'.")