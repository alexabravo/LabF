import copy
import graphviz
import networkx as nx
from lexer import *


class Yalp(object):
    def __init__(self, archivo, simulacion):
        self.numero = 0
        self.subtoken = []
        self.tokens = []
        self.simulacion = simulacion
        self.producciones = [] 
        self.subproducciones = []
        self.subsets= [] 
        self.numeroSubsets = [] 
        self.ocurrencia = [] 
        self.transiciones = [] 

        leer = Lexer(archivo)
        _,funcionesTokens = leer.leerYalex()

        for sublista in funcionesTokens:
            if 'return' in sublista[1]:
                sublista[1] = sublista[1].replace('return ', '')
        self.tokenFunctions = funcionesTokens
        
    def yapar(self):
        comentario = False
        esToken = False
        esExpresion = True
        nombreFuncion = ""
        tokensProducidos = []
        separador = False

        for tipoToken, *values in self.simulacion:
            if tipoToken == "/*":
                comentario = True

            if not comentario:
                if tipoToken == "%%":
                    separador = True

                if separador:
                    if esExpresion and tipoToken == "minusword":
                        nombreFuncion = values[0][0].upper()
                        esExpresion = False
                    elif not esExpresion:
                        if tipoToken == "minusword":
                            tokensProducidos.append(values[0][0].upper())
                        elif tipoToken == "mayusword":
                            tokensProducidos.append(values[0])
                        elif tipoToken == "|":
                            self.producciones.append([nombreFuncion, tokensProducidos])
                            tokensProducidos = []
                        elif tipoToken == ";":
                            if tokensProducidos:
                                self.producciones.append([nombreFuncion, tokensProducidos])
                                tokensProducidos = []
                            esExpresion = True

                else:
                    if tipoToken == "%token":
                        esToken = True
                    elif tipoToken == "IGNORE":
                        esToken = False

                    if esToken and tipoToken == "mayusword":
                        self.tokens.append(values[0])
                        self.subtoken.append(values[0])
                    elif not esToken and tipoToken == "mayusword":
                        self.tokens.remove(values[0])
                        self.subtoken.remove(values[0])

            if tipoToken == "*/":
                comentario = False

        self.tokens = [tokenFuncion[0] if token == tokenFuncion[1] else token for token in self.tokens for tokenFuncion in self.tokenFunctions]

        for produccion in self.producciones:
            for i, token in enumerate(produccion[1]):
                for subtoken in self.subtoken:
                    if token == subtoken:
                        index = self.subtoken.index(subtoken)
                        produccion[1][i] = self.tokens[index]
        
    def construccion(self):

        valorInicial = self.producciones[0][0]
        self.producciones.insert(0, [valorInicial + "'", [valorInicial]])
        self.subproducciones = copy.deepcopy(self.producciones)

        for produccion in self.producciones:
            produccion[1].insert(0, ".")

        self.closure([self.producciones[0]])

        while self.ocurrencia:
            self.goto(self.ocurrencia.pop(0))

        estadoInicial = self.producciones[0][0]
        for subset in self.subsets:
            for item in subset:
                indexAceptado = item[1].index(".")
                if indexAceptado - 1 >= 0:
                    if item[0] == estadoInicial and item[1][indexAceptado - 1] == estadoInicial[:-1]:
                        indexFinal = self.subsets.index(subset)
                        self.transiciones.append([self.numeroSubsets[indexFinal], "$", "accept"])

        
    def closure(self, item, elemento=None, ciclo=None):
        closureArray = item.copy()

        while True:
            largo = len(closureArray)
            for item in closureArray:
                indexDot = item[1].index(".")
                if indexDot + 1 < len(item[1]):
                    valorSiguiente = item[1][indexDot + 1]
                    itemsNuevos = [y for y in self.producciones if y[0] == valorSiguiente and y not in closureArray]
                    closureArray.extend(itemsNuevos)

            if largo == len(closureArray):
                break

        itemsSorted = sorted(closureArray, key=lambda x: x[0])

        if itemsSorted not in self.subsets:
            self.subsets.append(itemsSorted)
            self.numeroSubsets.append(self.numero)
            self.numero += 1
            self.ocurrencia.append(itemsSorted)

        if elemento is not None and ciclo is not None:
            start_index = self.subsets.index(ciclo)
            end_index = self.subsets.index(itemsSorted)
            self.transiciones.append([self.numeroSubsets[start_index], elemento, self.numeroSubsets[end_index]])

        
    def goto(self, ocurrencia):
        elements = list(set(x[1][x[1].index(".") + 1] for x in ocurrencia if x[1].index(".") + 1 < len(x[1])))

        for elem in elements:
            temporal = [copy.deepcopy(y) for y in ocurrencia if y[1].index(".") + 1 < len(y[1]) and y[1][y[1].index(".") + 1] == elem]

            for item in temporal:
                indexDot = item[1].index(".")
                if indexDot + 1 < len(item[1]):
                    item[1][indexDot], item[1][indexDot + 1] = item[1][indexDot + 1], item[1][indexDot]

            self.closure(temporal, elem, ocurrencia)



    