
rows = 'ABCDEFGHI'
cols = '123456789'
total = []


for a in rows:  #tuve que hacer esto porque cuando hago mi diccionario me carga aleatoriamente o sea no me hace de la A-I
    for b in cols:
        total.append(a+b)

def cross(A, B):
        return [a+b for a in A for b in B]
    

    
class Sudoku:
    board={}
    
    def __init__(self):
            for a in rows:
                for b in cols:
                    
                    self.board[a+b]=['1','2','3','4','5','6','7','8','9']
            
    def print_board(self):
            for a in rows:
                print "\n"
                for b in cols:
                    print a+b,":",self.board[a+b],
                    
    def charge(self,list):
        list = [c for c in grid if c in '0.-123456789'] # para chupar en \n
        for t,l in zip(total,list):
            if l != '0':
                self.board[t]=[l]
                self.delete_option(t,l) # aqui recorrera los vecinos para el CP
            

    def delete_option(self,index,value):
        list = self.get_neighbor(index)
        
        #print list
        
        for i in list:
          
           if value in self.board[i]:
               self.board[i].remove(value)
        
            
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
    
    
    def constraint(self):
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
                            #self.print_board()
                        
        
            
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
        
        
grid = """
003020600
900305001
001806400
008102900
700000008
006708200
002609500
800203009
005010300"""