import re

#Leemos el .yal y .yalp 
yalFile = "slr-1.yal"
yalpFile = "slr-1.yalp"

#Abrimos el yalp 
with open(yalpFile) as y:
    yalpLines = y.read()

#Identificamos los tokens que se van a tomar en cuenta 
    tokens = re.findall(r'(?<=\n)%token\s+[^%\s][^\n]*', yalpLines)
    print("Tokens a utilizar: ", tokens)

    #Buscamos errores en los comentarios.
    if yalpLines.count("/*") != yalpLines.count("*/"):
        for i in range(len(yalpLines)):
            if yalpLines[i] == "/" and yalpLines[i+1] == "*":
                print("ERROR: Esta mal comentado" + str(i+1) + ".")
                break
    
    #Buscamos errores de puntuación : y ;  
    if yalpLines.count(";") != yalpLines.count(":"):
        print("ERROR: La cantidad de : y ; no es correcta")

