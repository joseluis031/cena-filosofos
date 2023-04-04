import time
import threading
import random
import tkinter as tk

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

class Ventana():
    def __init__(self):
        self.ventana=tk.Tk()
        self.ventana.title("FILOSOFOS")
        
        self.texto = tk.Text(self.ventana, width= 50, height= 10)
        self.scroll = tk.Scrollbar(self.ventana)
        
        self.total_comidas = []
        self.estado_filosofos = []
        self.estado_tenedores = []
        
        self.info()
        
        self.texto.configure(yscrollcommand= self.scroll.set)
        self.texto.pack(side= tk.LEFT) 
        self.scroll.config(command= self.texto.yview)
        self.scroll.pack(side= tk.RIGHT, fill= tk.Y)
        
        
        
    def info(self):
        for i in range(N):
            
            
            label = tk.Label(self.ventana, text= "FILOSOFO {}".format(str(i)), width= 10)
            label.place(x= 350, y= 50 + 25*i)
            
            label2 = tk.Label(self.ventana, text= "Tenedor {}".format(str(i)), width= 10)
            label2.place(x=850, y= 250  + 25*i)
            
            
            self.estado_filosofos.append(label)
            self.estado_tenedores.append(label2)
            
        
        
        tk.Label(self.ventana, text= "Comiendo:").place(x= 430, y= 350)
        tk.Label(self.ventana, text= "Pensando:").place(x= 430, y= 400)
            
        tk.Label(self.ventana, text= "Tenedor ocupado:").place(x= 430, y= 450)
        tk.Label(self.ventana, text= "Tenedor libre:").place(x= 430, y= 500)
        
        tk.Canvas(self.ventana, width= 50, height= 50, bg= "yellow").place(x= 600, y= 350)
        tk.Canvas(self.ventana, width= 50, height= 50, bg= "white").place(x= 600, y= 400)
        
        
        tk.Canvas(self.ventana, width= 50, height= 50, bg= "green").place(x= 600, y= 450)
        tk.Canvas(self.ventana, width= 50, height= 50, bg= "white").place(x= 600, y= 500)
    
    def logs(self, texto):
        self.texto.insert(tk.END, str(texto) + "\n")
        
    def mainloop(self):
        self.ventana.mainloop()
        
if __name__ == "__main__":
    ventana = Ventana()
    filosofos = []
    for i in range(N):
        filosofos.append(filosofo(ventana))
    for i in range(N):
        filosofos[i].start()
    ventana.mainloop()
    
    for i in range(N):
        filosofos[i].join()