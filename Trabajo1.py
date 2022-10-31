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


movimientos=30
paredes = ((0,0),(0,1),(0,2),(0,3),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3),(1,3),(2,3),(3,3))
objetivos = ((1,1)) # ponerle los correctos
jugador=(3,1)
INICIAL=((2,4), jugador, movimientos)


class SokobanProblem(SearchProblem):
    def cost(self, state1, action, state2): 
        return 1

    def is_goal(self, state):   
        cajas, jugador, movimientos_restantes=state
        for caja in cajas:
            if caja not in objetivos:
                return False
        #if movimientos_restantes<0:
         #   return False
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
       # fila_caja, columna_caja = camino_caja
        #fila_jugador , columna_jugador = jugador
        return aux #+ (abs(fila_caja-fila_jugador)+abs(columna_caja-columna_jugador))# retorna 1 por cada caja, hay que mejorarlo 
# heuristica de manhattan desde el jugador a alguna caja que no esta en su lugar

#viewer = WebViewer()
viewer = BaseViewer()
#result = breadth_first(SokobanProblem(INICIAL),
#                        graph_search=True)
# result = breadth_first(SokobanProblem(INICIAL),
                       # viewer=viewer)
# result = depth_first(SokobanProblem(INICIAL), graph_search=True)
# result = uniform_cost(SokobanProblem(INICIAL))
# result = limited_depth_first(SokobanProblem(INICIAL), 5)
# result = iterative_limited_depth_first(SokobanProblem(INICIAL))
# result = greedy(SokobanProblem(INICIAL))
result = astar(SokobanProblem(INICIAL))

print("Estado meta:")
print(result.state)

for action, state in result.path():
    print("Haciendo", action, "llegué a:")
    print(state)

print("Profundidad:", len(list(result.path())))

print("Stats:")
print(viewer.stats)