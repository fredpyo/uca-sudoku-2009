# -*- encoding: utf-8 -*-
'''
Sudoku Solver
Resolvedor de Sudoku mediante el uso de Algoritmos Evolutivos
Autores:
    Sergio Stanichevsky
    Federico Caceres
    Sergio Gonzalez
Materia: Informatica 2
Universidad Catolica "Nuestra Se�ora de la Asunci�n
'''

import re
import os
import sys
import os.path
from time import time
from subprocess import Popen

from src.sudoku import SudokuEvo

PUZZLES_FILE = "puzzles.txt" # archivo con los puzzless


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
        values = "".join(buff).replace("_","").split(",")
        values.pop()
        return values
    except Exception, e:
        exit("Error al intentar parsear el archivo de puzzles: %s" % e)


def solve(n):
    '''Instancia la clase Sudoku, busca el puzzle deseado y se lo pasa a la clase'''
    print "Cargando puzzle %d..." % n
    puzzle = load_puzzle(n)

# bootstrap
if __name__ == '__main__':
    args = sys.argv
    a = os.path.basename(sys.argv[0])
    PATH = os.path.dirname(sys.argv[0]).decode(sys.getfilesystemencoding())
    
    if len(args) == 1:
        exit('Debe indicar un parametro para correr.\nEjecute "' + a + ' --help" para mas ayuda')
        
    else:
        if args[1] == '--help':
            print 'Modo de ejecucion:'
            print '\t' + a + ' --help:  Esta ayuda'
            print '\t' + a + ' [puzzle]: Resolver un puzzle'
            print
            print '  puzzle: un valor del 1 al 100 donde las dificultades son las siguientes'
            print '    1 al 20   muy facil\n'
            print '    21 al 40  facil\n'
            print '    41 al 60  medio\n'
            print '    61 al 80  dificil\n'
            print '    80 al 100  muy dificil\n'
        else:
            try:
                n = int(args[1])
            except:
                exit("Especifico un numero de puzzle incorrecto, no se pudo interpretar como numero")
            else:
                if 1 <= n <= 100:
                    solve(n)
                else:
                    exit("El numero esta fuera de rango, elija uno entre 1 y 100")
