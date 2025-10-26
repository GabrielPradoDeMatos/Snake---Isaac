import pygame
import random
import os
import json 

# --- CLASSE SPRITESHEET (IMPLEMENTADA CONFORME SOLICITADO) ---
# (Com melhorias para transparência de PNG)

class Spritesheet:
    def __init__(self, filename):
        """
        Carrega a spritesheet (imagem) e seu arquivo de metadados (.json).
        'filename' deve ser o caminho para o arquivo .png.
        O .json correspondente deve estar na mesma pasta e com o mesmo nome.
        """
        self.filename = filename
        try:
            # Usa convert_alpha() para suportar transparência de PNG
            self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Erro ao carregar a imagem da spritesheet: {filename}")
            raise e # Propaga o erro para o bloco try/except principal

        # Gera o nome do arquivo JSON a partir do nome do arquivo PNG
        self.meta_data = self.filename.replace('.png', '.json')
        try:
            with open(self.meta_data) as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(f"Erro: Não foi encontrado o arquivo JSON: {self.meta_data}")
            raise # Propaga o erro
        except json.JSONDecodeError:
            print(f"Erro: O arquivo JSON está mal formatado: {self.meta_data}")
            raise # Propaga o erro

    def get_sprite(self, x, y, w, h):
        """
        Extrai uma sub-imagem (sprite) da spritesheet principal.
        """
        # Cria uma nova superfície com transparência total (SRCALPHA)
        sprite = pygame.Surface((w, h), pygame.SRCALPHA)
        # Copia a porção da spritesheet para a nova superfície
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        """
        Obtém uma sprite usando seu nome (definido no arquivo JSON).
        """
        try:
            # Busca os dados da sprite pelo 'name' no JSON
            sprite_data = self.data['frames'][name]['frame']
            x, y, w, h = sprite_data["x"], sprite_data["y"], sprite_data["w"], sprite_data["h"]
            # Usa get_sprite para extrair a imagem
            image = self.get_sprite(x, y, w, h)
            return image
        except KeyError:
            print(f"Erro: Sprite com o nome '{name}' não encontrado no JSON ({self.meta_data}).")
            raise # Propaga o erro


# --- 1. Inicialização do Pygame ---
pygame.init()
pygame.font.init()

# --- 2. Configurações Principais ---

# Tamanho da tela
SCREEN_WIDTH = 918
SCREEN_HEIGHT = 612

# Variável de velocidade
SNAKE_SPEED = 8

# Tamanhos das texturas (para redimensionamento)
HEAD_SIZE = (35, 35)
BODY_SIZE = (27, 22)
FOOD_SIZE = (18, 19)
HEAD_P = 0.75

# Cores Padrão (Fallback caso as imagens não sejam encontradas)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_HEAD_FALLBACK = (0, 200, 0)
COLOR_BODY_FALLBACK = (0, 150, 0)
COLOR_FOOD_FALLBACK = (200, 0, 0)

# Configurações de Jogo
FPS = 30
BODY_SPACING = 3

# --- 3. Setup da Tela e Relógio ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake - Movimento Livre")
clock = pygame.time.Clock()

# --- FONTES ---
score_font = pygame.font.Font(None, 50)
game_over_font = pygame.font.Font(None, 75)
restart_font = pygame.font.Font(None, 40)


# --- 4. Função de Fallback (para caso o carregamento falhe) ---
def create_fallback_surface(size, color):
    """Cria uma superfície de cor sólida se a imagem falhar."""
    surface = pygame.Surface(size)
    surface.fill(color)
    return surface

# --- 5. Carregar Assets do Jogo (USANDO SPRITESHEET E CAMINHO CORRIGIDO) ---

# --- CONFIGURAÇÃO DO CAMINHO (CORRIGIDO) ---
# Pega o caminho absoluto para o diretório onde este script está
# Isso garante que ele sempre encontre a pasta 'assets' relativa ao script
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Fallback se __file__ não estiver definido (ex: rodando em um REPL interativo)
    script_dir = os.getcwd() 

# Define o ASSET_PATH como a pasta 'assets' DENTRO do diretório do script
ASSET_PATH = os.path.join(script_dir, 'assets') 
SPRITESHEET_FILENAME = 'snake_sprites.png' # O .json deve ter o mesmo nome
# ---------------------------------------------

# Agora, full_spritesheet_path será o caminho completo e correto
# Ex: C:\Users\C129704\Snake Isaac\assets\snake_sprites.png
full_spritesheet_path = os.path.join(ASSET_PATH, SPRITESHEET_FILENAME)

try:
    # 1. Tenta carregar a spritesheet
    print(f"Carregando spritesheet de: {full_spritesheet_path}")
    my_spritesheet = Spritesheet(full_spritesheet_path)
    
    # 2. Tenta extrair as imagens usando os nomes do JSON
    #    (O seu JSON deve conter os nomes 'head', 'body' e 'food')
    print("Extraindo sprites: 'head', 'body', 'food'...")
    head_original_img_unscaled = my_spritesheet.parse_sprite('head')
    body_img_unscaled = my_spritesheet.parse_sprite('body')
    food_img_unscaled = my_spritesheet.parse_sprite('food')
    
    # 3. Redimensiona as imagens para os tamanhos definidos no Jogo
    head_original_img = pygame.transform.scale(head_original_img_unscaled, HEAD_SIZE)
    body_img = pygame.transform.scale(body_img_unscaled, BODY_SIZE)
    food_img = pygame.transform.scale(food_img_unscaled, FOOD_SIZE)
    
    print("Sprites carregadas com sucesso!")

except (pygame.error, FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as e:
    # 4. Se qualquer coisa der errado (arquivo não encontrado, JSON errado, nome da sprite errada)
    print(f"\n--- AVISO! ---")
    print(f"ERRO: Não foi possível carregar os assets da spritesheet.")
    print(f"Causa: {e}")
    print(f"Verifique se o caminho '{full_spritesheet_path}' está correto.")
    print(f"Verifique se o arquivo JSON '{full_spritesheet_path.replace('.png', '.json')}' existe e está formatado corretamente.")
    print("Usando cores sólidas (fallback) no lugar.")
    print("---------------\n")
    
    # Usa as cores sólidas como fallback
    head_original_img = create_fallback_surface(HEAD_SIZE, COLOR_HEAD_FALLBACK)
    body_img = create_fallback_surface(BODY_SIZE, COLOR_BODY_FALLBACK)
    food_img = create_fallback_surface(FOOD_SIZE, COLOR_FOOD_FALLBACK)


# --- 6. Função Principal do Jogo ---
def game_loop():
    running = True
    game_over = False

    # Variáveis da Cobra
    snake_head_rect = head_original_img.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    )
    snake_head_img = head_original_img
    head_position_history = []
    
    # Direção inicial
    direction_x = SNAKE_SPEED
    direction_y = 0
    current_angle = 270 

    # --- MODIFICADO: CONTROLE DE COOLDOWN DE CURVA ---
    last_turn_position = snake_head_rect.center 
    last_direction_x = direction_x
    last_direction_y = direction_y
    TURN_COOLDOWN_DISTANCE = HEAD_SIZE[0] * HEAD_P
    
    # --- NOVO: Variáveis de "Curva Pendente" ---
    pending_direction_x = None
    pending_direction_y = None
    pending_angle = None
    
    # Variáveis da Comida
    food_rect = food_img.get_rect(
        center=(random.randint(30, SCREEN_WIDTH - 30),
                random.randint(60, SCREEN_HEIGHT - 30))
    )

    # Placar
    score = 0

    while running:
        
        # --- 7. Tratamento de Eventos (Input) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                # LÓGICA PARA REINICIAR
                if game_over and event.key == pygame.K_r:
                    game_loop() # Chama a função de novo, reiniciando tudo
                
                # LÓGICA DE MOVIMENTO
                if not game_over:
                    if pending_direction_x is None: 
                        if event.key == pygame.K_UP and direction_y == 0:
                            pending_direction_x = 0
                            pending_direction_y = -SNAKE_SPEED
                            pending_angle = 0
                        
                        elif event.key == pygame.K_DOWN and direction_y == 0:
                            pending_direction_x = 0
                            pending_direction_y = SNAKE_SPEED
                            pending_angle = 180
                        
                        elif event.key == pygame.K_LEFT and direction_x == 0:
                            pending_direction_x = -SNAKE_SPEED
                            pending_direction_y = 0
                            pending_angle = 90
                        
                        elif event.key == pygame.K_RIGHT and direction_x == 0:
                            pending_direction_x = SNAKE_SPEED
                            pending_direction_y = 0
                            pending_angle = 270
        
        if not game_over:
            
            # --- NOVO: LÓGICA DE APLICAÇÃO DE CURVA ---
            if pending_direction_x is not None:
                is_u_turn = (pending_direction_x == -last_direction_x and \
                             pending_direction_y == -last_direction_y)
                
                can_turn = False

                if not is_u_turn:
                    can_turn = True
                else:
                    current_pos = pygame.math.Vector2(snake_head_rect.center)
                    last_turn_pos = pygame.math.Vector2(last_turn_position)
                    distance_since_turn = current_pos.distance_to(last_turn_pos)
                    
                    if distance_since_turn > TURN_COOLDOWN_DISTANCE:
                        can_turn = True
                
                if can_turn:
                    last_direction_x = direction_x
                    last_direction_y = direction_y
                    
                    direction_x = pending_direction_x
                    direction_y = pending_direction_y
                    current_angle = pending_angle
                    
                    last_turn_position = snake_head_rect.center
                
                pending_direction_x = None
                pending_direction_y = None
                pending_angle = None
            # --- FIM DA LÓGICA DE APLICAÇÃO DE CURVA ---


            # --- 8. Lógica de Atualização do Jogo ---

            snake_head_img = pygame.transform.rotate(head_original_img, current_angle)
            new_head_rect = snake_head_img.get_rect(center=snake_head_rect.center)
            new_head_rect.move_ip(direction_x, direction_y)
            snake_head_rect = new_head_rect

            head_position_history.insert(0, snake_head_rect.center)

            max_history_len = (score + 2) * BODY_SPACING
            if len(head_position_history) > max_history_len:
                head_position_history.pop()

            # --- 9. Lógica de Colisão ---

            # Colisão com a Comida
            if snake_head_rect.colliderect(food_rect):
                score += 1
                food_rect.center = (random.randint(30, SCREEN_WIDTH - 30),
                                    random.randint(60, SCREEN_HEIGHT - 30))

            # Colisão com a Parede
            if (snake_head_rect.left < 0 or
                snake_head_rect.right > SCREEN_WIDTH or
                snake_head_rect.top < 0 or
                snake_head_rect.bottom > SCREEN_HEIGHT):
                print("Game Over: Bateu na parede!")
                game_over = True


        # --- 10. Lógica de Desenho (Renderização) ---
        
        screen.fill(COLOR_BLACK)
        screen.blit(food_img, food_rect)

        # Desenha o Corpo
        body_rect_list = []
        for i in range(score):
            history_index = (i + 1) * BODY_SPACING
            
            if history_index < len(head_position_history):
                segment_pos = head_position_history[history_index]
                body_rect = body_img.get_rect(center=segment_pos)
                
                if not game_over:
                    body_rect_list.append(body_rect)

                screen.blit(body_img, body_rect)

        # Desenha a Cabeça
        screen.blit(snake_head_img, snake_head_rect)
        
        # Desenha o Placar
        score_text_surface = score_font.render(f"Placar: {score}", True, COLOR_WHITE)
        score_text_rect = score_text_surface.get_rect(
            center=(SCREEN_WIDTH // 2, 30)
        )
        screen.blit(score_text_surface, score_text_rect)

        # Checagem final de colisão com o corpo
        if not game_over:
            ignore_segments = int(TURN_COOLDOWN_DISTANCE / SNAKE_SPEED) + 1 
            for body_rect in body_rect_list[ignore_segments:]:
                if snake_head_rect.colliderect(body_rect):
                    print("Game Over: Bateu no próprio corpo!")
                    game_over = True
                    break 

        # --- 11. DESENHAR TELA DE GAME OVER ---
        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            game_over_surface = game_over_font.render("VOCÊ PERDEU!", True, COLOR_WHITE)
            game_over_rect = game_over_surface.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
            )
            
            restart_surface = restart_font.render("Pressione [R] para reiniciar", True, COLOR_WHITE)
            restart_rect = restart_surface.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
            )
            
            screen.blit(game_over_surface, game_over_rect)
            screen.blit(restart_surface, restart_rect)

        pygame.display.flip()
        clock.tick(FPS)

    # --- 12. Fim do Jogo ---
    pygame.quit()
    quit()

# --- Inicia o Jogo ---
if __name__ == "__main__":
    game_loop()