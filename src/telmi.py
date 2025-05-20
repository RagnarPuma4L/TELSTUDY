import flet as ft
import requests

# Función para hablar con LLaMA
def chat_with_llama(prompt):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]

# Función principal de la app
def main(page: ft.Page):
    page.title = "Chat con LLaMA 2 (local)"
    chat_box = ft.TextField(multiline=True, expand=True, read_only=True, value="", height=400)
    input_box = ft.TextField(label="Tu mensaje", autofocus=True, on_submit=lambda e: send_message(None))
    send_btn = ft.ElevatedButton("Enviar", on_click=lambda e: send_message(None))

    def send_message(_):
        prompt = input_box.value.strip()
        if prompt == "":
            return
        chat_box.value += f"Tú: {prompt}\n"
        input_box.value = ""
        page.update()
        response = chat_with_llama(prompt)
        chat_box.value += f"LLaMA: {response}\n\n"
        page.update()

    page.add(chat_box, input_box, send_btn)

# Ejecutar la app
ft.app(target=main)
