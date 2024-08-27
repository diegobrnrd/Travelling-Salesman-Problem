from random import randint

def ler_arquivo():
    with open('berlin52.tsp', 'r') as arquivo:
        coordenadas = {}
        for linha in arquivo.readlines()[6:58]:
            cidade, x, y = linha.strip().split()
            coordenadas[int(cidade)] = (float(x), float(y))
    return coordenadas


def vizinho_mais_proximo(coordenadas):
    cidade_inicial = randint(1, len(coordenadas))
    percurso = [-1] * (len(coordenadas) + 1)
    menor_distancia_encontrada = 0
    cidades_nao_visitadas = list(coordenadas.keys())
    cidade_atual = cidade_inicial

    for k in range(len(coordenadas) - 1):
        cidade_mais_proxima = None
        menor_distancia = float("inf")
        cidades_nao_visitadas.remove(cidade_atual)

        for cidade in cidades_nao_visitadas:
            x1, y1 = coordenadas[cidade_atual]
            x2, y2 = coordenadas[cidade]
            distancia = calcular_distancia(x1, y1, x2, y2)

            if distancia < menor_distancia:
                cidade_mais_proxima = cidade
                menor_distancia = distancia

        percurso[k] = cidade_mais_proxima
        menor_distancia_encontrada += menor_distancia
        percurso[len(coordenadas) - 1] = cidade_atual
        cidade_atual = cidade_mais_proxima

    x1, y1 = coordenadas[cidade_atual]
    x2, y2 = coordenadas[cidade_inicial]
    distancia_para_inicial = calcular_distancia(x1, y1, x2, y2)
    percurso[len(coordenadas)] = -1
    menor_distancia_encontrada += distancia_para_inicial

    return percurso, menor_distancia_encontrada


def calcular_distancia(x1, y1, x2, y2):
    a = (x2 - x1) ** 2
    b = (y2 - y1) ** 2
    x = a + b
    return raiz_quadrada(x, 3.2, 0.001)


def raiz_quadrada(x, x0, e):
    if abs(x0 ** 2 - x) <= e:
        return x0
    else:
        return raiz_quadrada(x, ((x0 ** 2 + x) / (2 * x0)), e)


def funcao_principal():
    coordenadas = ler_arquivo()
    percurso, distancia = vizinho_mais_proximo(coordenadas)

    for c in percurso:
        print(c)
    print(int(distancia))


if __name__ == '__main__':
    funcao_principal()