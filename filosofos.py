import time
import threading
import random


N = 5

Max = 2

class filosofo(threading.Thread):
    semaforo = threading.Lock()
    estado = []
    tenedores = []
    count=0
    
    def __init__(self, ventana):
        super().__init__()
        self.ventana=ventana
        self.id=filosofo.count
        filosofo.count+=1
        self.veces= 0
        filosofo.estado.append('PENSANDO')
        filosofo.tenedores.append(threading.Semaphore(0))
        self.ventana.logs("FILOSOFO {} - PENSANDO".format(self.id))
        
    def __del__(self):
        self.ventana.logs("FILOSOFO {} - TERMINA de comer".format(self.id))
    
    def pensar(self):
        time.sleep(random.randint(0,5))
    
    def derecha(self,i):
        return (i-1)%N
    
    def izquierda(self,i):
        return(i+1)%N
    
    def verificar(self,i):
        if filosofo.estado[i] == 'HAMBRIENTO' and filosofo.estado[self.izquierda(i)] != 'COMIENDO' and filosofo.estado[self.derecha(i)] != 'COMIENDO':
            filosofo.estado[i]='COMIENDO'
            filosofo.tenedores[i].release()
            
    def tomar(self):
        filosofo.semaforo.acquire()
        filosofo.estado[self.id] = 'HAMBRIENTO'
        self.verificar(self.id)
        filosofo.semaforo.release()
        filosofo.tenedores[self.id].acquire()
    
    def soltar(self):
        filosofo.semaforo.acquire()
        filosofo.estado[self.id] = 'PENSANDO'
        self.ventana.estado_filosofos[self.id].config(bg= "white")
        self.verificar(self.izquierda(self.id))
        self.verificar(self.derecha(self.id))
        filosofo.semaforo.release()
        
    def comer(self):
    
        self.ventana.logs("FILOSOFO {} COMIENDO".format(self.id))
        self.ventana.estado_filosofos[self.id].config(bg= "yellow")
        self.ventana.estado_tenedores[self.id].config(bg= "green")
        time.sleep(random.randint(0,5))
        self.ventana.estado_filosofos[self.id].config(bg= "white")
        self.ventana.estado_tenedores[self.id].config(bg= "white")
        self.ventana.logs("FILOSOFO {} TERMINA de comer".format(self.id))
        
    def run(self):
        
        while self.veces < Max:
            self.pensar()
            self.tomar()
            self.comer()
            self.soltar()
            self.veces+=1
        del self
        
        