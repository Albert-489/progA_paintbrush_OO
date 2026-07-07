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


class Rabisco(Figura):
   
    def __init__(self, x, y, cor_borda="black"):
        super()._init_(cor_borda, cor_preenchimento="")
        self.pontos = [(x, y)]

    def atualizar(self, x, y):
        self.pontos.append((x, y))

    def desenhar(self, canvas, tracejado=False):
        if len(self.pontos) > 1:
            dash_pattern = (4, 2) if tracejado else ""
            
            canvas.create_line(self.pontos, fill=self.cor_borda, dash=dash_pattern)

    def esta_incompleta(self):
        return len(self.pontos) <= 1
    
class FiguraBidimensional(Figura):
  
    def __init__(self, x1, y1, cor_borda="black", cor_preenchimento=""):
        super()._init_(cor_borda, cor_preenchimento)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1 
        self.y2 = y1

    def atualizar(self, x, y):
        self.x2 = x
        self.y2 = y

    def esta_incompleta(self):
        return (self.x1, self.y1) == (self.x2, self.y2)


class Linha(FiguraBidimensional):
    def init(self, x1, y1, cor_borda="black"):
        super()._init_(x1, y1, cor_borda, cor_preenchimento="")

    def desenhar(self, canvas, tracejado=False):
        dash_pattern = (4, 2) if tracejado else ""
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, 
                           fill=self.cor_borda, dash=dash_pattern)


class Retangulo(FiguraBidimensional):
    def desenhar(self, canvas, tracejado=False):
        dash_pattern = (4, 2) if tracejado else ""
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, 
                                outline=self.cor_borda, 
                                fill=self.cor_preenchimento, 
                                dash=dash_pattern)


class Oval(FiguraBidimensional):
    def desenhar(self, canvas, tracejado=False):
        dash_pattern = (4, 2) if tracejado else ""
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, 
                            outline=self.cor_borda, 
                            fill=self.cor_preenchimento, 
                            dash=dash_pattern)
        

class Poligono(Figura):
 
    def __init__(self, x, y, num_lados, cor_borda="black", cor_preenchimento=""):
        super()._init_(cor_borda, cor_preenchimento)
        self.cx = x         
        self.cy = y          
        self.num_lados = num_lados
        self.pontos = []     

    def atualizar(self, x, y):

        raio = math.sqrt((x - self.cx)*2 + (y - self.cy)*2)
        
        angulo_base = math.atan2(y - self.cy, x - self.cx)
        
        self.pontos = []
        for i in range(self.num_lados):
            angulo = angulo_base + (2 * math.pi * i / self.num_lados)
            px = self.cx + raio * math.cos(angulo)
            py = self.cy + raio * math.sin(angulo)
            self.pontos.append((px, py))

    def desenhar(self, canvas, tracejado=False):
        if self.pontos:
            dash_pattern = (4, 2) if tracejado else ""
            canvas.create_polygon(self.pontos, 
                                  outline=self.cor_borda, 
                                  fill=self.cor_preenchimento, 
                                  dash=dash_pattern)

    def esta_incompleta(self):
        return len(self.pontos) < 3