% pagina 204, predicados recursivos que contienen listas

% procedimiento "miembro"
% se utiliza para averiguar si un cierto elemento X se encuentra en una lista A.
miembro(X, [X | _]).
miembro(X, [_ | Z]) :- miembro(X, Z).


% procedimiento "longitud"
% sea longitud(Lista, N) el predicado que tiene éxito si Lista contiene exacta-
% -mente N elementos.
longitud([], 0).
longitud([_ | Cola], Longitud) :- longitud(Cola, ColaN), Longitud is 1 + ColaN.


% procedimiento "anhadir"
anhadir([], Bs, Cs).
anhadir([A | ColaAs], Bs, [As | ColaCs]) :- anhadir(ColaAs, Bs, ColaCs).

