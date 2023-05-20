class Regex(object):
    def __init__(self, expresion_regular):
        self.expresion_regular = expresion_regular
        self.pila = []
        self.postfix = []

    #Le asignamos a cada operador su precedencia. 
    Operadores = {
        '|': 1,
        '•': 2,
        '?': 3,
        '*': 3,
        '+': 3
    }

    #El famoso algoritmo shunting yard, timando en cuenta todo los parentesis. 
    def convertir_postfix(self):
        for caracter in self.expresion_regular:
            if caracter in self.Operadores:
                while (
                    self.pila and
                    self.pila[-1] != '(' and
                    self.Operadores[caracter] <= self.Operadores[self.pila[-1]]
                ):
                    self.postfix.append(self.pila.pop())
                self.pila.append(caracter)
            elif caracter == '(':
                self.pila.append(caracter)
            elif caracter == ')':
                while self.pila and self.pila[-1] != '(':
                    self.postfix.append(self.pila.pop())
                if self.pila and self.pila[-1] == '(':
                    self.pila.pop()
            else:
                self.postfix.append(caracter)

        while self.pila:
            self.postfix.append(self.pila.pop())

        return self.postfix