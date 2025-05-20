import flet as ft
import random
from tasks import crear_lista_tareas
from notas import crear_zona_notas

def main(page: ft.Page):
 #Información básica
    page.bgcolor = ft.Colors.WHITE
    page.title = "Telematics Study Tool"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding=30
    page.spacing=30
    page.window.width=800
    page.window.height=600
    page.window.resizable=True

    estilo_botones = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4), bgcolor=ft.Colors.SECONDARY_CONTAINER)

    def on_navigation_change(e):
        selected_index=e.control.selected_index
        if selected_index == 0:
            mostrar_inicio(None)
        elif selected_index == 1:
            change_study(None)
        elif selected_index == 2:
            change_telmi(None)
        elif selected_index == 3:
            change_maps(None)
    
    navigation_bar= ft.NavigationBar(
        selected_index=0,
        on_change=on_navigation_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Inicio"),
            ft.NavigationBarDestination(icon=ft.Icons.TIMER, label="Pomodoro"),
            ft.NavigationBarDestination(icon=ft.Icons.PSYCHOLOGY, label="Telmi"),
            ft.NavigationBarDestination(icon=ft.Icons.DRAW, label="Pizarra")],
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            indicator_color=ft.Colors.BLUE_700
    )

    frases = [
            "¡Tú puedes con esto! 💪",
            "Un paso a la vez. ✨",
            "Confía en tu proceso.",
            "¡Eres más capaz de lo que crees!",
            "Sigue adelante, incluso si es lento. 🐢"
          ]
    
    notas = crear_zona_notas(page, estilo_botones)

      #Esta es la página prinicipal
    def mostrar_inicio(e):
        page.clean()
    
        titulo = ft.Text("Telematics Study Tool",
                     size=40, color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD)
        telmi_imagen = ft.Image(src="telmiclon.jpg", width=60, height=60)

        frase_motivadora = ft.Text(
            random.choice(frases),
            italic=True,
            color=ft.Colors.BLUE_GREY_700,
            size=16)

        frase_con_telmi = ft.Row(
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


ft.app(target=main, assets_dir="assets")
