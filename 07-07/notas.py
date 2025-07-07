import flet as ft
import json

def guardar_notas(notas_texto, archivo="notas_guardadas.json"):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(notas_texto, f, ensure_ascii=False, indent=4)

def cargar_notas(archivo="notas_guardadas.json"):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def crear_zona_notas(page, estilo_botones):
    notas = [] 
    lista_notas = ft.Column(spacing=10)

    input_nota = ft.TextField(
        label="Escribe una nota rápida",
        expand=True,
        border_radius=12,
        filled=True,
        bgcolor="#1E3A8A",
        border_color="#4F46E5", 
        color="#E0E7FF"
    )

    def eliminar_nota(e, nota_control):
        if nota_control in lista_notas.controls:
            lista_notas.controls.remove(nota_control)
            for n in notas:
                if n[1] == nota_control:
                    notas.remove(n)
                    break
            guardar_notas([n[0] for n in notas])
            page.update()

    def crear_nota_control(texto):
        nota_container = ft.Container(
            padding=12,
            bgcolor="#1E40AF", 
            border=ft.border.all(1, "#818CF8"),
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=6, color="#6366F1", offset=ft.Offset(0, 3))
        )

        btn_eliminar = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color="#F87171",
            tooltip="Eliminar",
            on_click=lambda e: eliminar_nota(e, nota_container)
        )

        nota_container.content = ft.Row([
            ft.Text(texto, expand=True, size=14, color="#E0E7FF"),
            btn_eliminar
        ])

        return nota_container

    def agregar_nota(e):
        texto = input_nota.value.strip()
        if texto:
            nueva_nota = crear_nota_control(texto)
            notas.append((texto
                          , nueva_nota))
            lista_notas.controls.append(nueva_nota)
            input_nota.value = ""
            guardar_notas([n[0] for n in notas])
            page.update()

    notas_guardadas = cargar_notas()
    for texto in notas_guardadas:
        nota_control = crear_nota_control(texto)
        notas.append((texto, nota_control))
        lista_notas.controls.append(nota_control)

    boton_agregar = ft.ElevatedButton(
        "Agregar nota",
        on_click=agregar_nota,
        style=estilo_botones
    )

    notas_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text(
                    "Notas rápidas",
                    size=22,
                    weight=ft.FontWeight.W_700,
                    color="#A5B4FC"
                ),
                ft.Row([input_nota, boton_agregar], alignment=ft.MainAxisAlignment.START, spacing=10),
                lista_notas
            ]),
            padding=24,
            bgcolor="#0A2F55",
            border_radius=16,
            shadow=ft.BoxShadow(
                blur_radius=8,
                color="#4F46E5",
                offset=ft.Offset(0, 6)
            )
        )
    )
    return notas_card
