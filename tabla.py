import copy
import pandas as pd
from tabulate import tabulate

class Tabla(object):
    def __init__(self, transiciones, sets, numeros, reglas):
        self.transiciones = transiciones
        self.sets = sets
        self.reglas = reglas
        self.noTerminales = []
        
        self.estado = numeros
        self.first = []
        self.actionDatos = []
        self.action = []
        self.gotoDatos = []
        self.goto = []
        
        for token in self.reglas:
            if token[0] not in self.noTerminales:
                self.noTerminales.append(token[0])
                
    def tabla(self):
        self.gotoDatos = sorted(list(set(x[1] for x in self.transiciones if x[1].isupper())))
        self.actionDatos = sorted(list(set(x[1] for x in self.transiciones if not x[1].isupper())), reverse=True)

        def encontrarTransiciones(estado, simbolo):
            return [(x[0], x[1], x[2]) for x in self.transiciones if x[0] == estado and x[1] == simbolo]

        for estado in self.estado:
            for simbolo in self.gotoDatos:
                self.goto.extend(encontrarTransiciones(estado, simbolo))
            for simbolo in self.actionDatos:
                self.action.extend(encontrarTransiciones(estado, simbolo))

        first = self.reglas[0][1][0]

        for rule in self.reglas:
            visited = [rule[0]]
            for y in visited:
                new_visited = [z[1][0] for z in self.reglas if y == z[0] and z[1][0] not in visited]
                visited.extend(new_visited)

            self.first.append([rule[0], sorted(list(set(y for y in visited if y in self.actionDatos)))])

        for i, estado in enumerate(self.sets):
            for item in estado:
                if item[1][-1] == ".":
                    index = item[1].index(".")
                    if item[1][index - 1] != first:
                        copiaTrans = copy.deepcopy(item)
                        copiaTrans[1].remove(".")
                        for j, rule in enumerate(self.reglas):
                            if rule == copiaTrans:
                                transaccion = self.follow(copiaTrans[0], first)
                                self.action.extend([(i, w, "r" + str(j)) for w in transaccion])

        print("GOTO: ", self.goto)
        print("ACTION: ", self.action)

        
    def follow(self, estado, estadoAceptado):
        estadoAceptado += "'"
        revisar = {estado}

        while True:
            revisado = set()
            for y in revisar:
                for x in self.reglas:
                    if y in x[1]:
                        index = x[1].index(y)
                        if index == len(x[1]) - 1:
                            revisado.add(x[0])
                        elif index + 1 < len(x[1]) and x[1][index + 1] in self.noTerminales:
                            valoresFirst = [z[1] for z in self.first if z[0] == x[1][index + 1]]
                            revisado.update(valoresFirst[0] if valoresFirst else [])

            if len(revisar) == len(revisar | revisado):
                break

            revisar |= revisado

        transaccions = set()
        for x in revisar:
            for y in self.reglas:
                if x in y[1]:
                    index = y[1].index(x)
                    if index + 1 < len(y[1]) and y[1][index + 1] not in self.noTerminales:
                        transaccions.add(y[1][index + 1])

        if estadoAceptado in revisar:
            transaccions.add("$")

        return list(transaccions)


    def dibujoTabla(self):
        columns = self.actionDatos + self.gotoDatos
        df = pd.DataFrame(columns=columns)

        for row, col, value in self.goto + self.action:
            df.at[row, col] = value

        df.fillna('', inplace=True)

        df.index.name = 'ESTADO'

        headers = ['ACTION'] * len(self.actionDatos) + ['GOTO'] * len(self.gotoDatos)
        df.columns = pd.MultiIndex.from_tuples(zip(headers, df.columns))
        
        df.sort_index(inplace=True)
        
        tabla = tabulate(df, headers='keys', tablefmt='heavy_grid', showindex=True)
        print(tabla)