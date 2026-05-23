"""
CC BY: Thiago Pacheco Carneiro 2022
https://creativecommons.org/licenses/by/4.0/
"""

import random
import math


def _bresenham_line(
    x1: int,
    y1: int,
    x2: int,
    y2: int,
) -> list[tuple[int, int]]:
    points: list[tuple[int, int]] = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        points.append((x1, y1))
        if x1 == x2 and y1 == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

    return points


def obtem_linha_secao(
    largura: int = 1024,
    altura: int = 1024,
    largura_secao: int = 512,
) -> list[tuple[int, int]]:
    """Retorna uma linha 2D aleatória dentro de um retângulo.

    A linha começa em um ponto aleatório na face superior e termina
    em outro ponto que também está dentro do retângulo.

    Args:
        largura (int, optional): largura do retângulo. Defaults to 1024.
        altura (int, optional): altura do retângulo. Defaults to 1024.
        largura_secao (int, optional): comprimento da linha.
            Defaults to 512.

    Returns:
        list[tuple[int, int]]: lista de pontos inteiros entre as duas pontas.
    """
    if largura <= 0 or altura <= 0:
        raise ValueError("largura e altura devem ser maiores que zero")
    if largura_secao <= 0:
        raise ValueError("largura_secao deve ser maior que zero")

    max_len = math.hypot(largura - 1, altura - 1)
    if largura_secao > max_len:
        raise ValueError(
            "largura_secao não pode ser maior que a diagonal do retângulo"
        )

    x1 = random.randrange(largura)
    y1 = random.randrange(altura)
    x2 = -1
    y2 = -1

    while (x2 < 0 or x2 >= largura or y2 < 0 or y2 >= altura):
        theta = random.random() * 2 * math.pi
        x2 = int(round(x1 + largura_secao * math.cos(theta)))
        y2 = int(round(y1 + largura_secao * math.sin(theta)))

    return _bresenham_line(x1, y1, x2, y2)

    raise RuntimeError("Não foi possível encontrar uma linha válida dentro do retângulo")


def main():
    """Exemplo de uso de obtem_linha_secao em um volume menor."""
    import numpy as np
    import matplotlib.pyplot as plt

    largura, altura, profundidade = 1024, 1024, 1024
    cubo = np.zeros((largura, altura, profundidade), dtype=np.uint8)
    centro = largura // 2

    for z in range(profundidade):
        raio = int((z + 1) * centro / profundidade)
        if raio < 1:
            continue
        perimetro_int = max(8, math.ceil(2 * math.pi * raio))
        for arco in range(perimetro_int):
            theta = 2 * math.pi * arco / perimetro_int
            x = centro + int(raio * math.cos(theta))
            y = centro + int(raio * math.sin(theta))
            if 0 <= x < largura and 0 <= y < altura:
                cubo[x, y, z] = 1

    largura_secao = 1024
    linha_secao = obtem_linha_secao(largura, altura, largura_secao)

    img = np.stack([cubo[x, y, :] for x, y in linha_secao], axis=0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Seção vertical (projeção ao longo da profundidade)
    ax1.imshow(img.T, aspect="auto", origin="lower", cmap="gray")
    ax1.set_title("Seção vertical aleatória do volume")
    ax1.set_xlabel("profundidade")
    ax1.set_ylabel("posição ao longo da seção")

    # Visão superior (topo) com a linha da seção desenhada sobre o retângulo
    top = np.zeros((largura, altura), dtype=np.uint8)
    for x, y in linha_secao:
        if 0 <= x < largura and 0 <= y < altura:
            top[x, y] = 1

    ax2.imshow(top.T, origin="lower", cmap="gray")
    ax2.set_title("Visão superior (topo) com linha de seção")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
