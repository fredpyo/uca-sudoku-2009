# -*- encoding: utf-8 -*-
'''
Clases generales para la resolución de problemas que requieran del uso de Algoritmos Evolutivos

@author: Federico Cáceres <fede.caceres@gmail.com>
'''
import copy
import random

# definiciones varias utilies, funciones utilitarias, excepciones

class GeneticException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)


def is_iterable(x):
    """Función utilitaria para verificar si una variable es de tipo iterable"""
    return isinstance(x, str) or isinstance(x, unicode) or isinstance(x, list) or isinstance(x, tuple)

def convertir(objeto, tipo):
    """Reconvertir una lista a otro tipo"""
    if tipo == type(unicode()):
        objeto = "".join([unicode(x) for x in objeto])
    elif tipo == type(str()):
        objeto = "".join([str(x) for x in objeto])
    elif tipo == type(tuple()):
        objeto = tuple(objeto)
    elif tipo == type(list()):
        pass
    return objeto

# definición de las clases principales


class Cromosoma(object):
    """
    Clase genérica para el planteamiento de algoritmos evolutivos
    Métodos que se deben overridear:
    - aptitud
    - combinar_genes
    - mutar_genes
    """
    
    def __init__(self, genes, generacion=0, genes_reemplazables=None, valores_para_los_genes=None):
        """
        Inicializa el cromosoma
        @param genes: una variable iterable (string, tuple, list, etc) con los genes del cromosoma
        @param genes_reemplazables: genes del cromosoma_inicial que se podrán reemplazar (por ejemplo string vacio "" o espacio " " para un string, o None para una lista o tupla)
        @param valores_para_los_genes: iterable (string o tupla, lista, etc) con los posibles valores que pueden tomar las suceciones de este cromosoma  
        """
        # validar los tipos del input
        if not is_iterable(genes):
            raise GeneticException("Los genes deben de ser de tipo iterable (str, unicode, list, tuple) sin embargo el tipo recibido fue %s" % type(genes))
        # validar genes_reemplazables
        if generacion == 0:
            if not is_iterable(valores_para_los_genes):
                raise GeneticException("valores_para_los_genes debe ser de tipo iterable (str, unicode, list, tuple) sin embargo el tipo recibido fue %s" % type(valores_para_los_genes))
            if type(valores_para_los_genes[0]) != type(genes[0]):
                raise GeneticException("Los elementos valores_para_los_genes deben de ser de tipo que el de los elementos de los genes recibidos, se recibio tipo %s y se esperaba tipo %s" % (type(valores_para_los_genes[0]), type(genes[0])))
        # cargar los datos
        self.genes = genes
        self.generacion = generacion
        self.genes_reemplazables = genes_reemplazables
        self.valores_para_los_genes = valores_para_los_genes
    
    @classmethod
    def new_Cromosoma(cls, genes, generacion=0, genes_reemplazables=None, valores_para_los_genes=None):
        """
        Glorioso uso de los classmethods para la generacion de instancias indicadas...
        Explicacion: si un objeto hereda a esta clase, cls tiene como valor a esa clase y no a esta clase padre, entonces
        efectivamente se crea una nueva instancia de la clase desde la cual se ejecuta la funcion, FANTASTICO!!!
        """
        return cls(genes, generacion, genes_reemplazables, valores_para_los_genes)
    
    def llenar_genes_vacios(self, genes):
        """Llena los genes vacios aleatoriamente"""
        tipo_original = type(genes)
        genes = list(genes) # convertir a lista para cambiar sus elementos... leer un poco de python para entender
        # asigar aleatoriamente los genes
        for i in self.genes_reemplazables:
            genes[i] = random.choice(self.valores_para_los_genes)
        # reconvertir a su tipo original y retornar
        return convertir(genes, tipo_original)
    
    def generar_poblacion_inicial(self, cantidad):
        '''Genera una lista de cromosomas'''
        
        cromosomas = []
        for i in xrange(cantidad):
            genes = copy.copy(self.genes)
            genes = self.llenar_genes_vacios(genes)
            nuevo_cromosoma = self.new_Cromosoma(genes, self.generacion+1, self.genes_reemplazables, self.valores_para_los_genes)
            cromosomas.append(nuevo_cromosoma)
        return cromosomas
        
    def aptitud(self):
        """Esta funcion debe ser overrided por la clase que herede a esta clase"""
        return 0
    
    def combinar_genes(self, genes1, genes2):
        """
        Combina los genes
        @todo: abstracto, overridear
        
        """
        return genes1
    
    def cruzar(self, cromosoma):
        """
        Se cruza con otra instancia de cromosoma
        @param cromosoma: Otra instancia de la clase Cromosoma 
        """
        mis_genes = self.genes
        sus_genes = cromosoma.genes
        nuevos_genes = self.combinar_genes(mis_genes, sus_genes)
        nuevo_cromosoma1 = self.new_Cromosoma(nuevos_genes[0], self.generacion + 1, self.genes_reemplazables, self.valores_para_los_genes)
        nuevo_cromosoma2 = self.new_Cromosoma(nuevos_genes[1], self.generacion + 1, self.genes_reemplazables, self.valores_para_los_genes)
        return (nuevo_cromosoma1,nuevo_cromosoma2)
    
    def mutar_genes(self):
        """Override con el criterio de mutacion"""
        pass
        
    def __repr__(self):
        return "<Cromosoma (%s)>" % self.genes


if __name__ == "__main__":
    """Pruebas de estas clases"""
    print "Demostracion de la clase cromosoma"
    cromo = Cromosoma("ab  efg", 0, " ", "abcdefg")
    print "Generado un cromosoma: %s" % cromo
    print "Generando una poblacion de 10 elementos a partir del cromosoma original..."
    pop = cromo.generar_poblacion_inicial(10)
    print "Poblacion generada:"
    print pop