from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    limited_depth_first,
    iterative_limited_depth_first,
    astar,
    greedy,
)
from simpleai.search.viewers import WebViewer, BaseViewer

from test_entrega1 import DIRECCIONES
import  pydot

def jugar(paredes, cajas, objetivos, jugador, maximos_movimientos, usar_viewer=False):

    INICIAL=(tuple(cajas), jugador, maximos_movimientos)

    class SokobanProblem(SearchProblem):
        def cost(self, state1, action, state2): 
            return 1

        def is_goal(self, state):   
            cajas, jugador, movimientos_restantes=state
            for caja in cajas:
                if caja not in objetivos:
                    return False
            if movimientos_restantes<0:
               return False
            return True
                

        def actions(self, state):  
            aux=[]
            acciones_disponibles = []
            cajas, jugador,_ = state
            fila, columna= jugador
            aux.append((fila-1,columna))
            aux.append((fila+1,columna))
            aux.append((fila,columna+1))
            aux.append((fila,columna-1))
            for nueva_posicion in aux:
                if nueva_posicion not in paredes:
                    if nueva_posicion not in cajas:
                        acciones_disponibles.append((nueva_posicion))
                    else:
                        fila_nueva, columna_nueva = nueva_posicion
                        # tenes que verificar que si tenes lugar disponible despues de la caja
                        segunda_fila=fila+(fila_nueva-fila)*2 # Se hace este calculo para llegar a la posicion que esta despues de la caja 
                        segunda_columna= columna+(columna_nueva-columna)*2
                        posicion_siguiente_de_caja=(segunda_fila,segunda_columna)
                        if posicion_siguiente_de_caja not in cajas and posicion_siguiente_de_caja not in paredes:
                            acciones_disponibles.append((nueva_posicion))
            return acciones_disponibles
            
        def result(self, state, action):
            aux=[]
            cajas, jugador, movimientos = state
            fila,columna= jugador
            if action in cajas: #se verifica que la posicion a la que se mueve no haya una caja
                for caja in cajas:
                    if caja== action:
                        aux.append((fila+(action[0]-fila)*2,columna+(action[1]-columna)*2))
                    else:
                        aux.append(caja)
                return (tuple(aux),action,movimientos-1)
            return (cajas,action,movimientos-1)
        
        def heuristic(self, state):
            cajas,jugador,_=state
            aux=0
            camino_caja=jugador
            for caja in cajas:
                if caja not in objetivos:
                    aux+=1
                    camino_caja= caja
            fila_caja, columna_caja = camino_caja
            fila_jugador , columna_jugador = jugador
            return (aux + (abs(fila_caja-fila_jugador)+abs(columna_caja-columna_jugador))-1)# retorna 1 por cada caja, hay que mejorarlo 
    # heuristica de manhattan desde el jugador a alguna caja que no esta en su lugar

    viewer = WebViewer()
    #viewer = BaseViewer()
    #result = breadth_first(SokobanProblem(INICIAL),
    #                        graph_search=True)
    # result = breadth_first(SokobanProblem(INICIAL),
                        # viewer=viewer)
    # result = depth_first(SokobanProblem(INICIAL), graph_search=True)
    # result = uniform_cost(SokobanProblem(INICIAL))
    # result = limited_depth_first(SokobanProblem(INICIAL), 5)
    # result = iterative_limited_depth_first(SokobanProblem(INICIAL))
    # result = greedy(SokobanProblem(INICIAL))
    if usar_viewer:
        result = astar(SokobanProblem(INICIAL),graph_search=True, viewer=viewer)
    else:
        result = astar(SokobanProblem(INICIAL),graph_search=True)

    print("Estado meta:")

    print(result.state)
    pasos=[]
    for action, state in result.path():
        if action is not None:
            fila_nueva, columna_nueva = action
            fila, columna = posicion_pj         
            if fila<fila_nueva:
                pasos.append("abajo")
            if fila>fila_nueva:
                pasos.append("arriba")
            if columna<columna_nueva:
                pasos.append("derecha")
            if columna>columna_nueva:
                pasos.append("izquierda")
        posicion_pj=state[1]               
        print("Moviendo Jugador", action, "llegu?? a:")
        print(pasos)
        print(state)
    return pasos

if __name__ == "__main__":
    print(jugar(
        paredes = ((0,0),(3,3)),
        cajas=((1,2),),
        objetivos=((1,1),),
        jugador=(3,1),
        maximos_movimientos=10,
        usar_viewer=True,
    ))
   