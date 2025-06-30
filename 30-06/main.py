import flet as ft
from pomsim import pomodoro
from notas import crear_zona_notas
from telmi import telmi_ai, widget_frase_motivadora

def main(page: ft.Page):
    # GENERAL
    page.bgcolor = "#0A1E3F"
    page.title = "Telematics Study Tool"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 24
    page.spacing = 24
    page.window.width = 1100
    page.window.height = 700
    page.window.resizable = True

    # Fuentes
    page.fonts = {
        "Nunitoblack": "fonts/Nunito-Black.ttf",
        "Nunitoregular": "fonts/Nunito-Regular.ttf",
        "Nunitobold": "fonts/Nunito-SemiBold.ttf",
        "OS": "fonts/OpenSans-Regular.ttf"
    }
    page.theme = ft.Theme(
        font_family="Nunito",
        text_theme=ft.TextTheme(
            body_large=ft.TextStyle(font_family="Nunitoregular",size=18, color="#E0E7FF", weight=ft.FontWeight.W_500),
            body_medium=ft.TextStyle(font_family="Nunitoregular",size=16, color="#CBD5E1"),
            title_large=ft.TextStyle(font_family="Nunitoblack",size=40, color="#A5B4FC", weight=ft.FontWeight.W_700),
            title_medium=ft.TextStyle(font_family="Nunitobold",size=24, color="#C7D2FE", weight=ft.FontWeight.W_600)
        ),
        use_material3=True
    )

    # Estilo para botones
    estilo_botones = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=12),
        bgcolor="#4F46E5",
        color="#F1F5F9",
        overlay_color="#6366F1",
        elevation=4,
        shadow_color="#4F46E550",
        padding=ft.padding.all(20)   )

    # NOTAS
    notas = crear_zona_notas(page, estilo_botones)

    # Función para mostrar la pantalla de inicio
    def mostrar_inicio(e):
        page.clean()

        cabecera = ft.Column(
            controls=[
                ft.Text("Telematics Study Tool", style=page.theme.text_theme.title_large),
                ft.Text("Tu espacio de estudio organizado y motivador",
                        style=page.theme.text_theme.body_medium,
                        italic=True)
            ],
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        telmi_imagen = ft.Container(
            width=100,
            height=100,
            border_radius=100,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Image(src="telmifr.png", fit=ft.ImageFit.COVER),
            shadow=ft.BoxShadow(
            color="#1E40AF", blur_radius=10, offset=ft.Offset(0, 4)
            ))

        frase_con_telmi = ft.Row(
            controls=[
                telmi_imagen,
                widget_frase_motivadora(page)
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        accesos_rapidos = ft.Column(
            controls=[
                ft.ElevatedButton(
                    icon=ft.Icons.PSYCHOLOGY,
                    text="Telmi",
                    on_click=change_telmi,
                    style=estilo_botones,
                    width=200,
                    height=60,
                ),
                ft.ElevatedButton(
                    icon=ft.Icons.TIMER,
                    text="Pomodoro",
                    on_click=change_study,
                    style=estilo_botones,
                    width=200,
                    height=60,
                ),
                ft.ElevatedButton(
                    icon=ft.Icons.DRAW,
                    text="Pizarra",
                    on_click=change_maps,
                    style=estilo_botones,
                    width=200,
                    height=60,
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
        )

        derecha = ft.Column(controls=[frase_con_telmi, accesos_rapidos], spacing=36, expand=True)
        izquierda = ft.Column(controls=[notas], spacing=20, expand=True)

        contenido = ft.Row(controls=[izquierda, derecha], spacing=36, expand=True)

        page.add(cabecera, contenido, navigation_bar)
        page.update()

    # Selección Pomodoro
    def change_study(e):
        page.clean()
        modo = ft.Text("Elige la modalidad pomodoro", size=60, color="#A5B4FC", weight=ft.FontWeight.W_700)

        simple = ft.ElevatedButton(
            content=ft.Column([
                ft.Image(src="pomsim.png", width=300, height=300),
                ft.Text("Pomodoro + Lista de Tareas", color="#F1F5F9", text_align="center")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            on_click=simple_pom,
            style=estilo_botones,
            width=440,
            height=500
        )

        adv = ft.ElevatedButton(
            content=ft.Column([
                ft.Image(src="pomsim.png", width=300, height=300),
                ft.Text("Pomodoro + Lista de Tareas + Planificación", color="#F1F5F9", text_align="center")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            on_click=simple_pom,  # Puedes cambiar esto si tienes otra función para modo avanzado
            style=estilo_botones,
            width=440,
            height=500
        )

        fila_modos = ft.Row(controls=[simple, adv], alignment="center", expand=True)

        page.add(modo, fila_modos, navigation_bar)
        page.update()

    # Pomodoro Simple
    def simple_pom(e):
        page.clean()
        simple = pomodoro(page)
        page.add(simple, navigation_bar)
        page.update()

    # Telmi IA
    def change_telmi(e):
        page.clean()
        telmi_widget = telmi_ai(page)
        page.add(telmi_widget, navigation_bar)
        page.update()

    # Pizarra
    def change_maps(e):
        page.clean()
        piza = ft.Text("PIZARRA", size=30, color="#A5B4FC", weight=ft.FontWeight.W_700)
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
        bgcolor="#1E40AF",
        indicator_color="#818CF8",
        elevation=8,
        height=60,
    )

    # Inicio mostrando la pantalla principal
    mostrar_inicio(None)

ft.app(target=main, assets_dir="assets")
