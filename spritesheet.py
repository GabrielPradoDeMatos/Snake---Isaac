# spritesheet.py
# Classe responsável por carregar e analisar a spritesheet.
#Atributo sprite_sheet armazena a imagem completa do arquivo snake_sprites, depois tem que quebrar pra pegar individual

import pygame
import json
import os

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        try:
            #convert_alpha : otimiza a imagem para o formato da tela e preserva a transparencia
            self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Erro ao carregar a imagem da spritesheet: {filename}")
            raise e
        #Pegar os dados do arquivo JSON para mapear as texturas
        self.meta_data = self.filename.replace('.png', '.json')
        try:
            with open(self.meta_data) as f:
                #Atributo data recebe um dicionário de dicionários com as informacoes do JSON
                self.data = json.load(f)
        except FileNotFoundError:
            print(f"Erro: Não foi encontrado o arquivo JSON: {self.meta_data}")
            raise
        except json.JSONDecodeError:
            print(f"Erro: O arquivo JSON não está em um formato adequado: {self.meta_data}")
            raise

    def parse_sprite(self, name):
        try:
            #Recebe um dicionario com as informacoes, x,y,w,h da sprite solicitada         
            sprite_data = self.data['frames'][name]['frame']
            x, y, w, h = sprite_data["x"], sprite_data["y"], sprite_data["w"], sprite_data["h"]
            #Agora, possuindo a localizacao da sprite solicitada posso extrair a imagem
            image = self.get_sprite(x, y, w, h)
            return image
        except KeyError:
            print(f"Erro: Sprite com o nome '{name}' não encontrado no JSON ({self.meta_data}).")
            raise

    def get_sprite(self, x, y, w, h):
        #Cria uma surface que suporta transparência
        sprite = pygame.Surface((w, h), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite