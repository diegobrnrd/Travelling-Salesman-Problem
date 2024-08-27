import random


def gerar_populacao_inicial(num_listas, tamanho_lista):
    listas = []

    while len(listas) < num_listas:
        nova_lista = random.sample(range(1, tamanho_lista + 1), tamanho_lista)
        if nova_lista not in listas:
            listas.append(nova_lista)

    return listas  # lista com num_listas solucoes diferentes, cada solucao possui tamanho_lista pontos que não se repetem


def encontrarcoordenadas(arquivo):
    with open(arquivo, 'r') as file:

        linhas = [linha.strip().split() for linha in
                  file.readlines()[6:58]]  # o arquivo berlim 52 só começa os dados de fato na linha 7 e vai até a 58
        lista_coordenadas = {}

        for indice in range(len(linhas)):
            for elemento in range(len(linhas[0])):
                if elemento == 0:
                    lista_coordenadas[str(indice + 1)] = {}
                elif elemento == 1:
                    lista_coordenadas[str(indice + 1)]['X'] = int(float(linhas[indice][elemento]))
                else:
                    lista_coordenadas[str(indice + 1)]['Y'] = int(float(linhas[indice][elemento]))
        return lista_coordenadas  # lista com os pontos na primeira posição das listas e suas coordenadas nas posições 1 e 2


def estimativa_inicial(x):
    if x > 1:
        return x / 2  # Aproximação simples para x > 1
    elif x == 0:
        return 0
    else:
        return 1  # Aproximação simples para x < 1


def raiz_quadrada(x, x0, e):
    if abs(x0 ** 2 - x) <= e:
        return x0
    else:
        return raiz_quadrada(x, ((x0 ** 2 + x) / (2 * x0)), e)


def calcular_distancia_solucao(caminho, lista_de_pontos):
    tamanho_do_caminho = 0

    for pos, ponto in enumerate(caminho):

        if ponto != caminho[len(caminho) - 1]:
            distancia_dois_pontos = 0

            a = (lista_de_pontos[str(ponto)]['X'], lista_de_pontos[str(caminho[pos + 1])]['X'])
            b = (lista_de_pontos[str(ponto)]['Y'], lista_de_pontos[str(caminho[pos + 1])]['Y'])

            x = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
            # cálculo com base na métrica euc_2d
            distancia_dois_pontos = raiz_quadrada(x, estimativa_inicial(x), 0.0001)
            tamanho_do_caminho += int(distancia_dois_pontos)

    return tamanho_do_caminho


def selecao_roleta(solucoes, vagas, listapontos):
    fitness_solucoes = [calcular_distancia_solucao(individuo, listapontos) for individuo in solucoes]
    fitness_inverso = [1 / fitness if fitness != 0 else float('inf') for fitness in
                       fitness_solucoes]  # individuos com a MENOR distância vão ter mais chances de serem escolhidos
    total_fitness_inverso = sum(fitness_inverso)
    probabilidades = [fitness / total_fitness_inverso for fitness in fitness_inverso]
    individuos_selecionados = random.choices(solucoes, weights=probabilidades,
                                             k=vagas)  # seleciona n solucoes para sofrerem crossover, sendo n = vagas

    return individuos_selecionados


def crossover(pai1, pai2):
    ponto_de_corte = (len(pai1) // 2)
    pai1clone = pai1[:]

    for ponto in range(ponto_de_corte):

        if pai1clone[ponto] != pai2[ponto]:
            pos_do_a_ser_trocado = None

            for indice, point in enumerate(pai1clone):

                if point == pai2[ponto]:
                    pos_do_a_ser_trocado = indice
                    break

            pai1clone[ponto], pai1clone[pos_do_a_ser_trocado] = pai1clone[pos_do_a_ser_trocado], pai1clone[ponto]

    return pai1clone


def gerar_filhos(pai1, pai2):
    child1 = crossover(pai1, pai2)
    child2 = crossover(pai2, pai1)
    return mutacao(child1), mutacao(child2)


def mutacao(solucao):  # ainda vamos querer a solucao sem ser mutada?
    for ponto in range(len(solucao)):

        if random.random() < 0.01:
            indice_a_ser_trocado = random.choice([i for i in range(len(solucao)) if i != ponto])

            solucao[ponto], solucao[indice_a_ser_trocado] = solucao[indice_a_ser_trocado], solucao[ponto]

    return solucao


def main():
    pop_inicial = gerar_populacao_inicial(100, 52)
    dic_pontos = encontrarcoordenadas('berlin52.tsp')
    primeiros_escolhidos = selecao_roleta(pop_inicial, 50, dic_pontos)
    populacao = [None] * 100

    for individuo in range(0, len(primeiros_escolhidos), 2):
        novos_filhos = gerar_filhos(primeiros_escolhidos[individuo], primeiros_escolhidos[individuo + 1])
        populacao[individuo] = primeiros_escolhidos[individuo]
        populacao[individuo + 1] = primeiros_escolhidos[individuo + 1]
        populacao[individuo + 50] = novos_filhos[0]
        populacao[individuo + 51] = novos_filhos[1]

    for iteracao in range(50):
        escolhidos = selecao_roleta(populacao, 50, dic_pontos)
        for individuo in range(0, len(primeiros_escolhidos), 2):
            novos_filhos = gerar_filhos(escolhidos[individuo], escolhidos[individuo + 1])
            populacao[individuo] = escolhidos[individuo]
            populacao[individuo + 1] = escolhidos[individuo + 1]
            populacao[individuo + 50] = novos_filhos[0]
            populacao[individuo + 51] = novos_filhos[1]

    tamanhos_populacao_final = [calcular_distancia_solucao(solu, dic_pontos) for solu in populacao]
    menor_distancia = float('inf')
    respectiva_solucao = None
    for indice, soluc in enumerate(tamanhos_populacao_final):
        if soluc < menor_distancia:
            menor_distancia = soluc
            respectiva_solucao = indice

    return populacao[respectiva_solucao], menor_distancia


if __name__ == '__main__':
    resposta = main()
    sequencia = resposta[0]
    distancia = resposta[1]
    print(sequencia, distancia)
