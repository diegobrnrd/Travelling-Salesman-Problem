"""berlin52 - KNN"""


import random
random.seed(33)


def ler_arquivo():
    """Coleta as coordenadas e as armazena em um dicionário."""
    coordenadas = {}
    with open('berlin52.tsp', 'r') as arquivo:
        for linha in arquivo.readlines()[6:58]:
            cidade, x, y = linha.strip().split()
            coordenadas[int(cidade)] = (float(x), float(y))
    return coordenadas


def vizinho_mais_proximo(coordenadas):
    """Implementa o algoritmo do vizinho mais próximo."""
    cidades = list(coordenadas.keys())
    cidade_inicial = random.randint(1, 52)
    cidade_atual = cidade_inicial

    percurso = [-1] * (len(coordenadas) + 1)
    percurso[0] = cidade_atual
    distancia_total = 0

    # Itera sobre o número de cidades menos uma vez, pois a cidade inicial já está no percurso.
    for k in range(1, len(coordenadas)):
        i = cidades.index(cidade_atual)
        cidades[i] = 0

        cidade_mais_proxima, menor_distancia = encontrar_cidade_mais_proxima(cidade_atual, cidades, coordenadas)

        # Adiciona a cidade mais próxima ao percurso e atualiza a distância total.
        percurso[k] = cidade_mais_proxima
        distancia_total += menor_distancia

        # Define a cidade mais próxima como a cidade atual para a próxima iteração.
        cidade_atual = cidade_mais_proxima

    # Calcula a distância para voltar à cidade inicial.
    x1, y1 = coordenadas[cidade_atual]
    x2, y2 = coordenadas[cidade_inicial]
    distancia_total += calcular_distancia(x1, y1, x2, y2)

    # Retorna o percurso completo e a distância total percorrida.
    return percurso, distancia_total


def encontrar_cidade_mais_proxima(cidade_atual, cidades, coordenadas):
    """Encontra a cidade mais próxima e a distância para a cidade atual."""
    cidade_mais_proxima = None
    menor_distancia = float("inf")

    # Calcula a distância para cada cidade não visitada e encontra a mais próxima.
    for cidade in cidades:
        if cidade == 0:
            continue
        x1, y1 = coordenadas[cidade_atual]
        x2, y2 = coordenadas[cidade]
        distancia = calcular_distancia(x1, y1, x2, y2)

        # Atualiza a cidade mais próxima e a menor distância encontrada.
        if distancia < menor_distancia:
            cidade_mais_proxima = cidade
            menor_distancia = distancia

    return cidade_mais_proxima, menor_distancia


def calcular_distancia(x1, y1, x2, y2):
    """Calcula a distância euclidiana entre dois pontos no plano cartesiano."""
    a = (x2 - x1) ** 2
    b = (y2 - y1) ** 2
    x = a + b
    return raiz_quadrada(x, 3.2, 0.001)


def raiz_quadrada(x, x0, e):
    """Calcula a raiz quadrada."""
    if abs(x0 ** 2 - x) <= e:
        return x0
    else:
        return raiz_quadrada(x, ((x0 ** 2 + x) / (2 * x0)), e)


def gravar_resultado(percurso=None, distancia=None, tempo=None, senha=0):
    """Grava informações sobre um percurso em um arquivo de texto chamado 'resultado.txt'."""
    with open('resultado_2.txt', 'w') as arquivo:
        if senha == 0:
            arquivo.write(f'Percurso: {percurso}\n')
            arquivo.write(f'Distancia: {int(distancia)}\n')
        else:
            arquivo.write(f'Tempo: {tempo:.6f}\n\n')


def funcao_central():
    """Função central que gerencia a chamada de todas as outras funções."""
    coordenadas = ler_arquivo()
    percurso, distancia = vizinho_mais_proximo(coordenadas)
    gravar_resultado(percurso=percurso, distancia=distancia)


if __name__ == '__main__':
    """Cronometra o tempo necessário para a execução do algoritmo."""
    import timeit
    for _ in range(30):
        tempo_de_execucao = timeit.timeit(funcao_central, number=1)
        gravar_resultado(tempo=tempo_de_execucao, senha=1)