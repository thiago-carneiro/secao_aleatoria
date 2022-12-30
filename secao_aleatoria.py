'''
CC BY: Thiago Pacheco Carneiro 2022
https://creativecommons.org/licenses/by/4.0/
'''

import random
import math


def obtem_linha_secao(largura: int = 1024,
                      altura: int = 1024,
                      largura_corte: int = 512) -> list[tuple[int, int]]:
    x1 = random.randint(0, largura-1)
    y1 = random.randint(0, altura-1)

    x2 = -1
    y2 = -1

    while((x2 not in range(largura)) or (y2 not in range(altura))):
        tetha = random.random()*math.pi*2
        x2 = int(x1 + largura_corte*math.cos(tetha))
        y2 = int(y1 + largura_corte*math.sin(tetha))
        pontos = []
    for i in range(largura_corte):
        x_ponto = int(x1 + i*math.cos(tetha))
        y_ponto = int(y1 + i*math.sin(tetha))
        if((x_ponto in range(largura)) and (y_ponto in range(altura))):
            pontos.append((x_ponto, y_ponto))
        else:
            raise ValueError('Erro no ponto:\n' +
                             f'i {i}\tx {x_ponto}\ty {y_ponto}\n' +
                             f'x1 {x1}\tx2 {x2}\ty1 {y1}\ty2 {y2}\ttetha {tetha}')
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
    matplotlib.use('TkAgg')

    # gerando o cubo com um cone

    cubo = np.zeros((1024, 1024, 1024))
    for i in range(1024):
        perimetro_int = math.ceil(2*math.pi*(i+1))
        for arco in range(perimetro_int):
            tetha = 2*math.pi*arco/perimetro_int
            cubo[512+int(i*math.cos(tetha)/2), 512 +
                 int(i*math.sin(tetha)/2), i] = 1

    # obtendo os pontos da seção na superfície do cubo
    largura_corte = 768
    linha_corte = obtem_linha_secao(largura_corte=largura_corte)

    # gerando a seção
    img = np.zeros((largura_corte, 1024))
    for i in range(largura_corte):
        x = linha_corte[i][0]
        y = linha_corte[i][1]
        img[i] = cubo[x, y]

    plt.imshow(img.T)
    plt.show()


if(__name__ == '__main__'):
    main()
