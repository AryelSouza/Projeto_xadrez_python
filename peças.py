"""
modulo que cria as peças e seus movimentos
"""

#constantes
NOME = 0
LINHA = 2
COLUNA = 3
COR = 4
PRIMEIRO_MOVIMENTO = 5
JA_MOVIMENTOU = 5


def peaoverf(numero):
    """
    auxilia a verificar os movimentos do peao
    :param numero: resultado do movimento
    :return: resultado valido
    """
    if numero < 0:
        return -numero
    return numero


def criarPecas(cor):
    """
    cria as peças na matriz
    :param cor: define a cor da peça
    :return: as peças criadas
    """
    pecas = []

    # config
    linha_peao = 1
    linha_outras_pecas = 0
    simbolo_peao = '♟'
    simbolo_torre = '♜'
    simbolo_cavalo = '♞'
    simbolo_bispo = '♝'
    simbolo_rainha = '♛'
    simbolo_rei = '♚'

    if cor == "preta":
        linha_peao = 6
        linha_outras_pecas = 7
        simbolo_peao = '♙'
        simbolo_torre = '♖'
        simbolo_cavalo = '♘'
        simbolo_bispo = '♗'
        simbolo_rainha = '♕'
        simbolo_rei = '♔'

    # peoes
    for i in range(0, 8):
        pecas.append(['peao', simbolo_peao, linha_peao, i, cor, True])

    # torres
    pecas.append(['torre', simbolo_torre, linha_outras_pecas, 0, cor, False])
    pecas.append(['torre', simbolo_torre, linha_outras_pecas, 7, cor, False])

    # cavalos
    pecas.append(['cavalo', simbolo_cavalo, linha_outras_pecas, 1, cor])
    pecas.append(['cavalo', simbolo_cavalo, linha_outras_pecas, 6, cor])

    # bispos
    pecas.append(['bispo', simbolo_bispo, linha_outras_pecas, 2, cor])
    pecas.append(['bispo', simbolo_bispo, linha_outras_pecas, 5, cor])

    # rei
    pecas.append(['rei', simbolo_rei, linha_outras_pecas, 4, cor, False])

    # rainha
    pecas.append(['rainha', simbolo_rainha, linha_outras_pecas, 3, cor])

    return pecas


def pegaPeca(pecas, linha, coluna):
    """
    função para encontrar as peças
    :param pecas:lista todas as peças
    :param linha: linha selecionada
    :param coluna: coluna selecionada
    :return: None caso não tenha  nenhuma peça,peca caso tenha uma peça
    """
    for peca in pecas:
        if peca[LINHA] == linha and peca[COLUNA] == coluna:
            return peca

    return None


def retirarPeca(peca, pecas):
    """
    função para remover a peça do tabuleiro
    :param peca:a peça selecionada
    :param pecas: lista todas as peças
    :return:
    """
    for i in range(0, len(pecas)):
        if pecas[i] == peca:
            pecas.remove(peca)
            break


def movimentarCavalo(cavalo, linha, coluna, pecas_brancas, pecas_pretas):
    """
    lista os movimentos do cavalo e se eles são validos
    :param cavalo: peça do cavalo
    :param linha: linha selecionada
    :param coluna: coluna selecionada
    :param pecas_brancas: lista as peças brancas
    :param pecas_pretas: lista as peças pretas
    :return: False se o movimento não for valido,True se ele for valido
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

    # realiza o movimento
    cavalo[LINHA] = linha
    cavalo[COLUNA] = coluna

    return True


def movimentarRei(rei, linha, coluna, pecas_brancas, pecas_pretas):
    """
        lista os movimentos do rei e se eles são validos
        :param rei: peça do rei
        :param linha: linha selecionada
        :param coluna: coluna selecionada
        :param pecas_brancas: lista as peças brancas
        :param pecas_pretas: lista as peças pretas
        :return: False se o movimento não for valido,True se ele for valido
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

    # realiza o movimento
    rei[LINHA] = linha
    rei[COLUNA] = coluna
    rei[JA_MOVIMENTOU] = True

    return True


def movimentarTorre(torre, linha, coluna, pecas_brancas, pecas_pretas):
    """
        lista os movimentos da torre e se eles são validos
        :param torre: peça da torre
        :param linha: linha selecionada
        :param coluna: coluna selecionada
        :param pecas_brancas: lista as peças brancas
        :param pecas_pretas: lista as peças pretas
        :return: False se o movimento não for valido,True se ele for valido
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

    # realiza o movimento
    torre[LINHA] = linha
    torre[COLUNA] = coluna

    # por causa do reaproveitamento no caso da rainha
    if torre[NOME] == "torre":
        torre[JA_MOVIMENTOU] = True

    return True


def movimentarBispo(bispo, linha, coluna, pecas_brancas, pecas_pretas):
    """
        lista os movimentos do bispo e se eles são validos
        :param bispo: peça do bispo
        :param linha: linha selecionada
        :param coluna: coluna selecionada
        :param pecas_brancas: lista as peças brancas
        :param pecas_pretas: lista as peças pretas
        :return: False se o movimento não for valido,True se ele for valido
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

    # realiza o movimento
    bispo[LINHA] = linha
    bispo[COLUNA] = coluna

    return True


def movimentarRainha(rainha, linha, coluna, pecas_brancas, pecas_pretas):
    """
        lista os movimentos da rainha e se eles são validos
        :param rainha: peça da rainha
        :param linha: linha selecionada
        :param coluna: coluna selecionada
        :param pecas_brancas: lista as peças brancas
        :param pecas_pretas: lista as peças pretas
        :return: False se o movimento não for valido,True se ele for valido
        """
    resultado = movimentarTorre(rainha, linha, coluna, pecas_brancas, pecas_pretas)
    if resultado:
        return resultado

    resultado = movimentarBispo(rainha, linha, coluna, pecas_brancas, pecas_pretas)

    return resultado


def movimentarPeao(peao, linha, coluna, pecas_brancas, pecas_pretas):
    """
        lista os movimentos do peão e se eles são validos
        :param peao: peça do peão
        :param linha: linha selecionada
        :param coluna: coluna selecionada
        :param pecas_brancas: lista as peças brancas
        :param pecas_pretas: lista as peças pretas
        :return: False se o movimento não for valido,True se ele for valido
        """
    # mesma linha
    if linha == peao[LINHA]:
        return False

        # avancar casas demais
    if peaoverf(peao[LINHA] - linha) > 2:
        return False

    if peaoverf(peao[COLUNA] - coluna) > 1:
        return False

    # avancar duas casas e se deslocar para outra coluna
    if peaoverf(peao[LINHA] - linha) == 2 and (coluna == (peao[COLUNA] + 1) or coluna == (peao[COLUNA] - 1)):
        return False

    cor = peao[COR]

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

    # movimenta
    peao[LINHA] = linha
    peao[COLUNA] = coluna

    return True


def verificarSeHaPecasEntreTorreRei(torre, rei, pecas_brancas, pecas_pretas):
    """
    função que verifica se há casas entre a torre e o rei para a realização do roque
    :param torre: peça da torre
    :param rei: peça do rei
    :param pecas_brancas: lista as peças brancas
    :param pecas_pretas: lista as peças pretas
    :return: True se não houver peças entre eles,False se houver peças entre eles
    """
    linha = torre[LINHA]

    if torre[COLUNA] > rei[COLUNA]:
        for i in range(rei[COLUNA] + 1, 7):
            peca = pegaPeca(pecas_brancas, linha, i)
            if peca != None:
                return True

            peca = pegaPeca(pecas_pretas, linha, i)
            if peca != None:
                return True
    else:
        for i in range(1, rei[COLUNA]):
            peca = pegaPeca(pecas_brancas, linha, i)
            if peca != None:
                return True

            peca = pegaPeca(pecas_pretas, linha, i)
            if peca != None:
                return True

    return False


def verificarCasaAtacada(linha, coluna, cor, pecas_brancas, pecas_pretas):
    """
    verificas as casas ameaçadas para a realização do roque e do xeque
    :param linha:linha selecionada
    :param coluna:coluna selecionada
    :param cor:cor da peça selecionada
    :param pecas_brancas:lista as peças brancas
    :param pecas_pretas:lista as peças pretas
    :return:True se o movimento for valido,False se não for
    """
    # cavalo
    posicoes_possiveis = [
        [linha + 2, coluna + 1],
        [linha + 1, coluna + 2],
        [linha - 1, coluna + 2],
        [linha - 2, coluna + 1],
        [linha - 2, coluna - 1],
        [linha - 1, coluna - 2],
        [linha + 1, coluna - 2],
        [linha + 2, coluna - 1]
    ]

    for posicao in posicoes_possiveis:
        peca = None
        if cor == "preta":
            peca = pegaPeca(pecas_pretas, posicao[0], posicao[1])
        else:
            peca = pegaPeca(pecas_brancas, posicao[0], posicao[1])

        if peca != None and peca[NOME] == "cavalo":
            return True

    # vertical
    for i in range(linha + 1, 8):
        if cor == "preta":
            peca = pegaPeca(pecas_brancas, i, coluna)
            if peca != None:
                break

            peca = pegaPeca(pecas_pretas, i, coluna)
            if peca != None and (peca[NOME] == "rainha" or peca[NOME] == "torre"):
                return True
            elif peca != None:
                break
        else:
            peca = pegaPeca(pecas_pretas, i, coluna)
            if peca != None:
                break

            peca = pegaPeca(pecas_brancas, i, coluna)
            if peca != None and (peca[NOME] == "rainha" or peca[NOME] == "torre"):
                return True
            elif peca != None:
                break

    for i in range(linha - 1, -1, -1):
        if cor == "preta":
            peca = pegaPeca(pecas_brancas, i, coluna)
            if peca != None:
                break

            peca = pegaPeca(pecas_pretas, i, coluna)
            if peca != None and (peca[NOME] == "rainha" or peca[NOME] == "torre"):
                return True
            elif peca != None:
                break
        else:
            peca = pegaPeca(pecas_pretas, i, coluna)
            if peca != None:
                break

            peca = pegaPeca(pecas_brancas, i, coluna)
            if peca != None and (peca[NOME] == "rainha" or peca[NOME] == "torre"):
                return True
            elif peca != None:
                break

    # horizontal
    for i in range(coluna + 1, 8):
        if cor == "preta":
            peca = pegaPeca(pecas_brancas, linha, i)
            if peca != None:
                break

            peca = pegaPeca(pecas_pretas, linha, i)
            if peca != None and (peca[NOME] == "rainha" or peca[NOME] == "torre"):
                return True
            elif peca != None:
                break
        else:
            peca = pegaPeca(pecas_pretas, linha, i)
            if peca != None:
                break

            peca = pegaPeca(pecas_brancas, linha, i)
            if peca != None and (peca[NOME] == "rainha" or peca[NOME] == "torre"):
                return True
            elif peca != None:
                break

    for i in range(coluna - 1, -1, -1):
        if cor == "preta":
            peca = pegaPeca(pecas_brancas, linha, i)
            if peca != None:
                break

            peca = pegaPeca(pecas_pretas, linha, i)
            if peca != None and (peca[NOME] == "rainha" or peca[NOME] == "torre"):
                return True
            elif peca != None:
                break
        else:
            peca = pegaPeca(pecas_pretas, linha, i)
            if peca != None:
                break

            peca = pegaPeca(pecas_brancas, linha, i)
            if peca != None and (peca[NOME] == "rainha" or peca[NOME] == "torre"):
                return True
            elif peca != None:
                break

    # peao
    if cor == "preta":
        peca = pegaPeca(pecas_pretas, linha + 1, coluna - 1)
        if peca != None and peca[NOME] == "peao":
            return True

        peca = pegaPeca(pecas_pretas, linha + 1, coluna + 1)
        if peca != None and peca[NOME] == "peao":
            return True
    else:
        peca = pegaPeca(pecas_brancas, linha - 1, coluna - 1)
        if peca != None and peca[NOME] == "peao":
            return True

        peca = pegaPeca(pecas_brancas, linha - 1, coluna + 1)
        if peca != None and peca[NOME] == "peao":
            return True

    # diagonal
    linha_atual = linha
    coluna_atual = coluna

    while linha_atual != 8 and coluna_atual != 8:
        linha_atual += 1
        coluna_atual += 1

        if cor == "preta":
            peca = pegaPeca(pecas_brancas, linha_atual, coluna_atual)
            if peca != None:
                break

            peca = pegaPeca(pecas_pretas, linha_atual, coluna_atual)
            if peca != None and (peca[NOME] == "rainha" or peca[NOME] == "bispo"):
                return True
            elif peca != None:
                break
        else:
            peca = pegaPeca(pecas_pretas, linha_atual, coluna_atual)
            if peca != None:
                break

            peca = pegaPeca(pecas_brancas, linha_atual, coluna_atual)
            if peca != None and (peca[NOME] == "rainha" or peca[NOME] == "bispo"):
                return True
            elif peca != None:
                break

    linha_atual = linha
    coluna_atual = coluna

    while linha_atual != 0 and coluna_atual != 8:
        linha_atual -= 1
        coluna_atual += 1

        if cor == "preta":
            peca = pegaPeca(pecas_brancas, linha_atual, coluna_atual)
            if peca != None:
                break

            peca = pegaPeca(pecas_pretas, linha_atual, coluna_atual)
            if peca != None and (peca[NOME] == "rainha" or peca[NOME] == "bispo"):
                return True
            elif peca != None:
                break
        else:
            peca = pegaPeca(pecas_pretas, linha_atual, coluna_atual)
            if peca != None:
                break

            peca = pegaPeca(pecas_brancas, linha_atual, coluna_atual)
            if peca != None and (peca[NOME] == "rainha" or peca[NOME] == "bispo"):
                return True
            elif peca != None:
                break

    linha_atual = linha
    coluna_atual = coluna

    while linha_atual != 8 and coluna_atual != 0:
        linha_atual += 1
        coluna_atual -= 1

        if cor == "preta":
            peca = pegaPeca(pecas_brancas, linha_atual, coluna_atual)
            if peca != None:
                break

            peca = pegaPeca(pecas_pretas, linha_atual, coluna_atual)
            if peca != None and (peca[NOME] == "rainha" or peca[NOME] == "bispo"):
                return True
            elif peca != None:
                break
        else:
            peca = pegaPeca(pecas_pretas, linha_atual, coluna_atual)
            if peca != None:
                break

            peca = pegaPeca(pecas_brancas, linha_atual, coluna_atual)
            if peca != None and (peca[NOME] == "rainha" or peca[NOME] == "bispo"):
                return True
            elif peca != None:
                break

    linha_atual = linha
    coluna_atual = coluna

    while linha_atual != 0 and coluna_atual != 0:
        linha_atual -= 1
        coluna_atual -= 1

        if cor == "preta":
            peca = pegaPeca(pecas_brancas, linha_atual, coluna_atual)
            if peca != None:
                break

            peca = pegaPeca(pecas_pretas, linha_atual, coluna_atual)
            if peca != None and (peca[NOME] == "rainha" or peca[NOME] == "bispo"):
                return True
            elif peca != None:
                break
        else:
            peca = pegaPeca(pecas_pretas, linha_atual, coluna_atual)
            if peca != None:
                break

            peca = pegaPeca(pecas_brancas, linha_atual, coluna_atual)
            if peca != None and (peca[NOME] == "rainha" or peca[NOME] == "bispo"):
                return True
            elif peca != None:
                break

    return False


def roque(rei, torre, pecas_brancas, pecas_pretas):
    """
    função para realizar o roque
    :param rei: peça do rei
    :param torre: peça da torre
    :param pecas_brancas: lista as peças brancas
    :param pecas_pretas: lista as peças pretas
    :return:True se o roque pode ser realizado,False se não pode ser realizado
    """
    # requisito 1
    if rei[JA_MOVIMENTOU]:
        return False
    if torre[JA_MOVIMENTOU]:
        return False

    # requisito 2
    if verificarSeHaPecasEntreTorreRei(torre, rei, pecas_brancas, pecas_pretas):
        return False

    # requisito 3
    cor_atacante = "branca"
    if torre[COR] == cor_atacante:
        cor_atacante = "preta"

    if torre[COLUNA] < rei[COLUNA]:
        for i in range(torre[COLUNA] + 2, rei[COLUNA] + 1):
            if verificarCasaAtacada(torre[LINHA], i, cor_atacante, pecas_brancas, pecas_pretas):
                return False

        torre[COLUNA] = torre[COLUNA] + 3
        rei[COLUNA] = rei[COLUNA] - 2
    else:
        for i in range(torre[COLUNA] - 1, rei[COLUNA] + 1, -1):
            if verificarCasaAtacada(torre[LINHA], i, cor_atacante, pecas_brancas, pecas_pretas):
                return False

        torre[COLUNA] = torre[COLUNA] - 2
        rei[COLUNA] = rei[COLUNA] + 2

    rei[JA_MOVIMENTOU] = True
    torre[JA_MOVIMENTOU] = True

    return True




