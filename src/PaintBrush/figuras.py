from abc import ABC, abstractmethod

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
