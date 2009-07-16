# -*- encoding: utf-8 -*- 
import copy

# CRITERIOS DE ORDENAMIENTO DE OPCIONES (VARIABLES)
VAR_ORDER_MINIMUN_REMAINING_VALUES = 1
VAR_ORDER_MAXIMUM_REMAINING_VALUES = 2
VAR_ORDER_SECUENTIAL = 3
# CRITERIOS DE ORDENAMIENTO DE VALORES
VAL_ORDER_LEAST_CONFLICTS = 4
VAL_ORDER_MOST_CONFLICTS = 5
VAL_ORDER_SECUENTIAL = 6

rows = 'ABCDEFGHI'
cols = '123456789'
total = []

for a in rows:  #tuve que hacer esto porque cuando hago mi diccionario me carga aleatoriamente o sea no me hace de la A-I
    for b in cols:
        total.append(a+b)

def cross(A, B):
    return [a+b for a in A for b in B]

    
class Sudoku:
    '''Clase sencilla para la implementación del Puzzle Sudoku'''
    board = {}
    attempts = 0
    var_order = VAR_ORDER_SECUENTIAL
    val_order = VAL_ORDER_SECUENTIAL
    
    def __init__(self, puzzle=None):
        for a in rows:
            for b in cols:
                self.board[a+b]=['1','2','3','4','5','6','7','8','9']
        if puzzle:
            self.load(puzzle)
            
    def print_board(self):
        """Imprimir los diccionarios del tablero"""
        for a in rows:
            print "\n"
            for b in cols:
                print a+b,":",self.board[a+b],
    
    def printb(self):
        '''Imprime el estado actual del tablero, omitiendo las casillas que tengan mas de una opcion'''
        print " ".join(' ' + cols)
        for a in rows:
            # la comprension de lista utilizada a continuacion basicamente realiza lo siguiente:
            # compactar todos los valores de una fila eligiendo el primer valor de cada lista si es que
            # dicha casilla tiene un solo valor (valor unico, el definitivo), o si es que tiene mas 
            # de un valor, retornar un espacio vacio (casilla sin decidir)
            print " ".join(a + "".join([self.board[a+x][0] if len(self.board[a+x]) == 1 else ' ' for x in cols]))
            
    def printb2(self):
        """Impresion similar a printb, solo que muestra las opciones por cada casilla, similar a print_board"""
        print "  ",
        for b in cols:
            print b, " " * 7,
        for a in rows:
            print "\n", a, "",
            for b in cols:
                print "%s%s" % ("".join(self.board[a+b]), " " * (9-len(self.board[a+b]))),
        print
        
    def load(self, values):
        """Cargar datos, llamado por __init__"""
        list = [c for c in values if c in '0.-123456789'] # para chupar en \n
        for t,l in zip(total,list):
            if l not in '0.':
                self.board[t]=[l]
    
    def charge(self,list):
        list = [c for c in grid if c in '0.-123456789'] # para chupar en \n
        for t,l in zip(total,list):
            if l == '0' or l == '.':
               pass
            else : 
                self.board[t]=[l]

    def get_neighbor(self,index):
        """Retornar los vecinos de una casilla"""
        list=[]
        for a in cols:
            list.append(index[0]+a) #todas las columnas
        for b in rows:
            list.append(b+index[1]) #todas las filas
        mini_rows , mini_cols = self.mini_board(index) #el mini tablero
        for a in mini_rows:
           for b in mini_cols:
            list.append(a+b)
        list = [x for x in list if x not in locals()['_[1]']] #para elimiar datos repetidos
        list.remove(index) #yo no soy vecino de yo
        return list
        
    def constraint(self):
        """Propagación de restricciones"""
        ban=True
        while ban==True:
            ban=False
            for a in total:
                if len(self.board[a]) == 1:
                    list=self.get_neighbor(a)
                    value=self.board[a][0]
                    for i in list:
                        if value in self.board[i]:
                            ban=True
                            self.board[i].remove(value)
                            if len(self.board[i]) == 0:
                                return False                #bad solution
        return True                                         #All constraint checked
                        
    def mini_board(self,index):
        """Retornar la región correspondiente a una casilla"""
        if index[0] in 'ABC':
            mini_rows='ABC'
        elif index[0] in 'DEF':
            mini_rows='DEF'
        elif index[0] in 'GHI':
            mini_rows='GHI'
        if index[1] in '123':
            mini_cols='123'
        elif index[1] in '456':
            mini_cols='456'
        elif index[1] in '789':
            mini_cols='789'
        return mini_rows ,mini_cols

    def solved(self):
        """Verificar si el tablero está resuelto"""
        for i in total:
            if len(self.board[i]) != 1:
                return False
        return True

    def count_conflicts(self, index, value):
        """Cuenta cuantos conflictos tiene este valor en este indice"""
        neigh = self.get_neighbor(index)
        conflicts = 0
        for n in neigh:
            conflicts += n.count(value)
        return conflicts
    
    def order_rest(self, rest):
        """Ordena las variables del problema (las casillas) segun un criterio"""
        new_rest = copy.copy(rest)
        if self.var_order == VAR_ORDER_MINIMUN_REMAINING_VALUES:
            new_rest.sort(cmp=lambda x,y: cmp(len(self.board[x]), len(self.board[y])), reverse=False)
        elif self.var_order == VAR_ORDER_MAXIMUM_REMAINING_VALUES:
            new_rest.sort(cmp=lambda x,y: cmp(len(self.board[x]), len(self.board[y])), reverse=True)
        elif self.var_order == VAR_ORDER_SECUENTIAL:
            pass
        return new_rest

    def order_vales(self, index):
        """Recibe una posición y retorna los valores de esa posicion ordenados según un criterio"""
        new_values = copy.copy(self.board[index])
        if self.val_order == VAL_ORDER_LEAST_CONFLICTS:
            new_values.sort(cmp=lambda x,y: cmp(self.count_conflicts(index, x), self.count_conflicts(index,y)), reverse=False)
        elif self.val_order == VAL_ORDER_MOST_CONFLICTS:
            new_values.sort(cmp=lambda x,y: cmp(self.count_conflicts(index, x), self.count_conflicts(index,y)), reverse=True)
        elif self.val_order == VAL_ORDER_SECUENTIAL:
            pass
        return new_values
    
    def back_cp(self,rest=total):
        """Backtracking en toda su gloria"""
        self.attempts += 1
        if rest == None:
            rest = total
        if not self.silencioso and self.attempts % 1000:
            print "·",
        if self.solved():
            return True
        else:
            rest = self.order_rest(rest)
            i=rest[0]
            aux = self.order_vales(i)
            for j in aux:
                trace=self.check_option(i,j)
                if  trace != False:
                    self.board[i]=[j]
                    rest.pop(0)
                    if not self.back_cp(rest):
                        self.rollback(trace, j)  
                        rest.insert(0,i)
                        self.board[i]=aux
                    else:
                        return True
            self.board[i]=aux    
            return False 
      
    def check_option(self,index,value):
        """Selecciona un valor para un indice y ademas realiza *forward checking*"""
        list = self.get_neighbor(index)
        trace=[]
        for i in list:
           if value in self.board[i]:
               if len(self.board[i])>1:
                   self.board[i].remove(value)
                   trace.append(i)
               else:
                   for t in trace:
                       self.board[t].append(value)
                   return False
        return trace
        
    def rollback(self,trace,value):
        """Deshacer un cambio"""
        for i in trace:
          self.board[i].append(value)

       
grid = """
200080300
060070084
030500209
000105408
000000000
402706000
301007040
720040060
004010003"""


if __name__ == "__main__":
    print "Para ejecutar el resolvedor de sudokus ejecutar el script solver.py"