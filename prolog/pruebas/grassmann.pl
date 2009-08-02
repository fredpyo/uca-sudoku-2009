
% Consultamos primero la base de datos - 1 punto
:- consult('pistas.pl').



% Devuelve el indice de la lista.
indexsergio(Fila, Columna, Indice) :- Indice is 9*(Fila-1) + Columna.


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

% cargar tablero vacio, es decir, llenos de 0s.
cargartablerovacio(Tablero, 0) :- append(Tablero, [0]).
cargartablerovacio(Tablero, Cantidadelementos) :-
    Cantidadelementosmenosuno is Cantidadelementos - 1,
    cargartablerovacio(Tablero,Cantidadelementosmenosuno)

% recibe el Tablero, que es una lista de 81 elementos
% Devuelve el Tablero con las pistas cargadas
cargartablerosudoku([])
cargartablerosudoku([_|ColaTablero]) :- anhadir(_, pista(X, Y, Z), ColaTablero).



nth1
fila, columna, valor
X, Y, Z



f(9, 9) = 9*(9-1) + 9
        = 72 + 9
        = 81

[1, 2, 3, 4, ..., 9
 10, 11, ..., 18,
 81]



KISS
Keep It Simple, Stupid.
Dejalo simple, estupido.

