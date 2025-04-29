import cv2
import numpy as np
from mss import mss
import time
import keyboard
from PIL import ImageGrab
import pyautogui
import pydirectinput
import sys
import random

# ================= CONFIGURAÇÕES =================
DIAMETRO = 100
ALTURA = 5
TEMPO_QUEBRAR_BLOCO = 1.3
PAUSA_ENTRE_ACOES = 0.15
BRILHO_MINIMO = 40
MOVIMENTO_90_GRAUS = 500
TECLA_INICIAR = 'c'
TECLA_PARAR = 'v'
# Configurações de picaretas
picaretas = {
    'madeira': [100, 100, 100],  # 3 picaretas de madeira
    'pedra': [150, 150, 150],  # 3 picaretas de pedra
    'ferro': [250, 250],  # 2 picaretas de ferro
    'diamante': [500],  # 1 picareta de diamante
    'ouro': [200],  # 1 picareta de ouro
}

PICARETAS_HOTBAR = {
    'madeira': 1,
    'pedra': 2,
    'ferro': 3,
    'diamante': 4
}

# Cores dos minérios em BGR
MINERIOS = {
    'carvao': {'min': (30, 30, 30), 'max': (70, 70, 70)},
    'ferro': {'min': (60, 80, 120), 'max': (100, 120, 180)},
    'ouro': {'min': (20, 160, 200), 'max': (50, 200, 255)},
    'diamante': {'min': (200, 150, 50), 'max': (255, 200, 100)},
    'redstone': {'min': (0, 0, 150), 'max': (20, 20, 255)},
    'esmeralda': {'min': (60, 160, 20), 'max': (100, 200, 100)},
    'pedra': {'min': (90, 90, 90), 'max': (150, 150, 150)}
}

LAVA_E_AGUA = {
    'agua': {'min': (50, 50, 200), 'max': (150, 150, 255)},
    'lava': {'min': (0, 0, 150), 'max': (50, 50, 255)}
}

# ================= MAPEAMENTO =================
mapa = {}
posicao = {"x": 0, "y": 0, "z": 0}
direcao = "norte"  # norte, sul, leste, oeste


# ================= FUNÇÕES DE VISÃO COMPUTACIONAL =================
def ajustar_brilho(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if np.mean(gray) < BRILHO_MINIMO:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[..., 2] = np.clip(hsv[..., 2] * 1.5, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return img

def esperar_por_tecla(tecla=TECLA_INICIAR, mensagem=None):
    """Espera até que a tecla especificada seja pressionada"""
    if mensagem:
        print(mensagem)
    print(f"Pressione '{tecla.upper()}' para continuar...")
    while not keyboard.is_pressed(tecla):
        time.sleep(0.1)
    time.sleep(0.5)  # Pequeno delay para evitar detecção múltipla


def detectar_bloco_frente():
    """Detecta o bloco à frente usando visão computacional"""
    try:
        x, y = pyautogui.size()
        bbox = (x // 2 - 50, y // 2 - 50, x // 2 + 50, y // 2 + 50)
        screenshot = np.array(ImageGrab.grab(bbox=bbox))
        screenshot = ajustar_brilho(screenshot)

        # Verificar minerios primeiro
        minerio = verificar_minerio()
        if minerio:
            return minerio

        # Verificar perigos (água/lava)
        substancia = verificar_lava_agua()
        if substancia:
            return substancia

        # Se não for nenhum dos acima, provavelmente é pedra ou ar
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        if np.mean(gray) > 100:  # Valor alto indica bloco sólido
            return "pedra"
        return "ar"
    except Exception as e:
        print(f"Erro ao detectar bloco: {e}")
        return "ar"


def detectar_bloco_baixo():
    """Detecta o bloco abaixo do jogador"""
    try:
        # Olhar para baixo temporariamente
        pydirectinput.move(0, 50, relative=True)
        time.sleep(0.1)

        x, y = pyautogui.size()
        bbox = (x // 2 - 50, y // 2, x // 2 + 50, y // 2 + 100)
        screenshot = np.array(ImageGrab.grab(bbox=bbox))
        screenshot = ajustar_brilho(screenshot)

        # Verificar perigos (água/lava)
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        for substancia, cores in LAVA_E_AGUA.items():
            lower = np.array(cores['min'])
            upper = np.array(cores['max'])
            mask = cv2.inRange(hsv, lower, upper)
            if cv2.countNonZero(mask) > 50:
                return substancia

        # Voltar a olhar para frente
        pydirectinput.move(0, -50, relative=True)
        time.sleep(0.1)

        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        if np.mean(gray) > 100:
            return "pedra"
        return "ar"
    except Exception as e:
        print(f"Erro ao detectar bloco abaixo: {e}")
        return "ar"


def verificar_minerio():
    """Verifica se há minério no centro da tela"""
    try:
        x, y = pyautogui.size()
        bbox = (x // 2 - 50, y // 2 - 50, x // 2 + 50, y // 2 + 50)
        screenshot = np.array(ImageGrab.grab(bbox=bbox))
        screenshot = ajustar_brilho(screenshot)
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)

        for minerio, cores in MINERIOS.items():
            lower = np.array(cores['min'])
            upper = np.array(cores['max'])
            mask = cv2.inRange(hsv, lower, upper)
            if cv2.countNonZero(mask) > 50:
                return minerio
        return None
    except Exception as e:
        print(f"Erro ao verificar minério: {e}")
        return None


# ================= FUNÇÕES DE MAPEAMENTO =================
def atualizar_mapa(x, y, z, bloco):
    """Atualiza o mapa interno com a informação do bloco"""
    mapa[(x, y, z)] = bloco


def atualizar_posicao():
    """Atualiza a posição no mapa baseado na direção"""
    frente = detectar_bloco_frente()
    baixo = detectar_bloco_baixo()

    # Atualiza o mapa
    if direcao == "norte":
        atualizar_mapa(posicao["x"], posicao["y"] - 1, posicao["z"] - 1, frente)  # Bloco à frente
        atualizar_mapa(posicao["x"], posicao["y"] - 1, posicao["z"], baixo)  # Bloco abaixo
    elif direcao == "sul":
        atualizar_mapa(posicao["x"], posicao["y"] - 1, posicao["z"] + 1, frente)
        atualizar_mapa(posicao["x"], posicao["y"] - 1, posicao["z"], baixo)
    elif direcao == "leste":
        atualizar_mapa(posicao["x"] + 1, posicao["y"] - 1, posicao["z"], frente)
        atualizar_mapa(posicao["x"], posicao["y"] - 1, posicao["z"], baixo)
    elif direcao == "oeste":
        atualizar_mapa(posicao["x"] - 1, posicao["y"] - 1, posicao["z"], frente)
        atualizar_mapa(posicao["x"], posicao["y"] - 1, posicao["z"], baixo)


# ================= FUNÇÕES DE MOVIMENTO =================
def andar_frente():
    """Move o personagem para frente e atualiza a posição"""
    global posicao

    pydirectinput.keyDown('w')
    time.sleep(0.3)
    pydirectinput.keyUp('w')

    if direcao == "norte":
        posicao["z"] -= 1
    elif direcao == "sul":
        posicao["z"] += 1
    elif direcao == "leste":
        posicao["x"] += 1
    elif direcao == "oeste":
        posicao["x"] -= 1

    atualizar_posicao()
    print(f"Andou para {direcao}. Nova posição: {posicao}")


def virar_direita():
    """Vira 90 graus para a direita"""
    global direcao

    pydirectinput.move(MOVIMENTO_90_GRAUS, 0, relative=True)
    time.sleep(0.3)

    novas_direcoes = {
        "norte": "leste",
        "leste": "sul",
        "sul": "oeste",
        "oeste": "norte"
    }
    direcao = novas_direcoes[direcao]
    print(f"Virou para {direcao}")


def virar_esquerda():
    """Vira 90 graus para a esquerda"""
    global direcao

    pydirectinput.move(-MOVIMENTO_90_GRAUS, 0, relative=True)
    time.sleep(0.3)

    novas_direcoes = {
        "norte": "oeste",
        "oeste": "sul",
        "sul": "leste",
        "leste": "norte"
    }
    direcao = novas_direcoes[direcao]
    print(f"Virou para {direcao}")




def trocar_picareta(tipo_picareta):
    """Troca para a próxima picareta disponível"""
    if tipo_picareta == 'madeira':
        proximo_tipo = 'pedra'
    elif tipo_picareta == 'pedra':
        proximo_tipo = 'ferro'
    elif tipo_picareta == 'ferro':
        proximo_tipo = 'diamante'
    else:
        print("Todas as picaretas acabaram!")
        sys.exit()

    selecionar_picareta_por_tipo(proximo_tipo)


# ================= FUNÇÕES DE NAVEGAÇÃO =================
def evitar_perigos():
    """Verifica e evita perigos como lava e água"""
    frente = detectar_bloco_frente()
    baixo = detectar_bloco_baixo()

    if frente in ["lava", "agua"] or baixo in ["lava", "agua"]:
        print(f"Perigo detectado: {frente}/{baixo}. Evitando...")
        virar_direita()
        return True
    return False


def minerar_adjacentes():
    """Minera blocos adjacentes (frente, cima, baixo)"""
    # Bloco à frente
    minerar_bloco("pedra")

    # Olhar para cima
    pydirectinput.move(0, -120, relative=True)
    time.sleep(0.1)
    minerar_bloco("pedra")

    # Olhar para baixo
    pydirectinput.move(0, 275, relative=True)
    time.sleep(0.1)
    minerar_bloco("pedra")

    # Voltar para frente
    pydirectinput.move(0, -150, relative=True)
    time.sleep(0.1)


def detectar_buraco():
    """Detecta se há um buraco à frente do jogador"""
    try:
        x, y = pyautogui.size()
        # Área de detecção (parte inferior central da tela)
        bbox = (x // 2 - 50, y // 2 + 30, x // 2 + 50, y // 2 + 100)
        screenshot = np.array(ImageGrab.grab(bbox=bbox))
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # Limiarização para detectar vazios
        _, threshold = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
        contornos, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Se encontrar uma área escura significativa
        if len(contornos) > 0 and cv2.contourArea(max(contornos, key=cv2.contourArea)) > 500:
            print("⚠ Buraco detectado à frente!")
            return True
        return False
    except Exception as e:
        print(f"Erro ao detectar buraco: {e}")
        return False


def evitar_buracos():
    """Toma ações para evitar cair em buracos"""
    if detectar_buraco():
        print("Evitando buraco...")
        # Passo para o lado
        pydirectinput.keyDown('a')
        time.sleep(0.3)
        pydirectinput.keyUp('a')
        # Pula para garantir
        pydirectinput.press('space')
        time.sleep(0.2)
        # Volta para frente
        pydirectinput.keyDown('d')
        time.sleep(0.3)
        pydirectinput.keyUp('d')
        return True
    return False


def ajustar_mira_para_minerio():
    """Ajusta a mira automaticamente para minérios próximos"""
    try:
        x, y = pyautogui.size()
        bbox = (x // 2 - 100, y // 2 - 100, x // 2 + 100, y // 2 + 100)  # Área ampla ao redor do centro
        screenshot = np.array(ImageGrab.grab(bbox=bbox))
        screenshot = ajustar_brilho(screenshot)
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)

        # Máscaras para cada tipo de minério
        masks = {}
        for minerio, cores in MINERIOS.items():
            lower = np.array(cores['min'])
            upper = np.array(cores['max'])
            masks[minerio] = cv2.inRange(hsv, lower, upper)

        # Encontrar o minério mais próximo do centro
        minerio_detectado = None
        melhor_posicao = None
        melhor_distancia = float('inf')

        for minerio, mask in masks.items():
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                if cv2.contourArea(cnt) > 50:  # Área mínima para considerar
                    M = cv2.moments(cnt)
                    if M["m00"] > 0:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        distancia = np.sqrt((cX - 100) ** 2 + (cY - 100) ** 2)  # Distância do centro

                        if distancia < melhor_distancia:
                            melhor_distancia = distancia
                            melhor_posicao = (cX, cY)
                            minero_detectado = minerio

        if minero_detectado and melhor_posicao:
            print(f"Minério detectado: {minero_detectado}")
            # Calcular deslocamento necessário
            desloc_x = melhor_posicao[0] - 100
            desloc_y = melhor_posicao[1] - 100

            # Ajuste suave da mira
            for _ in range(3):  # Movimentos graduais
                pydirectinput.move(int(desloc_x * 0.3), int(desloc_y * 0.3), relative=True)
                time.sleep(0.05)

            return minero_detectado
        return None

    except Exception as e:
        print(f"Erro ao ajustar mira: {e}")
        return None


# ================= FUNÇÕES DE MINERAÇÃO ATUALIZADAS =================

def selecionar_picareta_por_tipo(tipo_picareta):
    """Seleciona a picareta de acordo com o tipo no hotbar"""
    # Verifica se há picaretas disponíveis deste tipo
    if tipo_picareta not in picaretas or not picaretas[tipo_picareta]:
        return None

    # Encontra a primeira picareta com durabilidade
    for i, durabilidade in enumerate(picaretas[tipo_picareta]):
        if durabilidade > 0:
            # Seleciona no hotbar
            slot = PICARETAS_HOTBAR[tipo_picareta]
            pydirectinput.press(str(slot))
            time.sleep(PAUSA_ENTRE_ACOES)

            # Atualiza a durabilidade
            picaretas[tipo_picareta][i] -= 1
            print(f"Usando {tipo_picareta} (slot {slot}) - Durabilidade restante: {picaretas[tipo_picareta][i]}")

            # Verifica se quebrou
            if picaretas[tipo_picareta][i] <= 0:
                print(f"⚡ Picareta de {tipo_picareta} quebrou!")
                picaretas[tipo_picareta][i] = 0  # Garante que não fique negativo
                trocar_picareta(tipo_picareta)

            return True

    # Se todas estiverem quebradas
    print(f"Todas as picaretas de {tipo_picareta} quebraram!")
    trocar_picareta(tipo_picareta)
    return False


def trocar_picareta(tipo_atual):
    """Troca automaticamente para a próxima picareta disponível"""
    ordem_picaretas = ['diamante', 'ferro', 'pedra', 'madeira']

    try:
        # Encontra a posição atual na hierarquia
        idx = ordem_picaretas.index(tipo_atual)

        # Procura pela próxima picareta disponível
        for proximo_tipo in ordem_picaretas[idx + 1:]:
            if picaretas.get(proximo_tipo) and any(d > 0 for d in picaretas[proximo_tipo]):
                print(f"Trocando para picareta de {proximo_tipo}")
                return selecionar_picareta_por_tipo(proximo_tipo)

        # Se não encontrou nenhuma
        print("⚠️ Todas as picaretas acabaram!")
        sys.exit()

    except ValueError:
        print("Tipo de picareta inválido")
        sys.exit()


def minerar_bloco(tipo_picareta='pedra'):
    """Minera o bloco à frente com controle de durabilidade"""
    if not selecionar_picareta_por_tipo(tipo_picareta):
        return False

    try:
        pydirectinput.mouseDown(button='left')
        # Tempo baseado no tipo de bloco (pode ser ajustado)
        time.sleep(TEMPO_QUEBRAR_BLOCO)
        pydirectinput.mouseUp(button='left')
        time.sleep(PAUSA_ENTRE_ACOES)
        return True
    except Exception as e:
        print(f"Erro ao minerar: {e}")
        return False


def cavar_espiral():
    """Realiza mineração em espiral com varredura completa em 8 direções"""
    try:
        passos = DIAMETRO
        prioridade_minerios = ['diamante', 'esmeralda', 'ouro', 'ferro', 'carvao']
        PADRAO_VARREDURA = [
            # Camada Próxima (30px)
            (0, 0), (0, 30), (30, 30), (30, 0), (30, -30), (0, -30), (-30, -30), (-30, 0), (-30, 30),

            # Camada Estendida (60px) - Pontos estratégicos
            (0, 60), (45, 45), (60, 0), (45, -45), (0, -60), (-45, -45), (-60, 0), (-45, 45),

            # Pontos de verificação extras (ângulos importantes)
            (25, 80), (60, 25), (25, -80), (80, -25), (-25, -80), (-80, -25), (-25, 80), (-80, 25),
            (0, 0)
        ]
        while passos > 0 and not keyboard.is_pressed(TECLA_PARAR):
            for lado in range(2):
                for passo_atual in range(passos):
                    if keyboard.is_pressed(TECLA_PARAR):
                        print("Parando mineração...")
                        return False

                    # Variáveis de controle de posição
                    deslocamento_acumulado = [0, 0]
                    posicao_inicial = pyautogui.position()

                    # Loop de mineração contínua
                    while True:
                        minerio_encontrado = None
                        direcao_deteccao = None

                        # Varredura completa na área atual
                        for i, (ang_v, ang_h) in enumerate(PADRAO_VARREDURA):
                            # Movimento relativo (exceto primeira posição que é o centro)
                            if i > 0:
                                pydirectinput.move(ang_h, ang_v, relative=True)
                                deslocamento_acumulado[0] += ang_h
                                deslocamento_acumulado[1] += ang_v
                                time.sleep(0.05)

                            # Verificação de minério
                            minerio = verificar_minerio()
                            if minerio in prioridade_minerios:
                                minerio_encontrado = minerio
                                direcao_deteccao = (ang_v, ang_h)
                                break

                            # Retorno ao centro após cada verificação
                            if i > 0:
                                pydirectinput.move(-ang_h, -ang_v, relative=True)
                                deslocamento_acumulado[0] -= ang_h
                                deslocamento_acumulado[1] -= ang_v
                                time.sleep(0.03)

                        # Se não encontrou mais minérios, sair do loop
                        if not minerio_encontrado:
                            break

                        # Mineração do recurso encontrado
                        print(f"⛏ {minerio_encontrado.upper()} detectado - minerando...")

                        # Mover para o minério (se não for no centro)
                        if direcao_deteccao != (0, 0):
                            pydirectinput.move(direcao_deteccao[1], direcao_deteccao[0], relative=True)
                            deslocamento_acumulado[0] += direcao_deteccao[1]
                            deslocamento_acumulado[1] += direcao_deteccao[0]
                            time.sleep(0.1)

                        # Configurações de mineração dinâmicas
                        picareta = 'diamante' if minerio_encontrado in ['diamante', 'esmeralda'] else \
                            'ferro' if minerio_encontrado == 'ouro' else 'pedra'

                        tempo = {
                            'diamante': 2.0,
                            'esmeralda': 1.8,
                            'ouro': 1.5,
                            'ferro': 1.2,
                            'carvao': 0.8
                        }.get(minerio_encontrado, TEMPO_QUEBRAR_BLOCO)

                        # Execução da mineração
                        selecionar_picareta_por_tipo(picareta)
                        pydirectinput.mouseDown(button='left')
                        time.sleep(tempo)
                        pydirectinput.mouseUp(button='left')
                        time.sleep(PAUSA_ENTRE_ACOES)
                        pydirectinput.keyDown('w')
                        time.sleep(0.15)
                        pydirectinput.keyUp('w')
                        # Retorno à posição de varredura
                        if deslocamento_acumulado != [0, 0]:
                            pydirectinput.move(-deslocamento_acumulado[0], -deslocamento_acumulado[1], relative=True)
                            time.sleep(0.1)
                            deslocamento_acumulado = [0, 0]  # Reset

                    # Mineração padrão se não encontrou recursos especiais
                    minerar_adjacentes()

                    # Movimento na espiral
                    if passo_atual < passos - 1:
                        pydirectinput.keyDown('w')
                        time.sleep(0.15)
                        pydirectinput.keyUp('w')


                # Curva na espiral
                virar_direita() if lado == 0 else virar_esquerda()
                time.sleep(0.2)

            # Descida de camada
            passos -= 1
            if passos > 0:
                descer_camada()

        return True

    except Exception as e:
        print(f"ERRO: {e}")
        return False
def descer_camada():
    """Desce uma camada na mina"""
    print("Descendo uma camada...")
    # Olhar para baixo
    pydirectinput.move(0, 50, relative=True)
    time.sleep(0.5)

    # Cavar para baixo
    pydirectinput.mouseDown(button='left')
    time.sleep(2.0)
    pydirectinput.mouseUp(button='left')

    # Voltar a olhar para frente
    pydirectinput.move(0, -50, relative=True)
    time.sleep(0.5)

    # Atualizar posição Y
    posicao["y"] -= 1


def main():
    try:
        print("=== MINERADOR AUTOMÁTICO AVANÇADO ===")
        print("Configurações:")
        print(f"- Diâmetro da espiral: {DIAMETRO} blocos")
        print(f"- Altura da mina: {ALTURA} camadas")
        print(f"- Tecla para iniciar: {TECLA_INICIAR.upper()}")
        print(f"- Tecla para parar: {TECLA_PARAR.upper()}")

        # Calibração inicial
        print("\n=== CALIBRAÇÃO INICIAL ===")
        print("Posicione-se no ponto inicial e olhe para a primeira parede")
        esperar_por_tecla(TECLA_INICIAR, f"Pressione {TECLA_INICIAR.upper()} para começar a calibração...")

        # Iniciar mineração
        print("\n=== INICIANDO MINERAÇÃO ===")
        print(f"Pressione {TECLA_PARAR.upper()} a qualquer momento para parar")

        for camada in range(ALTURA):
            print(f"\nCamada {camada + 1}/{ALTURA}")
            if not cavar_espiral():
                print(f"Mineração interrompida pelo usuário (tecla {TECLA_PARAR.upper()})")
                break
            if camada < ALTURA - 1:
                descer_camada()

        print("\nMineração concluída com sucesso!")

    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário")
    except Exception as e:
        print(f"\nErro: {str(e)}")


if __name__ == "__main__":
    main()