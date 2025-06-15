import time


print("POMODORO EN  PYTHON ")
pom_w = True
while pom_w:
    work_min = int(input("Ingrese tiempo de minutos de trabajo: "))
    restante_min = work_min
    primer = work_min
    work_s = 0
    print(f"La duracion de su temporizador de trabajo es de {work_min} minutos y {work_s} segundos, ¿Desea modificarla? (y/n)", end = "\n")
    try:
        pom_election = input()
        pom_e = pom_election.lower()
        if pom_e == "y":
            pom_w = True
            
        elif  pom_e == "n":
            pom_w = False
        else: 
            print("Solo se aceptan dos opciones (y/n), recuerda que y = Aceptar y n = Denegar")
    except:
        print("Ingresa un valor valido")


pom_d = not pom_w
while pom_d:
    rest_min = int(input("Ingrese tiempo de descanso en minutos: "))
       
    rest_s = 0
    print(f"La duracion de su temporizador de descanso de {rest_min} minutos y {rest_s} segundos, ¿Desea modificarla? (y/n)", end = "\n")
    try:
        pom_election2 = input()
        pom_e2 = pom_election2.lower()
        if pom_e2 == "y":
            pom_d = True        
        elif  pom_e == "n":
            pom_d = False
        else: 
            print("Solo se aceptan dos opciones (y/n), recuerda que y = Aceptar y n = Denegar")
    except:
        print("Ingresa un valor valido")
"""

Ingreso de valores del temporizador, de descanso y trbajo

"""

    
    
for i in range (0, work_min + 1): #recorre minuto a minuto
     
    if restante_min != 0: #Activa cuenta regresiva
        segundos = 59
        sec = segundos
        
        if restante_min == primer:
            print(f"Quedan {restante_min} minutos y {0} segundos")
            time.sleep(1)
        for a in range(0, segundos + 1):
            print(f"Quedan {restante_min-1} minutos y {sec} segundos")
            time.sleep(1)
            sec -=1
        restante_min -= 1


        print("Comienza tu descanso")
#Demporizador de descanso



restante_min = rest_min
primer = rest_min
for a in range (0, work_min + 1): #recorre minuto a minuto
     
    if restante_min != 0: #Activa cuenta regresiva
        segundos = 59
        sec = segundos
        
        if restante_min == primer:
            print(f"Quedan {restante_min} minutos y {0} segundos")
            time.sleep(1)
        for b in range(0, segundos + 1):
            print(f"Quedan {restante_min-1} minutos y {sec} segundos")
            time.sleep(1)
            sec -=1
        restante_min -= 1


"""
rest_min_final = int((rest_min * 60 + rest_s) / 60)

rest_s_final = int(((((rest_min * 60 + rest_s) / 60) - rest_min_final) * 60)) # segundos totales de descanso
print(f"{rest_min_final}:{rest_s_final}")















while rest_min_final > 0:
    segundos = 60
    
    
    for a in range (0, rest_min + 1): #recorre minuto a minuto
     
        if rest_min_final != 0: #Activa cuenta regresiva
            segundos = 59
            sec = segundos
        
            if rest_min_final == rest_min:
                print(f"Quedan {restante_min} minutos y {0} segundos")
                time.sleep(1)
            for a in range(0, segundos + 1):
                print(f"Quedan {restante_min-1} minutos y {sec} segundos")
                time.sleep(1)
                sec -=1
            rest_min_final -= 1

print("ha terminado")
"""        
            
        
        
        




            
    


    

