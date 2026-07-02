import tkinter as tk
from tkinter import ttk
import figuras  

class PaintApp:
     def __init__(self, root):
        self.root = root
        self.root.title("Mini Paint - Orientado a Objetos")
        
        self.figuras_desenhadas = []       
        self.figura_atual = None 
        
        self.configurar_interface()

     def configurar_interface(self):
  
        frame_controles = tk.Frame(self.root)
        frame_controles.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

 
        ttk.Label(frame_controles, text='Ferramenta:').pack(side=tk.LEFT, padx=5)
        self.ferramenta_var = tk.StringVar()
        self.combobox_ferramenta = ttk.Combobox(frame_controles, textvariable=self.ferramenta_var, state="readonly", width=12)
        self.combobox_ferramenta['values'] = ('Linha', 'Mão Livre', 'Retângulo', 'Oval', 'Triângulo', 'Pentágono', 'Hexágono')
        self.combobox_ferramenta.set('Linha')
        self.combobox_ferramenta.pack(side=tk.LEFT, padx=5)

        ttk.Label(frame_controles, text='Borda:').pack(side=tk.LEFT, padx=5)
        self.cor_borda_var = tk.StringVar()
        self.combobox_borda = ttk.Combobox(frame_controles, textvariable=self.cor_borda_var, state="readonly", width=10)
        self.combobox_borda['values'] = ('black', 'red', 'blue', 'green', 'yellow')
        self.combobox_borda.set('black')
        self.combobox_borda.pack(side=tk.LEFT, padx=5)

        ttk.Label(frame_controles, text='Preenchimento:').pack(side=tk.LEFT, padx=5)
        self.cor_preenchimento_var = tk.StringVar()
        self.combobox_preenchimento = ttk.Combobox(frame_controles, textvariable=self.cor_preenchimento_var, state="readonly", width=10)
        self.combobox_preenchimento['values'] = ('Nenhum', 'white', 'red', 'blue', 'green', 'yellow')
        self.combobox_preenchimento.set('Nenhum')
        self.combobox_preenchimento.pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(self.root, bg='white', width=600, height=600)
        self.canvas.pack(side=tk.BOTTOM, padx=5, pady=5)


        self.canvas.bind('<ButtonPress-1>', self.iniciar_figura_nova)
        self.canvas.bind('<B1-Motion>', self.atualizar_figura_nova)
        self.canvas.bind('<ButtonRelease-1>', self.incluir_figura_nova)

     def criar_instancia_figura(self, ferramenta, x, y, cor_b, cor_p):
 
        fill_color = "" if cor_p == "Nenhum" else cor_p

        if ferramenta == 'Mão Livre':
            return figuras.Rabisco(x, y, cor_b)
        elif ferramenta == 'Linha':
            return figuras.Linha(x, y, cor_b)
        elif ferramenta == 'Retângulo':
            return figuras.Retangulo(x, y, cor_b, fill_color)
        elif ferramenta == 'Oval':
            return figuras.Oval(x, y, cor_b, fill_color)
        elif ferramenta == 'Triângulo':
            return figuras.Poligono(x, y, 3, cor_b, fill_color)
        elif ferramenta == 'Pentágono':
            return figuras.Poligono(x, y, 5, cor_b, fill_color)
        elif ferramenta == 'Hexágono':
            return figuras.Poligono(x, y, 6, cor_b, fill_color)
        return None

     def iniciar_figura_nova(self, event):
        ferramenta = self.ferramenta_var.get()
        cor_borda = self.cor_borda_var.get()
        cor_preenchimento = self.cor_preenchimento_var.get()
        
        self.figura_atual = self.criar_instancia_figura(ferramenta, event.x, event.y, cor_borda, cor_preenchimento)

     def atualizar_figura_nova(self, event):
        if self.figura_atual:
            self.figura_atual.atualizar(event.x, event.y)
            self.renderizar_tela()

     def incluir_figura_nova(self, event):
        if self.figura_atual:
            if not self.figura_atual.esta_incompleta():
                self.figuras_desenhadas.append(self.figura_atual)
            self.figura_atual = None
            self.renderizar_tela()

     def renderizar_tela(self):
   
        self.canvas.delete("all")
        
        for figura in self.figuras_desenhadas:
            figura.desenhar(self.canvas)
            
        if self.figura_atual:
            self.figura_atual.desenhar(self.canvas, tracejado=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()