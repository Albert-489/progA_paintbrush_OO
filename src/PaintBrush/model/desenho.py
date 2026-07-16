import json
from model.figuras import figura_from_dict, FiguraComposta

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

    def agrupar_selecionadas(self):
        selecionadas = [f for f in self.figuras_selecionadas if f in self.figuras_desenhadas]

        if len(selecionadas) < 2:
            return None

        indice_insercao = min(self.figuras_desenhadas.index(f) for f in selecionadas)

        for figura in selecionadas:
            self.figuras_desenhadas.remove(figura)

        grupo = FiguraComposta(selecionadas)
        self.figuras_desenhadas.insert(indice_insercao, grupo)

        self.figuras_selecionadas = [grupo]
        return grupo

    def desagrupar_selecionadas(self):
        grupos = [f for f in self.figuras_selecionadas
                  if isinstance(f, FiguraComposta) and f in self.figuras_desenhadas]

        if not grupos:
            return []

        novas_selecionadas = []
        for grupo in grupos:
            indice = self.figuras_desenhadas.index(grupo)
            self.figuras_desenhadas.pop(indice)
            for i, filha in enumerate(grupo.figuras):
                self.figuras_desenhadas.insert(indice + i, filha)
            novas_selecionadas.extend(grupo.figuras)

        self.figuras_selecionadas = novas_selecionadas
        return novas_selecionadas

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
