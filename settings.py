# settings.py
# Arquivo para guardar todas as constantes e configurações do jogo.

import os

# --- 1. Configurações de Tela e Jogo ---
SCREEN_WIDTH = 918
SCREEN_HEIGHT = 612
FPS = 30
SNAKE_SPEED = 8

# --- 2. Configurações da Cobra ---
HEAD_SIZE = (35, 35)
BODY_SIZE = (27, 22)
HEAD_P = 0.75 # Percentual da cabeça para cooldown de curva
BODY_SPACING = 5 # Espaçamento entre os segmentos do corpo

# --- 3. Configurações da Comida ---
FOOD_SIZE = (18, 19)

# --- 4. Cores (Usadas como fallback e para UI) ---
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_HEAD_FALLBACK = (0, 200, 0)
COLOR_BODY_FALLBACK = (0, 150, 0)
COLOR_FOOD_FALLBACK = (200, 0, 0)

# --- 5. Configurações de Caminho (Assets) ---
# Pega o caminho absoluto para o diretório onde este script está
try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Fallback se __file__ não estiver definido (ex: rodando em um REPL)
    SCRIPT_DIR = os.getcwd() 

ASSET_PATH = os.path.join(SCRIPT_DIR, 'assets') 
SPRITESHEET_FILENAME = 'snake_sprites.png'