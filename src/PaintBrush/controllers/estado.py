from abc import ABC, abstractmethod
import model.figuras as figuras
from model.selecao_utils import ponto_esta_na_figura, mover_figura

class EstadoApp(ABC):
    @abstractmethod
    def mouse_press(self, event, controlador): pass
    
    @abstractmethod
    def mouse_drag(self, event, controlador): pass
    
    @abstractmethod
    def mouse_release(self, event, controlador): pass

class EstadoDesenhandoBase(EstadoApp):
    @abstractmethod
    def criar_figura(self, x, y, cor_b, cor_p):
        pass

    def mouse_press(self, event, controlador):
        cor_b = controlador.interface.cor_borda_var.get()
        cor_p = controlador.interface.cor_preenchimento_var.get()
        controlador.desenho.figura_atual = self.criar_figura(event.x, event.y, cor_b, cor_p)

    def mouse_drag(self, event, controlador):
        if controlador.desenho.figura_atual:
            controlador.desenho.figura_atual.atualizar(event.x, event.y)
            controlador.renderizar_tela()

    def mouse_release(self, event, controlador):
        if controlador.desenho.figura_atual:
            controlador.desenho.adicionar_figura()
            controlador.renderizar_tela()


class EstadoDesenhandoLinha(EstadoDesenhandoBase):
    def criar_figura(self, x, y, cor_b, cor_p):
        return figuras.Linha(x, y, cor_b)

class EstadoDesenhandoMaoLivre(EstadoDesenhandoBase):
    def criar_figura(self, x, y, cor_b, cor_p):
        return figuras.Rabisco(x, y, cor_b)

class EstadoDesenhandoRetangulo(EstadoDesenhandoBase):
    def criar_figura(self, x, y, cor_b, cor_p):
        fill_color = "" if cor_p == "Nenhum" else cor_p
        return figuras.Retangulo(x, y, cor_b, fill_color)

class EstadoDesenhandoOval(EstadoDesenhandoBase):
    def criar_figura(self, x, y, cor_b, cor_p):
        fill_color = "" if cor_p == "Nenhum" else cor_p
        return figuras.Oval(x, y, cor_b, fill_color)

class EstadoDesenhandoTriangulo(EstadoDesenhandoBase):
    def criar_figura(self, x, y, cor_b, cor_p):
        fill_color = "" if cor_p == "Nenhum" else cor_p
        return figuras.Poligono(x, y, 3, cor_b, fill_color)

class EstadoDesenhandoPentagono(EstadoDesenhandoBase):
    def criar_figura(self, x, y, cor_b, cor_p):
        fill_color = "" if cor_p == "Nenhum" else cor_p
        return figuras.Poligono(x, y, 5, cor_b, fill_color)

class EstadoDesenhandoHexagono(EstadoDesenhandoBase):
    def criar_figura(self, x, y, cor_b, cor_p):
        fill_color = "" if cor_p == "Nenhum" else cor_p
        return figuras.Poligono(x, y, 6, cor_b, fill_color)


class EstadoSelecionando(EstadoApp):
    def __init__(self):
        self.arrastando = False
        self.ultimo_x = None
        self.ultimo_y = None

    def mouse_press(self, event, controlador):
        desenho = controlador.desenho
        figura_clicada = None

        # percorre de tras pra frente: seleciona a figura desenhada por ultimo (fica visualmente por cima)
        for figura in reversed(desenho.figuras_desenhadas):
            if ponto_esta_na_figura(figura, event.x, event.y):
                figura_clicada = figura
                break

        desenho.figura_selecionada = figura_clicada
        self.arrastando = figura_clicada is not None
        self.ultimo_x = event.x
        self.ultimo_y = event.y
        controlador.renderizar_tela()

    def mouse_drag(self, event, controlador):
        desenho = controlador.desenho
        if self.arrastando and desenho.figura_selecionada:
            dx = event.x - self.ultimo_x
            dy = event.y - self.ultimo_y
            mover_figura(desenho.figura_selecionada, dx, dy)
            self.ultimo_x = event.x
            self.ultimo_y = event.y
            controlador.renderizar_tela()

    def mouse_release(self, event, controlador):
        self.arrastando = False
