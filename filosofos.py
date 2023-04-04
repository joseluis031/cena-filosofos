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
from tkinter import *
class ventana():
    def __init__(self):
         
        self.estado_filosofos = []
        self.estado_tenedores = []
        self.logs = []
        self.filosofos = []
        self.root = Tk()
        self.root.title("FILOSOFOS")
        self.root.geometry("800x600")
        self.root.resizable(0,0)
        self.root.config(bg= "black")
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.root.mainloop()
    
    def logs(self, texto):
        self.logs.append(Tk.Label(self.root, text=texto, bg="black", fg="white"))
        self.logs[-1].place(x=10, y=10+20*len(self.logs))
        self.root.update()
    
    def estado_filosofo(self, i):
        self.estado_filosofos.append(Tk.Label(self.root, text="FILOSOFO {}".format(i), bg="white", fg="black"))
        self.estado_filosofos[-1].place(x=10+100*i, y=10)
        self.root.update()
        
    def estado_tenedor(self, i):
        self.estado_tenedores.append(Tk.Label(self.root, text="Tenedor {}".format(i), bg="white", fg="black"))
        self.estado_tenedores[-1].place(x=10+100*i, y=40)
        self.root.update()
        
    def cerrar(self):
        for i in self.filosofos:
            del i
        self.root.destroy()
    
    def iniciar(self):
        for i in range(N):
            self.estado_filosofo(i)
            self.estado_tenedor(i)
        for i in range(N):
            self.filosofos.append(filosofo(self))
            self.filosofos[-1].start()
        self.root.mainloop()
        
if __name__ == "__main__":
    v = ventana()
    v.iniciar()


