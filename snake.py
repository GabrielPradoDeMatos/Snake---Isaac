# snake.py
# Classe que representa a Cobra lá ele

import pygame
from settings import *

class Snake:
    #Para iniciar a cobra é necessário passar a textura da cabeca e do corpo
    def __init__(self, head_img, body_img):
        #Deixar a textura no tamanho da cabeca, que esta definido no arquivo settings.py
        #original_head_img será usada para fazer a rotacão da cabeca pois, ao rotacionar uma surface ,já rotacionada, a qualidade da imagem diminui.
        self.original_head_img = pygame.transform.scale(head_img, HEAD_SIZE)
        self.body_img = pygame.transform.scale(body_img, BODY_SIZE)
        self.head_img = self.original_head_img

        self.rect = self.head_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.position_history = []
        self.body_rects = []
        
        #Vetores de direcão. No pygame o eixo Y é ao contrário e o 0° é no lugar do 90°, (0=Cima, 90=Esquerda, 180=Baixo, 270=Direita)
        self.DIR_RIGHT = pygame.math.Vector2(SNAKE_SPEED, 0)
        self.DIR_LEFT = pygame.math.Vector2(-SNAKE_SPEED, 0)
        self.DIR_UP = pygame.math.Vector2(0, -SNAKE_SPEED)
        self.DIR_DOWN = pygame.math.Vector2(0, SNAKE_SPEED)
        
        #Início da cobra
        self.direction = self.DIR_RIGHT
        self.angle = 0
        self.flip = (False, False)
        
        #---------------------------------------------------------------------------------------------------------------
        #Ao fazer uma curva muito fechada a cabeca da cobra bate no corpo, por esse motivo
        #será necessário implementar uma trava para que seja impossível fazer curvas muito fechadas.
        
        self.pending_direction = None
        self.pending_angle = None
        self.pending_flip = (False, False)
        self.last_turn_position = self.rect.center
        self.last_direction = self.direction.copy()
        self.turn_cooldown_distance = HEAD_SIZE[0] * HEAD_P
        #---------------------------------------------------------------------------------------------------------------
       
        self.score = 0
   
    #Verificar teclas pressionadas
    def handle_input(self, event):        
        if event.type != pygame.KEYDOWN:
            return
           
        #Não permite registrar uma nova intencão se já houver uma
        if self.pending_direction is None:
            #Bloquear inversão da direcão exemplo: cobra andando para baixo e aperto para cima ou cobra indo para direita e aperto para esquerda)
            if event.key == pygame.K_UP and self.direction != self.DIR_DOWN:
                self.pending_direction = self.DIR_UP
                self.pending_angle = 0
                self.pending_flip = (False, False)
            
            elif event.key == pygame.K_DOWN and self.direction != self.DIR_UP:
                self.pending_direction = self.DIR_DOWN
                self.pending_angle = 180
                self.pending_flip = (False, False)
            
            elif event.key == pygame.K_LEFT and self.direction != self.DIR_RIGHT:
                self.pending_direction = self.DIR_LEFT
                self.pending_angle = 0
                self.pending_flip = (True, False)
            
            elif event.key == pygame.K_RIGHT and self.direction != self.DIR_LEFT:
                self.pending_direction = self.DIR_RIGHT
                self.pending_angle = 0
                self.pending_flip = (False, False)

    def _apply_turn(self):
        
        if self.pending_direction is None:
            return

        #---------------------------------------------------------------------------------------------------------------
        #Ao fazer uma curva muito fechada a cabeca da cobra bate no corpo, por esse motivo
        #será necessário implementar uma trava para que seja impossível fazer curvas muito fechadas.
        #exemplo: cobra indo para direita, pressiona para cima e depois esquerda
        # Verifica se é uma "curva em U" (180 graus)
        is_u_turn = (self.pending_direction == -self.last_direction)
        
        can_turn = False
        if not is_u_turn:
            #Curva que não é fechada
            can_turn = True
        else:
            #Curva em U só é permitida após o cooldown de distância, ou seja, após a cabeca virar por completo
            current_pos = pygame.math.Vector2(self.rect.center)
            last_turn_pos = pygame.math.Vector2(self.last_turn_position)
            distance_since_turn = current_pos.distance_to(last_turn_pos)
            
            if distance_since_turn > self.turn_cooldown_distance:
                can_turn = True
        
        if can_turn:
            self.last_direction = self.direction.copy()
            self.direction = self.pending_direction
            self.angle = self.pending_angle
            self.flip = self.pending_flip
            self.last_turn_position = self.rect.center
        
        #Limpar o comando de virar mesmo que ele não tenha sido executado
        self.pending_direction = None
        self.pending_angle = None
        self.pending_flip = (False,False)
             
    def update(self):

        self._apply_turn()

        # 2. Rotaciona a cabeça e move
        self.head_img = pygame.transform.flip(self.original_head_img, *self.flip)
        self.head_img = pygame.transform.rotate(self.head_img, self.angle)
        
        new_head_rect = self.head_img.get_rect(center=self.rect.center)
        new_head_rect.move_ip(self.direction)
        self.rect = new_head_rect

        # 3. Adiciona a posição central ao histórico
        self.position_history.insert(0, self.rect.center)

        # 4. Limita o tamanho do histórico com base no placar
        max_history_len = (self.score + 2) * BODY_SPACING
        if len(self.position_history) > max_history_len:
            self.position_history.pop()
            
        # 5. (IMPORTANTE) Atualiza a lista de rects do corpo para colisões
        self._update_body_rects()
        


    def grow(self):
        """Aumenta o placar (e consequentemente o corpo)."""
        self.score += 1



    def _update_body_rects(self):
        """Cria os rects do corpo com base no histórico (para colisão)."""
        self.body_rects.clear()
        for i in range(self.score):
            history_index = (i + 1) * BODY_SPACING
            if history_index < len(self.position_history):
                segment_pos = self.position_history[history_index]
                body_rect = self.body_img.get_rect(center=segment_pos)
                self.body_rects.append(body_rect)

    def draw_body(self, surface):
        """Desenha apenas o corpo na tela (usando os rects já calculados)."""
        for rect in self.body_rects:
            surface.blit(self.body_img, rect)

    def draw_head(self, surface):
        """Desenha apenas a cabeça na tela (por cima do corpo)."""
        surface.blit(self.head_img, self.rect)

    def check_collision_food(self, food_rect):
        """Verifica colisão com a comida."""
        if self.rect.colliderect(food_rect):
            self.grow()
            return True
        return False

    def check_collision_wall(self):
        """Verifica colisão com as paredes."""
        return (self.rect.left < 0 or
                self.rect.right > SCREEN_WIDTH or
                self.rect.top < 0 or
                self.rect.bottom > SCREEN_HEIGHT)

    def check_collision_self(self):
        """Verifica colisão com o próprio corpo."""
        # Pula os primeiros segmentos (para não colidir com o "pescoço")
        ignore_segments = int(self.turn_cooldown_distance / SNAKE_SPEED) + 1 
        
        # Itera sobre os rects do corpo (exceto o pescoço)
        for body_rect in self.body_rects[ignore_segments:]:
            if self.rect.colliderect(body_rect):
                return True
        return False