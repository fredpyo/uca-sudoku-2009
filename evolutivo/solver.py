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
from subprocess import Popen

from src.sudoku import CromosomaSudoku

PUZZLES_FILE = "puzzles.txt" # archivo con los puzzless
ITERACION_TOPE = 100
POBLACION = 44


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
    cromosoma = CromosomaSudoku(puzzle, 0, reemplazables, ['1','2','3','4','5','6','7','8','9'])

    f = open("salida.csv", 'w')
    f.write("Iteracion;%s;Mejor Generacion\n" % ";".join([str(x+1) for x in range(POBLACION)]))

    pop = cromosoma.generar_poblacion_inicial(POBLACION)
    pop.sort(cmp=lambda x,y: cmp(x.aptitud(), y.aptitud()))
    iteracion = 0
    f.write("%d;%s;%d\n" % (iteracion, ";".join([str(x.aptitud()) for x in pop]), pop[0].generacion))
    while (pop[0] != 0 and iteracion <= ITERACION_TOPE):
        print "Generacion", iteracion
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
        f.write("%d;%s;%d\n" % (iteracion, ";".join([str(x.aptitud()) for x in pop]), pop[0].generacion))
        
    f.close()

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
