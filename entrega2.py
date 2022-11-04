from itertools import combinations
from simpleai.search import MOST_CONSTRAINED_VARIABLE, CspProblem, backtrack,LEAST_CONSTRAINING_VALUE,HIGHEST_DEGREE_VARIABLE


def armar_mapa(filas,columnas,cantidad_paredes,cantidad_cajas_objetivos): 
    dominios={}
    dominio_cajas=[]
    dominio_total=[]
    for fila in range(filas):
        for columna in range(columnas):
            if (((fila,columna)!=(0,0)) and ((fila,columna)!=((filas-1),0)) and ((fila,columna)!=(filas-1,columnas-1)) and ((fila,columna)!=(0,columnas-1))): 
                dominio_cajas.append((fila,columna))
            dominio_total.append((fila,columna))
    
    dominios['J']=dominio_total #Dominio del jugador 
     
    aux_cajas=[]
    objetivos=[]
    for caja in range(cantidad_cajas_objetivos):
        aux_cajas.append(('C'+str(caja)))
        objetivos.append(('O'+str(caja)))
        dominios['O'+str(caja)]=dominio_total
        dominios['C'+str(caja)]=dominio_total
       
    aux_paredes=[]
    for pared in range(cantidad_paredes):
        aux_paredes.append(('P'+str(pared)))
        dominios['P'+str(pared)]=dominio_total

    variables= aux_cajas + aux_paredes + objetivos + ['J']
    restricciones=[]

    #Hasta aca esta todo perfecto, tenemos que mejorar abajo

    def son_diferentes(variables, values):
        val1, val2 = values  
        return val1 != val2
    
    Varibles_fisicas= aux_cajas +aux_paredes+ ['J']
    for v1,v2 in combinations((Varibles_fisicas),2): # diferentes cajas, paredes y jugador 
        restricciones.append(((v1,v2),son_diferentes))
    
    for o1,o2 in combinations((objetivos+aux_paredes),2):
        restricciones.append(((o1,o2),son_diferentes))

    def ganable(variables,values):
        cajas=list(values[0:cantidad_cajas_objetivos])
        objetivos=list(values[cantidad_cajas_objetivos:])
        cajas.sort()
        objetivos.sort()
        return cajas!=objetivos

    restricciones.append((tuple(aux_cajas+objetivos),ganable))   

    def adyacentes(posicion): #generamos una lista con las posiciones adyacentes 
        fila,columna=posicion
        lista_adyacentes=[]
        if fila>0:
            lista_adyacentes.append((fila-1,columna))
        if fila<filas:
            lista_adyacentes.append((fila+1,columna))
        if columna>0:
            lista_adyacentes.append((fila,columna-1))
        if columna<columnas:
            lista_adyacentes.append((fila,columna+1))
        return lista_adyacentes

    def cantidad_cajas_adyacentes(variable, values):
        pos_caja = values[0]
        fila_caja,columna_caja=pos_caja
        ady = adyacentes(pos_caja)
        c =0
        for pos_pared in values[1:]:
            if pos_pared in ady:
                c += 1
        if fila_caja==0 or fila_caja==filas-1 or columna_caja==0 or columna_caja == columnas-1:
            return c<0
        else:
            return c<1

    for caja in aux_cajas:
            if cantidad_paredes>1:
                for p1,p2 in combinations((aux_paredes),2):
                    restricciones.append(((caja,p1,p2),cantidad_cajas_adyacentes))
            else:
                restricciones.append((tuple([caja]+aux_paredes),cantidad_cajas_adyacentes))
             
    problema = CspProblem(variables, dominios, restricciones)
    solucion = backtrack(
        problema,
        inference=True,
        variable_heuristic=MOST_CONSTRAINED_VARIABLE,
        value_heuristic=LEAST_CONSTRAINING_VALUE,
    )

    lista_paredes=[]
    for pared in aux_paredes:
          lista_paredes.append(solucion[pared])

    lista_cajas=[]
    for caja in aux_cajas:
       lista_cajas.append(solucion[caja])

    lista_objetivo=[]
    for objetivo in objetivos:
       lista_objetivo.append(solucion[objetivo])  
    
    return(lista_paredes,lista_cajas,lista_objetivo,solucion['J'])
   
if __name__ == "__main__":
    resultado =(armar_mapa(filas = 5, columnas = 5, cantidad_paredes = 4,cantidad_cajas_objetivos = 3   ))
    print(resultado)