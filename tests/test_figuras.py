import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/PaintBrush')))

from model.figuras import Linha, Retangulo, Rabisco, Poligono, figura_from_dict

def test_geometria_linha():
    linha = Linha(10, 10, "black")
    assert linha.esta_incompleta() == True
    
    linha.atualizar(50, 50)
    assert linha.x2 == 50
    assert linha.y2 == 50
    assert linha.esta_incompleta() == False

def test_geometria_rabisco():
    rabisco = Rabisco(5, 5, "red")
    assert rabisco.esta_incompleta() == True
    
    rabisco.atualizar(10, 10)
    assert len(rabisco.pontos) == 2
    assert rabisco.esta_incompleta() == False

def test_serializacao_roundtrip_retangulo():
    ret = Retangulo(20, 20, "blue", "yellow")
    ret.atualizar(80, 80)
    
    dados = ret.to_dict()
    assert dados["tipo"] == "Retangulo"
    assert dados["cor_borda"] == "blue"
    assert dados["x2"] == 80
    
    ret_recriado = figura_from_dict(dados)
    assert isinstance(ret_recriado, Retangulo)
    assert ret_recriado.x2 == 80
    assert ret_recriado.cor_preenchimento == "yellow"

def test_serializacao_roundtrip_poligono():
    pol = Poligono(100, 100, 5, "green", "white")
    pol.atualizar(150, 150)
    
    dados = pol.to_dict()
    assert dados["tipo"] == "Poligono"
    assert dados["num_lados"] == 5
    
    pol_recriado = figura_from_dict(dados)
    assert isinstance(pol_recriado, Poligono)
    assert pol_recriado.num_lados == 5
    assert len(pol_recriado.pontos) == 5