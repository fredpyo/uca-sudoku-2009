# -*- encoding: utf-8 -*-
'''
Created on 10/07/2009

@author: fede
'''
import copy

class Cromosoma():
    def __init__(self, genes, generacion=0, genes_reemplazables=None, valores_para_los_genes=None):
        """
        Inicializa el cromosoma
        @param genes: una variable iterable (string, tuple, list, etc) con los genes del cromosoma
        @param genes_reemplazables: genes del cromosoma_inicial que se podrán reemplazar (por ejemplo string vacio para un string, o None para una lista o tupla)
        @param valores_para_los_genes: iterable (string o tupla, lista, etc) con los posibles valores que pueden tomar las suceciones de este cromosoma  
        """
        self.genes = genes
        self.generacion = generacion
        self.genes_reemplazables = genes_reemplazables
        self.valores_para_los_genes = valores_para_los_genes
    
    def llenar_genes_vacios(self, genes, genes_reemplazables, valores_para_los_genes):
        """Llena su panza"""
        return genes
    
    def generar_poblacion_inicial(self, cantidad):
        '''Genera una lista de cromosomas'''
        cromosomas = []
        for i in xrange(cantidad):
            genes = copy.copy(self.valor)
            genes = self.llenar_genes_vacios(genes, self.genes_reemplazablas, self.valores_para_los_genes)
            nuevo_cromosoma = Cromosoma(genes, self.generacion+1)
            cromosomas.append(nuevo_cromosoma)
        return cromosomas
        
    def aptitud(self):
        """Esta funcion debe ser overrided por la clase que herede a esta clase"""
        return 0
    
    def seleccion_de_genes_para_mutacion(self):
        """Selecciona una fraccion de los genes, debe haber una forma de llamara esta funcion dos veces para que retorne un lado de los genes de un cromosoma y otro lado"""
        # TODO: parametrizar la funcion de seleccion en el init...? o que sea overrided por el padre?
        return self.genes
    
    def cruzar(self, cromosoma):
        """
        Se cruza con otra instancia de cromosoma
        @param cromosoma: Otra instancia de la clase Cromosoma 
        """
        nuevo_cromosoma = Cromosoma() 
        return nuevo_cromosoma
    
    def mutar(self):
        """Override con el criterio de mutacion"""