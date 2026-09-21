from abc import ABC, abstractmethod

class Topologia_red(ABC):
    def __init__(self, id):
        self.id = id
        self.tuplas_salientes = []
        self.turno_salida = 0
        
    def _destino(self, destino):
        self.tuplas_salientes.append(destino)

# Función que maneja el caso en que un nodo tiene varias salidas, alternando la salida después de cada evento.
    def siguiente_destino(self):
        if not self.tuplas_salientes:
            return None

        destino = self.tuplas_salientes[
            self.turno_salida % len(self.tuplas_salientes)
        ]
        self.turno_salida += 1
        return destino

    @abstractmethod
    def transito(self, recorrido):
        pass

# Se añade el sumidero inicial
class DatosFuente(Topologia_red):
    def transito(self, recorrido):
        recorrido['ruta'].append(f"FUENTE {self.id}")
        return self.tuplas_salientes

# se añaden los datos de los Operadores intermedios junto a sus tiempos de servicio y replicas.
class DatosOperador(Topologia_red):
    def __init__(self, id, t_servicio, replicas):
        super().__init__(id)
        self.t_servicio = int(t_servicio)
        self.replicas = int(replicas)
        # variable que realiza round robin
        self.turno_replica = 0 

    def siguiente_replica(self):
        replica = (self.turno_replica % self.replicas) + 1
        self.turno_replica += 1
        return replica

    def transito(self, recorrido):
        replica_usada = self.siguiente_replica()
        recorrido['t_acumulado'] += self.t_servicio
        
        if self.replicas > 1:
            recorrido['ruta'].append(f"OPERADOR {self.id} (Replica {replica_usada}) (Tiempo: {self.t_servicio})")
        else:
            recorrido['ruta'].append(f"OPERADOR {self.id} (Tiempo: {self.t_servicio})")
            
        return self.tuplas_salientes

#Se añade el sumidero a la red (Final)
class DatosSumidero(Topologia_red):
    def transito(self, recorrido):
        recorrido['ruta'].append(f"SUMIDERO {self.id}")
        # El sumidero no tiene conexiones salientes, detiene el flujo
        return [] 

class Grafo_transiciones:
    def __init__(self, tabla_simbolos):
        self.tabla = tabla_simbolos
        self.nodos = {}
        self.fuentes = []
        self.sumideros = []

    def crear_red(self):
        # Iteramos sobre los nodos reales de la tabla de simbolos
        for entrada in self.tabla.all_nodes():
            if entrada.tipo == 'FUENTE':
                nuevo_nodo = DatosFuente(entrada.instruccion)
                self.fuentes.append(nuevo_nodo)
            elif entrada.tipo == 'OPERADOR':
                nuevo_nodo = DatosOperador(entrada.instruccion, entrada.t_servicio, entrada.replicas)
            elif entrada.tipo == 'SUMIDERO':
                nuevo_nodo = DatosSumidero(entrada.instruccion)
                self.sumideros.append(nuevo_nodo)
            
            # Guardamos la instancia en el diccionario general
            self.nodos[entrada.instruccion] = nuevo_nodo

    def conectar_nodos(self, origen, destino):
        if origen not in self.nodos or destino not in self.nodos:
            raise ValueError(f"Error entre {origen} y {destino}")
        self.nodos[origen]._destino(self.nodos[destino])

    def validar_topologia(self):
        if not self.fuentes:
            raise ValueError("No existen nodos fuente en la red")
        if not self.sumideros:
            raise ValueError("No existen nodos sumideros en la red")

    def simular_evento(self, numero_evento):
        # Alterna la fuente si tiene existen mas
        fuente_inicio = self.fuentes[(numero_evento - 1) % len(self.fuentes)]
        
        recorrido = {
            't_acumulado': 0,
            'ruta': []
        }

        nodo_actual = fuente_inicio
        while nodo_actual:
            siguientes = nodo_actual.transito(recorrido)
            
            if not siguientes:
                if not isinstance(nodo_actual, DatosSumidero):
                    raise RuntimeError("Flujo fallido sin llegar al sumidero")
                break
            
            # Reparte los eventos entre las salidas de forma circular.
            nodo_actual = nodo_actual.siguiente_destino()

        return recorrido