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