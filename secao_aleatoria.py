"""
CC BY: Thiago Pacheco Carneiro 2022
https://creativecommons.org/licenses/by/4.0/
"""

import random
import math


def obtem_linha_secao(largura: int = 1024,
                      altura: int = 1024,
                      largura_secao: int = 512
                      ) -> list[tuple[int, int]]:
    """Função que retorna uma linha na face superior de um paralelepípedo.
    Esta linha define a aresta superior de uma seção vertical aleatória
    do interior do paralelepípedo.

    Args:
        largura (int, optional): largura da face do paralelepípedo.
                                 Defaults to 1024.
        altura (int, optional): altura da face do paralelepípedo.
                                Defaults to 1024.
        largura_secao (int, optional): largura da seção.
                                       Defaults to 512.

    Returns:
        list[tuple[int, int]]: Lista de todos os pontos da linha.
    """

    x1 = random.randint(0, largura - 1)
    y1 = random.randint(0, altura - 1)
    x2 = -1
    y2 = -1

    # obtendo a segunda ponta da seção, dentro do paralelepípedo
    while (x2 not in range(largura)) or (y2 not in range(altura)):
        tetha = random.random() * math.pi * 2
        x2 = int(x1 + largura_secao * math.cos(tetha))
        y2 = int(y1 + largura_secao * math.sin(tetha))

    # obtendo cada ponto entre as duas pontas da seção
    pontos = []
    for i in range(largura_secao):
        x_ponto = int(x1 + i * math.cos(tetha))
        y_ponto = int(y1 + i * math.sin(tetha))
        if (x_ponto in range(largura)) and (y_ponto in range(altura)):
            pontos.append((x_ponto, y_ponto))
    return pontos


def main():
    """
    Exemplo de como usar o obtem_linha_corte.
    Aqui preenchemos um cubo com um cone e depois
    obtemos seções verticais aleatórias do cone.
    """
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib

    matplotlib.use("TkAgg")

    # gerando o cubo com um cone
    cubo = np.zeros((1024, 1024, 1024))
    for i in range(1024):
        perimetro_int = math.ceil(2 * math.pi * (i + 1))
        for arco in range(perimetro_int):
            tetha = 2 * math.pi * arco / perimetro_int
            cubo[
                512 + int(i * math.cos(tetha) / 2),
                512 + int(i * math.sin(tetha) / 2),
                i,
            ] = 1

    # obtendo os pontos da seção na superfície do cubo
    largura_secao = 768
    linha_secao = obtem_linha_secao(largura_secao=largura_secao)

    # gerando a seção
    img = np.zeros((largura_secao, 1024))
    for i in range(largura_secao):
        x = linha_secao[i][0]
        y = linha_secao[i][1]
        img[i] = cubo[x, y]

    plt.imshow(img.T)
    plt.show()


if __name__ == "__main__":
    main()
