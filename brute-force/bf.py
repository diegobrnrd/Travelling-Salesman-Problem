"""berlin52 - BF"""


def ler_arquivo():
    """Coleta as coordenadas e as armazena em um dicionário."""
    coordenadas = {}
    with open('berlin52.tsp', 'r') as arquivo:
        for linha in arquivo.readlines()[6:16]:
            cidade, x, y = linha.strip().split()
            coordenadas[int(cidade)] = (float(x), float(y))
    return coordenadas


def gerar_rotas(lista):
    """Gera todas as combinações possíveis de rotas."""
    if len(lista) == 0:
        return []
    if len(lista) == 1:
        return [lista + [lista[0]]]

    permutacoes = []
    for i in range(len(lista)):
        elemento = lista[i]
        restante = lista[:i] + lista[i + 1:]
        for p in gerar_rotas(restante):
            permutacoes.append([elemento] + p[:-1] + [elemento])

    return permutacoes


def calcular_rotas(coordenadas, rotas):
    """Calcula a distância total para cada uma das rotas possíveis."""
    menor_percurso = [(), float('inf')]
    for rota_atual in rotas:
        distancia_total = 0
        for i in range(len(rota_atual) - 1):
            x1, y1 = coordenadas[int(rota_atual[i])]
            x2, y2 = coordenadas[int(rota_atual[i + 1])]
            distancia_total += calcular_distancia(x1, y1, x2, y2)
        if distancia_total < menor_percurso[1]:
            menor_percurso[0], menor_percurso[1] = rota_atual, distancia_total

    return menor_percurso


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
    """Grava informações sobre um percurso em um arquivo de texto chamado."""
    with open('resultado.txt', 'w') as arquivo:
        if senha == 0:
            arquivo.write(f'Percurso: {percurso}\n')
            arquivo.write(f'Distancia: {int(distancia)}\n')
        else:
            arquivo.write(f'Tempo: {tempo:.6f}\n\n')


def funcao_central():
    """Função central que gerencia a chamada de todas as outras funções."""
    coordenadas = ler_arquivo()
    cidades = [str(c) for c in coordenadas.keys()]
    rotas = gerar_rotas(cidades)
    menor_percurso = calcular_rotas(coordenadas, rotas)
    gravar_resultado(menor_percurso[0], menor_percurso[1])


if __name__ == '__main__':
    """Cronometra o tempo necessário para a execução do algoritmo."""
    import timeit
    tempo_de_execucao = timeit.timeit(funcao_central, number=1)
    gravar_resultado(tempo=tempo_de_execucao, senha=1)
