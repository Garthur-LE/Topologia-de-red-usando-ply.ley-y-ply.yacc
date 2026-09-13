import ply.lex as lex
# Lista de tokens se pueden añadir mas en caso de definir un DSL mas grande (Este solo sera en base a lo solicitado en el control, 
# pero incluso al añadir mas comandos en restringido, o tokens de aceptacion, este deberia funcionar igualmente)

restringido = {
    'FUENTE' : 'FUENTE',
    'OPERADOR' : 'OPERADOR',
    'TIEMPO_SERVICIO' : 'TIEMPO_SERVICIO',
    'REPLICAS' : 'REPLICAS',
    'SUMIDERO' : 'SUMIDERO',
    'CONECTAR' : 'CONECTAR',
    'A' : 'A',
    'SIMULAR' : 'SIMULAR'
}
tokens = ['ID', 'NUM'] + list(restringido.values())
# reglas de expresiones regulares simples
t_ignore = ' \t'
# Reglas de expresiones regulares como 
def t_ignore_COMENTARIO(t):
    r'(\#.*)'
    pass

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Comparamos las cadenas restringidas para evitar que se reconozcan como ID
    t.type = restringido.get(t.value, 'ID') 
    return t
# esta regla compara numeros y convierte la cadena en un entero de Python.
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el analizador léxico (no me funciono asi que lo hare funcion)

def iniciar_lexer():
    return lex.lex()
#   lexer = lex.lex()

# Borrar comentarios para probar el analizador léxico
## lexer.input('/* FUENTE f1 OPERADOR ope1 TIEMPO_SERVICIO 5 REPLICAS 2 SUMIDERO s1 CONECTAR f1 A ope1 CONECTAR f1 a s1 SIMULAR 1 */')
## while True:
##     tok = lexer.token()
##     if not tok: 
##         break      # No more input
##     print(tok)