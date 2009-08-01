% RECURSIVIDAD
% La longitud de la lista vacia es cero

longitud([], 0).

% La longitud de una lista es la longitud
% del resto mas uno. Como el contenido
% de la cabeza no nos interesa,
% utilizamos la variable anonima

longitud( [_|Resto], Longitud) :-
    longitud(Resto, LongitudResto),
    Longitud is LongitudResto + 1.



% %%%%%%%%%%
% Concatenar
% Concatenar vacio con L es L...

concatena([], L, L).

% Para concatenar dos listas, sacamos 
% la cabeza de la primera lista, 
% luego concatenamos el resto con la segunda lista 
% y al resultado le ponemos la cabeza 
% de la primera lista como 
% cabeza del resultado... 

concatena([Cabeza|Resto], Lista, [Cabeza|RestoConcatenado]):-
    concatena(Resto, Lista, RestoConcatenado). 



% RECURSIVIDAD - Parametros de acumulacion
longitud2_aux([], Parcial, Parcial).
  
longitud2_aux([_|Resto], Parcial, Result) :-
    NParcial is Parcial + 1,
    longitud2_aux(Resto, NParcial, Result).

longitud2(Lista, Longitud) :-
    longitud2_aux(Lista, 0, Longitud).


