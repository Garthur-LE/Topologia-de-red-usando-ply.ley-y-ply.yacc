# Este archivo yacc se puede modificar al añadir definiciones de funciones segun corresponda a las modificaciones añadidas en el lex
# (Caso se añadan mas tokens). Se deberan añadir instrucciones si o si del tipo:
#  def p_ejemplo(p):
#  'tipo de instruccion(en caso de que esto sea un nuevo nodo o nueva arista) : (cualquier cosa que se definio, id, number, alguna operacion matematica, etc)
# 'p[0] = p[1] + p[2] + ... + p[n] (En caso de una instruccion usar 'INSTRUCCION')
#
# Esto permitira al archivo ser modificado a gusto solo agregando nuevas instrucciones y tokens.
 
import ply.yacc as yacc
from lex import tokens

# Programa permite identificar al programa solo hecho por instrucciones y nada mas.

def p_secuencia_instrucciones(p):
    'programa : instrucciones'
    p[0] = p[1]

# Lista de instrucciones aumentativa o simple
# puede haber una acumulacion para poder leer la topologia completa
# -> primera instruccion seria 
# fuente A -> instruccion_nodo.
# operador B tiempo_servicio 5 replicas 2 -> instruccion_nodo, instruccion_nodo.  (Acumulativamente)
# sumidero C -> instruccion_nodo, instruccion_nodo, instruccion_nodo. (Acumulativamente)
# conectar A a B -> instruccion_arista, instruccion_nodo, instruccion_nodo, instruccion_nodo. (Acumulativamente)

#Esto se repite hasta el final de la topologia, donde existe la simulacion de la misma, que seria la ultima instruccion.

def p_instrucciones_orden(p):
    '''instrucciones : instrucciones instruccion_nodo
                    | instrucciones instruccion_aristas
                    | instrucciones instruccion_simulacion
                    | instruccion_nodo
                    | instruccion_aristas
                    | instruccion_simulacion'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# analogo a un spout
def p_fuente_instruccion(p):
    'instruccion_nodo : FUENTE ID'
    p[0] = 'FUENTE', p[2]
# analogo a un bolt con replica usada
def p_operador_instruccion_con_replica(p):
    'instruccion_nodo : OPERADOR ID TIEMPO_SERVICIO NUM REPLICAS NUM'
    p[0] = 'OPERADOR', p[2], 'TIEMPO_SERVICIO', p[4], 'REPLICAS', p[6]
# sin replica usada se asume una sola instancia
def p_operador_instruccion_sin_replica(p):
    'instruccion_nodo : OPERADOR ID TIEMPO_SERVICIO NUM'
    p[0] = 'OPERADOR', p[2], 'TIEMPO_SERVICIO', p[4], 'REPLICAS', 1

def p_sumidero_instruccion(p):
    'instruccion_nodo : SUMIDERO ID'
    p[0] = 'SUMIDERO', p[2]

def p_conectar_instruccion(p):
    'instruccion_aristas : CONECTAR ID A ID'
    p[0] = 'CONECTAR', p[2], 'A', p[4]

def p_simular_instruccion(p):
    'instruccion_simulacion : SIMULAR NUM'
    p[0] = 'SIMULAR', p[2]

# Regla de error para errores de sintaxis 
def p_error(p): 
    print("¡Error de sintaxis en la entrada!") 

def iniciar_parser():
    return yacc.yacc()