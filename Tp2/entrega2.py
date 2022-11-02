from itertools import combinations

from simpleai.search import CspProblem, backtrack, MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE, HIGHEST_DEGREE_VARIABLE

def armar_mapa(filas,columnas,cantidad_paredes,cajas):
    
    dominio={}
    dominio_cajas=[]
    dominio_total=[]
    for fila in filas:
        for columna in columnas:
            if (fila,columna)!=(0,0) and (fila,columna) != (filas,0) and (fila,columna) != (filas,columnas) and (fila,columna) != (0,columnas): 
                dominio_cajas.append((fila,columna))
            dominio_total.append((fila,columna))
    
    dominio['J']=dominio_total #Dominio del jugador 
     
    aux_cajas=[]
    objetivos=[]
    for index,caja in range(cajas):
        dominio['C'+index] =dominio_cajas # Misma cantidad de Cajas que de objetivos 
        dominio['O'+index]=dominio_total
        aux_cajas.append('C'+index)
        objetivos.append('O'+index)

    aux_paredes=[]
    for index,pared in range(cantidad_paredes):
        dominio['P'+index]=dominio_total # Dominio de las paredes 
        aux_paredes.append('P'+index)
    
    restricciones=[]

    def son_diferentes(variables, values):
        val1, val2 = values  #tupla (fila,columna)
        return val1 != val2
    
    #verificar que as cajas no esten en el mismo lugar 
    for index, caja in aux_cajas:
        ti=index+1
        if index!= cajas:
            for ti in range(cajas-1):
                restricciones.append((caja,aux_cajas[ti]),son_diferentes)
