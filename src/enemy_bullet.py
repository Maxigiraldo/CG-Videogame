import pygame
import math
import random
from src.sprite_manager import extraer_sprite

class EnemyBullet(pygame.sprite.Sprite):
    ''' 
    Clase que representa una bala disparada por un enemigo.
    
    Atributos:
        x (int): Posición horizontal de la bala.
        y (int): Posición vertical de la bala.
        angle_deg (float): Ángulo de disparo en grados.
        speed (int): Velocidad de la bala.
        is_mine (bool): Indica si es una mina o una bala normal.
        owner: Referencia al enemigo que disparó esta bala.
    '''
    def __init__(self, x, y, angle_deg, speed=4, is_mine=False, owner=None):
        super().__init__()
        self.bullet_sheet = pygame.image.load("assets/bullet/Bullets-0001.png").convert_alpha()
        bullets_sprites = [
            extraer_sprite(self.bullet_sheet, 84, 144, 8, 15, 1.5),  # Bullet sprite
            extraer_sprite(self.bullet_sheet, 16, 79, 17, 22, 1.5),   # Alternate bullet sprite
        ]
        if is_mine:
            self.image = bullets_sprites[1]  # Use alternate sprite for mine
        else:
            self.image = bullets_sprites[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = math.radians(angle_deg)
        self.speed = speed
        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed
        self.is_mine = is_mine
        self.mine_timer = 0
        self.owner = owner  # Guarda referencia al enemigo que disparó

    def update(self):
        '''
        Actualiza la posición de la bala.
        Si es una mina, flota en el lugar y explota después de 3 segundos.
        '''
        if self.is_mine:
            self.mine_timer += 1
            if self.mine_timer > 180:  # Explota después de 3 segundos
                self.explode()
                self.kill()
            else:
                # Flota en el lugar
                self.rect.y += math.sin(pygame.time.get_ticks() / 500) * 0.5
        else:
            # Comportamiento normal
            self.rect.x += self.vel_x
            self.rect.y += self.vel_y
        
        # Usar los valores reales de pantalla
        SCREEN_WIDTH = 480
        SCREEN_HEIGHT = 670
        # Eliminar la bala solo si está completamente fuera de la pantalla
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()
    
    def explode(self):
        '''
        Crea nuevas balas en todas direcciones al explotar.
        Si es una mina, crea 8 balas en ángulos de 45 grados.
        '''
        # Crea 8 balas en todas direcciones al explotar
        for angle in range(0, 360, 45):
            new_bullet = EnemyBullet(
                self.rect.centerx,
                self.rect.centery,
                angle,
                speed=3,
                owner=self.owner
            )
            self.groups()[0].add(new_bullet)  # Añade al mismo grupo