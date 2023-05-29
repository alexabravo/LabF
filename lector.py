class Lector(object):
    def __init__(self, token_functions):
        self.token_functions = token_functions
        
    def create_python(self):
        with open("scanner.py", "w") as file:
            file.write("from tokens import *\n\n")
            file.write("def scan(token):\n")
            
            for token, code in self.token_functions:
                file.write(f"    if token == '{token}':\n")
                
                if not code:
                    file.write("        return\n")
                else:
                    file.write("        try:\n")
                    file.write(f"            {code}\n")
                    file.write("        except Error:\n")
                    file.write("            return f'El token es indefinido'\n")
            
            file.write("    return f'Token indefinido: '\n")
            file.close
    
    def create_scanner_output(self):
        with open("scanner.py", "a") as file:
            file.write("\n")
            file.write("def output_scanner(simulation):\n")
            file.write("    with open('tokensText.txt', 'w') as f:\n")
            file.write("        for s in simulation:\n")
            file.write("            scanner = scan(s[0])\n")
            file.write("            f.write(f'{s} ==> Definicion: {scanner}\\n')\n")
            file.close()
