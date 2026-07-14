import json
from model.figuras import figura_from_dict

class Desenho:
    def __init__(self):
        self.figuras_desenhadas = []
        self.figura_atual = None
        self.figuras_selecionadas = []

    def remover_figura(self, figura):
        if figura in self.figuras_desenhadas:
            self.figuras_desenhadas.remove(figura)
        if figura in self.figuras_selecionadas:
            self.figuras_selecionadas.remove(figura)

    def adicionar_figura(self):
        if self.figura_atual and not self.figura_atual.esta_incompleta():
            self.figuras_desenhadas.append(self.figura_atual)
        self.figura_atual = None

    def mover_para_frente(self):
        for figura in list(self.figuras_selecionadas):
            if figura in self.figuras_desenhadas:
                self.figuras_desenhadas.remove(figura)
                self.figuras_desenhadas.append(figura)

    def mover_para_tras(self):
        for figura in reversed(list(self.figuras_selecionadas)):
            if figura in self.figuras_desenhadas:
                self.figuras_desenhadas.remove(figura)
                self.figuras_desenhadas.insert(0, figura)

    def salvar_para_arquivo(self, caminho):
        dados = [figura.to_dict() for figura in self.figuras_desenhadas]
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4)

    def carregar_de_arquivo(self, caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        self.figuras_desenhadas = []
        self.figuras_selecionadas = []
        for item in dados:
            figura = figura_from_dict(item)
            if figura:
                self.figuras_desenhadas.append(figura)
