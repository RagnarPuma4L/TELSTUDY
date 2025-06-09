import time

print("POMODORO EN  PYTHON ")

pom_w = True
while pom_w:
    work_min = int(input("Ingrese tiempo de minutos de trabajo: "))
    work_s = int(input("Ingrese segundos de trabajo: "))
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
    rest_s = int(input("Ingrese el tiempo de descanso en segundos: "))
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
