import re
from Regex import *
from lexer import *
from arbol import * 
from afd import *
from yapar import *
from tabla import *
from lector import *
#Leemos el .yal y .yalp 
yalFile = "slr-1.yal"
yalpFile = "slr-1.yalp"

#Abrimos el yalp 
with open(yalpFile) as y:
    yalpLines = y.read()

#Identificamos los tokens que se van a tomar en cuenta 
    tokens = re.findall(r'(?<=\n)%token\s+[^%\s][^\n]*', yalpLines)
    tokenID = re.findall(r'(?<=\n)%token\s+[^%\s][^\n]*', yalpLines)
    print("Tokens a utilizar: ", tokens)
    print("-------------------------------------------------------")
    #Buscamos errores en los comentarios.
    if yalpLines.count("/*") != yalpLines.count("*/"):
        for i in range(len(yalpLines)):
            if yalpLines[i] == "/" and yalpLines[i+1] == "*":
                print("ERROR: Esta mal comentado" + str(i+1) + ".")
                break
    
    #Buscamos errores de puntuación : y ;  
    if yalpLines.count(";") != yalpLines.count(":"):
        print("ERROR: La cantidad de : y ; no es correcta")

    for token in tokens:
        nombreTokens = token.split()[1]
        tkn = token.split()[0]

        #Guardamos los tokens en una lista
        yalpTokens = [] 
        yalpTokens.append(nombreTokens)


    #Creamos una lista de tokens aprobados
    tokensValidos = ["%token"]

    for token in tokenID:
        lineToken = token.split()
        tkn = lineToken[0]
        if not tkn.startswith("%") or (tkn not in tokensValidos and len(lineToken) < 3):
            print(f"El token {' '.join(lineToken[1:])} no es válido.")
        else:
            for nombreTokens in lineToken[1:]:
                print(f"El token {nombreTokens} es válido.")
            yalpTokens.append(nombreTokens)

    print("-------------------------------------------------------")
    yalpTokens = list(dict.fromkeys(yalpTokens))
    tokensYalp = re.findall(r'(?<=\n)token\s+[^\s][^\n]*', yalpLines)
    
    #Errores en la redaccion de los %tokens
    if len(tokensYalp) > 0:
        for i in range(len(tokensYalp)):
            print("Token con error de redacción: ", tokensYalp[i])

    print("-------------------------------------------------------")
    #Buscamos los tokens que se ignoran 
    for line in yalpLines.split('\n'):
            if "IGNORE" in line:
                ignoreLista = line[line.find("IGNORE")+6:].strip()
                tokensIgnorados = [tok.strip() for tok in ignoreLista.split(' ')]
                break
                
    print("Tokens a ignorar: ", tokensIgnorados)
    print("-------------------------------------------------------")
    #Creamos una lista para guardar los tokens
    yalTokens =[]

    #Abrimos el yal
    with open(yalFile) as y:
        yalLines = y.read()

        #Buscamos los "rule tokens"
        if "rule tokens =" in yalLines:
            tokensCadena = yalLines[yalLines.find("rule tokens ="):]
            tokensLista = tokensCadena.split("|")
            #Los metemos a un diccionario
            tokensDic = {}
            for token in tokensLista:
                nombre, valor = token.split("return")
                tokensDic[nombre.strip()] = valor.strip().strip("\"")

            for key, value in tokensDic.items():
              pass

            for key, value in tokensDic.items():
                valorToken = value.strip()
                #Limpiamos los tokens
                valorToken = valorToken.replace("{", "").replace("}", "")
                valorToken = valorToken.split("(")[0].strip()
                yalTokens.append(valorToken.strip())

    #Verificamos que los tokens de yal, esten en yalp 
    for token in yalpTokens:
        if token not in yalTokens:
            print("ERROR: El token " + token + "NO se encuentra en el archivo .yal")
        else: 
            print("El token " + token + " se encuentra en el archivo .yal")
print("-------------------------------------------------------")


yalp = "analizadorYalp.yal"


regex, tokens = Lexer(yalp).leerYalex()
post = Regex(regex)
postfix = post.convertir_postfix()
arbol = Arbol(yalp)
arbol.arbol(postfix)
resultado = arbol.izquierda()
afd = AFD(resultado)
directo = afd.Dstate()

simulacion = Simulacion(directo[0], directo[1], yalpLines)
sim = simulacion.simular()

yalp = Yalp(yalFile, sim)
yalp.yapar()
yalp.construccion()

parse = Tabla(yalp.transiciones, yalp.subsets, yalp.numeroSubsets, yalp.subproducciones)
parse.tabla()
parse.dibujoTabla()  

yal = "slr-1.yal"
regex, token_functions = Lexer(yal).leerYalex()
post = Regex(regex)
postfix = post.convertir_postfix()
tree = Arbol(yal)
tree.arbol(postfix)
result = tree.izquierda()

dfa = AFD(result)
direct= dfa.Dstate()

#Leemos el archivo 
test = "slr-1.1.yal.run"
with open(test) as f:
    test = f.readlines()

#Creamos la simulación 
simulation = Simulacion(direct[0], direct[1], test)
sim = simulation.simular()
#Creamos el archivo 
python_file = Lector(tokens)
python_file.create_python()

#Observamos la simulacion de tokens
print(f"simulacion: {sim}")

#Usamos nuestro archivo implementado 
from implementacion import *
#Abrimos y creamos un texto en donde se ven los tokens
with open("tokensText.txt", "w") as f:
    for s in sim:
        scanner = scan(s[0])
        f.write(f"{s}:{scanner}\n")