def ler_arquivo():
    """Coleta as coordenadas e as armazena em um dicionário."""
    with open('berlin52.tsp', 'r') as arquivo:
        coordenadas = {}
        for linha in arquivo.readlines()[6:58]:
            cidade, x, y = linha.strip().split()
            coordenadas[int(cidade)] = (float(x), float(y))

    return coordenadas


def vizinho_mais_proximo(coordenadas):
    """Implementa o algoritmo do vizinho mais próximo."""
    cidades = list(coordenadas.keys())
    cidade_inicial = choice(cidades)
    cidade_atual = cidade_inicial

    percurso = [-1] * (len(coordenadas) + 1)
    percurso[0] = cidade_atual
    distancia_total = 0

    # Itera sobre o número de cidades menos uma vez, pois a cidade inicial já está no percurso.
    for k in range(1, len(coordenadas)):
        cidade_mais_proxima = None
        menor_distancia = float("inf")

        # Remove a cidade atual da lista de cidades a serem visitadas.
        cidades.remove(cidade_atual)

        # Calcula a distância para cada cidade não visitada e encontra a mais próxima.
        for cidade in cidades:
            x1, y1 = coordenadas[cidade_atual]
            x2, y2 = coordenadas[cidade]
            distancia = calcular_distancia(x1, y1, x2, y2)

            # Atualiza a cidade mais próxima e a menor distância encontrada.
            if distancia < menor_distancia:
                cidade_mais_proxima = cidade
                menor_distancia = distancia

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


def funcao_central():
    coordenadas = ler_arquivo()
    percurso, distancia = vizinho_mais_proximo(coordenadas)

    for c in percurso:
        print(c)

    print(f'\n{int(distancia)}')


if __name__ == '__main__':
    """Cronometra o tempo necessário para a execução do algoritmo."""
    from random import choice
    import timeit
    tempo_de_execucao = timeit.timeit(funcao_central, number=1)
    print(f'\nTempo de execução: {tempo_de_execucao:.6f} segundos.')