
% Consultamos primero la base de datos - 1 punto
:- consult('pistas.pl').


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
% no se si vamos a usar este procedimiento amigos.
anhadir([], B, B).
anhadir([A | ColaA], B, [A | ColaC]) :- anhadir(ColaA, B, ColaC).


% by Sergio
cargartablerosudoku
cargartablerosudoku([_|ColaTablero]) :- anhadir(_, pista(X, Y, Z), ColaTablero).

