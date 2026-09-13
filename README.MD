Asignatura: Lenguajes de Programación II

## Integrantes
Gabriel Gonzalez
[Nombre Integrante 2]
[Nombre Integrante 3]

## 1. Instrucciones de Ejecución
Este proyecto incluye un archivo Makefile para facilitar su ejecución en entornos Linux/Unix. 
Para correr el intérprete y la simulación, ubíquese en el directorio del proyecto y utilice los siguientes comandos en la terminal:

Instalar dependencias (PLY):** `make setup`
Ejecutar el intérprete:** `make run` (Este comando lee el archivo `red.txt` e imprime la simulación por consola).
Limpiar archivos precompilados:** `make clean` (Elimina cachés y archivos temporales generados por Yacc).
Asegúrese de que el archivo con la topología se llame exactamente `red.txt` y se encuentre en la raíz del proyecto.

## 2. Expresiones Regulares
El análisis léxico (Lex) reconoce los tokens mediante las siguientes Expresiones Regulares:

Texo r'[a-zA-Z_][a-zA-Z0-9_]*' (Reconoce nombres de variables alfanuméricas, excluyendo palabras reservadas mediante un diccionario restrictivo).
Números (NUM): r'\d+' (Reconoce secuencias de dígitos y los convierte a enteros).
Comentarios: r'(\#.*)' (Ignora cualquier texto que comience con el símbolo # hasta el final de la línea).
Ignorados: Tabulaciones y espacios en blanco (r' \t'), saltos de línea (r'\n+').

## 3. Gramática Libre de Contexto
El análisis sintáctico (Yacc) estructura el AST bajo la siguiente gramática:

programa -> instrucciones

instrucciones -> instrucciones instruccion_nodo
               | instrucciones instruccion_aristas
               | instrucciones instruccion_simulacion
               | instruccion_nodo
               | instruccion_aristas
               | instruccion_simulacion

instruccion_nodo -> FUENTE ID
                  | OPERADOR ID TIEMPO_SERVICIO NUM REPLICAS NUM
                  | OPERADOR ID TIEMPO_SERVICIO NUM
                  | SUMIDERO ID

instruccion_aristas -> CONECTAR ID A ID

instruccion_simulacion -> SIMULAR NUM

## 4. Links utilizados para la realizacion de codigo
https://www.dabeaz.com/ply/ply.html#ply_nn1 
https://www.geeksforgeeks.org/operating-systems/round-robin-scheduling-in-operating-system/
https://www.youtube.com/watch?v=xVzgQukMcVE

## 5. Réplicas Adyacentes
Se optó por una estrategia de encapsulamiento. Cuando un Operador A (origen) envía tuplas a un Operador B replicado (destino), el Operador A simplemente transfiere la tupla al "nodo general" de B. Es el propio nodo de destino (Operador B) quien se encarga internamente de gestionar su estado de Round-Robin mediante el método _siguiente_replica(), asignando la tupla a la réplica correspondiente. Esta decisión de diseño mantiene un bajo acoplamiento, ya que la lógica de ruteo general no necesita conocer el estado interno de las réplicas de los nodos adyacentes.

## 6. Declaración de Uso de IA
Herramienta utilizada: Gemini de Google.

Uso: Asistente de código para la depuración (debugging) de errores de atributos en Python, corrección de ambigüedades en PLY (shift/reduce conflicts)

Log de Prompts:
Error de sintaxis en docstrings (PLY): "Bro, me sale un error rojo gigante ply.yacc.YaccError: Unable to build parser. El Yacc se confunde en la regla p_operador_instruccion_sin_replica porque escribí 'instruccion_nodo: OPERADOR' todo pegado. ¿Me faltó un espacio en los dos puntos?"

Discordancia de nombres en las reglas: "Pana, el parser dice que hay una regla que no existe. En mi bloque p_instrucciones_orden llamé a la instrucción instruccion_aristas (con s al final), pero en la función de abajo la definí como instruccion_arista (sin s). ¿Es por eso que falla?"
Este fue otro error de escritura (Literal me falto una 's')


Uso incorrecto de listas (AttributeError): "En mi archivo de reglas, estoy intentando sacar el string del token usando tokens.get('FUENTE'), pero como tokens es una lista importada de lex, me tira un AttributeError. ¿Cómo devuelvo el string directamente?"

Error de instanciación del Parser (AttributeError): "Traté de leer el texto haciendo instruccciones = usar_yacc.parse(...), pero me salta 'function' object has no attribute 'parse'. En mi función iniciar_parser() estoy retornando yacc.yacc sin paréntesis. ¿Tengo que instanciarlo primero?"

Llamada al método de Yacc (TypeError): "Ayua, puse usar_yacc(codigo_topologia, lexer=usar_lex) y me tira un error de argumentos inesperados. ¿Me faltó ponerle el método .parse() para que el objeto lea el texto?"

Desempaquetado de tuplas (ValueError): "Modifiqué mi función uso_lex_yacc para que devuelva 3 cosas (nodo, aristas, simulaciones), pero en mi main la estoy llamando con solo 2 variables (tabla, conexiones = uso_lex_yacc()) y me tira too many values to unpack. ¿Me falta agregar una variable en el main?"

Error de tipo al acceder a listas: "Python explota en la validación de mis conexiones porque escribí nodo.obtener_nodo([3]) pasándole una lista con el número 3 adentro, en lugar de pasarle el elemento de la tupla i[3]. xd"

Falta de retorno en función: "Al principio mi función uso_lex_yacc no tenía un return al final, entonces devolvía None por defecto y el main colapsaba al intentar separar los datos. ¿Qué tengo que retornar?"

Impresión de objetos en memoria: "Mi tabla de símbolos funciona, pero al hacerle un print me sale <tabla_simbolos.crear_tabla_nodos object at 0x...> en vez de los datos. ¿Cómo le agrego el método __str__ para que me imprima los IDs y los tiempos de servicio bonitos?"

Acceso seguro a diccionarios (KeyError): "Para validar si un nodo existe, estaba usando return self._tabla_nodos[id], pero si el nodo no existe el programa crashea feo. ¿Cómo lo cambio por .get(id) para que solo me devuelva None sin explotar?"

Error semántico (Typo en el .txt): "El script me lanza RuntimeError: Flujo fallido sin llegar al sumidero. Ya vi que en el archivo red.txt creé el operador como ope1, pero en el CONECTAR le pasé op1. Como el diccionario no lo encontró, el nodo f1 quedó flotando sin conexiones. ¿Solo tengo que corregir el nombre en el txt verdad?" Este ultimo lo vio la IA yo solo le envie todo por que no podia encontrar que fallaba jaja.


