import flet as ft

def crear_zona_notas(page, estilo_botones):
    notas = []
    input_nota = ft.TextField(
        label="Escribe una nota rápida",
        expand=True,
        border_radius=10,
        bgcolor=ft.Colors.WHITE,
    )
    lista_notas = ft.Column(spacing=10)

    def agregar_nota(e):
        if input_nota.value.strip():
            nota_texto = input_nota.value.strip()

            nueva_nota = ft.Container(
                content=ft.Row([
                    ft.Text(nota_texto, expand=True, size=14),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.RED_400,
                        tooltip="Eliminar",
                        on_click=lambda ev, nota=nota_texto: eliminar_nota(ev, nota)
                    )
                ]),
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

            notas.append((nota_texto, nueva_nota))
            lista_notas.controls.append(nueva_nota)
            input_nota.value = ""
            page.update()

    def eliminar_nota(e, contenido):
        for nota in notas:
            if nota[0] == contenido:
                lista_notas.controls.remove(nota[1])
                notas.remove(nota)
                break
        page.update()

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
