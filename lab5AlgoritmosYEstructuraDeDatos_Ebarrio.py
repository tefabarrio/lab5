import simpy
import random
import math
import statistics

env = simpy.Environment()
num =[25,50,100,200] # Cantidad de procesos a realizar
Intervalo = 10# Intervalo de los procesos
InstruccionesCPU = 6  # Cuantas instrucciones realiza el CPU por unidad de tiempo
TiempoOperacionInOut = 1  # Tiempo de operacion I/O
TiemposDeProcesos = []  # Lista para almacenar tiempos
random.seed(15) 
RAM = simpy.Container(env, init=200, capacity=200)
CPU = simpy.Resource(env, capacity=1)

class Proceso:

    def __init__(self, id, no, env):
        # Atributos del proceso
        self.id = id
        self.no = no
        self.instrucciones = random.randint(1, 10)
        self.memoria_necesaria = random.randint(1, 10)
        self.env = env
        self.terminated = False
        self.createdTime = 0
        self.finishedTime = 0
        self.totalTime = 0
        self.proceso = env.process(self.procesar(env))

    def procesar(self, env):
        inicio = env.now
        self.createdTime = inicio
        #Se crea el proceso
        print(str(self.id),": Creado en", str(inicio),"(Estado: new)")
        #Se pide RAM
        with RAM.get(self.memoria_necesaria) as getRam:
            yield getRam
            #Nos indica el orden sobre que va despues de running
            siguiente = 0  
            while not self.terminated:\
                #Se asegura de pedir el CPU hasta que termine
                with CPU.request() as req:
                    yield req

                    #Inicio uso de CPU
                    for i in range(InstruccionesCPU):  #El numero de operaciones a realizar del proceso
                        if self.instrucciones > 0:
                            self.instrucciones -= 1 
                            siguiente = random.randint(1, 2)  #Indica si va a seguir operando las instrucciones o va a esperar
                    yield env.timeout(1)  

                    #Inicio proceso I/O
                    if siguiente == 1:
                        yield env.timeout(TiempoOperacionInOut)

                    if self.instrucciones == 0:
                        self.terminated = True  #En caso de que se terminen las instrucciones por completar

            print(str(self.id),": Terminado en ", str(env.now),"(Estado: Terminated)")
            RAM.put(self.memoria_necesaria)  #Regresa la RAM que se utilizo
        fin = env.now
        self.finishedTime = fin  # Termina
        self.totalTime = int(self.finishedTime - self.createdTime)  # Se obtiene el tiempo en que cada proceso estuvo en la computadora
        TiemposDeProcesos.append(self.totalTime)


# Generador de procesos
def generador_de_procesos(env):
    for i in range(num_de_procesos):
        tiempo_creacion = math.exp(1.0/Intervalo)
        Proceso('Proceso %d' % i, i, env)
        yield env.timeout(tiempo_creacion)  
def prome(s):
    prom=0
    suma=0
    for i in range(len(s)):
        suma=suma+int(s[i])
    prom=float(suma/int(len(s)))
    return prom       
lista2=[]
for i in range(4):
    num_de_procesos=num[i]
    print('Numero de procesos: ', str(num_de_procesos))
    env.process(generador_de_procesos(env))  
    env.run()
    promedio = prome(TiemposDeProcesos)
    lista2.append([num_de_procesos,promedio])
    varianza = statistics.variance(TiemposDeProcesos,promedio)
    print("El tiempo promedio en que se lleva acabo un proceso para un simulacion con ",str(len(TiemposDeProcesos))," procesos es de: ", str(promedio), " y la varianza es: ", str(varianza))
    print('--------------------------------------------------------------------------------')
print(lista2)
    
    


