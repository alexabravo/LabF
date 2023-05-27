#Declaramos la clase Nodo.
class Nodo(object):
    def __init__(self, hijo):
        self.hijo = hijo
        self.hijoI = None
        self.hijoD = None

#Declaramos la clase árbol 
class Arbol:
    #La inicializamos con su raiz y etiqueta
    def __init__(self, etiqueta):
        self.raiz = None
        self.etiqueta = etiqueta

    #Iniciamos la clase constructora del árbol
    def arbol(self, postfix):
        
        pila = []
        #Bucscamos los tokens especiales y los vamos acomodando al nodo 
        for caracter in postfix:
            if str(caracter) not in "|*•+?":
                if isinstance(caracter, int):
                    caracter = str(caracter)
                node = Nodo(caracter)
                pila.append(node)
            elif caracter == "|" or caracter == "•":
                node = Nodo(caracter)
                node.hijoD = pila.pop()
                node.hijoI = pila.pop()
                pila.append(node)
            elif caracter in ["*", "+", "?"]:
                node = Nodo(caracter)
                node.hijoI = pila.pop()
                pila.append(node)
        
        self.root = pila.pop()

    #Leemos y declaramos la parte izquierda del arbol  
    def izquierda(self):
        if self.root is None:
            return []

        pila = [self.root]
        resultado = []

        while pila:
            node = pila.pop(0)
            resultado.append(node.hijo)

            if node.hijoI:
                pila.insert(0, node.hijoI)
            if node.hijoD:
                pila.insert(0, node.hijoD)

        return list(reversed(resultado))

    #Recursividad en las ramas, con los nodos e hijos
    def rama(self, nodo, graph):
        if nodo is not None:
            graph.nodo(str(id(nodo)), str(nodo.hijo)) 
            
            if nodo.hijoI is not None:
                graph.ramas(str(id(nodo)), str(id(nodo.hijoI)))
                self.rama(nodo.hijoI, graph)
            
            if nodo.hijoD is not None:
                graph.ramas(str(id(nodo)), str(id(nodo.hijoD)))
                self.rama(nodo.hijoD, graph)
