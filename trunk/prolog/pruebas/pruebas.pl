
contar(L,R) :- contar(L,0,R).
contar([],VI,VI).
contar([_|T],VI,R):- VS is VI+1,contar(T,VS,R).


switch(1):-write(1).
switch(2):-!,write(2).
switch(_):-write(3).



recorrerMat(Filas,Columnas,L):-recorrerFila(1,Filas,Columnas,L).

recorrerFila(FA,FF,_,L):-FA>FF,!.
recorrerFila(FA,FF,CF,L):-recorrerColumnas(FA,1,CF,L),F2 is FA+1,
	recorrerFila(F2,FF,CF,L).

recorrerColumnas(_,CA,CF,_):-CA>CF,nl,!.
recorrerColumnas(F,CA,CF,L):-write(F),write(','),write(CA),write(' '),
	member(casilla(F,CA,_),L),
 CS is CA+1,recorrerColumnas(F,CS,CF,L).


noquieroprogramar(L):-L = [casilla(1, 1, _), casilla(1, 2, _), casilla(2, 1, _), casilla(2, 2, _)].

% contar(L,81),recorrerMat(9,9,L),bagof(V, F^(member(casilla(F,7,V),L),
% ),Col7),member(1,Col7) ,write(L).

