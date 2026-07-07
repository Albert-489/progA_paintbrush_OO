from abc import ABC, abstractmethod
import model.figuras as figuras

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
