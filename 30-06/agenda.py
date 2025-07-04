import flet as ft
import json
import os
from datetime import datetime
import threading
import time
from winotify import Notification #pip install winotify

ARCHIVO = "agenda.json"

def cargar_eventos():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_eventos(eventos):
    eventos_ordenados = sorted(eventos, key=lambda e: f"{e['fecha']} {e.get('hora', '00:00')}")
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(eventos_ordenados, f, indent=4, ensure_ascii=False)

def notificar(titulo, mensaje):
    toast = Notification(app_id="Agenda Organizada", title=titulo, msg=mensaje)
    toast.show()

def notificar_eventos(eventos_shared, lock):
    notificados = set()
    while True:
        ahora = datetime.now()
        with lock:
            eventos = list(eventos_shared)
        for e in eventos:
            fecha_hora_str = e["fecha"] + " " + e.get("hora", "00:00")
            try:
                fecha_evento = datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M")
            except:
                continue
            if fecha_evento <= ahora and e["titulo"] not in notificados:
                notificar(f"Evento: {e['titulo']}", f"{e.get('descripcion', '')}\n{fecha_hora_str}")
                notificados.add(e["titulo"])
        time.sleep(60)  # Revisa cada minuto

def crear_agenda(page, eventos, lock):
    titulo = ft.TextField(
        label="Título",
        border_radius=12,
        filled=True,
        bgcolor="#1E3A8A",
        border_color="#4F46E5",
        color="#E0E7FF",
    )
    descripcion = ft.TextField(
        label="Descripción",
        multiline=True,
        border_radius=12,
        filled=True,
        bgcolor="#1E3A8A",
        border_color="#4F46E5",
        color="#E0E7FF",
    )
    fecha = ft.TextField(
        label="Fecha",
        read_only=True,
        hint_text="Selecciona fecha",
        border_radius=12,
        filled=True,
        bgcolor="#1E3A8A",
        border_color="#4F46E5",
        color="#E0E7FF",
        expand=True,
    )
    hora = ft.TextField(
        label="Hora",
        read_only=True,
        hint_text="Selecciona hora",
        border_radius=12,
        filled=True,
        bgcolor="#1E3A8A",
        border_color="#4F46E5",
        color="#E0E7FF",
        expand=True,
    )

    lista_hoy = ft.Column(spacing=10)
    lista_pasados = ft.Column(spacing=10)
    lista_futuros = ft.Column(spacing=10)

    def eliminar_evento(evento_a_borrar):
        with lock:
            eventos_actualizados = [
                e for e in eventos
                if not (
                    e["titulo"] == evento_a_borrar["titulo"] and
                    e["fecha"] == evento_a_borrar["fecha"] and
                    e.get("hora", "") == evento_a_borrar.get("hora", "")
                )
            ]
            eventos.clear()
            eventos.extend(eventos_actualizados)
            guardar_eventos(eventos_actualizados)
        mostrar()

    def crear_tarjeta(e, color_fondo):
        try:
            fecha_obj = datetime.strptime(e["fecha"], "%Y-%m-%d")
            fecha_formateada = fecha_obj.strftime("%d/%m/%Y")
        except:
            fecha_formateada = e["fecha"]
        texto_hora = e.get("hora", "")
        return ft.Container(
            margin=ft.Margin(0, 5, 0, 5),
            content=ft.Row([
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.Icons.EVENT, color="#A5B4FC"),
                        title=ft.Text(e["titulo"], size=14, weight=ft.FontWeight.BOLD, color="#E0E7FF"),
                        subtitle=ft.Text(f"{fecha_formateada} {texto_hora}\n{e['descripcion']}", color="#CBD5E1"),
                    ),
                    expand=True
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE,
                    icon_color="#F87171",
                    tooltip="Eliminar",
                    on_click=lambda _: eliminar_evento(e),
                )
            ]),
            bgcolor=color_fondo,
            border=ft.border.all(1, "#818CF8"),
            border_radius=12,
            padding=12,
            shadow=ft.BoxShadow(blur_radius=6, color="#6366F1", offset=ft.Offset(0, 3)),
        )

    def seccion_eventos(titulo_sec, eventos_sec, color_fondo):
        return ft.Card(
            content=ft.Container(
                bgcolor="#1E293BFF",
                padding=15,
                content=ft.Column(
                    [ft.Text(titulo_sec, size=20, weight=ft.FontWeight.BOLD, color="#93C5FD")]
                    + [crear_tarjeta(e, color_fondo) for e in eventos_sec]
                )
            )
        )

    def mostrar():
        lista_hoy.controls.clear()
        lista_pasados.controls.clear()
        lista_futuros.controls.clear()
        hoy = datetime.now().date()

        with lock:
            eventos_actualizados = list(eventos)

        pasados = [e for e in eventos_actualizados if datetime.strptime(e["fecha"], "%Y-%m-%d").date() < hoy]
        hoyes = [e for e in eventos_actualizados if datetime.strptime(e["fecha"], "%Y-%m-%d").date() == hoy]
        futuros = [e for e in eventos_actualizados if datetime.strptime(e["fecha"], "%Y-%m-%d").date() > hoy]

        pasados = sorted(pasados, key=lambda e: (e['fecha'], e.get('hora', '00:00')), reverse=True)
        hoyes = sorted(hoyes, key=lambda e: (e.get('hora', '00:00'),))
        futuros = sorted(futuros, key=lambda e: (e['fecha'], e.get('hora', '00:00')))

        if hoyes:
            lista_hoy.controls.append(seccion_eventos("Eventos de Hoy", hoyes, "#2563EB"))

        if pasados:
            lista_pasados.controls.append(seccion_eventos("Eventos Pasados", pasados, "#1E293B"))

        if futuros:
            lista_futuros.controls.append(seccion_eventos("Eventos Futuros", futuros, "#1E40AF"))

        page.update()

    def agregar(e):
        t = titulo.value.strip()
        d = descripcion.value.strip()
        f = fecha.value.strip()
        h = hora.value.strip()

        if not t or not f:
            page.snack_bar = ft.SnackBar(ft.Text("Título y fecha obligatorios"))
            page.snack_bar.open = True
            page.update()
            return

        with lock:
            for ev in eventos:
                if ev["titulo"] == t and ev["fecha"] == f and ev.get("hora", "") == h:
                    page.snack_bar = ft.SnackBar(ft.Text("Evento ya existe"))
                    page.snack_bar.open = True
                    page.update()
                    return

            eventos.append({"titulo": t, "descripcion": d, "fecha": f, "hora": h})
            guardar_eventos(eventos)

        titulo.value = ""
        descripcion.value = ""
        fecha.value = ""
        hora.value = ""

        mostrar()
        page.update()

    def seleccionar_fecha(e):
        if date_picker.value:
            fecha.value = date_picker.value.strftime("%Y-%m-%d")
            page.update()

    def seleccionar_hora(e):
        if time_picker.value:
            hora.value = time_picker.value.strftime("%H:%M")
            page.update()

    def abrir_picker_fecha(e):
        date_picker.open = True
        page.update()

    def abrir_picker_hora(e):
        time_picker.open = True
        page.update()

    date_picker = ft.DatePicker(on_change=seleccionar_fecha, first_date=datetime(2000, 1, 1), last_date=datetime(2100, 12, 31))
    time_picker = ft.TimePicker(on_change=seleccionar_hora)

    page.overlay.extend([date_picker, time_picker])

    mostrar()

    formulario = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Agrega un nuevo evento", size=18, weight=ft.FontWeight.BOLD, color="#93C5FD"),
                titulo,
                ft.Row([
                    fecha,
                    ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=abrir_picker_fecha),
                    hora,
                    ft.IconButton(icon=ft.Icons.ACCESS_TIME, on_click=abrir_picker_hora)
                ], spacing=10),
                descripcion,
                ft.ElevatedButton("Agregar evento", on_click=agregar),
            ], spacing=12),
            padding=24,
            bgcolor="#0A2F55",
            border_radius=16,
            shadow=ft.BoxShadow(blur_radius=8, color="#4F46E5", offset=ft.Offset(0, 6))
        )
    )

    contenedor_izquierda = ft.Column([
        formulario,
        lista_hoy,
    ], expand=True, spacing=15)

    contenedor_derecha = ft.Column([
        lista_futuros,
        lista_pasados,
    ], expand=True, spacing=15)

    return ft.Container(
        content=ft.Row([
            contenedor_izquierda,
            ft.VerticalDivider(width=15, color="#1E40AF"),
            contenedor_derecha
        ], expand=True, spacing=20),
        padding=20,
        bgcolor="#0A1E3F",
        border_radius=16,
        shadow=ft.BoxShadow(blur_radius=10, color="#2563EB", offset=ft.Offset(0, 8))
    )

def agenda(page: ft.Page):
    eventos = cargar_eventos()
    lock = threading.Lock()

    agenda = crear_agenda(page, eventos, lock)
    page.add(agenda)

    hilo_notificaciones = threading.Thread(target=notificar_eventos, args=(eventos, lock), daemon=True)
    hilo_notificaciones.start()

    return agenda
