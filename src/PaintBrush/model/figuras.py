from abc import ABC, abstractmethod
import math

class Figura(ABC):
    def __init__(self, cor_borda="black", cor_preenchimento=""):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    @abstractmethod
    def atualizar(self, x, y):
        pass

    @abstractmethod
    def desenhar(self, canvas, tracejado=False):
        pass

    @abstractmethod
    def esta_incompleta(self):
        pass

    def to_dict(self):
        return {
            "tipo": self.__class__.__name__,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento
        }

class Rabisco(Figura):
    def __init__(self, x, y, cor_borda="black"):
        super().__init__(cor_borda, cor_preenchimento="")
        self.pontos = [(x, y)]

    def atualizar(self, x, y):
        self.pontos.append((x, y))

    def desenhar(self, canvas, tracejado=False):
        if len(self.pontos) > 1:
            dash_pattern = (4, 2) if tracejado else None
            canvas.create_line(self.pontos, fill=self.cor_borda, dash=dash_pattern)

    def esta_incompleta(self):
        return len(self.pontos) <= 1

    def to_dict(self):
        data = super().to_dict()
        data["pontos"] = self.pontos
        return data

class FiguraBidimensional(Figura):
    def __init__(self, x1, y1, cor_borda="black", cor_preenchimento=""):
        super().__init__(cor_borda, cor_preenchimento)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1
        self.y2 = y1

    def atualizar(self, x, y):
        self.x2 = x
        self.y2 = y

    def esta_incompleta(self):
        return (self.x1, self.y1) == (self.x2, self.y2)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "x1": self.x1, "y1": self.y1,
            "x2": self.x2, "y2": self.y2
        })
        return data

class Linha(FiguraBidimensional):
    def __init__(self, x1, y1, cor_borda="black"):
        super().__init__(x1, y1, cor_borda, cor_preenchimento="")

    def desenhar(self, canvas, tracejado=False):
        dash_pattern = (4, 2) if tracejado else None
        canvas.create_line(self.x1, self.y1, self.x2, self.y2,
                           fill=self.cor_borda, dash=dash_pattern)

class Retangulo(FiguraBidimensional):
    def desenhar(self, canvas, tracejado=False):
        dash_pattern = (4, 2) if tracejado else None
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                 outline=self.cor_borda,
                                 fill=self.cor_preenchimento,
                                 dash=dash_pattern)

class Oval(FiguraBidimensional):
    def desenhar(self, canvas, tracejado=False):
        dash_pattern = (4, 2) if tracejado else None
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2,
                             outline=self.cor_borda,
                             fill=self.cor_preenchimento,
                             dash=dash_pattern)

class Poligono(Figura):
    def __init__(self, x, y, num_lados, cor_borda="black", cor_preenchimento=""):
        super().__init__(cor_borda, cor_preenchimento)
        self.cx = x
        self.cy = y
        self.num_lados = num_lados
        self.pontos = []

    def atualizar(self, x, y):
        raio = math.sqrt((x - self.cx)**2 + (y - self.cy)**2)
        angulo_base = math.atan2(y - self.cy, x - self.cx)

        self.pontos = []
        for i in range(self.num_lados):
            angulo = angulo_base + (2 * math.pi * i / self.num_lados)
            px = self.cx + raio * math.cos(angulo)
            py = self.cy + raio * math.sin(angulo)
            self.pontos.append((px, py))

    def desenhar(self, canvas, tracejado=False):
        if self.pontos:
            dash_pattern = (4, 2) if tracejado else None
            canvas.create_polygon(self.pontos,
                                   outline=self.cor_borda,
                                   fill=self.cor_preenchimento,
                                   dash=dash_pattern)

    def esta_incompleta(self):
        return len(self.pontos) < 3

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "cx": self.cx, "cy": self.cy,
            "num_lados": self.num_lados,
            "pontos": self.pontos
        })
        return data


def figura_from_dict(data):
    tipo = data.get("tipo")
    cor_b = data.get("cor_borda", "black")
    cor_p = data.get("cor_preenchimento", "")

    if tipo == "Rabisco":
        fig = Rabisco(0, 0, cor_b)
        fig.pontos = data["pontos"]
        return fig
    elif tipo == "Linha":
        fig = Linha(data["x1"], data["y1"], cor_b)
        fig.x2, fig.y2 = data["x2"], data["y2"]
        return fig
    elif tipo == "Retangulo":
        fig = Retangulo(data["x1"], data["y1"], cor_b, cor_p)
        fig.x2, fig.y2 = data["x2"], data["y2"]
        return fig
    elif tipo == "Oval":
        fig = Oval(data["x1"], data["y1"], cor_b, cor_p)
        fig.x2, fig.y2 = data["x2"], data["y2"]
        return fig
    elif tipo == "Poligono":
        fig = Poligono(data["cx"], data["cy"], data["num_lados"], cor_b, cor_p)
        fig.pontos = data["pontos"]
        return fig

    return None