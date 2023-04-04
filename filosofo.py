#codigo cena de los filosofos

from random import random
from time import sleep
import threading
from vpython import *

# Constantes
N = 5
T = 0.1
L = 0.5
R = 0.1
M = 0.1
H = 0.2
W = 0.2
D = 0.2
X = 0.5
Y = 0.5
Z = 0.5

# Variables
filosofos = []
tenedores = []
mesa = []

# Funciones
def crear_filosofos():
    global filosofos
    for i in range(N):
        filosofos.append(Filosofo(i))
    
def crear_tenedores():
    global tenedores
    for i in range(N):
        tenedores.append(Tenedor(i))

def crear_mesa():
    global mesa
    for i in range(N):
        mesa.append(threading.Semaphore(1))

def iniciar_filosofos():
    global filosofos
    for i in range(N):
        filosofos[i].start()

def dibujar_filosofos():
    global filosofos
    for i in range(N):
        filosofos[i].dibujar()

def dibujar_tenedores():
    global tenedores
    for i in range(N):
        tenedores[i].dibujar()

def dibujar_mesa():
    global mesa
    for i in range(N):
        mesa[i].dibujar()

def dibujar_todo():
    dibujar_filosofos()
    dibujar_tenedores()
    dibujar_mesa()
    
def pensar(filosofo):
    print('Filosofo', filosofo, 'pensando')
    sleep(random()*T)

def comer(filosofo):
    print('Filosofo', filosofo, 'comiendo')
    sleep(random()*T)

def tomar_tenedor(filosofo, tenedor):
    print('Filosofo', filosofo, 'tomando tenedor', tenedor)
    sleep(random()*T)
    
def soltar_tenedor(filosofo, tenedor):
    print('Filosofo', filosofo, 'soltando tenedor', tenedor)
    sleep(random()*T)

# Clases
class Filosofo(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id
        self.tenedor_izq = id
        self.tenedor_der = (id + 1) % N
        self.x = X * cos(2 * pi * id / N)
        self.y = Y * sin(2 * pi * id / N)
        self.z = Z
        self.esfera = sphere(pos=(self.x, self.y, self.z), radius=R, color=color.yellow)
        self.cilindro = cylinder(pos=(self.x, self.y, self.z))

        
    def run(self):
        while 1:
            pensar(self.id)
            mesa[self.tenedor_izq].acquire()
            tomar_tenedor(self.id, self.tenedor_izq)
            mesa[self.tenedor_der].acquire()
            tomar_tenedor(self.id, self.tenedor_der)
            comer(self.id)
            mesa[self.tenedor_izq].release()
            soltar_tenedor(self.id, self.tenedor_izq)
            mesa[self.tenedor_der].release()
            soltar_tenedor(self.id, self.tenedor_der)
            
    def dibujar(self):
        self.esfera.pos = (self.x, self.y, self.z)
        self.cilindro.pos = (self.x, self.y, self.z)
        self.label.pos = (self.x, self.y, self.z)
        self.label.text = str(self.id)
        
class Tenedor:


    def __init__(self, id):
        self.id = id
        self.x = X * cos(2 * pi * id / N)
        self.y = Y * sin(2 * pi * id / N)
        self.z = Z
        self.cubo = box(pos=(self.x, self.y, self.z), length=L, height=H, width=W, color=color.red)
        self.label = label(pos=(self.x, self.y, self.z), text=str(self.id), color=color.black, box=0, opacity=0)
        
    def dibujar(self):
        self.cubo.pos = (self.x, self.y, self.z)
        self.label.pos = (self.x, self.y, self.z)
        self.label.text = str(self.id)
        
class Mesa:
    def __init__(self, id):
        self.id = id
        self.x = X * cos(2 * pi * id / N)
        self.y = Y * sin(2 * pi * id / N)
        self.z = Z
        self.cubo = box(pos=(self.x, self.y, self.z), length=L, height=H, width=W, color=color.red)
        self.label = label(pos=(self.x, self.y, self.z), text=str(self.id), color=color.black, box=0, opacity=0)
        
    def dibujar(self):
        self.cubo.pos = (self.x, self.y, self.z)
        self.label.pos = (self.x, self.y, self.z)
        self.label.text = str(self.id)

# Main
crear_filosofos()
crear_tenedores()
crear_mesa()
iniciar_filosofos()
while 1:
    rate(10)
    dibujar_todo()

