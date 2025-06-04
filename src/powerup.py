# src/powerup.py

import pygame
import random

from src.config import POWERUP_TYPES
from src.sprite_manager import cargar_sprites, animar_sprites

class PowerUp(pygame.sprite.Sprite):
    ''' 
    Clase que representa un potenciador en el juego.
    
    Atributos:
        x (int): Posición horizontal del potenciador.
        y (int): Posición vertical del potenciador.
        tipo (str): Tipo de potenciador, elegido aleatoriamente de POWERUP_TYPES.
        '''
    def __init__(self, x, y):
        super().__init__()
        self.tipo = random.choice(POWERUP_TYPES)

        sprites_list = cargar_sprites("assets/powerups/Bonuses-0001.png", 5, 5, 1.6)
        sprite_health = [sprites_list[0], sprites_list[5], sprites_list[10], sprites_list[15], sprites_list[20]]
        sprite_shield = [sprites_list[1], sprites_list[6], sprites_list[11], sprites_list[16], sprites_list[21]]
        sprite_speed = [sprites_list[2], sprites_list[7], sprites_list[12], sprites_list[17], sprites_list[22]]
        sprite_shoot = [sprites_list[3], sprites_list[8], sprites_list[13], sprites_list[18], sprites_list[23]]
        sprite_double_points = [sprites_list[4], sprites_list[9], sprites_list[14], sprites_list[19], sprites_list[24]]
        
        self.animation = {
            "health": animar_sprites(sprite_health, 1),
            "shoot": animar_sprites(sprite_shoot, 1),
            "speed": animar_sprites(sprite_speed, 1),
            "shield": animar_sprites(sprite_shield, 1),
            "double_points": animar_sprites(sprite_double_points, 1)
        }
        
        self.current_frame = 0
        self.animation_speed = 0.1  # Adjust for speed
        self.image = self.animation[self.tipo][self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2
        self.last_update = pygame.time.get_ticks()

    def update(self, time_factor=1.0):
        '''
        Actualiza la posición del potenciador y su animación.
        Si el potenciador sale de la pantalla, se elimina.
        
        Args:
            time_factor (float): Factor de tiempo para ajustar la velocidad de movimiento.
        '''
        # Animation update
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:  # Change frame every 100ms
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animation[self.tipo])
            self.image = self.animation[self.tipo][self.current_frame]
        
        # Movement
        self.rect.y += int(self.speed * time_factor)
        if self.rect.top > 670:
            self.kill()