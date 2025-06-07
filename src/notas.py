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
    notas = []  # lista de tuplas (texto, control)
    lista_notas = ft.Column(spacing=10)

    input_nota = ft.TextField(
        label="Escribe una nota rápida",
        expand=True,
        border_radius=8,
        filled=True,
        bgcolor=ft.Colors.WHITE,
        border_color="#3B82F6",
        color="#1E293B"
    )

    def eliminar_nota(e, nota_control):
        # Eliminamos la nota visual
        if nota_control in lista_notas.controls:
            lista_notas.controls.remove(nota_control)
            # Eliminamos de la lista de notas y guardamos cambios
            for n in notas:
                if n[1] == nota_control:
                    notas.remove(n)
                    break
            # Guardar lista de textos actualizada
            guardar_notas([n[0] for n in notas])
            page.update()

    def crear_nota_control(texto):
        nota_container = ft.Container(
            padding=10,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border(
                left=ft.BorderSide(1, ft.Colors.BLUE_100),
                top=ft.BorderSide(1, ft.Colors.BLUE_100),
                right=ft.BorderSide(1, ft.Colors.BLUE_100),
                bottom=ft.BorderSide(1, ft.Colors.BLUE_100),
            ),
            border_radius=8,
            shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.BLUE_100),
        )

        btn_eliminar = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color=ft.Colors.RED_400,
            tooltip="Eliminar",
            on_click=lambda e: eliminar_nota(e, nota_container)
        )

        nota_container.content = ft.Row([
            ft.Text(texto, expand=True, size=14),
            btn_eliminar
        ])

        return nota_container

    def agregar_nota(e):
        texto = input_nota.value.strip()
        if texto:
            nueva_nota = crear_nota_control(texto)
            notas.append((texto, nueva_nota))
            lista_notas.controls.append(nueva_nota)
            input_nota.value = ""
            # Guardamos la lista actualizada (solo texto)
            guardar_notas([n[0] for n in notas])
            page.update()

    # Cargar notas guardadas al iniciar
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
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700
                ),
                ft.Row([input_nota, boton_agregar], alignment=ft.MainAxisAlignment.START),
                lista_notas
            ]),
            padding=20,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=12,
            shadow=ft.BoxShadow(
                blur_radius=6,
                color=ft.Colors.BLUE_100,
                offset=ft.Offset(0, 4)
            )
        )
    )
    return notas_card
