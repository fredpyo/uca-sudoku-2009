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
import datetime

from sudoku import Sudoku
from sudoku import VAR_ORDER_MINIMUN_REMAINING_VALUES, VAR_ORDER_MAXIMUM_REMAINING_VALUES, VAR_ORDER_SECUENTIAL 
from sudoku import VAL_ORDER_LEAST_CONFLICTS, VAL_ORDER_MOST_CONFLICTS, VAL_ORDER_SECUENTIAL


PUZZLES_FILE = "puzzles.txt" # archivo con los puzzless
HARD_PUZZLES_FILE = "puzzles-hard.txt" # archivo con los puzzless
MODO_SILENCIOSO = False

VAR_ORDER = VAR_ORDER_SECUENTIAL
VAL_ORDER = VAL_ORDER_SECUENTIAL

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
    sudo.var_order = VAR_ORDER
    sudo.val_order = VAL_ORDER
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
            print '\t' + a + ' puzzle [opciones]: Resolver un puzzle'
            print
            print '  puzzle: un valor del 1 al 100 donde las dificultades son las siguientes'
            print '    1 al 20   muy facil'
            print '    21 al 40  facil'
            print '    41 al 60  medio'
            print '    61 al 80  dificil'
            print '    80 al 100  muy dificil'
            print '    101 al 195  muy muy muy dificil'
            print 
            print '  opciones:'
            print '    --silent:    Corre en modo silencioso, solo imprime un resumen del trabajo realizado,'
            print '                 si no se pasa este argumento se imprime el tablero antes y despues de la'
            print '                 ejecucion.'
            print '    --var-order criterio: Determina el orden por el cual se escogeran las variables (casillas).'
            print '                 Puede ser una de las siguientes:'
            print '                   secuencial: no ordena las casillas'
            print '                   minimo: elige primero las casillas con menor cantidad de valores restantes'
            print '                   maximo: elige primero las casilals con mayor cantidad de valores restantes'
            print '    --var-order criterio: Determina el orden por el cual se escogeran los valores.'
            print '                 Puede ser una de las siguientes:'
            print '                   secuencial: no ordena los valores'
            print '                   menos: elige primero los valores menos conflictivos'
            print '                   mas: elige primero los valores mas conflictivos'
                
        else:
            try:
                n = int(args[1])
            except:
                exit("Especifico un numero de puzzle incorrecto, no se pudo interpretar como numero")
            else:
                # argumentos adicionales
                if len(args) > 2:
                    next_is_varo = False
                    next_is_valo = False
                    for a in args[2:]:
                        if next_is_varo:
                            if a == 'secuencial':
                                VAR_ORDER = VAR_ORDER_SECUENTIAL
                            elif a == 'minimo':
                                VAR_ORDER = VAR_ORDER_MINIMUN_REMAINING_VALUES
                            elif a == 'maximo':
                                VAR_ORDER = VAR_ORDER_MAXIMUM_REMAINING_VALUES 
                            next_is_varo = False
                        elif next_is_valo:
                            if a == 'secuencial':
                                VAL_ORDER = VAL_ORDER_SECUENTIAL
                            elif a == 'menos':
                                VAL_ORDER = VAL_ORDER_LEAST_CONFLICTS
                            elif a == 'mas':
                                VAL_ORDER = VAL_ORDER_MOST_CONFLICTS
                            next_is_valo = False
                        elif a == '--silent':
                            MODO_SILENCIOSO = True
                        elif a == '--var-order' or a == '-varo':
                            next_is_varo = True
                        elif a == '--val-order' or a == '-valo':
                            next_is_valo = True
                        
                # ejecutar
                if 1 <= n <= 195:
                    solve(n)
                else:
                    exit("El numero esta fuera de rango, elija uno entre 1 y 100")
