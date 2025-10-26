# Classe que representa o coco da cobra
# Se sobrar tempo implementar a funcao de seed
import pygame
import random

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FOOD_SIZE

#Para iniciar a comida é necessário passar a textura da comida
class Food:
    def __init__(self, image):

        self.image = pygame.transform.scale(image, FOOD_SIZE)
        self.rect = self.image.get_rect()
        
        self.respawn()

    #Gera a comida em um lugar aleatório no mapa
    def respawn(self):
        #A comida não deve aparecer nas bordas do mapa
        margin_x = 30
        margin_y = 60 # Margem maior no topo para o placar
        
        rand_x = random.randint(margin_x, SCREEN_WIDTH - margin_x)
        rand_y = random.randint(margin_y, SCREEN_HEIGHT - margin_x)
        self.rect.center = (rand_x, rand_y)

    #Desenha a comida na tela
    def draw(self, surface):  
                     
        surface.blit(self.image, self.rect)