#Librerias
import flet as ft 
import random
from tasks import crear_lista_tareas
from notas import crear_zona_notas


def main(page: ft.Page):
 
 #Información básica
    page.bgcolor = ft.Colors.WHITE   #Color de fondo
    page.title = "Telematics Study Tool"   #Título del programa
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER        #Hace que todos los elementos se centren en el centro.
    page.padding=30       #Espacio entre los elementos y el borde del programa.
    page.spacing=30       #Espacio entre los elementos.
    page.window.width=800   #Ancho y Alto de la ventana del programa.
    page.window.height=600
    page.window.resizable=True   #Hace que el usuario pueda agrandar la ventana del programa.

    estilo_botones = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4), bgcolor=ft.Colors.SECONDARY_CONTAINER)   #Una variable que guarda el estilo de la mayoría de botones, lo pueden usar si quieren. :D
    #Hace que el botón tenga un borde levemente circular, pero manteniendo su forma rectangular, bgcolor igual es el fondo DEL BOTÓN.

    def on_navigation_change(e):     #Función que hará que la barra de navegación cambie de contenido en la ventana.
        selected_index=e.control.selected_index
        if selected_index == 0:    #Si es que se elige "Home" en el programa, pues se irá al inicio del programa.
            mostrar_inicio(None)     
        elif selected_index == 1:    #Lo mismo, pero este muestra la elección de modos de pomodoro. 
            change_study(None)
        elif selected_index == 2:     #Muestra Chat de Telmi.
            change_telmi(None)
        elif selected_index == 3:       #Muestra pizarra
            change_maps(None)
    
    navigation_bar= ft.NavigationBar(   #La barra de navegación en si, está guardada en una variable llamada navigation_bar para poder incorporarla rápidamente.
        selected_index=0,         #la index "0" es el inicio del programa, en si, mostrar_inicio.
        on_change=on_navigation_change,  #Al hacer click en alguno de los iconos de la barra de navegación, se llama a la función que creamos arriba, que se encarga de cambiar el contenido del programa.
        destinations=[         #Cuáles son los destinos a los que llevará la barra de navegación.
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Inicio"),            #Destino de barra de navegación, que contiene un icono de una casita, y texto.
            ft.NavigationBarDestination(icon=ft.Icons.TIMER, label="Pomodoro"),         #Lo mismo, pero para el pomodoro.
            ft.NavigationBarDestination(icon=ft.Icons.PSYCHOLOGY, label="Telmi"),       #Telmi
            ft.NavigationBarDestination(icon=ft.Icons.DRAW, label="Pizarra")],          #Pizarra
            bgcolor=ft.Colors.SECONDARY_CONTAINER,                                      #Color de fondo de la barra.
            indicator_color=ft.Colors.BLUE_700                                          #No sé como explicar este, pero es el color de fondo del botón del icono y el texto.
    )

    frases = [                                    #Variable que guarda strings con las frases que dice telmi.
            "¡Tú puedes con esto! 💪",
            "Un paso a la vez. ✨",
            "Confía en tu proceso.",
            "¡Eres más capaz de lo que crees!",
            "Sigue adelante, incluso si es lento. 🐢"
          ]
    
    notas = crear_zona_notas(page, estilo_botones)             #Aquí agrego una variable que guardará la función que está en el archivo notas.py 

      #Esta es la página prinicipal
    def mostrar_inicio(e):
        page.clean()      #Limpia todo lo que aparece en pantalla.
    
        titulo = ft.Text("Telematics Study Tool",     #Agrega un texto en una variable.
                     size=40, color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD)    #Tamaño 40, color, y grueso del texto.
        telmi_imagen = ft.Image(src="telmiclon.jpg", width=60, height=60)    #Agrega Imagen en una variable, src agrega QUÉ imagen(telmiclon.jpg) de la carpeta de assets, ancho y alto. 

        frase_motivadora = ft.Text( 
            random.choice(frases),
            italic=True,
            color=ft.Colors.BLUE_GREY_700,
            size=16)

        frase_con_telmi = ft.Row(        #Decoración para la frases de telmi
            controls=[
                telmi_imagen,
                ft.Container(
                    content=frase_motivadora,
                    padding=10,
                    bgcolor=ft.Colors.BLUE_100,
                    border_radius=10
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10)

    # Botones verticales
        accesos_rapidos = ft.Column(
            controls=[
            ft.ElevatedButton(
                icon=ft.Icons.PSYCHOLOGY,
                text="Telmi",
                on_click=change_telmi,
                style=estilo_botones
            ),
            ft.ElevatedButton(
                icon=ft.Icons.TIMER,
                text="Pomodoro",
                on_click=change_study,
                style=estilo_botones
            ),
            ft.ElevatedButton(
                icon=ft.Icons.DRAW,
                text="Pizarra",
                on_click=change_maps,
                style=estilo_botones
            )
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=10)

    # Parte derecha (frase + botones)
        derecha = ft.Column(
        controls=[frase_con_telmi, accesos_rapidos],
        spacing=20,
        expand=True)

    # Parte izquierda: Notas rápidas
        izquierda = ft.Column(
        controls=[notas],
        spacing=10,
        expand=True)
    # Fila principal que contiene izquierda y derecha
        contenido = ft.Row(
        controls=[izquierda, derecha],
        spacing=30,
        expand=True)

        page.add(titulo, contenido, navigation_bar)
        page.update()


       #Lleva a la página de elegir modalidad de Pomodoro
    def change_study(e):
        page.clean()
        modo = ft.Text("Elige la modalidad pomodoro",
                       size=40, color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD)
        simple = ft.ElevatedButton(content=ft.Column([
                                       ft.Image(src="pomsim.png",width=150, height=150),
                                       ft.Text("Pomodoro + Lista de Tareas", color=ft.Colors.BLUE_700, text_align="center")
                                   ],
                                   alignment=ft.MainAxisAlignment.CENTER,
                                   horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                   on_click=simple_pom, style=estilo_botones, width=220, height= 250)
        adv = ft.ElevatedButton(content=ft.Column([
                                       ft.Image(src="pomsim.png",width=150, height=150),
                                       ft.Text("Pomodoro + Lista de Tareas + Planificación", color=ft.Colors.BLUE_700, text_align="center")
                                   ],
                                   alignment=ft.MainAxisAlignment.CENTER,
                                   horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                   on_click=simple_pom, style=estilo_botones, width=220, height= 250)
                              
        fila_modos=ft.Row(
            controls=[simple, adv],
            alignment="center",
            expand=True)
        page.add(modo, fila_modos, navigation_bar)
        page.update()

    #Pomodoro Simple
    def simple_pom(e):
        page.clean()
        
        #LISTA DE TAREAS
        lista_tareas_ui = crear_lista_tareas(page, change_study)
        page.add(lista_tareas_ui, navigation_bar)
        page.update()


    #Lleva a la página de la IA
    def change_telmi(e):
        page.clean()
        wait = ft.Text("IA")
        page.add(wait, navigation_bar)
        page.update()

    #LLeva a la página de la pizarra      
    def change_maps(e):
        page.clean()
        piza = ft.Text("PIZARRA")
        page.add(piza, navigation_bar)
        page.update()



    #Muestra la pantalla principal 
    mostrar_inicio(None)


ft.app(target=main, assets_dir="assets")   #ft.app corre el programa y todo lo que este en el archivo main.py, también dice que todos los elementos visuales están en la carpeta de "assets" (Imagenes, sonidos en el futuro tal vez, etc)
