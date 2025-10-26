import pygame
import json
import os
import sys

# --- CLASSE SPRITESHEET (Copiada do jogo principal) ---
# (Com melhorias para transparência de PNG)

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        try:
            self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Erro ao carregar a imagem da spritesheet: {filename}")
            raise e

        self.meta_data = self.filename.replace('.png', '.json')
        try:
            with open(self.meta_data) as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(f"Erro: Não foi encontrado o arquivo JSON: {self.meta_data}")
            raise
        except json.JSONDecodeError:
            print(f"Erro: O arquivo JSON está mal formatado: {self.meta_data}")
            raise

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        try:
            sprite_data = self.data['frames'][name]['frame']
            x, y, w, h = sprite_data["x"], sprite_data["y"], sprite_data["w"], sprite_data["h"]
            image = self.get_sprite(x, y, w, h)
            return image
        except KeyError:
            print(f"Erro: Sprite com o nome '{name}' não encontrado no JSON ({self.meta_data}).")
            raise

# --- 1. Configurações do Visualizador ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COLOR_BACKGROUND = (50, 50, 50) # Cinza escuro
COLOR_WHITE = (255, 255, 255)
COLOR_ERROR = (255, 100, 100) # Vermelho claro para erros

# --- 2. Inicialização do Pygame ---
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Visualizador de Spritesheet")
clock = pygame.time.Clock()

# Fontes para desenhar os nomes e mensagens de erro
font_sprite_name = pygame.font.Font(None, 24)
font_error = pygame.font.Font(None, 30)

# --- 3. Lógica de Carregamento de Assets ---

# --- CONFIGURAÇÃO DO CAMINHO (Exatamente como no jogo) ---
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd() 

ASSET_PATH = os.path.join(script_dir, 'assets') 
SPRITESHEET_FILENAME = 'snake_sprites.png' # Nome do seu arquivo de sprites
# ---------------------------------------------------

full_spritesheet_path = os.path.join(ASSET_PATH, SPRITESHEET_FILENAME)

# Lista para guardar as imagens carregadas e seus nomes
loaded_sprites = []
loading_failed = False
error_message = ""

try:
    print(f"Carregando spritesheet de: {full_spritesheet_path}")
    my_spritesheet = Spritesheet(full_spritesheet_path)
    
    # --- LÓGICA PRINCIPAL DESTE SCRIPT ---
    # Itera sobre TODOS os 'frames' definidos no arquivo JSON
    
    # .data['frames'] é o dicionário principal no seu JSON
    # .keys() pega o nome de cada sprite (ex: 'head', 'body', 'food')
    
    print("Elementos encontrados no JSON:")
    for sprite_name in my_spritesheet.data['frames'].keys():
        print(f"- {sprite_name}")
        # Carrega a imagem da sprite usando o nome
        image = my_spritesheet.parse_sprite(sprite_name)
        # Adiciona a imagem e seu nome na lista para desenhar
        loaded_sprites.append((image, sprite_name))
    
    if not loaded_sprites:
        raise ValueError("JSON carregado, mas nenhum 'frame' foi encontrado.")
        
    print(f"\nSucesso! {len(loaded_sprites)} sprites carregadas.")

except Exception as e:
    # Se qualquer coisa der errado (arquivo não encontrado, JSON mal formatado)
    print(f"\n--- ERRO AO CARREGAR ASSETS ---")
    print(f"Erro: {e}")
    print("Verifique se os arquivos .png e .json existem na pasta 'assets'.")
    print("---------------------------------")
    loading_failed = True
    error_message = str(e)


# --- 4. Loop Principal (Apenas para Desenhar) ---
running = True
while running:
    # --- Tratamento de Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # Permite sair com a tecla ESC
                running = False

    # --- Lógica de Desenho ---
    screen.fill(COLOR_BACKGROUND)

    if loading_failed:
        # Mostra a mensagem de erro na tela
        title_surf = font_error.render("Falha ao carregar assets:", True, COLOR_ERROR)
        msg_surf = font_error.render(error_message, True, COLOR_WHITE)
        help_surf = font_error.render("Verifique o console. Pressione ESC para sair.", True, COLOR_WHITE)
        
        screen.blit(title_surf, (20, 20))
        screen.blit(msg_surf, (20, 60))
        screen.blit(help_surf, (20, 120))
        
    else:
        # Desenha todas as sprites carregadas
        current_y = 20 # Posição Y inicial
        padding_x = 20
        
        for image, name in loaded_sprites:
            # 1. Desenha a imagem da sprite
            screen.blit(image, (padding_x, current_y))
            
            # 2. Desenha o nome da sprite e suas dimensões ao lado
            img_width = image.get_width()
            img_height = image.get_height()
            
            text = f"Nome: '{name}' (Tam: {img_width}x{img_height}px)"
            text_surf = font_sprite_name.render(text, True, COLOR_WHITE)
            
            # Calcula a posição do texto (à direita da imagem, centralizado verticalmente)
            text_x = padding_x + img_width + 15
            text_y = current_y + (img_height / 2) - (text_surf.get_height() / 2)
            
            screen.blit(text_surf, (text_x, text_y))
            
            # 3. Atualiza a posição Y para a próxima sprite
            current_y += img_height + 10 # Adiciona 10 pixels de espaçamento

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(30)

# --- 5. Fim ---
pygame.quit()
sys.exit()