import string

class AFD:
    def __init__(self, postfix):
        self.postfix = postfix
        self.postfix.append('#')
        self.postfix.append('•')
        self.postfixNuevo = []
        self.listaNueva = []

        #Listas para los estados nullable, firstPos, lastPos y followPos
        self.nullable= []
        self.firstPos= []
        self.lastPos = []
        self.followPos = [] 

        #Listass para los estados nullable, firstPos, lastPos y followPos que se eliminan
        self.firstPosEliminado = []
        self.lastPosEliminado = []
        self.nullableEliminado = []
        self.qu = []
        self.estadosNumerados()
        self.afd()
        self.followpos()
    
    #Enumeramos los estados 
    def estadosNumerados(self):
        self.qu = list(range(1, 1000))
        self.postfixNuevo = [self.qu.pop(0) if x not in '*|•?+ε' else x for x in self.postfix]


    #Construimos el AFD
    def afd(self):
        for node in self.postfixNuevo:
            if str(node) in '*|•?+ε':
                if node == '*':
                    #Revisamos el nullable, firstPos y lastPos
                    self.nullable.append(True)
                    self.firstPos.append(self.firstPosEliminado[-1])
                    self.lastPos.append(self.lastPosEliminado[-1])

                    self.nullableEliminado.append(True)
                    self.firstPosEliminado.append(self.firstPosEliminado[-1])
                    self.lastPosEliminado.append(self.lastPosEliminado[-1])

                    #Eliminamos el nullable, firstPos y lastPos
                    self.nullableEliminado.pop(-2)
                    self.firstPosEliminado.pop(-2)
                    self.lastPosEliminado.pop(-2)

                elif node == '|':
                    #Revisamos el nullable, firstPos y lastPos
                    nodo1 = self.nullableEliminado[-2]
                    nodo2 = self.nullableEliminado[-1]
                    if nodo1 or nodo2:
                        self.nullable.append(True)
                        self.nullableEliminado.append(True)
                    else:
                        self.nullable.append(False)
                        self.nullableEliminado.append(False)
                    #Eliminamos el nullable
                    self.nullableEliminado.pop(-2)
                    self.nullableEliminado.pop(-2)

                    #Agregamos el firstPos
                    first = self.firstPosEliminado[-2] + self.firstPosEliminado[-1]
                    first.sort()
                    self.firstPos.append(first)
                    self.firstPosEliminado.append(first)
                    #Eliminamos el lastPos
                    self.firstPosEliminado.pop(-2)
                    self.firstPosEliminado.pop(-2)

                    #Agregamos el lastPos
                    last = self.lastPosEliminado[-2] + self.lastPosEliminado[-1]
                    last.sort()
                    self.lastPos.append(last)
                    self.lastPosEliminado.append(last)
                    #Eliminamos el lastpos
                    self.lastPosEliminado.pop(-2)
                    self.lastPosEliminado.pop(-2)

                elif node == '•':
                    #Revisamos si es nullable
                    nodo1 = self.nullableEliminado[-2]
                    nodo2 = self.nullableEliminado[-1]
                    if nodo1 and nodo2:
                        self.nullable.append(True)
                        self.nullableEliminado.append(True)
                    else:
                        self.nullable.append(False)
                        self.nullableEliminado.append(False)
                    #Eliminamos el nullable
                    self.nullableEliminado.pop(-2)
                    self.nullableEliminado.pop(-2)

                    #Agregamos el firstPos
                    if nodo1:
                        first = self.firstPosEliminado[-2] + self.firstPosEliminado[-1]
                        first.sort()
                        self.firstPos.append(first)
                        self.firstPosEliminado.append(first)
                        #Eliminamos el firstPos
                        self.firstPosEliminado.pop(-2)
                        self.firstPosEliminado.pop(-2)
                    else:
                        first = self.firstPosEliminado[-2]
                        self.firstPos.append(first)
                        self.firstPosEliminado.append(first)
                        #Eliminamos el firstPos
                        self.firstPosEliminado.pop(-2)
                        self.firstPosEliminado.pop(-2)
                    #Agregamos el lastpos
                    if nodo2:
                        last = self.lastPosEliminado[-2] + self.lastPosEliminado[-1]
                        last.sort()
                        self.lastPos.append(last)
                        self.lastPosEliminado.append(last)
                        #Eliminamos el lastpos
                        self.lastPosEliminado.pop(-2)
                        self.lastPosEliminado.pop(-2)
                    else:
                        last = self.lastPosEliminado[-1]
                        self.lastPos.append(last)
                        self.lastPosEliminado.append(last)
                        #Eliminamos el lastpos
                        self.lastPosEliminado.pop(-2)
                        self.lastPosEliminado.pop(-2)

                elif node == '?':
                    #Revisamos el nullable, firstPos y lastPos
                    self.nullable.append(True)
                    self.firstPos.append(self.firstPosEliminado[-1])
                    self.lastPos.append(self.lastPosEliminado[-1])

                    self.nullableEliminado.append(True)
                    self.firstPosEliminado.append(self.firstPosEliminado[-1])
                    self.lastPosEliminado.append(self.lastPosEliminado[-1])

                    #Eliminamos el nullable, firstPos y lastPos
                    self.nullableEliminado.pop(-2)
                    self.firstPosEliminado.pop(-2)
                    self.lastPosEliminado.pop(-2)

                elif node == '+':
                    #Revisamos si es nullable
                    nodo1 = self.nullableEliminado[-1]
                    if nodo1:
                        self.nullable.append(True)
                        self.nullableEliminado.append(True)
                    else:
                        self.nullable.append(False)
                        self.nullableEliminado.append(False)
                    #Eliminamos el nullable
                    self.nullableEliminado.pop(-2)

                    #Insertamos el firstPos y lastPos
                    self.firstPos.append(self.firstPosEliminado[-1])
                    self.lastPos.append(self.lastPosEliminado[-1])

                    self.firstPosEliminado.append(self.firstPosEliminado[-1])
                    self.lastPosEliminado.append(self.lastPosEliminado[-1])

                    #Eliminamos el firstPos y lastPos
                    self.firstPosEliminado.pop(-2)
                    self.lastPosEliminado.pop(-2)

                elif node == 'ε':
                    #Revisamos nullable, firstPos y lastPos
                    self.nullable.append(True)
                    self.firstPos.append([])
                    self.lastPos.append([])

                    self.nullableEliminado.append(True)
                    self.firstPosEliminado.append([])
                    self.lastPosEliminado.append([])
            else:
                self.nullable.append(False)
                self.firstPos.append([node])
                self.lastPos.append([node])

                self.nullableEliminado.append(False)
                self.firstPosEliminado.append([node])
                self.lastPosEliminado.append([node])
    #Followpos    
    def followpos(self):
        self.firstPosEliminado = []
        self.lastPosEliminado = []
        #Buscamos los tokens
        for valores in range(len(self.postfixNuevo)):
            if str(self.postfixNuevo[valores]) not in "*?•+|":
                self.followPos.append([self.postfixNuevo[valores]])
        #Evaluamos los tokens especiales
        for valores in range(len(self.postfixNuevo)):
            nodoss = []
            agregarNodos = []

            if self.postfixNuevo[valores] == "*":
                nodoss.extend(self.lastPosEliminado[-1])
                agregarNodos.extend(self.firstPosEliminado[-1])

                for nod in range(len(self.followPos)):
                    if self.followPos[nod][0] in nodoss:
                        if len(self.followPos[nod]) > 1:
                            for x in agregarNodos:
                                if x not in self.followPos[nod][1]:
                                    self.followPos[nod][1].append(x)
                            self.followPos[nod][1].sort()
                        else:
                            self.followPos[nod].append(agregarNodos)

                self.firstPosEliminado.append(self.firstPos[valores])
                self.lastPosEliminado.append(self.lastPos[valores])

                self.lastPosEliminado.pop(-2)
                self.firstPosEliminado.pop(-2)

            elif self.postfixNuevo[valores] == "+":
                nodoss.extend(self.lastPosEliminado[-1])
                agregarNodos.extend(self.firstPosEliminado[-1])

                for nod in range(len(self.followPos)):
                    if self.followPos[nod][0] in nodoss:
                        if len(self.followPos[nod]) > 1:
                            for x in agregarNodos:
                                if x not in self.followPos[nod][1]:
                                    self.followPos[nod][1].append(x)
                            self.followPos[nod][1].sort()
                        else:
                            self.followPos[nod].append(agregarNodos)

                self.firstPosEliminado.append(self.firstPos[valores])
                self.lastPosEliminado.append(self.lastPos[valores])

                self.lastPosEliminado.pop(-2)
                self.firstPosEliminado.pop(-2)

            elif self.postfixNuevo[valores] == "•":
                nodo1 = self.lastPosEliminado[-2]
                nodo2 = self.firstPosEliminado[-1]
                nodoss.extend(nodo1)
                agregarNodos.extend(nodo2)

                for nod in range(len(self.followPos)):
                    if self.followPos[nod][0] in nodoss:
                        if len(self.followPos[nod]) > 1:
                            for x in agregarNodos:
                                if x not in self.followPos[nod][1]:
                                    self.followPos[nod][1].append(x)
                            self.followPos[nod][1].sort()
                        else:
                            self.followPos[nod].append(agregarNodos)

                self.firstPosEliminado.append(self.firstPos[valores])
                self.lastPosEliminado.append(self.lastPos[valores])

                self.firstPosEliminado.pop(-2)
                self.firstPosEliminado.pop(-2)

                self.lastPosEliminado.pop(-2)
                self.lastPosEliminado.pop(-2)

            elif self.postfixNuevo[valores] == '|':
                self.firstPosEliminado.append(self.firstPos[valores])
                self.lastPosEliminado.append(self.lastPos[valores])

                self.firstPosEliminado.pop(-2)
                self.firstPosEliminado.pop(-2)

                self.lastPosEliminado.pop(-2)
                self.lastPosEliminado.pop(-2)

            elif self.postfixNuevo[valores] == '?':
                self.firstPosEliminado.append(self.firstPos[valores])
                self.lastPosEliminado.append(self.lastPos[valores])

                self.firstPosEliminado.pop(-2)
                self.lastPosEliminado.pop(-2)

            elif "#" in str(self.postfixNuevo[valores]):
                print(self.postfixNuevo[valores])

            else:
                self.firstPosEliminado.append(self.firstPos[valores])
                self.lastPosEliminado.append(self.lastPos[valores])

        self.followPos[-1].append(["∅"])

        for lar in range(len(self.followPos)):
            for value in range(len(self.postfixNuevo)):
                if self.followPos[lar][0] == self.postfixNuevo[value]:
                    if "#" in self.postfix[value]:
                        self.followPos[lar][1] = ["∅"]
    #AFD Directo
    def Dstate(self):
        sNode = self.firstPos[len(self.firstPos)-1]
        
        final = []
        for x in self.followPos:
            if "∅" in x[1]:
                final.append(x[0])

        #Lista de nodos
        P0 = []
        P0.append(sNode)
        self.variables = []
        for x in self.postfix:
            if x not in "|•*+?":
                if "#" not in x:
                    if x not in self.variables:
                        self.variables.append(x)
        
        tabla = []
        for x in P0:                

            conjuntos = []
            conjuntos.append(x)
            for alfa in self.variables:  
                movimiento = []
                movimiento.append(alfa)
                grupo = []
                for y in x: 

                    for l in range(len(self.postfix)):
                        if self.postfixNuevo[l] == y and self.postfix[l] == alfa:
                            for w in self.followPos:
                                if w[0] == y:
                                    for z in w[1]:
                                        if z not in grupo:
                                            grupo.append(z)
                grupo.sort()

                if grupo not in P0 and len(grupo) != 0:
                    P0.append(grupo)
                if len(grupo) != 0:
                    movimiento.append(grupo)
                    conjuntos.append(movimiento)

                if conjuntos not in tabla:
                    tabla.append(conjuntos)

        for sub_array in tabla:
            if len(sub_array) > 1:
                for i in range(1,len(sub_array)):

                    new_element = [sub_array[0], sub_array[i][0], sub_array[i][1]]
                    self.listaNueva.append(new_element)
            else:
                self.listaNueva.append(sub_array)

        
        #Convertimos la lista en Mayusculas
        q = list(string.ascii_uppercase)

        node = []
        alfanode = []
        for x in self.listaNueva:
            if x[0] not in node:
                node.append(x[0])
                alfanode.append(q.pop(0))

        
        for x in self.listaNueva:

            if len(x) > 1:
                for y in range(len(node)):

                    if x[0] == node[y]:
                        x[0] = alfanode[y]
                    if x[2] == node[y]:
                        x[2] = alfanode[y]
            else:
                for y in range(len(node)):

                    if x[0] == node[y]:
                        x[0] = "vacio"
        
        self.listaNueva = [sublista for sublista in self.listaNueva if 'vacio' not in sublista]
        
        
        start = []
        end = []
        endHash = []

        for ele in range(len(node)):
            if node[ele] == sNode:
                start.extend(alfanode[ele])
            for f in final:
                if f in node[ele]:
                    end.extend(alfanode[ele])
                    for val in range(len(self.postfixNuevo)):
                        if f == self.postfixNuevo[val]:
                            endHash.append(self.postfix[val])

        if len(node) == 1:
            end.extend(alfanode[0])
        
        sfPoint=[]
        sfPoint.append(start)
        sfPoint.append(end)  
        sfPoint.append(endHash)
            
        
        return [self.listaNueva, sfPoint]