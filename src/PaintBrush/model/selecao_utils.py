def ponto_esta_na_figura(figura, x, y, tolerancia=5):
    tipo = figura.__class__.__name__

    if tipo == "FiguraComposta":
        return figura.contem_ponto(x, y, tolerancia)

    if tipo in ("Retangulo", "Oval", "Linha"):
        x1, y1, x2, y2 = figura.x1, figura.y1, figura.x2, figura.y2
        xmin, xmax = min(x1, x2) - tolerancia, max(x1, x2) + tolerancia
        ymin, ymax = min(y1, y2) - tolerancia, max(y1, y2) + tolerancia
        return xmin <= x <= xmax and ymin <= y <= ymax

    if tipo == "Rabisco":
        for px, py in figura.pontos:
            if abs(px - x) <= tolerancia and abs(py - y) <= tolerancia:
                return True
        return False

    if tipo == "Poligono":
        if not figura.pontos:
            return False
        xs = [p[0] for p in figura.pontos]
        ys = [p[1] for p in figura.pontos]
        xmin, xmax = min(xs) - tolerancia, max(xs) + tolerancia
        ymin, ymax = min(ys) - tolerancia, max(ys) + tolerancia
        return xmin <= x <= xmax and ymin <= y <= ymax

    return False


def mover_figura(figura, dx, dy):
    tipo = figura.__class__.__name__

    if tipo == "FiguraComposta":
        figura.mover(dx, dy)
        return

    if tipo in ("Retangulo", "Oval", "Linha"):
        figura.x1 += dx
        figura.y1 += dy
        figura.x2 += dx
        figura.y2 += dy

    elif tipo == "Rabisco":
        figura.pontos = [(px + dx, py + dy) for px, py in figura.pontos]

    elif tipo == "Poligono":
        figura.cx += dx
        figura.cy += dy
        figura.pontos = [(px + dx, py + dy) for px, py in figura.pontos]
