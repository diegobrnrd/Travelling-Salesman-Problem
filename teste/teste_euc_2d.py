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

def funcao_principal():
    """Função central que gerencia a chamada de todas as outras funções."""
    a = (1, 2)
    b = (4, 6)
    c = (5, 1)
    d = (7, 3)
    e = (2, 8)

    x1, y1 = a
    x2, y2 = b
    distancia = calcular_distancia(x1, y1, x2, y2)
    print(f'{distancia:.2f}')

if __name__ == '__main__':
    funcao_principal()

    # Distâncias esperadas:
    # d(A, B) = 5.00
    # d(A, C) = 4.12
    # d(A, D) = 6.08
    # d(A, E) = 6.08
    # d(B, C) = 5.10
    # d(B, D) = 4.24
    # d(B, E) = 2.83
    # d(C, D) = 2.83
    # d(C, E) = 7.62
    # d(D, E) = 7.07
