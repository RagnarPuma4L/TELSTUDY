import flet as ft
import requests

API_KEY = "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"     #La key para usar a LLAMA3 con Groq

conversacion = [   #Dónde esta escrito el "Eres una asistente..." pueden decirle como debe actuar la IA, ayer estaba probando que puedes decirle cualquier cosa y actuará así, así que pueden ir probando con literalmente cualquier personalidad xd.
    {"role": "system", "content": "Eres una asistente educativa simpática, energética y tierna llamada Telmi, te interesa mucho el mundo tecnológico y también eres creada por y para estudiantes de la universidad federico santa maría en Chile. Ten en cuenta que tu fin es recomendar técnicas de estudio y apoyar en la organización."}
]
#Conecta llama con la API de Groq
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

def main(page: ft.Page):
    page.scroll = "auto"

    entrada_usuario = ft.TextField(label="Escribe tu duda", multiline=True, expand=True)   
    chat_area = ft.Column(scroll="always", expand=True)
    
    #envía tu pregunta
    def enviar(e):
        pregunta = entrada_usuario.value.strip()
        if not pregunta:
            return

        # Agrega tú pregunta a un "Historial"
        conversacion.append({"role": "user", "content": pregunta})

        # Mostrar en pantalla
        chat_area.controls.append(ft.Text(f"Tú: {pregunta}", selectable=True))
        entrada_usuario.value = ""
        page.update()

        # Obtener respuesta de la IA
        respuesta = pedir_a_llama()

        # Muestra la respuesta de Telmi
        conversacion.append({"role": "assistant", "content": respuesta})
        chat_area.controls.append(ft.Text(f"Telmi: {respuesta}", selectable=True))
        page.update()

    boton = ft.ElevatedButton("Enviar", on_click=enviar)

    page.add(
        ft.Text("Telmi-chan chat", size=20),
        chat_area,
        entrada_usuario,
        boton
    )

ft.app(target=main)
