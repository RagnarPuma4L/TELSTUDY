import flet as ft

def crear_lista_tareas(page: ft.Page):
    page.clean()

    tareas = ft.Column()
    nueva_tarea = ft.TextField(hint_text="¿Qué necesitas hacer?", expand=True)

    def añadir_tarea(e):
        if nueva_tarea.value.strip() != "":
            tarea_texto = nueva_tarea.value.strip()
            nueva_tarea.value = ""
            tareas.controls.append(crear_tarea(tarea_texto))
            page.update()

    def crear_tarea(texto):
        texto_tarea = ft.Text(value=texto, expand=True)
        campo_edicion = ft.TextField(value=texto, expand=True, visible=False)

        def borrar_tarea(e):
            tareas.controls.remove(fila_tarea)
            page.update()

        def comenzar_edicion(e):
            texto_tarea.visible = False
            campo_edicion.visible = True
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

        editar_btn = ft.IconButton(icon=ft.Icons.EDIT, on_click=comenzar_edicion)
        borrar_btn = ft.IconButton(icon=ft.Icons.DELETE, on_click=borrar_tarea)

        fila_tarea = ft.Row(
            controls=[
                ft.Checkbox(),
                texto_tarea,
                campo_edicion,
                editar_btn,
                borrar_btn
            ],
            alignment="spaceBetween"
        )

        return fila_tarea

    fila_input = ft.Row(
        controls=[
            nueva_tarea,
            ft.IconButton(icon=ft.Icons.ADD, on_click=añadir_tarea)
        ],
        alignment="center"
    )

    contenido = ft.Column(
        controls=[
            ft.Text("Lista de Tareas", size=25, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
            fila_input,
            tareas,
        ],
        spacing=20
    )

    return ft.Container(
        content=contenido,
        padding=20,
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        border_radius=10
    )
