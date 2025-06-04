import pygame
import random
import math
from src.config import SCREEN_WIDTH
from src.enemy_bullet import EnemyBullet
from src.sprite_manager import extraer_sprite

class Enemy(pygame.sprite.Sprite):
    '''
    Clase que representa un enemigo en el juego.
    
    Atributos:
        vida (int): Puntos de vida del enemigo.
        speed (int): Velocidad de movimiento del enemigo.
        tipo_movimiento (str): Tipo de movimiento del enemigo ("vertical", "zigzag", "lento", "salto").
        tipo_disparo (str): Tipo de disparo del enemigo ("directo", "abanico", "random", "sine", "mine").
        image (pygame.Surface): Imagen del enemigo.
        rect (pygame.Rect): Rectángulo que define la posición y tamaño del enemigo.
        shoot_timer (int): Temporizador para controlar el tiempo entre disparos.
        cooldown_disparo (int): Tiempo de recarga entre disparos.
    '''
    def __init__(self):
        super().__init__()

        # Posición horizontal aleatoria
        x = random.randint(20, SCREEN_WIDTH - 20)

        # Cargar los sprites del sheet SOLO una vez
        if not hasattr(Enemy, "sprites1"):
            sheet = pygame.image.load("assets/enemy/SpaceShips_Enemy-0001.png").convert_alpha()
            Enemy.sprites1 = [
                extraer_sprite(sheet, 32, 9, 48, 54, 1.5),
                extraer_sprite(sheet, 32, 99, 48, 54, 1.5),
                extraer_sprite(sheet, 32, 186, 48, 54, 1.5),
                extraer_sprite(sheet, 91, 17, 46, 35, 1.5),
                extraer_sprite(sheet, 91, 106, 46, 35, 1.5),
                extraer_sprite(sheet, 91, 193, 46, 35, 1.5),
                extraer_sprite(sheet, 149, 24, 32, 20, 1.5),
                extraer_sprite(sheet, 149, 113, 32, 20, 1.5),
                extraer_sprite(sheet, 149, 200, 32, 20, 1.5),
                extraer_sprite(sheet, 198, 27, 21, 18, 2),
                extraer_sprite(sheet, 198, 115, 21, 18, 2),
                extraer_sprite(sheet, 198, 202, 21, 18, 2)
            ]
            
        # Comportamiento aleatorio según tipo
        enemy_type = random.choice(["normal", "torreta", "tanque", "rapido"])

        if enemy_type == "torreta":
            self.vida = 30
            self.speed = 0
            self.tipo_movimiento = "vertical"
            self.tipo_disparo = random.choice(["sine", "abanico"])
            self.image = random.choice(Enemy.sprites1[0:3] )
        elif enemy_type == "tanque":
            self.vida = 50
            self.speed = 1
            self.tipo_movimiento = "lento"
            self.tipo_disparo = "random"
            self.image = random.choice(Enemy.sprites1[3:5])
        elif enemy_type == "rapido":
            self.vida = 10
            self.speed = 4
            self.tipo_movimiento = "zigzag"
            self.tipo_disparo = "mine"
            self.image = random.choice(Enemy.sprites1[5:8])
        else:
            self.vida = 20
            self.speed = 2
            self.tipo_movimiento = random.choice(["vertical", "zigzag"])
            self.tipo_disparo = "directo"
            self.image = random.choice(Enemy.sprites1[8:12])

        self.rect = self.image.get_rect(midtop=(x, -30))
        
        # Timers de disparo
        self.shoot_timer = random.randint(0, 30)
        self.cooldown_disparo = random.randint(60, 90)

    def shoot(self, player, group_global):
        '''
        Dispara balas hacia el jugador según el tipo de disparo.
        
        Args:
            player (Player): Referencia al jugador para calcular la dirección del disparo.
            group_global (pygame.sprite.Group): Grupo global donde se añadirán las balas.
        '''
        if self.tipo_disparo == "directo":
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            angle = math.degrees(math.atan2(dy, dx))
            group_global.add(EnemyBullet(self.rect.centerx, self.rect.bottom, angle, owner=self))

        elif self.tipo_disparo == "abanico":
            for offset in [-30, -15, 0, 15, 30]:
                group_global.add(EnemyBullet(self.rect.centerx, self.rect.bottom, 90 + offset, owner=self))

        elif self.tipo_disparo == "random":
            for _ in range(3):
                angle = random.randint(60, 120)
                group_global.add(EnemyBullet(self.rect.centerx, self.rect.bottom, angle, owner=self))
        
        elif self.tipo_disparo == "sine":
            self.shoot_sine_wave(group_global)
            
        elif self.tipo_disparo == "mine":
            self.shoot_mines(group_global)
    
    def update(self, player, time_factor=1.0, group_global = None):
        '''
        Actualiza la posición del enemigo y maneja el disparo.
        Mueve al enemigo hacia abajo a una velocidad constante y dispara balas
        hacia el jugador según el tipo de disparo.
        
        Args:
            player (Player): Referencia al jugador para calcular la dirección del disparo.
            time_factor (float): Factor de tiempo para ajustar la velocidad del enemigo.
            group_global (pygame.sprite.Group): Grupo global donde se añadirán las balas.
        '''
        self.rect.y += int(self.speed * time_factor)
        if self.rect.top > 670:  # Fuera de pantalla
            self.kill()
        if self.rect.top < 0:  # Si está por encima de la pantalla
            self.rect.y += 3
            return
        if self.rect.top >= 0:
            self.shoot_timer += 1
            if self.shoot_timer >= self.cooldown_disparo:  # Cada 1.5 seg
                self.shoot(player, group_global)  # Asume que pasas el jugador
                self.shoot_timer = 0
        
        if self.tipo_movimiento == "vertical":
            self.rect.y += int(self.speed * time_factor)

        elif self.tipo_movimiento == "zigzag":
            self.rect.y += int(self.speed * time_factor)
            self.rect.x += int(3 * math.sin(pygame.time.get_ticks() / 200))

        elif self.tipo_movimiento == "lento":
            self.rect.y += int((self.speed / 2) * time_factor)

        elif self.tipo_movimiento == "salto":
            self.rect.y += int((self.speed + 2 * abs(math.sin(pygame.time.get_ticks() / 300))) * time_factor)
    
    def hit(self, damage):
        '''
        Maneja el daño recibido por el enemigo.
        Si la vida del enemigo llega a 0 o menos, lo elimina.
        
        Args:
            damage (int): Cantidad de daño recibido.
        '''
        self.vida -= damage
        if self.vida <= 0:
            self.kill()
    
    def shoot_sine_wave(self, group_global):
        ''' 
        Dispara balas en una onda sinusoidal.
        Crea balas en posiciones horizontales separadas y las dispara hacia arriba. 
        Cada bala tiene un ángulo calculado basado en su posición horizontal.
        
        Args:
            group_global (pygame.sprite.Group): Grupo global donde se añadirán las balas.
        '''
        base_y = self.rect.bottom
        for x_offset in range(-80, 81, 40):  # Menos balas, más separación
            angle = math.degrees(math.atan2(1, x_offset / 50))
            group_global.add(EnemyBullet(
                self.rect.centerx + x_offset,
                base_y,
                angle,
                owner=self
            ))

    def shoot_mines(self, group_global):
        '''
        Dispara una mina en la posición del enemigo.
        Crea una bala que se comporta como una mina, flotando en su lugar
        y explotando después de un tiempo.
        
        Args:
            group_global (pygame.sprite.Group): Grupo global donde se añadirá la mina.
        '''
        mine = EnemyBullet(
            self.rect.centerx,
            self.rect.bottom,
            90,
            speed=2,
            is_mine=True,
            owner=self
        )
        mine.is_mine = True
        group_global.add(mine)