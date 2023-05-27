class Lexer(object):
    #Iniciamos el constructor
    def __init__(self, file):
        self.file = file
    
    #Leemos el archivo 
    def leerYalex(self):
        with open(self.file, 'r') as file:
            yalexLines = file.read()

        #Listas para guardar tokens 
        activo = False
        funcion = []
        regex = []
        palabra = ""

        #Vamos linea a linea 
        for linea in yalexLines:
            if activo:
                #Checamos que sea un |
                if linea == "|":
                    if regex[len(regex)-1] == "|":
                        palabra += linea
                        pass
                    else:
                        if palabra != "":
                            palabra=""
                        regex.append(linea.strip())
                else:
                    #Checamos que sea un espacio
                    if linea not in ["\n",'\t'] : 
                        palabra += linea
                        if "{" in palabra and "}" in palabra:
                            palabra = palabra.strip()
                            regex.append(palabra)
                            palabra = ""
                        if "(*" in palabra and "*)" in palabra:
                            palabra = ""
                    elif linea == "\n":
                        if palabra:
                            if "{" not in palabra:
                                palabra = palabra.strip()
                                if palabra != "":
                                    regex.append(palabra)
                        palabra+=" "
            else:
                palabra+=linea
                #Buscamos "let" y "rule"
                if '\n' in palabra:
                    if len(palabra) > 0:
                        if "let" in palabra:
                            palabra = palabra.strip()
                            palabra = palabra[3:].strip()
                            funcion.append(palabra)
                        if "rule" in palabra: 
                            activo = True
                        palabra = ""

        regex = list(filter(bool, regex))

        #Listas para guardar tokens        
        regexFiltrado = []
        regexTokens = []
        funTokens = []
        for x in range(len(regex)):
            listaTemporal = []
            palabraTemporal = ""
            tokenActivo = False
            #Vamos leyendo linea a linea y reemplazando comillas entre las llaves
            for linea in regex[x]:
                if tokenActivo:
                    if linea == "}":
                        palabraTemporal = palabraTemporal.replace("'","").replace('"',"").strip()
                        listaTemporal.append(palabraTemporal)
                        regexTokens.append(listaTemporal[0])
                        regexTokens.append("|")
                        palabraTemporal = ""
                        funTokens.append(listaTemporal)
                        break
                    palabraTemporal += linea
                else:
                    palabraTemporal += linea
                if linea == "{":
                    palabraTemporal = palabraTemporal[:-1].replace("'","").replace('"',"").strip()
                    listaTemporal.append(palabraTemporal)
                    palabraTemporal = ""
                    tokenActivo = True
             #Vamos leyendo linea a linea y reemplazando comillas entre |
            if palabraTemporal and "|" not in palabraTemporal and len(palabraTemporal) > 0:
                palabraTemporal = palabraTemporal.strip()
                listaTemporal.append(palabraTemporal)
                listaTemporal.append("")
                regexTokens.append(listaTemporal[0])
                regexTokens.append("|")
                funTokens.append(listaTemporal)

        regexTokens.pop()

        funFiltrados = []
        #Se realiza el proceso para obtener el token temporal 
        for x in range(len(regex)):
            palabraTemporal = ""
            for l in regex[x]:
                palabraTemporal += l
                if "{" in palabraTemporal:
                    palabraTemporal = palabraTemporal[:-1].strip()
                    break 
                if "(*" in palabraTemporal :
                    if palabraTemporal[0] == "(":
                        palabraTemporal = palabraTemporal[:-2].strip()
                        break 
            if palabraTemporal.count("'") == 2 or palabraTemporal.count('"') == 2:
                palabraTemporal = palabraTemporal[1:-1]

            regex[x] = palabraTemporal
        
        for x in regex:
            if len(x) != 0:
                if x.count('"') == 2:
                    x = x[1:-1]
                regexFiltrado.append(x)

        #Asigamos los tokens a eliminar y otris a una lista temporal
        for f in funcion:
            listaEliminar = []
            listaTemporal = []
            nombre, definicion = f.split("=")

            nombre = nombre.strip()
            definicion = definicion.strip()
            listaTemporal.append(nombre)
            palabra= ""

            if definicion[0] == "[":
                definicion = definicion[1:-1]
                for x in definicion:
                    palabra+=x
                    if palabra[0] == '"' or palabra[0] == "'":
                        if palabra.count("'") == 2:
                            palabra = palabra[1:-1]
                            if len(palabra) == 2:
                                if palabra == "\s":
                                    palabra = bytes(' ', 'utf-8').decode('unicode_escape')
                                else:
                                    palabra = bytes(palabra, 'utf-8').decode('unicode_escape')
                                listaEliminar.append(ord(palabra))
                            else:
                                if palabra == " ":
                                    palabra = bytes(' ', 'utf-8').decode('unicode_escape')
                                    listaEliminar.append(ord(palabra))
                                else:
                                    listaEliminar.append(ord(palabra))
                            palabra = ""
                        if palabra.count('"') == 2:
                            palabra = palabra[1:-1]
                            palabraTemporal = ""
                            if chr(92) in palabra:
                                for y in palabra:
                                    palabraTemporal+=y
                                    if palabraTemporal.count(chr(92)) == 2:
                                        if palabraTemporal[:-1] == "\s":
                                            tempPalabra = ' '
                                        else:
                                            tempPalabra = palabraTemporal[:-1]
                                        
                                        palabra = bytes(tempPalabra, 'utf-8').decode('unicode_escape')
                                        listaEliminar.append(ord(palabra))
                                        palabraTemporal = palabraTemporal[2:]
                                if len(palabraTemporal) != 0:
                                    if palabraTemporal == "\s":
                                        tempPalabra = ' '
                                    else:
                                        tempPalabra = palabraTemporal
  
                                    palabra = bytes(tempPalabra, 'utf-8').decode('unicode_escape')
                                    listaEliminar.append(ord(palabra))
                            else:
                                palabra = list(palabra)
                                for w in range(len(palabra)):
                                    palabra[w] = ord(palabra[w])
                                listaEliminar.extend(palabra)
                                
                    else:
                        listaEliminar.append(palabra)
                        palabra = ""
            
            #Buscamos los tokens actuales 
            else:
                tokens = []
                tokenActual = ""
                
                for caracter in definicion:
                    
                    if "]" in tokenActual:
                        palabra = ""
                        array = []
                        array.append("(")
                        
                        tokenActual = tokenActual[1:-1]
                        for tok in tokenActual:
                            palabra += tok
                            if palabra.count("'") == 2:
                                palabra = ord(palabra[1:-1])
                                array.append(palabra)
                                array.append("|")
                                palabra = ""
                        array[len(array)-1] = ")"
                        tokens.extend(array)
                        tokenActual = ""
                    
                    if tokenActual.count("'") == 2:
                        if "[" not in tokenActual:
                            tokenActual = ord(tokenActual[1:-1])
                            tokens.append(tokenActual)
                            tokenActual = ""
                    #Buscamos los tokens especiales
                    if caracter in ("(", ")", "*", "?", "+", "|","."):
                        if "'" not in tokenActual:
                            if tokenActual:
                                if len(tokenActual) == 1:
                                    tokenActual = ord(tokenActual)
                                tokens.append(tokenActual)
                                tokenActual = ""
                            if caracter == ".":
                                caracter = ord(caracter)
                            tokens.append(caracter)
                        else:
                            tokenActual += caracter.strip()
                    else:
                        tokenActual += caracter.strip()
                if tokenActual:
                    tokens.append(tokenActual)
                listaEliminar.extend(tokens)
                
                
            listaTemporal.append(listaEliminar)
        
            funFiltrados.append(listaTemporal)

        for x in range(len(funFiltrados)):
            funcional = True
            
            for c in ["+","*","(",")","?","|"]:
                if c in funFiltrados[x][1]:
                    funcional = False
                
            
            if funcional == False:
                #Creamos una lista temporal de los tokens especiales
                listaTemporal = []
                for y in funFiltrados[x][1]:
                    listaTemporal.append(y)
                    listaTemporal.append("•")
                for z in range(len(listaTemporal)):
                    if listaTemporal[z] == "(":
                        if listaTemporal[z+1] == "•":
                            listaTemporal[z+1] = ''
                    if listaTemporal[z] == ")":
                        if listaTemporal[z-1] == "•":
                            listaTemporal[z-1] = ''
                    if listaTemporal[z] == "*":
                        if listaTemporal[z-1] == "•":
                            listaTemporal[z-1] = ''
                    if listaTemporal[z] == "|":
                        if listaTemporal[z-1] == "•":
                            listaTemporal[z-1] = ''
                        if listaTemporal[z+1] == "•":
                            listaTemporal[z+1] = ''
                    if listaTemporal[z] == "+":
                        if listaTemporal[z-1] == "•":
                            listaTemporal[z-1] = ''
                    if listaTemporal[z] == "?":
                        if listaTemporal[z-1] == "•":
                            listaTemporal[z-1] = ''
                listaTemporal = [element for element in listaTemporal if element != '']
                            
                funFiltrados[x][1] = listaTemporal[:-1]
            #Por si tenemos tokens ascii
            else:
                listaAscii=[]
                listaString = []
                if '-' in funFiltrados[x][1]:
                    for z in range(len(funFiltrados[x][1])):
                        if funFiltrados[x][1][z] == '-':
                            for i in range(funFiltrados[x][1][z-1],funFiltrados[x][1][z+1]+1):
                                listaAscii.append(i)
                    for i in listaAscii:
                        listaString.append(i)
                    funFiltrados[x][1] = listaString

                listaString = []
                for y in funFiltrados[x][1]:
                    listaString.append(y)
                    listaString.append('|')
                    
                listaString = listaString[:-1]
                funFiltrados[x][1] = listaString
                
        for func in funFiltrados:
            func[1].insert(0,"(")
            func[1].insert(len(func[1]),")")

        listaFunciones = []

        for x in funFiltrados:
            listaFunciones.append(x[0])
        listaFunciones.append('|')

        for x in range(len(regexFiltrado)):
            if regexFiltrado[x] not in listaFunciones:
                if len(regexFiltrado[x]) == 1:
                    regexFiltrado[x] = ord(regexFiltrado[x])
            if regexFiltrado[x] == "|" and regexFiltrado[x-1] == "|":
                regexFiltrado[x] = ord(regexFiltrado[x])
                
        #Le agregamos temporalmente los tokens especiales al regex
        regexTemporal = []
        for x in range(len(regexFiltrado)):
            if regexFiltrado[x] != "|":
                regexTemporal.append("(")
                regexTemporal.append(regexFiltrado[x])
                regexTemporal.append("•")
                regexTemporal.append("#"+str(regexTokens[x]))
                regexTemporal.append(")")
            else:
                regexTemporal.append(regexFiltrado[x])
        
        regexFiltrado = regexTemporal

        regexFinal = []
        
        for token in regexFiltrado:
            exists = False
            for f in funFiltrados:
                if token == f[0]:
                    exists = True
                    temporalRegex = []
                    temporalRegex.extend(f[1])
                    length = 0
                    while (length != len(temporalRegex)):
                                    
                        length = len(temporalRegex)
                        i = 0
                        revisionRegex = []
                        while (i < len(temporalRegex)):
                            validation = False
                            for x in funFiltrados:
                                if temporalRegex[i] == x[0]:
                                    validation = True
                                    revisionRegex.extend(x[1])
                                    revisionRegex.extend(temporalRegex[i+1:])
                                    temporalRegex = revisionRegex
                                    i = len(temporalRegex)
                                    revisionRegex = []
                                    break

                            if validation == False:
                                revisionRegex.append(temporalRegex[i])
                                i+=1
                            
                    regexFinal.extend(temporalRegex)
                    
            if exists == False:
                if isinstance(token, str):
                    if len(token) > 1:
                        if '#' not in token:

                            temporal = []
                            temporal.append("(")
                            for i in token:
                                temporal.append(ord(i))
                                temporal.append("•")
                            temporal.pop(len(temporal)-1)
                            temporal.append(")")

                            regexFinal.extend(temporal)
                        else:
                            regexFinal.append(token)
                    else:
                        regexFinal.append(token)
                else:
                    regexFinal.append(token)

        return regexFinal,funTokens
    
class Simulacion:
    def __init__(self, afd, sfPoint, prueba):
        self.afd = afd
        self.inicio = sfPoint[0]
        self.fin = sfPoint[1]
        self.tokens = sfPoint[2]
        self.prueba = prueba
        self.resultado = []
        
    def simular(self):
        texto = ""
        posicion = self.inicio[0]
        for token in self.prueba:
            for lex in token:
                listo = False
                existe = True
                valor = ord(lex)
                while not (listo):
                    
                    for pos in self.afd:
                        if pos[0] == posicion and pos[1] == str(valor):
                            texto += chr(valor)
                            posicion = pos[2]
                            existe = False
                            listo = True
                            break
                
                    if existe:
                        if posicion == self.inicio[0]:
                            self.resultado.append(["lexical error", lex])
                            texto = ""
                            listo = True

                        else:
                            
                            indice = self.fin.index(posicion)
                            self.resultado.append([self.tokens[indice].replace("#",""), texto])
                            texto = ""
                            posicion = self.inicio[0]

        if texto:
            if posicion == self.inicio[0]:
                self.resultado.append(["lexical error", texto])
                texto = ""
            else:
                indice = self.fin.index(posicion)
                self.resultado.append([self.tokens[indice].replace("#",""), texto])
                texto = ""
                position = self.inicio[0]
            
                        
        return self.resultado