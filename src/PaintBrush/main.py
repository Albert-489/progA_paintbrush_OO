from tkinter import ttk

def iniciar_figura_nova(event):
    global figura_nova
    ferramenta = ferramenta_var.get()
    
    cor_borda = cor_borda_var.get()
    cor_preenchimento = cor_preenchimento_var.get()
    
    if ferramenta == 'Mão Livre':
        figura_nova = ("rabisco", [(event.x, event.y)], cor_borda, cor_preenchimento)
    else:
  
        figura_nova = (ferramenta.lower(), (event.x, event.y, event.x, event.y), cor_borda, cor_preenchimento)


def atualizar_figura_nova(event):
    global figura_nova
    tipo, values, cor_b, cor_p = figura_nova
    
    if tipo == "rabisco":
        values.append((event.x, event.y))
        figura_nova = (tipo, values, cor_b, cor_p)
    else:
        figura_nova = (tipo, (values[0], values[1], event.x, event.y), cor_b, cor_p)
        
    desenhar()
    desenhar_figura_nova()

def incluir_figura_nova(event):
    if not incompleta(figura_nova): 
        figuras.append(figura_nova)
    desenhar()

def desenhar():
    canvas.delete("all")
    for tipo, values, cor_borda, cor_preenchimento in figuras:
        fill_color = "" if cor_preenchimento == "Nenhum" else cor_preenchimento
        
        if tipo == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3], fill=cor_borda)
        elif tipo == "retângulo":
            canvas.create_rectangle(values[0], values[1], values[2], values[3], outline=cor_borda, fill=fill_color)
        elif tipo == "oval":
            canvas.create_oval(values[0], values[1], values[2], values[3], outline=cor_borda, fill=fill_color)
        elif tipo == "rabisco":
            canvas.create_line(values, fill=cor_borda)

def desenhar_figura_nova():
    tipo, values, cor_borda, cor_preenchimento = figura_nova
    fill_color = "" if cor_preenchimento == "Nenhum" else cor_preenchimento
    
    if tipo == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], fill=cor_borda, dash=(4, 2))
    elif tipo == "retângulo":
        canvas.create_rectangle(values[0], values[1], values[2], values[3], outline=cor_borda, fill=fill_color, dash=(4, 2))
    elif tipo == "oval":
        canvas.create_oval(values[0], values[1], values[2], values[3], outline=cor_borda, fill=fill_color, dash=(4, 2))
    elif tipo == "rabisco":
        canvas.create_line(values, fill=cor_borda, dash=(4, 2))

def incompleta(figura):
    tipo, values, _, _ = figura
    if tipo == "rabisco":
        return len(values) <= 1
    else:
    
        return (values[0], values[1]) == (values[2], values[3])


figuras = []       
figura_nova = None 


def main():
    global canvas, ferramenta_var, cor_borda_var, cor_preenchimento_var

    root = tk.Tk()
    root.title("Mini Paint - Entrega 3")
    
    frame_controles = tk.Frame(root)
    frame_controles.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

  
    lbl_ferramenta = ttk.Label(frame_controles, text='Ferramenta:')
    lbl_ferramenta.pack(side=tk.LEFT, padx=5)
    
    ferramenta_var = tk.StringVar(root)
    combobox_ferramenta = ttk.Combobox(frame_controles, textvariable=ferramenta_var, state="readonly", width=12)
    combobox_ferramenta['values'] = ('Linha', 'Mão Livre', 'Retângulo', 'Oval')
    combobox_ferramenta.set('Linha')
    combobox_ferramenta.pack(side=tk.LEFT, padx=5)

    #Componente 2: Seleção de Cor da Borda ---
    lbl_borda = ttk.Label(frame_controles, text='Borda:')
    lbl_borda.pack(side=tk.LEFT, padx=5)
    
    cor_borda_var = tk.StringVar(root)
    combobox_borda = ttk.Combobox(frame_controles, textvariable=cor_borda_var, state="readonly", width=10)
    combobox_borda['values'] = ('black', 'red', 'blue', 'green', 'yellow')
    combobox_borda.set('black')
    combobox_borda.pack(side=tk.LEFT, padx=5)

    lbl_preenchimento = ttk.Label(frame_controles, text='Preenchimento:')
    lbl_preenchimento.pack(side=tk.LEFT, padx=5)
    
    cor_preenchimento_var = tk.StringVar(root)
    combobox_preenchimento = ttk.Combobox(frame_controles, textvariable=cor_preenchimento_var, state="readonly", width=10)
    combobox_preenchimento['values'] = ('Nenhum', 'white', 'red', 'blue', 'green', 'yellow')
    combobox_preenchimento.set('Nenhum')
    combobox_preenchimento.pack(side=tk.LEFT, padx=5)

    canvas = tk.Canvas(root, bg='white', width=600, height=600)
    canvas.pack(side=tk.BOTTOM, padx=5, pady=5)

    canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
    canvas.bind('<B1-Motion>', atualizar_figura_nova)
    canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

    root.mainloop()

if __name__ == "__main__":
    main()por enquanto.
