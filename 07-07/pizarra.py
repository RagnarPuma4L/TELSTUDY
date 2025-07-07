from tkinter import *

# Crear ventana principal
Window = Tk()

#Instrucciones
Window.title("Pizarra")

# Crear canvas
canvas = Canvas(Window, width=800, height=600, bg="white")
canvas.pack()

# Variables globales
is_drawing = False
last_x, last_y = 0, 0
lines = []
color_actual = "black"  # Color por defecto

# Iniciar dibujo
def start_drawing(event):
    global is_drawing, last_x, last_y
    is_drawing = True
    last_x, last_y = event.x, event.y

# Terminar dibujo
def stop_drawing(event):
    global is_drawing
    is_drawing = False

# Dibujar línea
def draw(event):
    global last_x, last_y, color_actual
    if is_drawing:
        line = canvas.create_line(last_x, last_y, event.x, event.y, fill=color_actual, width=2)
        lines.append(line)
        last_x, last_y = event.x, event.y

# Deshacer última línea
def undo(event):
    if lines:
        canvas.delete(lines.pop())

# Borrar todo
def clear_canvas(event=None):
    canvas.delete("all")
    lines.clear()

# Cambiar color del lápiz
def cambiar_color(nuevo_color):
    global color_actual
    color_actual = nuevo_color

# Enlazar eventos del mouse
canvas.bind('<Button-1>', start_drawing)
canvas.bind('<ButtonRelease-1>', stop_drawing)
canvas.bind('<B1-Motion>', draw)

# Atajos de teclado
Window.bind('<Control-z>', undo)
Window.bind('<Control-x>', clear_canvas)

# Botones de color
colores = ["black", "red", "blue", "green", "orange", "purple"]
for c in colores:
    btn = Button(Window, text=c.capitalize(), bg=c, fg="white" if c != "yellow" else "black",
                 command=lambda col=c: cambiar_color(col))
    btn.pack(side=LEFT, padx=2)


def cerrar_pizarra():
    with open("pizarra_cerrada.flag", "w") as f:
        f.write("") 
    Window.destroy()

Window.protocol("WM_DELETE_WINDOW", cerrar_pizarra)

Window.mainloop()
