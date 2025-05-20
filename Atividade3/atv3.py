import numpy as np
import cv2
import math

def ex1():
    # Matriz de transformação A
    A = np.array([
        [4, 1, 0, 4],
        [1, 0, 1, 3],
        [2, 0, 2, 4],
        [3, 1, 0, 5]
    ])

    # Ponto P7 no mundo (formato homogêneo)
    P7 = np.array([4, 2, 1, 1])

    # Projeção na câmera: Pc = A * P7
    Pc = A @ P7

    # Converter para coordenadas (x, y)
    x = Pc[0] / Pc[3]
    y = Pc[1] / Pc[3]

    print(f"Coordenada observada na câmera: x = {x}, y = {y}")

def ex2():
    print("f, i, e, d, g, h, b, a, c.")

def ex3():
    # λ e B fornecidos
    λ = 3
    B = 3

    # Posição da câmera A = (0, 0, 0), B = (3, 0, 0), C = (6, 0, 0)

    # Pontos na imagem
    x1A, y1A = 3, 6
    x2A, y2A = 4, 6
    x1B, y1B = 1, 6
    x2B, y2B = 2, 6
    x3B, y3B = 0, 6
    x2C, y2C = 0, 6
    x3C, y3C = -2, 6

    # Estereoscopia: Z = λ * B / (x1 - x2)
    def calcular_z(x1, x2):
        return λ - ((λ * B) / (x2 - x1))

    # Cálculo dos pontos no mundo
    Z1 = calcular_z(x1A, x2A)
    X1 = (x1A / λ) * (λ - Z1)
    Y1 = (y1A / λ) * (λ - Z1)

    Z2 = calcular_z(x1B, x2B)
    X2 = (x1B / λ) * (λ - Z2)
    Y2 = (y1B / λ) * (λ - Z2)

    # Pontos médios
    W12 = ((X1 + X2)/2, (Y1 + Y2)/2)

    Z3 = calcular_z(x2B, x3B)
    X3 = (x2B / λ) * (λ - Z3)
    Y3 = (y2B / λ) * (λ - Z3)

    Z4 = calcular_z(x2C, x3C)
    X4 = (x2C / λ) * (λ - Z4)
    Y4 = (y2C / λ) * (λ - Z4)

    W23 = ((X3 + X4)/2, (Y3 + Y4)/2)

    print(f"Ponto médio W12: {W12}")
    print(f"Ponto médio W23: {W23}")

def ex4():
    # λ e B
    λ = 3
    B = 5

    # Pontos na imagem
    x3, x4 = 1, -5
    y3, y4 = 5, -5
    x1, x2 = 3, -3
    y1, y2 = 5, -5

    # Estereoscopia
    Z = λ - ((λ * B) / (x2 - x1))
    Xw = (x1 / λ) * (λ - Z)
    Yw = (y1 / λ) * (λ - Z)
    Xk = (x3 / λ) * (λ - Z)
    Yk = (y3 / λ) * (λ - Z)

    delta_x = Xw - Xk
    delta_y = Yw - Yk

    distancia = math.sqrt(delta_x**2 + delta_y**2)

    # Distância entre k e w
    print(f"Distância entre os pontos w e k: {distancia} metros")

def ex5():
    # Fator de conversão de pixels para metros
    F = 0.004125

    # Dicionário global de coordenadas
    coords = {'x1': None, 'x2': None}

    def clique_img1(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            largura = param.shape[1]
            coords['x1'] = (x - largura // 2) * F
            print(f"x1 corrigido (em metros): {coords['x1']}")

    def clique_img2(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            largura = param.shape[1]
            coords['x2'] = (x - largura // 2) * F
            print(f"x2 corrigido (em metros): {coords['x2']}")

    # Caminhos das imagens
    img1_path = 'img01_B1.5.png'  # imagem esquerda
    img2_path = 'img01_B1.5.png'  # imagem direita (mesma imagem por simplicidade, pode ser trocada)

    # Leitura
    img1 = cv2.imread(img1_path,1)
    img2 = cv2.imread(img2_path,1)

    # Mostrar imagens
    cv2.imshow("Imagem Esquerda", img1)
    cv2.imshow("Imagem Direita", img2)

    cv2.setMouseCallback("Imagem Esquerda", clique_img1, img1)
    cv2.setMouseCallback("Imagem Direita", clique_img2, img2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Salvar as coordenadas para o segundo script
    with open("coordenadas.txt", "w") as f:
        f.write(f"{coords['x1']}\n{coords['x2']}")

def ex5Compl():
    # Constante fornecida
    λ = 2.1513

    # Nome do par de imagem que você usou (para extrair B)
    nome_imagem = "img01_B1.5.png"

    # Extrair B do nome do arquivo
    import re
    match = re.search(r'_B([0-9.]+)\.png$', nome_imagem)
    if match:
        B = float(match.group(1))
    else:
        raise ValueError("Não foi possível extrair o valor de B do nome da imagem.")

    # Ler coordenadas salvas
    with open("coordenadas.txt", "r") as f:
        x1 = float(f.readline())
        x2 = float(f.readline())

    # Cálculo da profundidade
    Z = λ - ((λ * B) / (x2 - x1))
    print(f"Distância estimada da câmera até o ponto clicado: {Z:.2f} metros")

def main():
    ex3()
    # ex4()
    # ex5()
    # ex5Compl()

if __name__ == "__main__":
    main()



