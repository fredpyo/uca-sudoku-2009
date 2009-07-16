#!/bin/python
# -*- encoding: utf-8 -*-
'''
Sudoku Solver
Resolvedor de Sudoku mediante el uso de CSP y Backtracking
Autores:
Sergio Stanichevsky
Federico Caceres
Materia:
Informatica 2
Universidad Catolica "Nuestra Señora de la Asunción
'''

import re
import os
import sys
import os.path
from time import time
from subprocess import Popen
import datetime

from sudoku import Sudoku, ORDEN_MENOR_CANTIDAD_DE_CONFLICTOS, ORDEN_MENOR_CANTIDAD_DE_OPCIONES, ORDEN_MAYOR_CANTIDAD_DE_OPCIONES, ORDEN_SECUENCIAL


PUZZLES_FILE = "puzzles.txt" # archivo con los puzzless
HARD_PUZZLES_FILE = "puzzles-hard.txt" # archivo con los puzzless
MODO_SILENCIOSO = False


def load_puzzle(n):
    '''Lee el puzzle n del archivo de puzzles'''
    if n > 100:
        return load_puzzle_hard(n)
    else:
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

def load_puzzle_hard(n):
    '''Lee el puzzle n del archivo de puzzles hadr top 95'''
    try:
        f = open(HARD_PUZZLES_FILE, 'r')
        lines = f.readlines()
        return lines[n-101]
        f.close()
    except Exception, e:
        exit("Error al intentar parsear el archivo de puzzles: %s" % e)

def solve(n):
    '''Instancia la clase Sudoku, busca el puzzle deseado y se lo pasa a la clase'''
    if not MODO_SILENCIOSO:
        print "Cargando puzzle %d..." % n
    puzzle = load_puzzle(n)
    sudo = Sudoku(puzzle)
    sudo.silencioso = MODO_SILENCIOSO
    sudo.order = ORDEN_SECUENCIAL
    if not MODO_SILENCIOSO:
        sudo.printb()
    inicio = datetime.datetime.now()
    sudo.constraint()
    resuelto = sudo.back_cp()
    transcurrido = datetime.datetime.now() - inicio
    if not MODO_SILENCIOSO:
        print "*"
        sudo.printb()
    if resuelto:
        if not MODO_SILENCIOSO:
            print "El tablero fue resuelto en %d pasos en %s segundos" % (sudo.attempts, transcurrido)
        else:
            print "%d - %d - %s" % (n, sudo.attempts, transcurrido)
    else:
        if not MODO_SILENCIOSO:
            print "El tablero no se pudo resolver"


# bloque principal de codigo
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
            print '    1 al 20   muy facil'
            print '    21 al 40  facil'
            print '    41 al 60  medio'
            print '    61 al 80  dificil'
            print '    80 al 100  muy dificil'
            print '    101 al 195  muy muy muy dificil\n'
        else:
            try:
                n = int(args[1])
            except:
                exit("Especifico un numero de puzzle incorrecto, no se pudo interpretar como numero")
            else:
                if 1 <= n <= 195:
                    if len(args) == 3 and args[2] == '--silent':
                        MODO_SILENCIOSO = True
                    solve(n)
                else:
                    exit("El numero esta fuera de rango, elija uno entre 1 y 100")
