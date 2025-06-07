#lIBRERIAS E IMPORTACIÓN DE OTROS ARCHIVOS .PY
import flet as ft
import random
from tasks import crear_lista_tareas
from notas import crear_zona_notas
from telmi import telmi_ai

def main(page: ft.Page):
    # GENERAL
    page.bgcolor = "#F0F4F8"
    page.title = "Telematics Study Tool"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30
    page.spacing = 30
    page.window.width = 800
    page.window.height = 600
    page.window.resizable = True

    # Fuentes
    page.fonts = {
        "Nunito": "fonts/Nunito-Black.ttf",
        "OS": "fonts/OpenSans-Regular.ttf"
    }
    page.theme = ft.Theme(font_family="Nunito")

    # Estilo para botones
    estilo_botones = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=6),
        bgcolor="#4F46E5",
        color=ft.Colors.WHITE,
        overlay_color="#6366F1"
    )

    # Frases motivadoras
    frases = [
        "¡Tú puedes con esto! 💪",
        "Un paso a la vez. ✨",
        "Confía en tu proceso.",
        "¡Eres más capaz de lo que crees!",
        "Sigue adelante, incluso si es lento. 🐢"
    ]

    # NOTAS
    notas = crear_zona_notas(page, estilo_botones)

    # Función para mostrar la pantalla de inicio
    def mostrar_inicio(e):
        page.clean()

        cabecera = ft.Column(
            controls=[
                ft.Text(
                    "Telematics Study Tool",
                    size=40,
                    color="#3B5BDB",
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Tu espacio de estudio organizado y motivador",
                    size=18,
                    color="#6279D2",
                    italic=True,
                ),
            ],
            spacing=2,
            horizontal_alignment="center",
        )

        telmi_imagen = ft.Image(src="telmiclon.jpg", width=60, height=60)

        frase_motivadora = ft.Text(
            random.choice(frases),
            italic=True,
            color=ft.Colors.BLUE_GREY_700,
            size=16
        )

        frase_con_telmi = ft.Row(
            controls=[
                telmi_imagen,
                ft.Container(
                    content=frase_motivadora,
                    padding=10,
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=10,
                    expand=True
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        )

        accesos_rapidos = ft.Column(
            controls=[
                ft.ElevatedButton(icon=ft.Icons.PSYCHOLOGY, text="Telmi", on_click=change_telmi, style=estilo_botones),
                ft.ElevatedButton(icon=ft.Icons.TIMER, text="Pomodoro", on_click=change_study, style=estilo_botones),
                ft.ElevatedButton(icon=ft.Icons.DRAW, text="Pizarra", on_click=change_maps, style=estilo_botones)
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.START
        )

        derecha = ft.Column(controls=[frase_con_telmi, accesos_rapidos], spacing=30, expand=True)
        izquierda = ft.Column(controls=[notas], spacing=10, expand=True)

        contenido = ft.Row(controls=[izquierda, derecha], spacing=30, expand=True)

        page.add(cabecera, contenido, navigation_bar)
        page.update()

    # Selección Pomodoro
    def change_study(e):
        page.clean()
        modo = ft.Text("Elige la modalidad pomodoro", size=40, color="#3B5BDB", weight=ft.FontWeight.BOLD)

        simple = ft.ElevatedButton(
            content=ft.Column([
                ft.Image(src="pomsim.png", width=150, height=150),
                ft.Text("Pomodoro + Lista de Tareas", color="#3B5BDB", text_align="center")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            on_click=simple_pom,
            style=estilo_botones,
            width=220,
            height=250
        )

        adv = ft.ElevatedButton(
            content=ft.Column([
                ft.Image(src="pomsim.png", width=150, height=150),
                ft.Text("Pomodoro + Lista de Tareas + Planificación", color="#3B5BDB", text_align="center")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            on_click=simple_pom,  # Aquí puedes cambiar si tienes otra función para el modo avanzado
            style=estilo_botones,
            width=220,
            height=250
        )

        fila_modos = ft.Row(controls=[simple, adv], alignment="center", expand=True)

        page.add(modo, fila_modos, navigation_bar)
        page.update()

    # Lista de Pomodoro Simple
    def simple_pom(e):
        page.clean()
        lista_tareas_ui = crear_lista_tareas(page, change_study)
        page.add(lista_tareas_ui, navigation_bar)
        page.update()

    # Telmi IA
    def change_telmi(e):
        page.clean()
        telmi_widget = telmi_ai(page)
        page.add(telmi_widget, navigation_bar)
        page.update()

    # PIZARRA
    def change_maps(e):
        page.clean()
        piza = ft.Text("PIZARRA", size=30, color="#3B5BDB", weight=ft.FontWeight.BOLD)
        page.add(piza, navigation_bar)
        page.update()

    # Barra de navegación
    def on_navigation_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            mostrar_inicio(None)
        elif selected_index == 1:
            change_study(None)
        elif selected_index == 2:
            change_telmi(None)
        elif selected_index == 3:
            change_maps(None)

    navigation_bar = ft.NavigationBar(
        selected_index=0,
        on_change=on_navigation_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Inicio"),
            ft.NavigationBarDestination(icon=ft.Icons.TIMER, label="Pomodoro"),
            ft.NavigationBarDestination(icon=ft.Icons.PSYCHOLOGY, label="Telmi"),
            ft.NavigationBarDestination(icon=ft.Icons.DRAW, label="Pizarra")
        ],
        bgcolor="#E0E7FF",
        indicator_color="#4338CA"
    )

    # Inicio mostrando la pantalla principal
    mostrar_inicio(None)

# Ejecutar la aplicación
ft.app(target=main, assets_dir="assets")
