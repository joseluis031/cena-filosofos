#codigo cena de los filosofos

from visual import *
from visual.graph import *
from random import random
from time import sleep
import threading
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
g = gdisplay(x=0, y=0, width=600, height=600, title='Filosofos', xtitle='x', ytitle='y', ztitle='z', foreground=color.black, background=color.white)
scene = display(x=600, y=0, width=600, height=600, title='Filosofos', x=0, y=0, center=(0,0,0), background=(0.5,0.5,0.5))
scene.select()
scene.autoscale = 0

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


