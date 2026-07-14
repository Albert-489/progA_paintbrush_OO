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

        self.figuras_copiadas = []
        
        self.interface.root.bind('<Delete>', self.apagar_figuras_selecionadas)
        self.interface.root.bind('<Control-c>', self.copiar_figuras)
        self.interface.root.bind('<Control-v>', self.colar_figuras)
        
        self.interface.root.bind('<Key-f>', self.trazer_para_frente)
        self.interface.root.bind('<Key-b>', self.enviar_para_tras)

    def mudar_estado(self, event=None):
        ferramenta = self.interface.ferramenta_var.get()
        self.estado_atual = self.estados[ferramenta]

    def mouse_press(self, event):
        self.estado_atual.mouse_press(event, self)

    def mouse_drag(self, event):
        self.estado_atual.mouse_drag(event, self)

    def mouse_release(self, event):
        self.estado_atual.mouse_release(event, self)

    def renderizar_tela(self):
        self.interface.canvas.delete("all")
        
        for figura in self.desenho.figuras_desenhadas:
            tracejada = figura in self.desenho.figuras_selecionadas
            figura.desenhar(self.interface.canvas, tracejado=tracejada)
            
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

    def apagar_figuras_selecionadas(self, event=None):
        for figura in list(self.desenho.figuras_selecionadas):
            self.desenho.remover_figura(figura)
        self.desenho.figuras_selecionadas = []
        self.renderizar_tela()

    def copiar_figuras(self, event=None):
        if self.desenho.figuras_selecionadas:
            self.figuras_copiadas = [copy.deepcopy(f) for f in self.desenho.figuras_selecionadas]

    def colar_figuras(self, event=None):
        if self.figuras_copiadas:
            novas_figuras = []
            for figura in self.figuras_copiadas:
                nova_figura = copy.deepcopy(figura)
                mover_figura(nova_figura, 20, 20)  # Desloca o lote clonado
                self.desenho.figuras_desenhadas.append(nova_figura)
                novas_figuras.append(nova_figura)
            
            self.desenho.figuras_selecionadas = novas_figuras
            self.figuras_copiadas = novas_figuras
            self.renderizar_tela()

    def trazer_para_frente(self, event=None):
        self.desenho.mover_para_frente()
        self.renderizar_tela()

    def enviar_para_tras(self, event=None):
        self.desenho.mover_para_tras()
        self.renderizar_tela()
