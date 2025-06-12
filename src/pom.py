import flet as ft
import threading
import time

def main(page: ft.Page):
    page.title = "POMODOROOOO"
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.window.width = 800
    page.window.height = 600

    # Temporizador en formato mm:ss
    timer_display = ft.Text("00:00", size=70, weight="bold", color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER)

    # Inputs trabajo
    work_min_input = ft.TextField(label="Minutos de trabajo", width=200, input_filter=ft.NumbersOnlyInputFilter())
    work_sec_input = ft.TextField(label="Segundos de trabajo", width=200, input_filter=ft.NumbersOnlyInputFilter())

    # Inputs descanso
    rest_min_input = ft.TextField(label="Minutos de descanso", width=200, input_filter=ft.NumbersOnlyInputFilter())
    rest_sec_input = ft.TextField(label="Segundos de descanso", width=200, input_filter=ft.NumbersOnlyInputFilter())

    confirm_btn = ft.ElevatedButton(text="Confirmar tiempos")
    start_btn = ft.ElevatedButton(text="Iniciar", visible=True,
                                  style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=15),  #Siempre olvido esta tontera de cómo hacer los botones más redondos
                                    padding=20,
                                    text_style=ft.TextStyle(size=20),      
                                    bgcolor=ft.Colors.WHITE,
                                    color="#007BA7",
                                  ))

    output = ft.Text()

    state = {
        "work_min": 0,
        "work_sec": 0,
        "rest_min": 0,
        "rest_sec": 0
    }

    # FORMATO MINUTOS:SEGUNDOS
    def formato_tiempo(minutos, segundos):
        return f"{minutos:02d}:{segundos:02d}"

    def temporizador(minutos, segundos, mensaje):
        restante_min = minutos

        if segundos > 0:
            sec = segundos
            while sec > 0:
                timer_display.value = formato_tiempo(restante_min, sec)
                output.value = f"{mensaje} - Quedan {restante_min} minutos y {sec} segundos"
                page.update()
                time.sleep(1)
                sec -= 1

        while restante_min > 0:
            restante_min -= 1
            sec = 60
            while sec > 0:
                timer_display.value = formato_tiempo(restante_min, sec - 1)
                output.value = f"{mensaje} - Quedan {restante_min} minutos y {sec - 1} segundos"
                page.update()
                time.sleep(1)
                sec -= 1

    # LA FUNCIÓN PARA CONFIRMAR TIEMPOS
    def confirmar_tiempos(e):
        try:
            state["work_min"] = int(work_min_input.value)
            state["work_sec"] = int(work_sec_input.value)
            state["rest_min"] = int(rest_min_input.value)
            state["rest_sec"] = int(rest_sec_input.value)

            output.value = f"Trabajo: {formato_tiempo(state['work_min'], state['work_sec'])} | Descanso: {formato_tiempo(state['rest_min'], state['rest_sec'])}"
            start_btn.visible = True
            page.update()
        except ValueError:
            output.value = "Por favor ingresa números válidos"
            page.update()

    def iniciar_pomodoro(e):
        def tarea():
            output.value = ""
            page.update()
            temporizador(state["work_min"], state["work_sec"], "ESTUDIO")
            output.value = "Descansa :D"
            page.update()
            temporizador(state["rest_min"], state["rest_sec"], "DESCANSO")
            output.value = "¡Descanso terminado!"
            page.update()

        threading.Thread(target=tarea).start()

    confirm_btn.on_click = confirmar_tiempos
    start_btn.on_click = iniciar_pomodoro

    page.add(
        ft.Column([
            ft.Container(   #Mira esa belleza de código mish, column, container, column
                content=ft.Column([
                    timer_display,
                    start_btn
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                alignment=ft.alignment.center,
                width=350,
                height=200,
                bgcolor="#007BA7",
                padding=10,
                border_radius=10,
            ),
            ft.Text("Trabajo", size=16, weight="bold"),
            work_min_input,
            work_sec_input,
            ft.Text("Descanso", size=16, weight="bold"),
            rest_min_input,
            rest_sec_input,
            confirm_btn,
            output
        ])
    )

ft.app(target=main)

