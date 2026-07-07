class Desenho:
    def __init__(self):
        self.figuras_desenhadas = []
        self.figura_atual = None

    def adicionar_figura(self):
        if self.figura_atual and not self.figura_atual.esta_incompleta():
            self.figuras_desenhadas.append(self.figura_atual)
        self.figura_atual = None