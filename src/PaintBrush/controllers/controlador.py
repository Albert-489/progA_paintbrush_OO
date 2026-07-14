import copy
import model.figuras as figuras
from controllers.estado import (
    EstadoDesenhandoLinha, EstadoDesenhandoMaoLivre, EstadoDesenhandoRetangulo,
    EstadoDesenhandoOval, EstadoDesenhandoTriangulo, EstadoDesenhandoPentagono, EstadoDesenhandoHexagono,
    EstadoSelecionando
)
from model.selecao_utils import mover_figura
from tkinter import filedialog

class Controlador:
    def __init__(self, desenho, interface):
        self.desenho = desenho
        self.interface = interface
        
        self.estados = {
            'Linha': EstadoDesenhandoLinha(),
            'Mão Livre': EstadoDesenhandoMaoLivre(),
            'Retângulo': EstadoDesenhandoRetangulo(),
            'Oval': EstadoDesenhandoOval(),
            'Triângulo': EstadoDesenhandoTriangulo(),
            'Pentágono': EstadoDesenhandoPentagono(),
            'Hexágono': EstadoDesenhandoHexagono(),
            'Selecionar': EstadoSelecionando()
        }
        
        ferramenta_inicial = self.interface.ferramenta_var.get()
        self.estado_atual = self.estados[ferramenta_inicial]

        self.interface.combobox_ferramenta.bind('<<ComboboxSelected>>', self.mudar_estado)

        self.interface.canvas.bind('<ButtonPress-1>', self.mouse_press)
        self.interface.canvas.bind('<B1-Motion>', self.mouse_drag)
        self.interface.canvas.bind('<ButtonRelease-1>', self.mouse_release)
        self.interface.btn_salvar.config(command=self.salvar_desenho)
        self.interface.btn_abrir.config(command=self.abrir_desenho)

        self.figura_copiada = None
        self.interface.root.bind('<Delete>', self.apagar_figura_selecionada)
        self.interface.root.bind('<Control-c>', self.copiar_figura)
        self.interface.root.bind('<Control-v>', self.colar_figura)

    def mudar_estado(self, event=None):
        ferramenta = self.interface.ferramenta_var.get()
        self.estado_atual = self.estados[ferramenta]

    # O Controlador não toma mais decisões, ele apenas delega para o estado atual
    def mouse_press(self, event):
        self.estado_atual.mouse_press(event, self)

    def mouse_drag(self, event):
        self.estado_atual.mouse_drag(event, self)

    def mouse_release(self, event):
        self.estado_atual.mouse_release(event, self)

    def renderizar_tela(self):
        self.interface.canvas.delete("all")
        
        for figura in self.desenho.figuras_desenhadas:
            figura.desenhar(self.interface.canvas)
            
        if self.desenho.figura_atual:
            self.desenho.figura_atual.desenhar(self.interface.canvas, tracejado=True)
    
    def salvar_desenho(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os Arquivos", "*.*")]
        )
        if caminho:
            self.desenho.salvar_para_arquivo(caminho)

    def abrir_desenho(self):
        caminho = filedialog.askopenfilename(
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os Arquivos", "*.*")]
        )
        if caminho:
            self.desenho.carregar_de_arquivo(caminho)
            self.renderizar_tela()

    def apagar_figura_selecionada(self, event=None):
        if self.desenho.figura_selecionada:
            self.desenho.remover_figura(self.desenho.figura_selecionada)
            self.renderizar_tela()

    def copiar_figura(self, event=None):
        if self.desenho.figura_selecionada:
            self.figura_copiada = copy.deepcopy(self.desenho.figura_selecionada)

    def colar_figura(self, event=None):
        if self.figura_copiada:
            nova_figura = copy.deepcopy(self.figura_copiada)
            mover_figura(nova_figura, 20, 20)  # desloca pra nao colar exatamente em cima
            self.desenho.figuras_desenhadas.append(nova_figura)
            self.desenho.figura_selecionada = nova_figura
            self.figura_copiada = nova_figura  # permite colar varias vezes com deslocamento incremental
            self.renderizar_tela()
