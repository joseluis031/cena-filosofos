# cena-filosofos

El link de este repositorio es el siguiente: [GitHub](https://github.com/joseluis031/cena-filosofos.git)

## Codigo del ejercicio

```
#importo librerias
import time
import threading
import random
import tkinter as tk

N = 5   #Numero de filosofos

Max = 2 #Numero de veces maximo que van a comer cada filosofo

class filosofo(threading.Thread):     
    semaforo = threading.Lock() 
    estado = []     #Lista de estados de los filosofos
    tenedores = []      #Lista de semaforos
    count=0     #Contador de filosofos
    
    def __init__(self, ventana):        #Funcion para inicializar el filosofo  
        super().__init__()
        self.ventana=ventana
        self.id=filosofo.count
        filosofo.count+=1
        self.veces= 0
        filosofo.estado.append('PENSANDO')      #Se inicializa el estado del filosofo como pensando
        filosofo.tenedores.append(threading.Semaphore(0))
        self.ventana.logs("FILOSOFO {} - PENSANDO".format(self.id))   #Se imprime en la ventana que el filosofo esta pensando
        
    def __del__(self):  #Funcion para que el filosofo se vaya de la mesa
        self.ventana.logs("FILOSOFO {} - TERMINA de comer".format(self.id))
    
    def pensar(self): #Funcion para que el filosofo piense
        time.sleep(random.randint(0,5))
    
    def derecha(self,i):    #Funcion para saber el filosofo de la derecha    
        return (i-1)%N
    
    def izquierda(self,i):  #Funcion para saber el filosofo de la izquierda
        return(i+1)%N
    
    def verificar(self,i):  #Funcion para verificar si el filosofo puede comer
        if filosofo.estado[i] == 'HAMBRIENTO' and filosofo.estado[self.izquierda(i)] != 'COMIENDO' and filosofo.estado[self.derecha(i)] != 'COMIENDO':      
            filosofo.estado[i]='COMIENDO'   #Si el filosofo puede comer, se cambia su estado a comiendo
            filosofo.tenedores[i].release()
            
    def tomar(self):    #Funcion para que el filosofo tome los tenedores
        filosofo.semaforo.acquire()
        filosofo.estado[self.id] = 'HAMBRIENTO' #Se cambia el estado del filosofo a hambriento
        self.verificar(self.id) #Se verifica si el filosofo puede comer
        filosofo.semaforo.release()     
        filosofo.tenedores[self.id].acquire()
    
    def soltar(self):   #Funcion para que el filosofo suelte los tenedores
        filosofo.semaforo.acquire() 
        filosofo.estado[self.id] = 'PENSANDO'   #Se cambia el estado del filosofo a pensando
        self.ventana.estado_filosofos[self.id].config(bg= "white")
        self.verificar(self.izquierda(self.id))
        self.verificar(self.derecha(self.id))
        filosofo.semaforo.release()
        
    def comer(self):    #Funcion para que el filosofo coma
    
        self.ventana.logs("FILOSOFO {} COMIENDO".format(self.id))   #Se imprime en la ventana que el filosofo esta comiendo
        self.ventana.estado_filosofos[self.id].config(bg= "red")
        self.ventana.estado_tenedores[self.id].config(bg= "blue")
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

class Ventana():    #Clase para la ventana
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
        
        
        
    def info(self): #Funcion para mostrar la informacion de la ventana
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
        
        tk.Canvas(self.ventana, width= 50, height= 50, bg= "red").place(x= 600, y= 350)
        tk.Canvas(self.ventana, width= 50, height= 50, bg= "white").place(x= 600, y= 400)
        
        
        tk.Canvas(self.ventana, width= 50, height= 50, bg= "blue").place(x= 600, y= 450)
        tk.Canvas(self.ventana, width= 50, height= 50, bg= "white").place(x= 600, y= 500)
    
    def logs(self, texto):  #Funcion para imprimir en la ventana
        self.texto.insert(tk.END, str(texto) + "\n")
        
    def mainloop(self): #Funcion para que la ventana se mantenga abierta
        self.ventana.mainloop()
```

## Codigo del main

```
if __name__ == "__main__":
    from filosofos import *
    ventana = Ventana()
    filosofos = []  
    for i in range(N):  
        filosofos.append(filosofo(ventana))
    for i in range(N):
        filosofos[i].start()
    ventana.mainloop()
    
    for i in range(N):
        filosofos[i].join()
```


## Ejecucion del codigo

![Captura de pantalla 2023-04-24 213953](https://user-images.githubusercontent.com/91721888/234099082-c3aa8985-4e4c-4395-ab88-6f6ac1876d00.png)
