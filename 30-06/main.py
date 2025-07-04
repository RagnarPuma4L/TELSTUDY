import flet as ft
from notas import crear_zona_notas
from telmi import telmi_ai, widget_frase_motivadora
from agenda import agenda
import threading
import time
import json
import os


def formato_tiempo2(minutos, segundos):
    return f"{minutos:02d}:{segundos:02d}"

def actualizar_tiempos(min, second, mode = "a"):
    if mode == "a":
        if bool(str(min)):
            with open("src\Tiempos Temporizador\work_min.txt","w") as wm:
                wm.write(str(min))
        if bool(str(second)):
            with open("src\Tiempos Temporizador\work_sec.txt", "w") as ws:
                ws.write(str(second))
    if mode == "b":
        if bool(str(min)):
            with open("src/Tiempos Temporizador/rest_min.txt", "w") as rm:
                rm.write(str(min))
        if bool(str(second)):
            with open("src/Tiempos Temporizador/rest_sec.txt", "w") as rs:
                rs.write(str(second))


def actualizar_tiempos_desde_archivo():
    pass

#variables del temporizador
work_min = 0
work_sec = 0
rest_min = 0
rest_sec = 0

stop = False
reasignacion = False
def reasignacion_change(a):
    global work_min
    global work_sec
    global rest_min
    global rest_sec
    work_min = 0
    work_sec = 0
    rest_min = 0
    rest_sec = 0

def stop_pomodoro_change(a):
    global stop
    stop = not stop

def main(page: ft.Page):
    blanco = "#F1F5F9"
    timer_display = ft.Text("00:00", size=50, weight="bold", color=blanco)
    timer_display2 = ft.Text("00:00", size=50, weight="bold", color=blanco)
    # GENERAL
    page.bgcolor = "#0A1E3F"
    page.title = "Telematics Study Tool"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 24
    page.spacing = 24
    page.window.width = 1250
    page.window.height = 750
    page.window.resizable = True

    def actualizar_displays(display, min1, sec1, display2, min2, sec2):
        global work_min
        global work_sec
        global rest_min
        global rest_sec
        nonlocal timer_display2
        nonlocal timer_display
        while True:
            time.sleep(0.5)
            timer_display.value = formato_tiempo2(work_min, work_sec)
            timer_display2.value = formato_tiempo2(rest_min, rest_sec)
            page.update()


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
                ft.ElevatedButton(
                    icon=ft.Icons.EVENT,
                    text="Agenda",
                    on_click=change_agenda,
                    style=estilo_botones,
                    width=200,
                    height=60,
                )
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
        )

        def pausa(a):
            global stop
            stop = True
            return stop
            page.update()
        pausa = ft.ElevatedButton(text= "Pausa", bgcolor= ft.Colors.RED_900, on_click= pausa)
        def reanudar(a):
            global stop
            stop = False
            return stop
        reanudar = ft.ElevatedButton(text= "Reanudar", bgcolor= ft.Colors.GREEN_500, on_click= reanudar)
        fila = ft.Row(controls=[pausa, reanudar], spacing= 20) 
        temporizador_card = ft.Container(
            content=ft.Column([
                ft.Text("Temporizador", size=25, weight="bold", color= ft.Colors.WHITE),
                timer_display, timer_display2,
                fila
            ], 
              alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=300,
            height=300,
            bgcolor=ft.Colors.BLUE_800,
            border_radius=25,
            on_click= simple_pom,
            padding=20,
            shadow=ft.BoxShadow(blur_radius=5, color="#4F46E5", offset=ft.Offset(0, 6))  
        )
        a = ft.Row(controls= [accesos_rapidos, temporizador_card], spacing= 80)
        derecha = ft.Column(controls=[frase_con_telmi, a], spacing=36, expand=True)
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

    def change_agenda(e):
        page.clean()
        widget_agenda=agenda(page)
        page.add(navigation_bar, widget_agenda)

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
        elif selected_index == 4:
            change_agenda(None)

    navigation_bar = ft.NavigationBar(
        selected_index=0,
        on_change=on_navigation_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Inicio"),
            ft.NavigationBarDestination(icon=ft.Icons.TIMER, label="Pomodoro"),
            ft.NavigationBarDestination(icon=ft.Icons.PSYCHOLOGY, label="Telmi"),
            ft.NavigationBarDestination(icon=ft.Icons.DRAW, label="Pizarra"),
            ft.NavigationBarDestination(icon=ft.Icons.EVENT, label="Agenda")
        ],
        bgcolor="#1E40AF",
        indicator_color="#818CF8",
        elevation=8,
        height=60,
    )


    def simple_pom(a = 2):
        blanco = "#F1F5F9"
        nonlocal timer_display
        nonlocal timer_display2

    # Pomodoro Simple
   
        def simple_pom2(b = 2):
            nonlocal timer_display
            nonlocal timer_display2
            page.clean()
            HISTORIAL_FILE = "pomodoros.json"
            azul = "#0A2F55"
            azul_claro = "#4F46E5"
            blanco = "#F1F5F9"
            gris_texto = "#94A3B8"
            verde = "#10B981"
            rojo = "#F87171"
            global work_min
            global rest_min
            global work_sec
            global rest_sec

            def formato_tiempo(minutos, segundos):
                return f"{minutos:02d}:{segundos:02d}"
        
            def temporizador_generico(display):

                nonlocal timer_display2
                nonlocal timer_display
                global stop
                global rest_min
                global work_min
                global rest_sec
                global work_sec
                page.update()
                if display == timer_display:
      
                    temporizador = 0
                    while temporizador >= 0:  # 1:0
                        while work_min > 0 or work_sec > 0 and stop == False:
                            time.sleep(1)
                            if work_sec == 0:
                                if work_min > 0:
                                    work_min -= 1
                                    work_sec = 59
                                else:
                                    break
                            else:
                                work_sec -= 1
                            display.value = formato_tiempo(work_min, work_sec)
                            page.update()
                        if work_min == 0 and work_sec == 0 and stop == False:
                            temporizador = -1
        

                if display == timer_display2:
                    temporizador = 0
                    while temporizador >= 0:  # 1:0
                        while rest_min > 0 or rest_sec > 0 and stop == False:
                            time.sleep(1)
                            
                            if rest_sec == 0:
                                if rest_min > 0:
                                    rest_min -= 1
                                    rest_sec = 59
                                else:
                                    break
                            else:
                                rest_sec -= 1

                            display.value = formato_tiempo(work_min, work_sec)
                            page.update()

                        if rest_min == 0 and rest_sec == 0 and stop == False:
                            temporizador = -1
 
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



            work_min_input = ft.TextField(
                label="Minutos trabajo", 
                width=150, 
                input_filter=ft.NumbersOnlyInputFilter(),
                bgcolor="#334155",
                border_color=azul_claro,
                label_style=ft.TextStyle(color=gris_texto),
                text_style=ft.TextStyle(color=blanco),
                border_radius=12
            )
            
            work_sec_input = ft.TextField(
                label="Segundos trabajo", 
                width=150, 
                input_filter=ft.NumbersOnlyInputFilter(),
                bgcolor="#334155",
                border_color=azul_claro,
                label_style=ft.TextStyle(color=gris_texto),
                text_style=ft.TextStyle(color=blanco),
                border_radius=12
            )
            
            rest_min_input = ft.TextField(
                label="Minutos descanso", 
                width=150, 
                input_filter=ft.NumbersOnlyInputFilter(),
                bgcolor="#334155",
                border_color=azul_claro,
                label_style=ft.TextStyle(color=gris_texto),
                text_style=ft.TextStyle(color=blanco),
                border_radius=12
            )
            
            rest_sec_input = ft.TextField(
                label="Segundos descanso", 
                width=150, 
                input_filter=ft.NumbersOnlyInputFilter(),
                bgcolor="#334155",
                border_color=azul_claro,
                label_style=ft.TextStyle(color=gris_texto),
                text_style=ft.TextStyle(color=blanco),
                border_radius=12
            )





            def agregar_pomodoro_al_historial(tipo, trabajo, descanso):
                historial = cargar_historial()
                historial.append({
                    "tipo": tipo,
                    "duracion_trabajo": trabajo,
                    "duracion_descanso": descanso
                })
                guardar_historial(historial)
                actualizar_historial_visual()

            def confirmar_tiempos(e):
                global work_min
                global work_sec
                global rest_min
                global rest_sec
                nonlocal timer_display2
                nonlocal timer_display
                try:
                    if bool(work_min_input.value):
                        work_min = int(work_min_input.value)
                    else:
                        work_min = 0

                    if bool(work_sec_input.value):
                        work_sec = int(work_sec_input.value)
                    else:
                        work_sec = 0

                    if bool(rest_min_input.value):
                        rest_min = int(rest_min_input.value)
                    else:
                        rest_min = 0

                    if bool(rest_sec_input.value):
                        rest_sec = int(rest_sec_input.value)
                    else:
                        rest_sec = 0
                    #transformar_tiempos
                    if work_sec >= 60:
                        work_min += work_sec // 60
                        work_sec = work_sec % 60
                    if rest_sec >= 60:
                        rest_min += rest_sec // 60
                        rest_sec = rest_sec % 60

                    agregar_pomodoro_al_historial(
                        tipo="normal",
                        trabajo=formato_tiempo(work_min, work_sec),
                        descanso=formato_tiempo(rest_min, rest_sec)
                    )
                    timer_display.value = formato_tiempo(work_min, work_sec)
                    timer_display2.value = formato_tiempo(rest_min, rest_sec)
                    output.value = f"Trabajo: {formato_tiempo(work_min, work_sec)} | Descanso: {formato_tiempo(rest_min, rest_sec)}"
                    page.update()
                except ValueError:
                    output.value = "Por favor ingresa números válidos"
                    output.color = rojo
                    page.update()


            confirm_btn = ft.ElevatedButton(
                text="Confirmar tiempos",
                style=ft.ButtonStyle(
                    bgcolor=azul_claro,
                    color=blanco,
                    padding=ft.padding.symmetric(horizontal=25, vertical=15),
                    shape=ft.RoundedRectangleBorder(radius=12),
                    text_style=ft.TextStyle(size=17, weight=ft.FontWeight.BOLD)
                )
            )

            start_btn = ft.ElevatedButton(
                text="Iniciar Pomodoro",
                style=ft.ButtonStyle(
                    bgcolor=verde,
                    color=blanco,
                    padding=ft.padding.symmetric(horizontal=25, vertical=15),
                    shape=ft.RoundedRectangleBorder(radius=12),
                    text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
                )
            )

            output = ft.Text("", size=16, color=gris_texto)

            state = {work_min, work_sec, rest_min, rest_sec}
            historial_text = ft.Column([], spacing=8, scroll = "always", expand = True)

            def actualizar_historial_visual():
                historial = cargar_historial()
                historial_text.controls.clear()
                if not historial:
                    historial_text.controls.append(ft.Text("No hay Pomodoros completados aún.", color=blanco))
                else:
                    for h in historial[-5:][::-1]:
                        item = ft.Row([
                            ft.Icon(name=ft.Icons.ACCESS_TIME, color=azul_claro, size=20),
                            ft.Text(
                                f"Trabajo: {h['duracion_trabajo']}  |  Descanso: {h['duracion_descanso']}",
                                size=14,
                                color=blanco
                            )
                        ])
                        historial_text.controls.append(item)
                page.update()





            stop_btn = ft.ElevatedButton(
                text= "Detener",
                on_click= stop_pomodoro_change,
                bgcolor=ft.Colors.RED_900)
            
            reasignar_btn = ft.ElevatedButton(
                text = "Reasignar Tiempos",
                on_click = reasignacion_change,
                bgcolor =ft.Colors.RED_700
            )

            def iniciar_pomodoro(e):
                page.update()
                global work_min
                global rest_min
                global work_sec
                global work_sec
                page.update()
                page.update()
                def tarea(a = 4):
                    page.update()
                    start_btn.disabled = True
                    confirm_btn.disabled = True
                    output.value = "¡Comienza el tiempo de estudio!"
                    output.color = azul_claro
                    page.update()
                    temporizador_generico(timer_display)       
                    output.value = "¡Tiempo de descanso!"
                    output.color = verde
                    page.update()
                    temporizador_generico(timer_display2)     
                    output.value = "¡Pomodoro completado!"
                    output.color = azul_claro
                    start_btn.disabled = False
                    confirm_btn.disabled = False
                    page.update()
                threading.Thread(target=tarea, daemon=True).start()

            confirm_btn.on_click = confirmar_tiempos
            start_btn.on_click = iniciar_pomodoro

            temporizador_card = ft.Container(
                content=ft.Column([
                    ft.Text("ESTUDIO", size=20, weight="bold", color=blanco),
                    timer_display
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=300,
                height=300,
                bgcolor=azul,
                border_radius=25,
                padding=20,
                shadow=ft.BoxShadow(blur_radius=5, color="#4F46E5", offset=ft.Offset(0, 6))
            )

            temporizador_card2 = ft.Container(
                content=ft.Column([
                    ft.Text("DESCANSO", size=20, weight="bold", color=blanco),
                    timer_display2
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=300,
                height=300,
                bgcolor=azul,
                border_radius=25,
                padding=20,
                shadow=ft.BoxShadow(blur_radius=5, color="#4F46E5", offset=ft.Offset(0, 6))
            )   
            izquierda = ft.Column([
                ft.Row([temporizador_card,temporizador_card2]),
                ft.Row([work_min_input, work_sec_input, rest_min_input, rest_sec_input ], spacing=10),
                ft.Row([confirm_btn, start_btn, stop_btn, reasignar_btn], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER),
                output
            ], spacing=25)

            def crear_lista_tareas(page: ft.Page):
                tareas = ft.Column(spacing=12)
                nueva_tarea = ft.TextField(
                    label="¿Qué necesitas hacer?",
                    expand=True,
                    bgcolor="#1E3A8A",
                    filled=True,
                    border_radius=12,
                    border_color="#4F46E5"
                )

                def añadir_tarea(e):
                    if nueva_tarea.value.strip():
                        tarea_texto = nueva_tarea.value.strip()
                        nueva_tarea.value = ""
                        tareas.controls.append(crear_tarea(tarea_texto))
                        page.update()

                def crear_tarea(texto):
                    check = ft.Checkbox()
                    texto_tarea = ft.Text(value=texto, expand=True, size=15, color="#F4F4F4")
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
                            texto_tarea.style = ft.TextStyle(decoration=ft.TextDecoration.NONE, color="#1E293B")
                        page.update()

                    check.on_change = toggle_completado
                    editar_btn = ft.IconButton(icon=ft.Icons.EDIT, on_click=comenzar_edicion, icon_color=blanco)
                    borrar_btn = ft.IconButton(icon=ft.Icons.DELETE, on_click=borrar_tarea, icon_color=rojo)

                    fila_tarea = ft.Container(
                        content=ft.Row(
                            controls=[check, texto_tarea, campo_edicion, editar_btn, borrar_btn],
                            alignment="spaceBetween",
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        padding=15,
                        bgcolor="#1E40AF",
                        border_radius=15,
                        shadow=ft.BoxShadow(blur_radius=5, color="#4F46E5", offset=ft.Offset(0, 6))
                    )
                    return fila_tarea

                fila_input = ft.Row(
                    controls=[nueva_tarea, ft.IconButton(icon=ft.Icons.ADD, on_click=añadir_tarea, icon_color=blanco, bgcolor="#1E40AF")],
                    alignment="center"
                )

                contenido = ft.Column(
                    controls=[
                        ft.Text("Lista de Tareas", size=22, weight=ft.FontWeight.BOLD, color=blanco),
                        fila_input,
                        tareas,
                    ],
                    scroll= "always", expand = True,
                    spacing=20
                )
                return ft.Container(
                    content=contenido,
                    padding=20,
                    bgcolor=azul,
                    border_radius=20,
                    width=450,
                    height=400,
                    shadow=ft.BoxShadow(blur_radius=5, offset=(0,6), color="#4F46E5")
                )
            lista_tareas = crear_lista_tareas(page)
            derecha = ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Text("Historial de Pomodoros", size=20, weight="bold", color=blanco),
                        historial_text,
                    ], spacing=15),
                    bgcolor=azul,
                    border_radius=20,
                    padding=25,
                    width=300,
                    height=200,
                    shadow=ft.BoxShadow(blur_radius=5, offset=(0,6), color="#4F46E5")
                ),
                lista_tareas
            ], spacing=20)
            layout=(
                ft.Row([
                    izquierda,
                    derecha
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ) 
            page.add(layout, navigation_bar)
            actualizar_historial_visual()
            page.update()
            #hilo1 = threading.Thread(target= temporizador_generico(timer_display, work_min, work_sec, "trabajo"), daemon= True)
            #hilo1.start()
            #timer_display2.value = formato_tiempo(rest_min, rest_sec)
            page.update()
            #hilo2 = threading.Thread(target= temporizador_generico(timer_display2, rest_min, rest_sec, "descaso"), daemon= True)
        # hilo2.start()
            page.update()
        threading.Thread(target=simple_pom2, daemon= True).start()
        threading.Thread(actualizar_displays(timer_display, work_min, work_sec, timer_display2, rest_min, rest_sec)).start()
        






        # Inicio mostrando la pantalla principal

    mostrar_inicio(None)

ft.app(target=main, assets_dir="assets")
