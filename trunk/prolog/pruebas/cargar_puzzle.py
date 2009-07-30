# -*- coding: utf-8 -*-
import re
import os
import sys
import os.path

PUZZLES_FILE = "puzzles.txt"
TRACKS_FILE = "pistas.pl" # grande Fede

def load_puzzle(n):
    '''Lee el puzzle n del archivo de puzzles'''
    try:
        f = open(PUZZLES_FILE, 'r')
        buff = []
        found = False
        for l in f:
            match = re.match("^(\d+)-", l)
            if match and found and int(match.group(1)) != n:
                break
            if found:
                buff.append(l.strip())
            if match and not found and int(match.group(1)) == n:
                found = True
        f.close()
        values = "".join(buff).replace("_","").replace(";","").split(",")
        return values
    except Exception, e:
        exit("Error al intentar parsear el archivo de puzzles: %s" % e)	

# bootstrap
if __name__ == '__main__':
    args = sys.argv
    a = os.path.basename(sys.argv[0])
    PATH = os.path.dirname(sys.argv[0]).decode(sys.getfilesystemencoding())
    
    if len(args) == 1:
        exit('Debe indicar un parametro para correr.\nEjecute "' + a + ' --help" para mas ayuda')
        
    else:
        # puzzle
        try:
            n = int(args[1])
        except:
            exit("Especifico un numero de puzzle incorrecto, no se pudo interpretar como numero")

    try: # mira que robo :D
        f = open(TRACKS_FILE, 'w')
    except Exception, e:
        exit("Error al intentar abrir el archivo de pistas: %s" % e)	

    puzzle = load_puzzle(n)
    # imprime puzzle(x,y,p) donde x=[1-9],y=[1-9],p=[1-9]
    x = 1
    y = 1
    for p in puzzle:
        if p: # no imprimir los espacios vacios
            f.write("pista(%d,%d,%s).\n" % (x, y, p))
        x = x + 1
        if x > 9:
            x = 1
            y = y + 1
