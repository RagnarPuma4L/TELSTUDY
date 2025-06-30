import flet as ft
import requests
import datetime
import threading

# API de Groq
API_KEY = "[APIKEY]"  #NO SUBIR API_KEY AL REPOSITORIO PLISSS ;-;, PUEDEN REVOCAR EL USO.

# Personalidad de Telmi
conversacion = [
    {
        "role": "system",
        "content": (
            "Eres una asistente educativa simpática, energética y tierna llamada Telmi. "
            "Te interesa mucho el mundo tecnológico y fuiste creada por y para estudiantes de la Universidad Federico Santa María "
            "Tu objetivo es recomendar técnicas de estudio y apoyar en la organización del tiempo"
            "Responde de manera corta, a menos que sea alguna pregunta seria."
        )
    }
]

# Trae a Llama
def pedir_a_llama():
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": conversacion,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Error al consultar con Telmi, RIP TELMI."
    

#BURBUJAS DE MENSAJE
def burbuja_mensaje(texto, es_usuario):
    return ft.Row(
        alignment=ft.MainAxisAlignment.END if es_usuario else ft.MainAxisAlignment.START,
        controls=[
            ft.Container(
                content=ft.Text(texto),
                padding=10,
                margin=ft.margin.only(top=5, bottom=5, left=10, right=10),
                bgcolor=ft.Colors.GREEN if es_usuario else ft.Colors.BLACK12,
                border_radius=ft.border_radius.all(12),
                width=400,
            )
        ]
    )



# PARTE VISUAL
def telmi_ai(page: ft.Page):
    
    page.scroll = "auto"

    def enviar(e):
        pregunta = entrada_usuario.value.strip()
        if not pregunta:
            return

        # GUARDAR PREGUNTA
        conversacion.append({"role": "user", "content": pregunta})

        # MUESTRA PREGUNTA EN PANTALLA
        chat_area.controls.append(burbuja_mensaje(f"Tú: {pregunta}", es_usuario=True))
        entrada_usuario.value = ""
        page.update()


        # CONSIGUE RESPUESTA DE TELMI
        respuesta = pedir_a_llama()

        # MUESTRA RESPUESTA DE TELMI
        conversacion.append({"role": "assistant", "content": respuesta})
        chat_area.controls.append(burbuja_mensaje(f"Telmi: {respuesta}", es_usuario=False))
        page.update()
    #label="Escribe tu duda"
     #Entrada para escribir tu pregunta
    entrada_usuario = ft.TextField(
        hint_text= "Escribe tu duda...",
        multiline=False,
        expand=True,
        fill_color="#1E3A8A",
        border_color="#4F46E5",
        on_submit=enviar
    )

    chat_area = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
        padding=10
    )
  

  #Literal solo el texto e imagen de Telmi arriba :v (Y aún así es harto código)
    encabezado_telmi = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                content=ft.Image(src="telmifr.png", width=50, height=50, fit=ft.ImageFit.COVER),
                width=50,
                height=50,
                border_radius=25,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS
            ),
            ft.Text("Telmi", size=24, weight="bold", color=ft.Colors.ON_SECONDARY_CONTAINER)
        ]
    )

    telmi_text = ft.Column(
        controls=[
            encabezado_telmi,
            ft.Text("Telmi")
        ]
    )

#ICONO PARA ENVIAR
    mensaje_enviar = ft.Row(
        controls=[
            entrada_usuario,
            ft.IconButton(
                icon=ft.Icons.SEND,
                tooltip="Enviar",
                on_click=enviar,
                bgcolor="#4F46E5"
            ),
        ],
    )

    #CONVIERTE TODO EN UN WIDGET REUSABLE CON ALGUNOS COMPONENTES VISUALES QUE FÁCILMENTE SE PUEDE AGREGAR EN MAIN.PY
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                encabezado_telmi,
                chat_area,
                mensaje_enviar
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20,
            bgcolor="#0A2F55",
            border_radius=15,
            expand=True,
        ),
    )
##########FUNCIÓN DE TELMI Q HACE LAS FRASES PERSONALIZADAS EN VEZ DE FRASES PREDETERMINADAS RANDOM
def generar_frase():
    ahora = datetime.datetime.now().hour

    if ahora < 12:
        momento = "la mañana"
    elif 12 <= ahora < 18:
        momento = "la tarde"
    else:
        momento = "la noche"

    prompt = f"Dame una frase corta y motivadora para un estudiante que está comenzando a estudiar en {momento}. Recuerda que eres Telmi, una IA tierna y energética, no asumas género plis."

    conversacion.append({"role": "user", "content": prompt})

    respuesta = pedir_a_llama()

    conversacion.append({"role": "assistant", "content": respuesta})

    return respuesta
    
def widget_frase_motivadora(page: ft.Page):

    loading_widget = ft.Row(
        controls=[
            ft.ProgressRing(width=20, height=20, stroke_width=3, color="#C7D2FE"),
            ft.Text("Telmi está pensando...", italic=True, color="#CBD5E1"),
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
    )

    frase_container = ft.Container(
        content=loading_widget,
        padding=12,
        bgcolor="#1E40AF",
        border_radius=12,
        expand=True,
        shadow=ft.BoxShadow(color="#1E40AF80", blur_radius=8, offset=ft.Offset(0, 3)),
    )

    def cargar_frase_ia():
        frase_real = generar_frase()
        frase_container.content = ft.Text(
            frase_real,
            italic=True,
            text_align=ft.TextAlign.CENTER,
            color="#CBD5E1"
        )
        page.update()

    threading.Thread(target=cargar_frase_ia, daemon=True).start()

    return frase_container
