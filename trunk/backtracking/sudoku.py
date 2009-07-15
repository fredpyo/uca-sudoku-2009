# -*- encoding: utf-8 -*- 
rows = 'ABCDEFGHI'
cols = '123456789'
total = []

import copy

for a in rows:  #tuve que hacer esto porque cuando hago mi diccionario me carga aleatoriamente o sea no me hace de la A-I
    for b in cols:
        total.append(a+b)

def cross(A, B):
    return [a+b for a in A for b in B]

    
class Sudoku:
    '''Clase sencilla para la implementación del Puzzle Sudoku'''
    
    board={}
    iterations = 0
    attempts = 0
    backtracks = 0
    tt = set()
    paths = set()
    
    def __init__(self, puzzle=None):
        for a in rows:
            for b in cols:
                self.board[a+b]=['1','2','3','4','5','6','7','8','9']
        if puzzle:
            self.load(puzzle)
                
            
    def print_board(self):
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
        print "  ",
        for b in cols:
            print b, " " * 7,
        for a in rows:
            print "\n", a, "",
            for b in cols:
                print "%s%s" % ("".join(self.board[a+b]), " " * (9-len(self.board[a+b]))),
        print
        
    def load(self, values):
        list = [c for c in values if c in '0.-123456789'] # para chupar en \n
        for t,l in zip(total,list):
            if l not in '0.':
                self.board[t]=[l]
    
    def count_combinations(self):
        i = 0
        for a in rows:
            for b in cols:
                if len(self.board[a+b]) > 1:
                    i += len(self.board[a+b])
        return i
        
    def count_free(self):
        i = 0
        for a in rows:
            for b in cols:
                if len(self.board[a+b]) > 1:
                    i += 1
        return i
    
    def charge(self,list):
        list = [c for c in grid if c in '0.-123456789'] # para chupar en \n
        #print list,"\n"
        for t,l in zip(total,list):
            if l == '0' or l == '.':
               pass
            else : 
                self.board[t]=[l]
                #self.delete_option(t,l) 
            

    def delete_option(self,index,value):
        list = self.get_neighbor(index)
        
        #print list
        
        for i in list:
          
           if value in self.board[i]:
               self.board[i].remove(value)
        
            
    def get_neighbours(self, index):
        neighbours = set()
        for a in cols:
            #print index[0]+a
            neighbours.add(index[0]+a) #todas las columnas
        for b in rows:
            #print b+index[1]
            neighbours.add(b+index[1]) #todas las filas
        mini_rows , mini_cols = self.mini_board(index) #el mini tablero
        #print mini_rows
        #print mini_cols
        for a in mini_rows:
           for b in mini_cols:
            neighbours.add(a+b)
        neighbours.remove(index)
        return list(neighbours)
    
    def get_neighbor(self,index):
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
        
        
    def choose_next(self):
        '''Elije la siguiente casilla con menos opciones'''
        rank = ["", 10]
        for a in total:
            choices_left = len(self.board[a])
            if choices_left < rank[1]:
                rank[0] = a
                rank[1] = choices_left
        return rank[0]
    
    def rank_next(self):
        '''Elije la siguiente casilla con menos opciones'''
        rank = []
        for a in total:
            choices_left = len(self.board[a])
            if choices_left > 1:
                rank.append((a, choices_left))
        #rank.sort(cmp=lambda x,y:cmp(x[0],y[0]))
        rank1 = list(rank)
        rank.sort(key=lambda x:x[1], reverse=True)
        
        #print ">>", rank
        return rank
    
    def constraint(self):
        self.iterations = self.iterations + 1
        ban=True
        constrained = 0
        while ban==True:
            ban=False
            for a in total:
                if len(self.board[a]) == 1:
                    list=self.get_neighbor(a)
                    value=self.board[a][0]
                    for i in list:
                        if value in self.board[i]:
                            constrained += 1
                            ban=True
                            self.board[i].remove(value)
                            if len(self.board[i]) == 0:
                                return False                #bad solution
                            #self.print_board()
        #print "Constrained", constrained
        return True                                         #All constraint checked
                        
                        
    def mini_board(self,index):
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
        for i in total:
            if len(self.board[i]) != 1:
                return False
        return True
    
    def set_value(self, index, value):
        '''Setea el valor de una celda y elimina esa opcion de sus vecinos'''
        old_values = self.board[index]
        conflicting_neighbours = []
        self.board[index] = [value]
        for n in self.get_neighbours(index):
            try:
                self.board[n].remove(value)
            except Exception, e:
                pass
            else:
                if len(self.board[n]) == 0:
                    self.board[n].append(value)
                    for x in conflicting_neighbours:
                        self.board[x].append(value)
                    self.board[index] = old_values
                    return False
                conflicting_neighbours.append(n)
        return (old_values, conflicting_neighbours)
    
    def rb(self, index, value, old_values, conflicted):
        #print "UNSETTING %s for %s" % (value, index)
        if "A9" in conflicted:
            print "////", conflicted, value
        for n in conflicted:
            self.board[n].append(value)
            if "A9" == n:
                print ">>>>", self.board[n]
        self.board[index] = old_values
    
    def dead_end(self):
        for a in total:
            if len(self.board[a]) == 0:
                #print a, self.board[a]
                return True
            if len(self.board[a]) == 1:
                for b in self.get_neighbours(a):
                    if len(self.board[b]) == 1 and self.board[b][0] == self.board[a][0]:
                        #print b, self.board[a][0], self.board[b][0]
                        return True
        return False
    
    def backtracking(self, path=[]):
        #print "BACKTRACKING !!!! %s" % str(path)
        #print "Attempt :", self.attempts
        #print 
        self.attempts += 1
        print self.attempts
        if self.dead_end():
            #print "DEAD END!"
            return False
        if len(path) > 81:
            exit("WOOPS!")
        if self.solved():
            print "YAY!"
            return True
        else:
            #old_state = copy.deepcopy(self.board)
            #self.constraint()
            if self.solved():
                print "YAY2"
                return True
            else:
                next_indexes = self.rank_next()
                for next in next_indexes:
                    for value in self.board[next[0]]:
                        path.append((next[0], value))
                        pp = "/".join(["%s:%s" % (i, v) for i, v in path])
                        #print "PATH: ", pp
                        self.paths.add(pp)
                        # old_values, conflicted
                        setted = self.set_value(next[0], value)
                        print "~" * (self.count_free())
                        print len(self.paths)
                        print len(path)
                        
                        #print setted
                        #print setted
                        # si set_value retorno False, saltar este valor porque genera dead ends
                        if not setted:
                            path.pop()
                            continue
                            
                        #print "DIFF PATHS:", len(self.paths)
                        #raw_input()
                        if self.backtracking(list(path)):
                            return True
                        else:
                            #raw_input()
                            #print "go back...", self.board["A9"]
                            self.rb(path[-1][0], value, setted[0], setted[1])
                            #print path
                            path.pop()
                            #print path
                #self.state = old_state
                return False
                        
            
    
    def back_cp(self,rest=total):
        self.attempts += 1
        if rest == None:
            rest = total
        if not self.silencioso and self.attempts % 1000:
            print "·",
        #print self.attempts, "-" * len(rest)
        if self.solved():
            #print "ya resolvi"
            return True
        else:
            i=rest[0]
            aux = self.board[i]
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