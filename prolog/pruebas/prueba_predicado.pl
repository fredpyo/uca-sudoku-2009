es_viejo(Individuo) :- 
    edad(Individuo,Valor), 
    Valor > 60.

mayor_que(Fulano,Mengano) :- 
    edad(Mengano,EdadMengano), 
    edad(Fulano,EdadFulano), 
    EdadFulano > EdadMengano.

edad(juan,32). 
edad(luis,20).

