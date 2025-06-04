# src/bullet.py

import pygame
from src.config import BULLET_SPEED
from src.sprite_manager import extraer_sprite

class Bullet(pygame.sprite.Sprite):
    '''
    Clase que representa una bala disparada por el jugador.
    
    Atributos:
        x (int): Posición horizontal de la bala.
        y (int): Posición vertical de la bala.
    '''
    def __init__(self, x, y):
        super().__init__()
        self.bullet_sheet = pygame.image.load("assets/bullet/Bullets-0001.png").convert_alpha()
        self.image = extraer_sprite(self.bullet_sheet, 148, 111, 6, 19, 1.5)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        '''
        Actualiza la posición de la bala.
        Mueve la bala hacia arriba a una velocidad constante definida por BULLET_SPEED.
        Si la bala sale de la pantalla por la parte superior, se elimina.
        '''
        self.rect.y += BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()
