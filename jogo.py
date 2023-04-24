import cv2
import numpy as np


# Definindo os movimentos
def area_jogada(area_maxima):
    if area_maxima < 11500 and area_maxima > 6000:
        return "Tesoura"
    elif area_maxima > 14500 and area_maxima < 17000:
        return "Papel"
    elif area_maxima > 11500 and area_maxima < 14000:
        return "Pedra"
    else:
        return ""


def resultado(img, text, origem, color):
    font = cv2.FONT_HERSHEY_PLAIN
    cv2.putText(img, text, origem, font, 2, color, 2, cv2.LINE_AA)


esquerda = 0
direita = 0

# Abrindo o vídeo
video = cv2.VideoCapture("pedra-papel-tesoura.mp4")

while video.isOpened():
    ret, img = video.read()

    sizex = 100
    sizey = 40
    color = (0, 0, 0)

    if img is None:
        cv2.destroyWindow('Pedra Papel e Tesoura')
        video.release()
    else:
        img = cv2.resize(img, (800, 600))

        # Divide a imagem
        mao1 = img[100:600, 100:450]
        mao2 = img[100:600, 350:800]

        # Convertendo a imagem
        img1 = cv2.cvtColor(mao1, cv2.COLOR_BGR2HSV)
        img2 = cv2.cvtColor(mao2, cv2.COLOR_BGR2HSV)
        # definindo a mascara
        image_lower_hsv = np.array([0, 0, 0])
        image_upper_hsv = np.array([245, 245, 245])

        mask_hsv = cv2.inRange(mao1, image_lower_hsv, image_upper_hsv)
        mask_hsv2 = cv2.inRange(mao2, image_lower_hsv, image_upper_hsv)
        # Encontrando o contorno
        contorno, _ = cv2.findContours(mask_hsv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contorno1, _ = cv2.findContours(mask_hsv2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        mask_rgb = cv2.cvtColor(mask_hsv, cv2.COLOR_GRAY2RGB)
        mask_rgb2 = cv2.cvtColor(mask_hsv2, cv2.COLOR_GRAY2RGB)
        contornos_img = mask_rgb.copy()
        contornos_img2 = mask_rgb2.copy()

        area_maxima = 0
        area_maxima1 = 0

        #Descobrindo a area das duas mãos
        for i in range(len(contorno)):
            area = cv2.contourArea(contorno[i])
            if area > area_maxima:
                area_maxima = area

        for i in range(len(contorno1)):
            area1 = cv2.contourArea(contorno1[i])
            if area1 > area_maxima1:
                area_maxima1 = area1

        # cv2.drawContours(contornos_img, contorno, -1, color = [255, 0, 0])
        # cv2.drawContours(contornos_img2, contorno1, -1, color =  [255, 0, 0])

        # Apresentando a jogada de acordo com a area
        texto_jogada = area_jogada(area_maxima)
        resultado(img, texto_jogada, (120, 100), (0, 0, 0))

        texto_jogada1 = area_jogada(area_maxima1)
        resultado(img, texto_jogada1, (480, 100), (128, 128, 128))

        moves_dict = {
            "Pedra": "Tesoura",
            "Papel": "Pedra",
            "Tesoura": "Papel"
        }

        # Verificando vencedor
        if texto_jogada == texto_jogada1:
            resultado(img, "Empate", (320, 25), (0, 0, 255))
        elif (texto_jogada == "Pedra" and texto_jogada1 == "Tesoura") or (
                texto_jogada == "Tesoura" and texto_jogada1 == "Papel") or (
                texto_jogada == "Papel" and texto_jogada1 == "Pedra"):
            resultado(img, "Jogador 1 venceu", (250, 25), (0, 255, 0))
            esquerda += 0.01
        else:
            resultado(img, "Jogador 2 venceu", (250, 25), (255, 0, 0))
            direita += 0.01

        pontos_esquerda = round(esquerda)
        pontos_direita = round(direita)

        # Mostrando os pontos de cada jogador
        texto_ponto = "Jogador 1: {}".format(pontos_esquerda)
        resultado(img, texto_ponto, (120, 70), (0, 0, 0))
        texto_ponto1 = "Jogador 2: {}".format(pontos_direita)
        resultado(img, texto_ponto1, (480, 70), (128, 128, 128))

        cv2.imshow('Pedra Papel e Tesoura', img)

        k = cv2.waitKey(10)
        if k == 27:
            break
