"""
modulo que faz o tabuleiro
"""

#TABULEIRO
def criarTabuleiro():
    """
    função que cria o tabuleiro na matriz
    :return: o tabuleiro na matriz
    """
    tabuleiro = []

    for i in range(0, 8):
        linha = []
        for j in range(0, 8):
            linha.append(' ')
        tabuleiro.append(linha)

    return tabuleiro


def limparTabuleiro(tabuleiro):
    """
    função que limpa o tabuleiro da matriz para renderiza-lo no console
    :param tabuleiro: tabuleiro da matriz
    :return: tabuleiro do console
    """
    for i in range(0, 8):
        for j in range(0, 8):
            tabuleiro[i][j] = ' '


def colocarPecasTabuleiro(tabuleiro, pecas_brancas, pecas_pretas):
    """
    coloca as peças no tabuleiro do console
    :param tabuleiro: tabuleiro da matriz
    :param pecas_brancas: lista as peças brancas
    :param pecas_pretas: lista as peças pretas
    :return: peças colocadas no tabuleiro
    """
    # pecas brancas
    for peca in pecas_brancas:
        linha = peca[2]
        coluna = peca[3]
        simbolo = peca[1]

        tabuleiro[linha][coluna] = simbolo

    # pecas pretas
    for peca in pecas_pretas:
        linha = peca[2]
        coluna = peca[3]
        simbolo = peca[1]

        tabuleiro[linha][coluna] = simbolo


def renderizarTabuleiro(tabuleiro):
    """
    imprime o tabuleiro completo no console
    :param tabuleiro: tabuleiro completo
    :return: tabuleiro no console
    """
    print("   A B C D E F G H")
    for i in range(7, -1, -1):
        print(i + 1, end=" |")
        for j in range(0, 8):
            print(f'{tabuleiro[i][j]}|', end="")
        print()


