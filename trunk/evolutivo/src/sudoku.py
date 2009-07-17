# -*- encoding: utf-8 -*-
'''
Implementacion de las clases para Algoritmos Evolutivos para resolver el problema Sudoku

@author: Federico Cáceres <fede.caceres@gmail.com>
'''

import random

from genetica import Cromosoma, convertir

class SudokuEvo(object):
    pass
    
class CromosomaSudoku(Cromosoma):
    """Implementacion del cromosoma especifico para el problema Sudoku"""
    
    def __init__(self, genes, generacion=0, genes_reemplazables=None, valores_para_los_genes=None, cruzamiento=1):
        super(CromosomaSudoku, self).__init__(genes, generacion, genes_reemplazables, valores_para_los_genes, cruzamiento)    
        #Cromosoma.__init__(self, genes, generacion, genes_reemplazables, valores_para_los_genes)    
    
    def get_fila(self, fila):
        """Funcion personalizada para obtener una fila (base 0) a partir de los genes"""
        return self.genes[fila*9 : fila*9+8]
    
    def get_columna(self, columna):
        """Funcion personalizada para obtener una columna (base 0) a partir de los genes"""
        mi_columna = []
        for fila in xrange(0, 80, 9):
            try:
                mi_columna.append(self.genes[fila + columna])
            except:
                print self.genes
                print len(self.genes)
                print fila + columna
                raise
        return convertir(mi_columna, type(self.genes))
    
    def get_region(self, region):
        """Funcion personalizada para obtener una region (base 0) a partir de los genes"""
        mi_region = []
        start = (region/3)*27 + (region%3)*3
        for j in xrange(0, 18, 9):
            for i in xrange(start, start + 3):
                mi_region.append(self.genes[i + j])        
        return convertir(mi_region, type(self.genes))
    
    def aptitud(self):
        """
        Aptitud de este cromosoma
        Método utilizado: Se cuentan las colisiones y se retorna eso como aptutid
        0 colisiones = solucion (obvio)
        """
        colisiones = 0
        # colisiones
        for i in xrange(9):
            for valor in "123456789":
                # filas
                count = self.get_fila(i).count(valor)
                if count > 1:
                    colisiones += count-1
                # columnas
                count = self.get_columna(i).count(valor)
                if count > 1:
                    colisiones += count-1
                # regiones
                count = self.get_region(i).count(valor)
                if count > 1:
                    colisiones += count-1
        return colisiones
        
    def combinar_genes(self, genes1, genes2):
        """Funcion tonta para combinar los genes, aleatoriamente"""
        combinacion1 = []
        combinacion2 = []
        if self.cruzamiento == 1:
            # combinar aleatoriamente
            for i in xrange(81):
                        if random.randint(0,1):
                            combinacion1.append(genes1[i])
                            combinacion2.append(genes2[i])
                        else:
                            combinacion1.append(genes2[i])
                            combinacion2.append(genes1[i])
        elif self.cruzamiento == 2:
            # combinar por cortes azarosos
            i = random.randint(0,80)
            combinacion1.extend(genes1[0:i])
            combinacion1.extend(genes2[i:81])
            combinacion2.extend(genes2[0:i])
            combinacion2.extend(genes1[i:81])
        elif self.cruzamiento == 3:
            # combinar por fila
            for i in xrange(9):
                if random.randint(0,1):
                    combinacion1.extend(genes1[i:i+9])
                    combinacion2.extend(genes2[i:i+9])
                else:
                    combinacion1.extend(genes2[i:i+9])
                    combinacion2.extend(genes1[i:i+9])
            pass
        # BINOMIAL PURO
        
        return (convertir(combinacion1, type(self.genes)), convertir(combinacion2, type(self.genes)))
    
    def mutar_genes(self):
        """Mutar genes, no estoy interesado en hacerlo"""
        for i in self.genes_reemplazables:
            if random.uniform(0,1) > 0.8:
                self.genes[i] = random.choice(self.valores_para_los_genes)
        
    def tablero(self):
        """Retornar el tablero en un string purete"""
        string = []
        for i in xrange(0,80, 9):
            string.append(" ".join(self.genes[i:i+9]))
        return "\n".join(string)
