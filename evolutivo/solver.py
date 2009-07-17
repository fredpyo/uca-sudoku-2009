# -*- encoding: utf-8 -*-
'''
Sudoku Solver
Resolvedor de Sudoku mediante el uso de Algoritmos Evolutivos
Autores:
    Sergio Stanichevsky
    Federico Caceres
    Sergio Gonzalez
Materia: Informatica 2
Universidad Catolica "Nuestra Señora de la Asunción
'''

import re
import os
import sys
import os.path
from time import time

from src.sudoku import CromosomaSudoku

PUZZLES_FILE = "puzzles.txt" # archivo con los puzzless
ITERACION_TOPE = 100
POBLACION = 44
CRUZAMIENTO = 1


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


def solve(n):
    '''Instancia la clase Sudoku, busca el puzzle deseado y se lo pasa a la clase'''
    print "Cargando puzzle %d..." % n
    puzzle = load_puzzle(n)
    reemplazables = []
    for i in xrange(len(puzzle)):
        if puzzle[i] == '':
            reemplazables.append(i)
    cromosoma = CromosomaSudoku(puzzle, 0, reemplazables, ['1','2','3','4','5','6','7','8','9'],CRUZAMIENTO)

    pop = cromosoma.generar_poblacion_inicial(POBLACION)
    pop.sort(cmp=lambda x,y: cmp(x.aptitud(), y.aptitud()))
    iteracion = 1
    print "Generacion;poblacion...;mejor generacion"
    print "%d;%s;%d" % (iteracion, ";".join([str(x.aptitud()) for x in pop]), pop[0].generacion)
    while (pop[0].aptitud() != 0 and iteracion <= ITERACION_TOPE):
        CromosomaSudoku.generaciones = iteracion
        nueva_poblacion = []
        for c in xrange(0,POBLACION/2,2):
            nuevos = pop[c].cruzar(pop[c+1])
            nuevos[0].mutar_genes()
            nuevos[1].mutar_genes()
            nueva_poblacion.append(nuevos[0])
            nueva_poblacion.append(nuevos[1])
        nueva_poblacion.extend(pop[0:POBLACION/2])
        pop = nueva_poblacion
        pop.sort(cmp=lambda x,y: cmp(x.aptitud(), y.aptitud()))
        iteracion += 1
        print "%d;%s;%d" % (iteracion, ";".join([str(x.aptitud()) for x in pop]), pop[0].generacion)
        
    if pop[0].aptitud() == 0:
        print "SOLUCION:"
        print pop[0].generacion
        print pop[0].tablero()

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
            print '\t' + a + ' [puzzle] [poblacion [generaciones [tipo_cruzamiento]]]: Resolver un puzzle'
            print
            print '  puzzle: un valor del 1 al 100 donde las dificultades son las siguientes'
            print '    1 al 20   muy facil'
            print '    21 al 40  facil'
            print '    41 al 60  medio'
            print '    61 al 80  dificil'
            print '    80 al 100  muy dificil'
            print '  poblacion: numero entero con la poblacion a generar'
            print '  generaciones: numero entero con la cantidad de generaciones a cruzar'
            print '  tipo_cruzamiento: uno de los siguientes valores'
            print '    aleatorio: selecciona los genes a cruzarse al azar'
            print '    corte: parte cada cromosoma al azar (dos grupos de genes)'
            print '    fila:  cruza las filas dejandolas intactas'
        else:
            # puzzle
            try:
                n = int(args[1])
            except:
                exit("Especifico un numero de puzzle incorrecto, no se pudo interpretar como numero")

            # poblacion
            try:
                POBLACION = int(args[2])
            except ValueError:
                exit("%s no es un valor valido para la poblacion" % args[2])
            except:
                pass
            
            # iteraciones
            try:
                ITERACION_TOPE = int(args[3])
            except ValueError:
                exit("%s no es un valor valido para la cantidad de iteraciones" % args[3])
            except:
                pass
            
            # cruzamiento
            try:
                if args[4] == 'aleatorio':
                    CRUZAMIENTO = 1
                elif args[4] == 'corte':
                    CRUZAMIENTO = 2
                elif args[4] == 'fila':
                    CRUZAMIENTO = 3
                print args[4]
                    
                ITERACION_TOP = int(args[3])
            except:
                pass
            
            if 1 <= n <= 100:
                solve(n)
            else:
                exit("El numero esta fuera de rango, elija uno entre 1 y 100")
