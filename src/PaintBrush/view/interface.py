import tkinter as tk
from tkinter import ttk

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Paint")
        
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
        self.combobox_borda['values'] = ('Preto', 'Vermelho', 'Azul', 'Verde', 'Amarelo')
        self.combobox_borda.set('Preto')
        self.combobox_borda.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame_controles, text='Preenchimento:').pack(side=tk.LEFT, padx=5)
        self.cor_preenchimento_var = tk.StringVar()
        self.combobox_preenchimento = ttk.Combobox(frame_controles, textvariable=self.cor_preenchimento_var, state="readonly", width=10)
        self.combobox_preenchimento['values'] = ('Nenhum', 'Branco', 'Vermelho', 'Azul', 'Verde', 'Amarelo')
        self.combobox_preenchimento.set('Nenhum')
        self.combobox_preenchimento.pack(side=tk.LEFT, padx=5)
        
        self.canvas = tk.Canvas(self.root, bg='white', width=600, height=600)
        self.canvas.pack(side=tk.BOTTOM, padx=5, pady=5)