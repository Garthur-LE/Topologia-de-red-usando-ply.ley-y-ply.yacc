# Almacenar todos los nodos generados.
class nodos:
    def __init__(self, id, tipo, t_servicio = 0, replicas = 1): #Se agrego =0 e =1 para que entren fuente y sumidero por que da error si no.
        self.instruccion = id               # f1, f2, ope1, ope2, s1, s2 
        self.tipo = tipo                    # Fuente, operador o sumidero.
        self.t_servicio = t_servicio        # tiempo del servicio.
        self.replicas = replicas            # replicas salientes.

    def __str__(self):
        return f"[Tipo: {self.tipo} | T_Servicio: {self.t_servicio} | Réplicas: {self.replicas}]"

class crear_tabla_nodos:
    def __init__(self):
        self._tabla_nodos = {}

    # Insertar un nuevo nodo
    def insertar_nodo(self, id, tipo, t_servicio = 0, replicas = 1):
        #no duplicados 
        if id in self._tabla_nodos:
            return ValueError("\t Nodo Duplicado")
        else:
            self._tabla_nodos[id]= nodos(id, tipo, t_servicio, replicas)


    # Claramente obtener el nodo para ver si existe
    def obtener_nodo(self, id):
        return self._tabla_nodos.get(id)

    # para mostrar la tabla completa despues de la lectura
    def all_nodes(self):
        return self._tabla_nodos.values()

    
    def __str__(self):
        if not self._tabla_nodos:
            return "La tabla de símbolos está vacía."
            
        texto_final = ""
        for id_nodo, datos_nodo in self._tabla_nodos.items():
            # Aquí usamos el id (ej. f1) y los datos que formateamos arriba
            texto_final += f"ID: {id_nodo} -> {datos_nodo}\n"
            
        return texto_final
    