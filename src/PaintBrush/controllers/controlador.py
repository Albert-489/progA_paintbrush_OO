import model.figuras as figuras
from controllers.estado import (
    EstadoDesenhandoLinha, EstadoDesenhandoMaoLivre, EstadoDesenhandoRetangulo,
    EstadoDesenhandoOval, EstadoDesenhandoTriangulo, EstadoDesenhandoPentagono, EstadoDesenhandoHexagono
)

class Controlador:
    def __init__(self, desenho, interface):
        self.desenho = desenho
        self.interface = interface
        
        # Mapeamento do padrão State (eliminando os if/elif)
        self.estados = {
            'Linha': EstadoDesenhandoLinha(),
            'Mão Livre': EstadoDesenhandoMaoLivre(),
            'Retângulo': EstadoDesenhandoRetangulo(),
            'Oval': EstadoDesenhandoOval(),
            'Triângulo': EstadoDesenhandoTriangulo(),
            'Pentágono': EstadoDesenhandoPentagono(),
            'Hexágono': EstadoDesenhandoHexagono()
        }
        
        # Define o estado inicial da aplicação
        ferramenta_inicial = self.interface.ferramenta_var.get()
        self.estado_atual = self.estados[ferramenta_inicial]
        
        # Evento para detectar quando o usuário muda a ferramenta no menu
        self.interface.combobox_ferramenta.bind('<<ComboboxSelected>>', self.mudar_estado)

        # Liga os cliques na tela aos métodos do controlador
        self.interface.canvas.bind('<ButtonPress-1>', self.mouse_press)
        self.interface.canvas.bind('<B1-Motion>', self.mouse_drag)
        self.interface.canvas.bind('<ButtonRelease-1>', self.mouse_release)

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
