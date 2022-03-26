"""
modulo que faz o xeque e xeque mate
"""

from peças import *
from tabuleiro import *
import copy


def movimentoPossivelPeao(peao, linha, coluna, pecas_brancas, pecas_pretas):
    """
    lista os movimentos possiveis do peao para a realização do xeque
    :param peao: peça do peão
    :param linha: linha selecionada
    :param coluna: coluna selecionada
    :param pecas_brancas: lista as peças brancas
    :param pecas_pretas: lista as peças brancas
    :return:True se o movimento for possivel,False se não for possivel
    """
    # mesma linha
    if linha == peao[LINHA]:
        return False

        # avancar casas demais
    if peaoverf(peao[LINHA] - linha) > 2:
        return False

    if peaoverf(peao[COLUNA] - coluna) > 1:
        return False

    cor = peao[COR]

    # avancar duas casas e captura
    if peaoverf(peao[LINHA] - linha) == 2 and (coluna == (peao[COLUNA] + 1) or coluna == (peao[COLUNA] - 1)):
        return False

    # verifica se a posicao da linha ta correta
    if cor == "preta" and linha > peao[LINHA]:
        return False
    elif cor == "branca" and linha < peao[LINHA]:
        return False

    # sobe ou desce
    vertical = 1
    if cor == "preta":
        vertical = -1

    # VERTICAL
    if coluna == peao[COLUNA]:
        # verifica se a posicao e do primeiro movimento
        if peaoverf(peao[LINHA] - linha) == 2:
            if not peao[PRIMEIRO_MOVIMENTO]:
                return False

        # verifica se tem peca no caminho
        for i in range(peao[LINHA] + vertical, linha + vertical, vertical):
            peca = pegaPeca(pecas_brancas, i, coluna)
            if peca != None:
                return False

            peca = pegaPeca(pecas_pretas, i, coluna)
            if peca != None:
                return False
    else:
        # DIAGONAL
        if cor == "preta":
            peca = pegaPeca(pecas_brancas, linha, coluna)
            if peca == None:
                return False
            retirarPeca(peca, pecas_brancas)
        else:
            peca = pegaPeca(pecas_pretas, linha, coluna)
            if peca == None:
                return False
            retirarPeca(peca, pecas_pretas)

    return True


def movimentoPossivelTorre(torre, linha, coluna, pecas_brancas, pecas_pretas):
    """
        lista os movimentos possiveis da torre para a realização do xeque
        :param torre: peça da torre
        :param linha: linha selecionada
        :param coluna: coluna selecionada
        :param pecas_brancas: lista as peças brancas
        :param pecas_pretas: lista as peças brancas
        :return:True se o movimento for possivel,False se não for possivel
        """
    # verifica se e a mesma posicao
    if torre[LINHA] == linha and torre[COLUNA] == coluna:
        return False

    # verifica se a nova posicao ta na diagonal
    if linha != torre[LINHA] and coluna != torre[COLUNA]:
        return False

    # sobe ou desce
    vertical = 1
    if linha < torre[LINHA]:
        vertical = -1

    # direita ou esquerda
    horizontal = 1
    if coluna < torre[COLUNA]:
        horizontal = -1

    # teste horizontal ou vertical - casas ocupadas durante o percurso
    if linha == torre[LINHA]:
        for i in range(torre[COLUNA] + horizontal, coluna, horizontal):
            peca = pegaPeca(pecas_brancas, linha, i)
            if peca != None:
                return False

            peca = pegaPeca(pecas_pretas, linha, i)
            if peca != None:
                return False
    else:
        for i in range(torre[LINHA] + vertical, linha, vertical):
            peca = pegaPeca(pecas_brancas, i, coluna)
            if peca != None:
                return False

            peca = pegaPeca(pecas_pretas, i, coluna)
            if peca != None:
                return False

    cor = torre[COR]
    if cor == "branca":
        # verifica se tem uma peca branca
        peca = pegaPeca(pecas_brancas, linha, coluna)
        if peca != None:
            return False

        # verifica se tem uma peca preta
        peca = pegaPeca(pecas_pretas, linha, coluna)
        if peca != None:
            retirarPeca(peca, pecas_pretas)
    else:
        # verifica se tem uma peca preta
        peca = pegaPeca(pecas_pretas, linha, coluna)
        if peca != None:
            return False

        # verifica se tem uma peca brancas
        peca = pegaPeca(pecas_brancas, linha, coluna)
        if peca != None:
            retirarPeca(peca, pecas_brancas)

    return True


def movimentoPossivelCavalo(cavalo, linha, coluna, pecas_brancas, pecas_pretas):
    """
        lista os movimentos possiveis do cavalo para a realização do xeque
        :param cavalo: peça do cavalo
        :param linha: linha selecionada
        :param coluna: coluna selecionada
        :param pecas_brancas: lista as peças brancas
        :param pecas_pretas: lista as peças brancas
        :return:True se o movimento for possivel,False se não for possivel
        """
    # movimentos possiveis
    movimentos_possiveis = [
        [cavalo[LINHA] + 2, cavalo[COLUNA] + 1],
        [cavalo[LINHA] + 1, cavalo[COLUNA] + 2],
        [cavalo[LINHA] - 1, cavalo[COLUNA] + 2],
        [cavalo[LINHA] - 2, cavalo[COLUNA] + 1],
        [cavalo[LINHA] - 2, cavalo[COLUNA] - 1],
        [cavalo[LINHA] - 1, cavalo[COLUNA] - 2],
        [cavalo[LINHA] + 1, cavalo[COLUNA] - 2],
        [cavalo[LINHA] + 2, cavalo[COLUNA] - 1]
    ]

    # checa se e para a mesma posicao
    if cavalo[LINHA] == linha and cavalo[COLUNA] == coluna:
        return False

    # checa se o movimento esta na lista
    if [linha, coluna] not in movimentos_possiveis:
        return False

    cor = cavalo[COR]
    if cor == "branca":
        # verifica se tem uma peca branca
        peca = pegaPeca(pecas_brancas, linha, coluna)
        if peca != None:
            return False

        # verifica se tem uma peca preta
        peca = pegaPeca(pecas_pretas, linha, coluna)
        if peca != None:
            retirarPeca(peca, pecas_pretas)
    else:
        # verifica se tem uma peca preta
        peca = pegaPeca(pecas_pretas, linha, coluna)
        if peca != None:
            return False

        # verifica se tem uma peca brancas
        peca = pegaPeca(pecas_brancas, linha, coluna)
        if peca != None:
            retirarPeca(peca, pecas_brancas)

    return True


def movimentoPossivelBispo(bispo, linha, coluna, pecas_brancas, pecas_pretas):
    """
        lista os movimentos possiveis do bispo para a realização do xeque
        :param bispo: peça do bispo
        :param linha: linha selecionada
        :param coluna: coluna selecionada
        :param pecas_brancas: lista as peças brancas
        :param pecas_pretas: lista as peças brancas
        :return:True se o movimento for possivel,False se não for possivel
        """
    # verifica se o a linha e coluna e a mesma - movimento vertical e horizontal
    if linha == bispo[LINHA] or coluna == bispo[COLUNA]:
        return False

    if abs(linha - bispo[LINHA]) != abs(coluna - bispo[COLUNA]):
        return False

    # sobe ou desce
    vertical = 1
    if linha < bispo[LINHA]:
        vertical = -1

    # direita ou esquerda
    horizontal = 1
    if coluna < bispo[COLUNA]:
        horizontal = -1

    # verifica se tem peca pelo caminho
    i = bispo[LINHA] + vertical
    j = bispo[COLUNA] + horizontal

    while (i != linha and j != coluna):
        peca = pegaPeca(pecas_brancas, i, j)
        if peca != None:
            return False

        peca = pegaPeca(pecas_pretas, i, j)
        if peca != None:
            return False

        i = i + vertical
        j = j + horizontal

    cor = bispo[COR]
    if cor == "branca":
        # verifica se tem uma peca branca
        peca = pegaPeca(pecas_brancas, linha, coluna)
        if peca != None:
            return False

        # verifica se tem uma peca preta
        peca = pegaPeca(pecas_pretas, linha, coluna)
        if peca != None:
            retirarPeca(peca, pecas_pretas)
    else:
        # verifica se tem uma peca preta
        peca = pegaPeca(pecas_pretas, linha, coluna)
        if peca != None:
            return False

        # verifica se tem uma peca brancas
        peca = pegaPeca(pecas_brancas, linha, coluna)
        if peca != None:
            retirarPeca(peca, pecas_brancas)

    return True


def movimentoPossivelRainha(rainha, linha, coluna, pecas_brancas, pecas_pretas):
    """
        lista os movimentos possiveis da rainha para a realização do xeque
        :param rainha: peça da rainha
        :param linha: linha selecionada
        :param coluna: coluna selecionada
        :param pecas_brancas: lista as peças brancas
        :param pecas_pretas: lista as peças brancas
        :return:True se o movimento for possivel,False se não for possivel
        """
    resultado = movimentoPossivelTorre(rainha, linha, coluna, pecas_brancas, pecas_pretas)
    if resultado:
        return resultado

    resultado = movimentoPossivelBispo(rainha, linha, coluna, pecas_brancas, pecas_pretas)

    return resultado


def movimentoPossivelRei(rei, linha, coluna, pecas_brancas, pecas_pretas):
    """
        lista os movimentos possiveis do rei para a realização do xeque
        :param rei: peça do rei
        :param linha: linha selecionada
        :param coluna: coluna selecionada
        :param pecas_brancas: lista as peças brancas
        :param pecas_pretas: lista as peças brancas
        :return:True se o movimento for possivel,False se não for possivel
        """
    # a casa esta sendo atacada
    cor = "branca"
    if rei[COR] == cor:
        cor = "preta"

    if verificarCasaAtacada(linha, coluna, cor, pecas_brancas, pecas_pretas):
        return False

    # movimentos possiveis
    movimentos_possiveis = [
        [rei[LINHA] + 1, rei[COLUNA] - 1],
        [rei[LINHA] + 1, rei[COLUNA]],
        [rei[LINHA] + 1, rei[COLUNA] + 1],
        [rei[LINHA], rei[COLUNA] + 1],
        [rei[LINHA] - 1, rei[COLUNA] + 1],
        [rei[LINHA] - 1, rei[COLUNA]],
        [rei[LINHA] - 1, rei[COLUNA] - 1],
        [rei[LINHA], rei[COLUNA] - 1]
    ]

    # verifica se esta na mesma posicao
    # checa se e para a mesma posicao
    if rei[LINHA] == linha and rei[COLUNA] == coluna:
        return False

    # verifica se esta nos movimentos possiveis
    if [linha, coluna] not in movimentos_possiveis:
        return False

    cor = rei[COR]
    if cor == "branca":
        # verifica se tem uma peca branca
        peca = pegaPeca(pecas_brancas, linha, coluna)
        if peca != None:
            return False

        # verifica se tem uma peca preta
        peca = pegaPeca(pecas_pretas, linha, coluna)
        if peca != None:
            retirarPeca(peca, pecas_pretas)
    else:
        # verifica se tem uma peca preta
        peca = pegaPeca(pecas_pretas, linha, coluna)
        if peca != None:
            return False

        # verifica se tem uma peca brancas
        peca = pegaPeca(pecas_brancas, linha, coluna)
        if peca != None:
            retirarPeca(peca, pecas_brancas)

    return True


def listarMovimentosPossiveis(cor, pecas_brancas, pecas_pretas):
    """
    junta todas as funções de movimentos possiveis anteriores para facilitar a execução do xeque
    :param cor: cor da peça
    :param pecas_brancas: lista as peças brancas
    :param pecas_pretas: lista as peças pretas
    :return: os movimentos possiveis
    """
    movimentos = []
    # faz copias para nao ocorre problemas
    copia_pecas_brancas = copy.deepcopy(pecas_brancas)
    copia_pecas_pretas = copy.deepcopy(pecas_pretas)

    if cor == "branca":
        for peca in copia_pecas_brancas:
            peca = peca.copy()
            if peca[NOME] == "peao":
                for i in range(0, 8):
                    for j in range(0, 8):
                        if movimentoPossivelPeao(peca, i, j, copia_pecas_brancas, copia_pecas_pretas):
                            movimentos.append([peca[LINHA], peca[COLUNA], i, j])
            elif peca[NOME] == "torre":
                for i in range(0, 8):
                    for j in range(0, 8):
                        if movimentoPossivelTorre(peca, i, j, copia_pecas_brancas, copia_pecas_pretas):
                            movimentos.append([peca[LINHA], peca[COLUNA], i, j])
            elif peca[NOME] == "cavalo":
                for i in range(0, 8):
                    for j in range(0, 8):
                        if movimentoPossivelCavalo(peca, i, j, copia_pecas_brancas, copia_pecas_pretas):
                            movimentos.append([peca[LINHA], peca[COLUNA], i, j])
            elif peca[NOME] == "bispo":
                for i in range(0, 8):
                    for j in range(0, 8):
                        if movimentoPossivelBispo(peca, i, j, copia_pecas_brancas, copia_pecas_pretas):
                            movimentos.append([peca[LINHA], peca[COLUNA], i, j])
            elif peca[NOME] == "rainha":
                for i in range(0, 8):
                    for j in range(0, 8):
                        if movimentoPossivelRainha(peca, i, j, copia_pecas_brancas, copia_pecas_pretas):
                            movimentos.append([peca[LINHA], peca[COLUNA], i, j])
            elif peca[NOME] == "rei":
                for i in range(0, 8):
                    for j in range(0, 8):
                        if movimentoPossivelRei(peca, i, j, copia_pecas_brancas, copia_pecas_pretas):
                            movimentos.append([peca[LINHA], peca[COLUNA], i, j])
    else:
        for peca in copia_pecas_pretas:
            peca = peca.copy()
            if peca[NOME] == "peao":
                for i in range(0, 8):
                    for j in range(0, 8):
                        if movimentoPossivelPeao(peca, i, j, copia_pecas_brancas, copia_pecas_pretas):
                            movimentos.append([peca[LINHA], peca[COLUNA], i, j])
            elif peca[NOME] == "torre":
                for i in range(0, 8):
                    for j in range(0, 8):
                        if movimentoPossivelTorre(peca, i, j, copia_pecas_brancas, copia_pecas_pretas):
                            movimentos.append([peca[LINHA], peca[COLUNA], i, j])
            elif peca[NOME] == "cavalo":
                for i in range(0, 8):
                    for j in range(0, 8):
                        if movimentoPossivelCavalo(peca, i, j, copia_pecas_brancas, copia_pecas_pretas):
                            movimentos.append([peca[LINHA], peca[COLUNA], i, j])
            elif peca[NOME] == "bispo":
                for i in range(0, 8):
                    for j in range(0, 8):
                        if movimentoPossivelBispo(peca, i, j, copia_pecas_brancas, copia_pecas_pretas):
                            movimentos.append([peca[LINHA], peca[COLUNA], i, j])
            elif peca[NOME] == "rainha":
                for i in range(0, 8):
                    for j in range(0, 8):
                        if movimentoPossivelRainha(peca, i, j, copia_pecas_brancas, copia_pecas_pretas):
                            movimentos.append([peca[LINHA], peca[COLUNA], i, j])
            elif peca[NOME] == "rei":
                for i in range(0, 8):
                    for j in range(0, 8):
                        if movimentoPossivelRei(peca, i, j, copia_pecas_brancas, copia_pecas_pretas):
                            movimentos.append([peca[LINHA], peca[COLUNA], i, j])

    return movimentos

def pegaPecaNome(nome, pecas):
    """
    seleciona a peça pelo nome para auxiliar no xeque
    :param nome: nome da peça
    :param pecas: lista das peças
    :return: peça selecionada
    """
    for peca in pecas:
        if peca[NOME] == nome:
            return peca
    return None


def verificarXeque(cor, pecas_brancas, pecas_pretas):
    """
    verifica se o xeque pode ocorrer
    :param cor: cor da peça
    :param pecas_brancas: lista peças brancas
    :param pecas_pretas: lista peças pretas
    :return: as casas que estão sendo atacadas
    """
    if cor == "branca":
        rei = pegaPecaNome("rei", pecas_brancas)
        return verificarCasaAtacada(rei[LINHA], rei[COLUNA], "preta", pecas_brancas, pecas_pretas)
    else:
        rei = pegaPecaNome("rei", pecas_pretas)
        return verificarCasaAtacada(rei[LINHA], rei[COLUNA], "branca", pecas_brancas, pecas_pretas)


def listarMovimentosParaSairXeque(cor, pecas_brancas, pecas_pretas):
    """
    função que mostra quais são os movimentos possiveis para sair do xeque
    :param cor: cor da peça
    :param pecas_brancas: lista peças brancas
    :param pecas_pretas: lista peças pretas
    :return: True se não houver movimentos possiveis,caso o contrario retorna a lista com os movimentos
    """
    movimentos_possiveis = listarMovimentosPossiveis(cor, pecas_brancas, pecas_pretas)

    # nao existem movimentos possiveis
    if len(movimentos_possiveis) == 0:
        return True

    # simula cada movimento e verifica se e possivel sair do Xeque e adiciona nos movimentos possiveis para sair
    movimentos_para_sair_xeque = []
    peca = None
    for movimento in movimentos_possiveis:
        # copia para nao estourar o erro
        copia_pecas_brancas = copy.deepcopy(pecas_brancas)
        copia_pecas_pretas = copy.deepcopy(pecas_pretas)

        # simula o movimento e checa se saiu do xeque
        if cor == "branca":
            peca = pegaPeca(copia_pecas_brancas, movimento[0], movimento[1])
        else:
            peca = pegaPeca(copia_pecas_pretas, movimento[0], movimento[1])

        if peca[NOME] == "peao":
            movimentarPeao(peca, movimento[2], movimento[3], copia_pecas_brancas, copia_pecas_pretas)
        elif peca[NOME] == "torre":
            movimentarTorre(peca, movimento[2], movimento[3], copia_pecas_brancas, copia_pecas_pretas)
        elif peca[NOME] == "cavalo":
            movimentarCavalo(peca, movimento[2], movimento[3], copia_pecas_brancas, copia_pecas_pretas)
        elif peca[NOME] == "bispo":
            movimentarBispo(peca, movimento[2], movimento[3], copia_pecas_brancas, copia_pecas_pretas)
        elif peca[NOME] == "rainha":
            movimentarRainha(peca, movimento[2], movimento[3], copia_pecas_brancas, copia_pecas_pretas)
        elif peca[NOME] == "rei":
            movimentarRei(peca, movimento[2], movimento[3], copia_pecas_brancas, copia_pecas_pretas)

        if not verificarXeque(cor, copia_pecas_brancas, copia_pecas_pretas):
            movimentos_para_sair_xeque.append(movimento)

    return movimentos_para_sair_xeque