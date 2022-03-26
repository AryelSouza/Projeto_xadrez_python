"""
Esse módulo prevê funções para levar a efeito o xadrez.
A interface deve usar essas funções para:
- Operar sobre o tabuleiro
- Operar sobre o turno dos jogadores
- Garantir as condições iniciais do jogo
- Verificar as condições de término do jogo
"""

from tabuleiro import *
from peças import *
from xeque import *
from termcolor import colored

# constantes
VEZ_BRANCAS = True
linha = 0
coluna = 0

# inicia o jogo
tabuleiro = criarTabuleiro()
pecas_brancas = criarPecas("branca")
pecas_pretas = criarPecas("preta")
colocarPecasTabuleiro(tabuleiro, pecas_brancas, pecas_pretas)
renderizarTabuleiro(tabuleiro)



def movimentarPeca(peca, linha, coluna, pecas_brancas, pecas_pretas):
    """
    Executa o movimento da peça selecionada
    :param peca: A peça escolhida
    :param linha: a linha onde a jogada deve ser feita
    :param coluna: a coluna onde a jogada deve ser feita
    :param pecas_brancas: lista todas as peças brancas
    :param pecas_pretas: lista todas as peças pretas
    :return: o movimento da peça
    """
    if peca[0] == 'peao':
        return movimentarPeao(peca, linha, coluna, pecas_brancas, pecas_pretas)
    if peca[0] == 'torre':
        return movimentarTorre(peca, linha, coluna, pecas_brancas, pecas_pretas)
    if peca[0] == 'cavalo':
        return movimentarCavalo(peca, linha, coluna, pecas_brancas, pecas_pretas)
    if peca[0] == 'bispo':
        return movimentarBispo(peca, linha, coluna, pecas_brancas, pecas_pretas)
    if peca[0] == 'rei':
        return movimentarRei(peca, linha, coluna, pecas_brancas, pecas_pretas)
    if peca[0] == 'rainha':
        return movimentarRainha(peca, linha, coluna, pecas_brancas, pecas_pretas)


# funcao que le a coordenada e devolve a coordenada lida
def lerCoordenada():
    """
    Le a coordenada e verifica se ela esta dentro do tabuleiro
    :return: coordenada se ela for valida ou mensagem de erro se não for
    """
    # leitura da jogada
    while True:
        try:
            coordenada = input(colored("Informe a coordenada da peca que deseja mover [Exs.: G1,roque(menor) ou ROQUE(maior)] ",'yellow'))

            # roque
            entradas_aceitas_roque = ["roque", "ROQUE"]
            if coordenada in entradas_aceitas_roque:
                return coordenada
            # demais jogadas
            else:
                coordenada = coordenada.strip().upper()
                # valor de entrada com mais do que dois caracteres ou menos
                if len(coordenada) != 2:
                    print(colored("Error: coordenada invalida! Tente novamente.",'red'))
                else:
                    # primeiro valor da coordenada nao e uma letra
                    if (coordenada[0] < 'A' or coordenada[0] > 'H') or (coordenada[1] < '1' or coordenada[1] > '9'):
                        print(colored("Error: coordenada invalida! Tente novamente.",'red'))
                    else:
                        return coordenada
        except:
            print(colored("Error: coordenada invalida! Tente novamente.",'red'))


# jogo
while True:
    # checa se ouve xeque
    if VEZ_BRANCAS:
        print("Agora é a vez das brancas!")
        if verificarXeque("branca", pecas_brancas, pecas_pretas):
            print(colored("ATENCAO: XEQUE",'red'))
            movimentos_sair_xeque = listarMovimentosParaSairXeque("branca", pecas_brancas, pecas_pretas)
            if len(movimentos_sair_xeque) == 0:
                print(colored("XEQUE MATE!! PRETAS VENCEM",'green'))
                break
            else:
                print(colored("---MOVIMENTOS POSSIVEIS---",'yellow'))
                for movimento in movimentos_sair_xeque:
                    print(f'{chr(movimento[1] + 65)}{movimento[0] + 1} -> {chr(movimento[3] + 65)}{movimento[2] + 1}')


                while True:
                    try:
                        coordenada1 = lerCoordenada()
                        linha1 = int(coordenada1[1]) - 1
                        coluna1 = ord(coordenada1[0]) % 65

                        coordenada2 = lerCoordenada()
                        linha2 = int(coordenada2[1]) - 1
                        coluna2 = ord(coordenada2[0]) % 65

                        if [linha1, coluna1, linha2, coluna2] in movimentos_sair_xeque:
                            peca = pegaPeca(pecas_brancas, linha1, coluna1)
                            movimentarPeca(peca, linha2, coluna2, pecas_brancas, pecas_pretas)
                            VEZ_BRANCAS = False
                            break
                        else:
                            print(colored("Error: jogada invalida!",'red'))
                    except:
                        print(colored("Error: jogada invalida!",'red'))

        else:
            # ler a coordenada
            coordenada = lerCoordenada()

            # PECAS BRANCAS
            if coordenada == "roque" or coordenada == "ROQUE":
                torre = None

                rei = pegaPeca(pecas_brancas, 0, 4)

                if coordenada == "roque":
                    torre = pegaPeca(pecas_brancas, 0, 7)
                else:
                    torre = pegaPeca(pecas_brancas, 0, 0)

                if torre == None or rei == None:
                    print(colored("Error: torre ou rei nao encontrado!",'red'))
                else:
                    resultado = roque(rei, torre, pecas_brancas, pecas_pretas)

                    if resultado:
                        VEZ_BRANCAS = False
                    else:
                        print(colored("Error: Nao foi possivel realizar o roque!",'red'))
            else:
                linha = int(coordenada[1]) - 1
                coluna = ord(coordenada[0]) % 65

                if (linha < 0 or linha > 7):
                    print(colored("Error: linha invalida!",'red'))
                elif (coluna < 0 or coluna > 7):
                    print(colored("Error: coluna invalida!",'red'))
                else:
                    peca = pegaPeca(pecas_brancas, linha, coluna)

                    if peca == None:
                        print(colored("Error: peca nao existe!", 'red'))
                    else:
                        coordenada = lerCoordenada()

                        linha = int(coordenada[1]) - 1
                        coluna = ord(coordenada[0]) % 65

                        if (linha < 0 or linha > 7):
                            print(colored("Error: linha invalida!",'red'))
                        elif (coluna < 0 or coluna > 7):
                            print(colored("Error: coluna invalida!",'red'))
                        else:
                            resultado = movimentarPeca(peca, linha, coluna, pecas_brancas, pecas_pretas)

                            if resultado:
                                VEZ_BRANCAS = False
                            else:
                                print(colored("Error: Nao foi possivel movimentar a peca!", 'red'))
    else:
        print("Agora é a vez das pretas!")

        if verificarXeque("preta", pecas_brancas, pecas_pretas):
            print(colored("ATENCAO: XEQUE",'red'))
            movimentos_sair_xeque = listarMovimentosParaSairXeque("preta", pecas_brancas, pecas_pretas)
            if len(movimentos_sair_xeque) == 0:
                print(colored("XEQUE MATE!! BRANCAS VENCEM",'green'))
                break
            else:
                print(colored("---MOVIMENTOS POSSIVEIS---",'yellow'))
                for movimento in movimentos_sair_xeque:
                    print(f'{chr(movimento[1] + 65)}{movimento[0] + 1} -> {chr(movimento[3] + 65)}{movimento[2] + 1}')


                while True:
                    try:
                        coordenada1 = lerCoordenada()
                        linha1 = int(coordenada1[1]) - 1
                        coluna1 = ord(coordenada1[0]) % 65

                        coordenada2 = lerCoordenada()
                        linha2 = int(coordenada2[1]) - 1
                        coluna2 = ord(coordenada2[0]) % 65

                        if [linha1, coluna1, linha2, coluna2] in movimentos_sair_xeque:
                            peca = pegaPeca(pecas_pretas, linha1, coluna1)
                            movimentarPeca(peca, linha2, coluna2, pecas_brancas, pecas_pretas)
                            VEZ_BRANCAS = False
                            break
                        else:
                            print(colored("Error: jogada invalida!",'red'))
                    except:
                        print(colored("Error: jogada invalida!",'red'))

        else:
            # ler a coordenada
            coordenada = lerCoordenada()

            if coordenada == "roque" or coordenada == "ROQUE":
                torre = None

                rei = pegaPeca(pecas_pretas, 7, 4)

                if coordenada == "roque":
                    torre = pegaPeca(pecas_pretas, 7, 7)
                else:
                    torre = pegaPeca(pecas_pretas, 7, 0)

                if torre == None or rei == None:
                    print(colored("Error: torre ou rei nao encontrado!",'red'))
                else:
                    resultado = roque(rei, torre, pecas_brancas, pecas_pretas)

                    if resultado:
                        VEZ_BRANCAS = True
                    else:
                        print(colored("Error: Nao foi possivel realizar o roque!",'red'))
            else:
                linha = int(coordenada[1]) - 1
                coluna = ord(coordenada[0]) % 65

                if (linha < 0 or linha > 7):
                    print(colored("Error: linha invalida!",'red'))
                elif (coluna < 0 or coluna > 7):
                    print(colored("Error: coluna invalida!", 'red'))
                else:
                    peca = pegaPeca(pecas_pretas, linha, coluna)

                    if peca == None:
                        print(colored("Error: peca nao existe!", 'red'))
                    else:
                        coordenada = lerCoordenada()

                        linha = int(coordenada[1]) - 1
                        coluna = ord(coordenada[0]) % 65

                        if (linha < 0 or linha > 7):
                            print(colored("Error: linha invalida!",'red'))
                        elif (coluna < 0 or coluna > 7):
                            print(colored("Error: coluna invalida!",'red'))
                        else:
                            resultado = movimentarPeca(peca, linha, coluna, pecas_brancas, pecas_pretas)

                            if resultado:
                                VEZ_BRANCAS = True
                            else:
                                print(colored("Error: Nao foi possivel movimentar a peca!", 'red'))

    # renderiza o tabuleiro
    limparTabuleiro(tabuleiro)
    colocarPecasTabuleiro(tabuleiro, pecas_brancas, pecas_pretas)
    renderizarTabuleiro(tabuleiro)