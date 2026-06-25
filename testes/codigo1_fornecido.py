# Desenha apenas uma linha
# Ao desenhar outra, apaga a anterior

import tkinter as tk
from tkinter import ttk

def marca_inicio(event):
    global ini_x, ini_y
    ini_x = event.x
    ini_y = event.y

def atualiza_fim(event):
    global fim_x, fim_y, id_figura_temp
    fim_x = event.x
    fim_y = event.y
    
    ferramenta = combobox_ferramenta.get()
    
    if id_figura_temp:
        canvas.delete(id_figura_temp)
    

    if ferramenta == "Linha":
        id_figura_temp = canvas.create_line(ini_x, ini_y, fim_x, fim_y, dash=(4, 4))
        
    elif ferramenta == "Retângulo":
        id_figura_temp = canvas.create_rectangle(ini_x, ini_y, fim_x, fim_y, dash=(4, 4))

def finaliza_desenho(event):
    global fim_x, fim_y, id_figura_temp
    fim_x = event.x
    fim_y = event.y
    

root = tk.Tk()

opcoes = ["Linha", "Retângulo", "Oval"]
combobox_ferramenta = ttk.Combobox(root, values=opcoes, state="readonly")
combobox_ferramenta.set("Linha") # Define "Linha" como padrão ao abrir
combobox_ferramenta.pack(pady=5)

canvas = tk.Canvas(root, bg='white', width=600, height=600)
canvas.pack()

ini_x = None
ini_y = None
fim_x = None
fim_y = None
id_figura_temp = None
canvas.bind('<ButtonPress-1>', marca_inicio)
canvas.bind('<B1-Motion>', atualiza_fim)
canvas.bind('<ButtonRelease-1>', finaliza_desenho)


root.mainloop()