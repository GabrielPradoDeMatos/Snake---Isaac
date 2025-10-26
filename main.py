import pygame
import sys
import os
import json

from settings import *
from spritesheet import Spritesheet
from snake import Snake
from food import Food

class Game:
    def __init__(self):
        
        pygame.init()
        pygame.font.init()
        
        #Criar a tela,onde o jogo sera executado, do tamnho definido
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake - Isaac")
        self.clock = pygame.time.Clock()

        #Carregar as texturas, caso as texturas nao sejam carregadas elas serão subistituidas por cores sólidas, que estão definidas no arquivo settings.py
        self._load_assets()
        self._create_fonts()
        
        self.game_state = "playing"

        #Cria os objetos do jogo
        self._start_new_game()
        
    #Loop principal
    def run(self):        
        while True:
            # 1. Processar Eventos (Input)
            self._handle_events()
            
            # 2. Atualizar Lógica do Jogo
            self._update()
            
            # 3. Desenhar na Tela
            self._draw()
            
            # 4. Controlar FPS
            self.clock.tick(FPS)
            
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()            
            #Passar a captura de eventos, do loop principal, para o objeto da cobra
            if self.game_state == "playing":
                self.snake.handle_input(event)
                
            elif self.game_state == "game_over":
                # Se for game over, procura pela tecla 'R'
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self._start_new_game()

    def _quit_game(self):
        print("Encerrando o jogo...")
        pygame.quit()
        quit()             

    def _load_assets(self):
        full_spritesheet_path = os.path.join(ASSET_PATH, SPRITESHEET_FILENAME)
        
        try:
            print(f"Carregando spritesheet de: {full_spritesheet_path}")
            my_spritesheet = Spritesheet(full_spritesheet_path)
            
            print("Extraindo sprites: 'cabeca', 'corpo', 'comida'...")
            #Carrega as imagens originais
            self.head_img_original = my_spritesheet.parse_sprite('head')
            self.body_img_original = my_spritesheet.parse_sprite('body')
            self.food_img_original = my_spritesheet.parse_sprite('food')
            
            print("Sprites carregadas com sucesso! :^}")

        except (pygame.error, FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"\n--- Erro! ---")
            print(f"Erro: Não foi possível carregar as texturas: {e}")
            print("O jogo será carregado com texturas sólidas :^| .")
            print("-------------------------------------------------\n")
            
            # Usa as cores sólidas como fallback
            self.head_img_original = self._create_fallback_surface(HEAD_SIZE, COLOR_HEAD_FALLBACK)
            self.body_img_original = self._create_fallback_surface(BODY_SIZE, COLOR_BODY_FALLBACK)
            self.food_img_original = self._create_fallback_surface(FOOD_SIZE, COLOR_FOOD_FALLBACK)

    def _create_fallback_surface(self, size, color):
        surface = pygame.Surface(size)
        surface.fill(color)
        return surface
    
    def _create_fonts(self):
        #Carrega fontes do jogo (se der tempo vou adicionar as fontes do Isaac, por enquanto usar fontes padrão do pygame)
        self.score_font = pygame.font.Font(None, 50)
        self.game_over_font = pygame.font.Font(None, 75)
        self.restart_font = pygame.font.Font(None, 40)

    def _start_new_game(self):
        #Cria/Reseta os objetos Snake e Food para um novo jogo.
        print("Iniciando novo jogo...")
        self.game_state = "playing"
        self.snake = Snake(self.head_img_original, self.body_img_original)
        self.food = Food(self.food_img_original)





    def _update(self):       
        if self.game_state != "playing":
            return
            
        self.snake.update()
        
        # Verifica colisão da cobra com a comida
        if self.snake.check_collision_food(self.food.rect):
            self.food.respawn() # Se comer, a comida muda de lugar
            
        # Verifica colisões de fim de jogo
        if self.snake.check_collision_wall() or self.snake.check_collision_self():
            print("Game Over: Colisão detectada!")
            self.game_state = "game_over"

    def _draw(self):    
        # 1. Limpa a tela
        self.screen.fill(COLOR_BLACK)
        
        # 2. Desenha os objetos
        self.food.draw(self.screen)
        self.snake.draw_body(self.screen)
        self.snake.draw_head(self.screen) # Cabeça por cima do corpo
        
        # 3. Desenha a UI (Placar)
        self._draw_score()
        
        # 4. Desenha a tela de Game Over (se aplicável)
        if self.game_state == "game_over":
            self._draw_game_over_overlay()

        # 5. Atualiza o display
        pygame.display.flip()

    def _draw_score(self):
        """Desenha o placar no topo da tela."""
        score_text = f"Placar: {self.snake.score}"
        score_surf = self.score_font.render(score_text, True, COLOR_WHITE)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(score_surf, score_rect)

    def _draw_game_over_overlay(self):
        """Desenha a tela de "VOCÊ PERDEU"."""
        # Overlay escuro
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) # Preto semi-transparente
        self.screen.blit(overlay, (0, 0))
        
        # Textos
        go_surf = self.game_over_font.render("VOCÊ PERDEU!", True, COLOR_WHITE)
        go_rect = go_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        
        restart_surf = self.restart_font.render("Pressione [R] para reiniciar", True, COLOR_WHITE)
        restart_rect = restart_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        
        self.screen.blit(go_surf, go_rect)
        self.screen.blit(restart_surf, restart_rect)




# --- Ponto de Entrada do Programa ---
if __name__ == "__main__":
    # 1. Cria uma instância do Jogo
    game = Game()
    # 2. Inicia o loop principal
    game.run()