import flet as ft
import threading
import time
import json
import os

# Ruta del archivo JSON
HISTORIAL_FILE = "pomodoros.json"

def cargar_historial():
    if os.path.exists(HISTORIAL_FILE):
        try:
            with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("historial", [])
        except json.JSONDecodeError:
            return []
    return []

def guardar_historial(historial):
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        json.dump({"historial": historial}, f, indent=4)

def pomodoro(page: ft.Page):
    page.title = "Pomodoro con Historial"
    page.bgcolor = "#F1F9FB"
    page.padding = 40
    page.window_width = 1100
    page.window_height = 650

    azul = "#007BA7"
    celeste = "#00B8D4"
    gris_claro = "#E0F7FA"
    blanco = "#FFFFFF"
    gris_texto = "#444"

    timer_display = ft.Text("00:00", size=90, weight="bold", color="white")

    # Inputs
    work_min_input = ft.TextField(label="Minutos trabajo", width=150, input_filter=ft.NumbersOnlyInputFilter())
    work_sec_input = ft.TextField(label="Segundos trabajo", width=150, input_filter=ft.NumbersOnlyInputFilter())
    rest_min_input = ft.TextField(label="Minutos descanso", width=150, input_filter=ft.NumbersOnlyInputFilter())
    rest_sec_input = ft.TextField(label="Segundos descanso", width=150, input_filter=ft.NumbersOnlyInputFilter())

    confirm_btn = ft.ElevatedButton(
        text="Confirmar tiempos",
        style=ft.ButtonStyle(
            bgcolor=celeste,
            color="white",
            padding=ft.padding.symmetric(horizontal=25, vertical=15),
            shape=ft.RoundedRectangleBorder(radius=15),
            text_style=ft.TextStyle(size=17, weight=ft.FontWeight.BOLD)
        )
    )

    start_btn = ft.ElevatedButton(
        text="Iniciar Pomodoro",
        visible=True,
        style=ft.ButtonStyle(
            bgcolor="white",
            color=azul,
            padding=ft.padding.symmetric(horizontal=25, vertical=15),
            shape=ft.RoundedRectangleBorder(radius=15),
            text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
        )
    )

    output = ft.Text("", size=16, color=gris_texto)

    state = {
        "work_min": 0,
        "work_sec": 0,
        "rest_min": 0,
        "rest_sec": 0
    }

    historial_text = ft.Column([], spacing=8)

    def actualizar_historial_visual():
        historial = cargar_historial()
        historial_text.controls.clear()

        if not historial:
            historial_text.controls.append(ft.Text("No hay Pomodoros completados aún.", color="white"))
        else:
            for h in historial[-5:][::-1]:
                item = ft.Row([
                    ft.Icon(name=ft.Icons.ACCESS_TIME, color="white", size=20),
                    ft.Text(
                        f"Trabajo: {h['duracion_trabajo']}  |  Descanso: {h['duracion_descanso']}",
                        size=14,
                        color="white"
                    )
                ])
                historial_text.controls.append(item)
        page.update()

    def agregar_pomodoro_al_historial(tipo, trabajo, descanso):
        historial = cargar_historial()
        historial.append({
            "tipo": tipo,
            "duracion_trabajo": trabajo,
            "duracion_descanso": descanso
        })
        guardar_historial(historial)
        actualizar_historial_visual()

    def formato_tiempo(minutos, segundos):
        return f"{minutos:02d}:{segundos:02d}"

    def temporizador(minutos, segundos, mensaje):
        restante_min = minutos

        if segundos > 0:
            sec = segundos
            while sec > 0:
                timer_display.value = formato_tiempo(restante_min, sec)
                output.value = f"{mensaje} - Quedan {restante_min} min {sec} seg"
                page.update()
                time.sleep(1)
                sec -= 1

        while restante_min > 0:
            restante_min -= 1
            sec = 60
            while sec > 0:
                timer_display.value = formato_tiempo(restante_min, sec - 1)
                output.value = f"{mensaje} - Quedan {restante_min} min {sec - 1} seg"
                page.update()
                time.sleep(1)
                sec -= 1

    def confirmar_tiempos(e):
        try:
            state["work_min"] = int(work_min_input.value)
            state["work_sec"] = int(work_sec_input.value)
            state["rest_min"] = int(rest_min_input.value)
            state["rest_sec"] = int(rest_sec_input.value)

            timer_display.value = formato_tiempo(state["work_min"], state["work_sec"])
            output.value = f"Trabajo: {formato_tiempo(state['work_min'], state['work_sec'])} | Descanso: {formato_tiempo(state['rest_min'], state['rest_sec'])}"
            page.update()
        except ValueError:
            output.value = "Por favor ingresa números válidos"
            page.update()

    def iniciar_pomodoro(e):
        def tarea():
            start_btn.disabled = True
            page.update()
            output.value = ""
            page.update()
            temporizador(state["work_min"], state["work_sec"], "ESTUDIO")
            output.value = "¡Descansa!"
            page.update()
            temporizador(state["rest_min"], state["rest_sec"], "DESCANSO")
            output.value = "¡Pomodoro completo!"
            agregar_pomodoro_al_historial(
                tipo="normal",
                trabajo=formato_tiempo(state["work_min"], state["work_sec"]),
                descanso=formato_tiempo(state["rest_min"], state["rest_sec"])
            )
            start_btn.disabled = False
            page.update()

        threading.Thread(target=tarea).start()

    confirm_btn.on_click = confirmar_tiempos
    start_btn.on_click = iniciar_pomodoro

    temporizador_card = ft.Container(
        content=ft.Column([
            ft.Text("Pomodoro", size=20, weight="bold", color="white"),
            timer_display
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        width=420,
        height=220,
        bgcolor=azul,
        border_radius=25,
        padding=20
    )

    izquierda = ft.Column([
        temporizador_card,
        ft.Row([work_min_input, work_sec_input]),
        ft.Row([rest_min_input, rest_sec_input]),
        ft.Row([confirm_btn, start_btn], spacing=20),
        output
    ], spacing=25)

    # LISTA DE TAREASSSSS

    def crear_lista_tareas(page: ft.Page):
        tareas = ft.Column(spacing=12)
        nueva_tarea = ft.TextField(
            hint_text="¿Qué necesitas hacer?",
            expand=True,
            bgcolor=blanco,
            border=ft.InputBorder.NONE,
            border_radius=ft.border_radius.all(12),
            filled=True
        )

        def añadir_tarea(e):
            if nueva_tarea.value.strip():
                tarea_texto = nueva_tarea.value.strip()
                nueva_tarea.value = ""
                tareas.controls.append(crear_tarea(tarea_texto))
                page.update()

        def crear_tarea(texto):
            check = ft.Checkbox()
            texto_tarea = ft.Text(value=texto, expand=True, size=15, color=ft.Colors.BLACK)
            campo_edicion = ft.TextField(value=texto, expand=True, visible=False)

            def borrar_tarea(e):
                tareas.controls.remove(fila_tarea)
                page.update()

            def comenzar_edicion(e):
                texto_tarea.visible = False
                campo_edicion.visible = True
                campo_edicion.focus()
                editar_btn.icon = ft.Icons.CHECK
                editar_btn.on_click = confirmar_edicion
                page.update()

            def confirmar_edicion(e):
                nuevo_texto = campo_edicion.value.strip()
                if nuevo_texto:
                    texto_tarea.value = nuevo_texto
                texto_tarea.visible = True
                campo_edicion.visible = False
                editar_btn.icon = ft.Icons.EDIT
                editar_btn.on_click = comenzar_edicion
                page.update()

            def toggle_completado(e):
                if check.value:
                    texto_tarea.style = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH, color="#888")
                else:
                    texto_tarea.style = ft.TextStyle(decoration=ft.TextDecoration.NONE, color=gris_texto)
                page.update()

            check.on_change = toggle_completado

            editar_btn = ft.IconButton(icon=ft.Icons.EDIT, on_click=comenzar_edicion, icon_color=azul)
            borrar_btn = ft.IconButton(icon=ft.Icons.DELETE, on_click=borrar_tarea, icon_color="#D32F2F")

            fila_tarea = ft.Container(
                content=ft.Row(
                    controls=[
                        check,
                        texto_tarea,
                        campo_edicion,
                        editar_btn,
                        borrar_btn
                    ],
                    alignment="spaceBetween",
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=15,
                bgcolor=blanco,
                border_radius=15,
                shadow=ft.BoxShadow(blur_radius=8, color="#00000020", offset=ft.Offset(0, 3))
            )

            return fila_tarea

        fila_input = ft.Row(
            controls=[
                nueva_tarea,
                ft.IconButton(icon=ft.Icons.ADD, on_click=añadir_tarea, icon_color=azul, bgcolor=blanco)
            ],
            alignment="center"
        )

        contenido = ft.Column(
            controls=[
                ft.Text("Lista de Tareas", size=22, weight=ft.FontWeight.BOLD, color="white"),
                fila_input,
                tareas,
            ],
            spacing=20
        )

        return ft.Container(
            content=contenido,
            padding=20,
            bgcolor=azul,
            border_radius=20,
            width=450,
            height=270
        )

    lista_tareas = crear_lista_tareas(page)

    derecha = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text("Historial de Pomodoros completados", size=20, weight="bold", color="white"),
                historial_text,
            ], spacing=15),
            bgcolor=azul,
            border_radius=20,
            padding=25,
            width=450,
            height=300
        ),
        lista_tareas
    ], spacing=20)

    page.add(
        ft.Row([
            izquierda,
            derecha
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

    actualizar_historial_visual()
