import json
from model.figuras import figura_from_dict
class Desenho:
    def __init__(self):
        self.figuras_desenhadas = []
        self.figura_atual = None
        self.figura_selecionada = None

    def remover_figura(self, figura):
        if figura in self.figuras_desenhadas:
            self.figuras_desenhadas.remove(figura)
        if self.figura_selecionada is figura:
            self.figura_selecionada = None

    def adicionar_figura(self):
        if self.figura_atual and not self.figura_atual.esta_incompleta():
            self.figuras_desenhadas.append(self.figura_atual)
        self.figura_atual = None
    def salvar_para_arquivo(self, caminho):
        dados = [figura.to_dict() for figura in self.figuras_desenhadas]
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4)

    def carregar_de_arquivo(self, caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        self.figuras_desenhadas = []
        for item in dados:
            figura = figura_from_dict(item)
            if figura:
                self.figuras_desenhadas.append(figura)
