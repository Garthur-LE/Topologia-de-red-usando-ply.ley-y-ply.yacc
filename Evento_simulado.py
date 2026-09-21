#Lectura de datos del lex y parser
import lex as lx
import yacc as yc
# Se nececita una tabla con los simbolos
from tabla_simbolos import crear_tabla_nodos
# Se añade la funcion que funciona como grafo
from Grafo import Grafo_transiciones

def uso_lex_yacc(path):
    with open(path,'r') as topology_storm:
        codigo_topologia = topology_storm.read()

    usar_lex = lx.iniciar_lexer()
    usar_yacc = yc.iniciar_parser()

    instruccciones = usar_yacc.parse(codigo_topologia, lexer=usar_lex)
    if not instruccciones:
        return UserWarning(" Topologia no reconocida/Vacia ")
    
    nodo = crear_tabla_nodos() #Lista de la tabla de simbolos o nodos
    aristas = [] # Lista de las aristas u conexiones
    simulaciones = 0
    for i in instruccciones:
        if i[0] == 'FUENTE':
            nodo.insertar_nodo(i[1], i[0])

        elif i[0] == 'OPERADOR':
            if len(i) == 6:
                nodo.insertar_nodo(i[1], i[0], t_servicio = i[3], replicas=i[5])
            else:
                nodo.insertar_nodo(i[1], i[0], t_servicio = i[3], replicas=1)

        elif i[0] == 'SUMIDERO':
            nodo.insertar_nodo(i[1], i[0])
        # Numero de simulaciones totales.
    for i in instruccciones:
        if i[0] == 'CONECTAR': # Solo se conectan los que existen. Aristas
            if not nodo.obtener_nodo(i[1]) or not nodo.obtener_nodo(i[3]):
                print(f"\tUn nodo no existe para la conexion entre el nodo {i[1]} y el nodo {i[3]}\t")
            else:
                aristas.append((i[1],i[3]))
        else: 
            pass

    for i in instruccciones:
        if i[0] == 'SIMULAR':
            simulaciones = i[1]
    return nodo, aristas, simulaciones

if __name__ == '__main__':
    ruta_archivo = './red.txt'
    
    # Leemos el archivo y creamos poblamos la tabla de simbolos
    tabla_simbolos, lista_aristas, num_simulaciones = uso_lex_yacc(ruta_archivo)
    
    if tabla_simbolos is not None and not isinstance(tabla_simbolos, UserWarning):

        
        # Iniciamos el grafo y le pasamos la tabla_simbolos
        grafo = Grafo_transiciones(tabla_simbolos)
        grafo.crear_red()
        
        # Conectamos los nodos en el grafo
        for origen, destino in lista_aristas:
            grafo.conectar_nodos(origen, destino)
            
        grafo.validar_topologia()

        #Inicio de simulacion
        for evento in range(1, int(num_simulaciones) + 1):
            resultados = grafo.simular_evento(evento)
            for i, resultado in enumerate(resultados):
                print(f"Evento {evento} (Rama {i+1}): Ruta = {' -> '.join(resultado['ruta'])}")
                print(f"Tiempo total = {resultado['t_acumulado']} |")