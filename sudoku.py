
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
    fin = False
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
        print list,"\n"
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
                            if len(self.board[i]) == 0:
                                return False                #bad solution
                            #self.print_board()
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
            if len(self.board[i]) > 1 or len(self.board[i]) ==0:
                return False
        return True
    
    def back_cp(self,rest=[]):
     if not self.fin:
        if self.solved():
            print "ya resolvi"
            self.print_board()
            self.fin=True
            quit()
            return True
        else:
            #for i in total:
                #if len(self.board[i])>1:
                    #print "\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
                    #self.print_board()
                    
                    i=rest[0]
                    aux = self.board[i]
                    #print rest
                    for j in aux:
                        
                        trace=self.check_option(i,j)
                        if  trace != False:
                           self.board[i]=[j]
                           print "\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
                           self.print_board()
                           rest.pop(0)
                           if not self.back_cp(rest):
                               self.rollback(trace, j)  
                               rest.insert(0,i)
                               self.board[i]=aux
                               print "\n7777777777777777777777777"
                               self.print_board()
                        #else:
                                #return False
                    self.board[i]=aux    
                    return False 
                           #break
                           #print "\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",i
                           #self.print_board()
                         
                           #print "\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",i
                           #self.back_cp()
                           #pass
                        #else:
                           #self.board[i]=aux
                           #return   
                        #print "+++++++++++++++++++++"
                        #self.print_board()
                        #break
                    
                        
                #elif len(self.board[i])==0:
                 #   pass
                    #return 
               
      
    def check_option(self,index,value):
        list = self.get_neighbor(index)
        trace=[]
        #print list
        #print 88888888888888888
        for i in list:
           
           if value in self.board[i]:
               if len(self.board[i])>1:
              #     print i ,value
                   self.board[i].remove(value)
                   trace.append(i)
               else:
                   #print trace
                   for t in trace:
                       self.board[t].append(value)
                   return False
        return trace
        
        
    def rollback(self,trace,value):
        #list = self.get_neighbor(index)
        #trace=[]
        #print list
        #print 88888888888888888
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