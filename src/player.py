# src/player.py

import pygame
from src.bullet import Bullet
from src.config import PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT
from src.sprite_manager import cargar_sprites, extraer_sprite

class Player(pygame.sprite.Sprite):
    '''
    Clase que representa al jugador en el juego.
    Nos permite controlar la nave, disparar balas y gestionar la salud, sobrecarga, impulso, escudo y potenciadores.
    Dibuja en pantalla la nave, las balas disparadas, la barra de salud, los corazones y los iconos de potenciadores.
    
    Atributos:
        x (int): Posición horizontal del jugador.
        y (int): Posición vertical del jugador.
        sprite_ship_normal (pygame.Surface): Sprite de la nave normal.
        sprite_ship_overcharge (pygame.Surface): Sprite de la nave sobrecargada.
        sprite_shield (pygame.Surface): Sprite del escudo.
        ui_icons (dict): Diccionario con los iconos de la interfaz de usuario.
        score_font (list): Lista de sprites para los dígitos del puntaje.
        image (pygame.Surface): Imagen actual del jugador.
        rect (pygame.Rect): Rectángulo que define la posición y tamaño del jugador.
        bullets (pygame.sprite.Group): Grupo de balas disparadas por el jugador.
        shoot_cooldown (int): Tiempo de recarga entre disparos.
        health (int): Puntos de vida del jugador.
        max_health (int): Puntos de vida máximos del jugador.
        shield (int): Cantidad de escudo activo.
        speed_boost (int): Cantidad de aumento de velocidad activo.
        double_shot (int): Cantidad de disparo doble activo.
        charge (int): Carga para la sobrecarga activa.
        charge_max (int): Carga máxima para la sobrecarga.
        charge_status (bool): Estado de la sobrecarga activa.
        charge_duration (int): Duración de la sobrecarga en frames.
        charge_timer (int): Temporizador para la sobrecarga.
        dash_cooldown (int): Tiempo de recarga entre dashes.
        dashing (bool): Indica si el jugador está en modo dash.
        dash_duration (int): Duración del dash en frames.
        dash_timer (int): Temporizador para el dash.
    '''
    def __init__(self, x, y):
        super().__init__()
        ship_sheet = pygame.image.load("assets/player/SpaceShips_Player-0001.png").convert_alpha()
        self.sprite_ship_normal = extraer_sprite(ship_sheet, 77, 71, 38, 40, 1.5)  # Nave normal
        self.sprite_ship_overcharge = extraer_sprite(ship_sheet, 12, 22, 38, 40, 1.5)  # Nave sobrecargada
        shield_sheet = pygame.image.load("assets/effects/Barrier-0001.png").convert_alpha()
        self.sprite_shield = extraer_sprite(shield_sheet, 15, 16, 67, 67, 1.5)
        self.ui_sheet = pygame.image.load("assets/ui/UI_sprites-0001.png").convert_alpha()
        self.ui_icons = {
            "full_health_icon": extraer_sprite(self.ui_sheet, 3, 82, 12, 10, 2.1),  # Icono de salud lleno
            "empty_health_icon": extraer_sprite(self.ui_sheet, 19, 82, 12, 10, 2.1),  # Icono de salud vacío
            "health_bar_icon": extraer_sprite(self.ui_sheet, 3, 11, 73, 20, 2.4),  # Barra de salud
            "shield_icon": extraer_sprite(self.ui_sheet, 93, 27, 22, 22, 1.5),  # Escudo
            "speed_icon": extraer_sprite(self.ui_sheet, 93, 51, 22, 22, 1.5),  # Velocidad
            "double_shot_icon": extraer_sprite(self.ui_sheet, 93, 77, 22, 22, 1.5),  # Disparo doble
            "double_points_icon": extraer_sprite(self.ui_sheet, 93, 102, 22, 22, 1.5),  # Puntos dobles
            "charge_icon": extraer_sprite(self.ui_sheet, 55, 80, 9, 13, 2.5),  # Sobre carga
            "charge_tank_full": extraer_sprite(self.ui_sheet, 16, 101, 7, 22, 2.4),  # Barra de carga llena
            "charge_tank_empty": extraer_sprite(self.ui_sheet, 26, 101, 7, 22, 2.4)  # Barra de carga vacía
        }
        self.score_font = [
            extraer_sprite(self.ui_sheet, 8, 68, 6, 6, 2.0),  # 1
            extraer_sprite(self.ui_sheet, 13, 68, 6, 6, 2.0),  # 2
            extraer_sprite(self.ui_sheet, 18, 68, 6, 6, 2.0), # 3
            extraer_sprite(self.ui_sheet, 23, 68, 6, 6, 2.0), # 4
            extraer_sprite(self.ui_sheet, 28, 68, 6, 6, 2.0), # 5
            extraer_sprite(self.ui_sheet, 33, 68, 6, 6, 2.0), # 6
            extraer_sprite(self.ui_sheet, 38, 68, 6, 6, 2.0), # 7
            extraer_sprite(self.ui_sheet, 43, 68, 6, 6, 2.0), # 8
            extraer_sprite(self.ui_sheet, 48, 68, 6, 6, 2.0), #9
            extraer_sprite(self.ui_sheet, 53, 68, 6, 6, 2.0)   #0
        ]
        self.image = self.sprite_ship_normal
        self.rect = self.image.get_rect(center=(x, y))
        self.bullets = pygame.sprite.Group()
        self.shoot_cooldown = 0
        self.health = 100  # Vida inicial
        self.max_health = 100
        self.shield = 0
        self.speed_boost = 0
        self.double_shot = 0  
        self.charge = 0 # Carga inicial para la sobrecarga
        self.charge_max = 100  # Carga máxima para la sobrecarga
        self.charge_status = False  # Estado de sobrecarga
        self.charge_duration = 60 # Duración de la sobrecarga en frames
        self.charge_timer = 0  # Temporizador para la sobrecarga
        self.dash_cooldown = 0
        self.dashing = False
        self.dash_duration = 5
        self.dash_timer = 0
        self.last_direction = pygame.Vector2(0, 0)
        self.double_points = 0

    def update(self, keys):
        '''
        Actualiza la posición del jugador, gestiona la recarga de disparos, la salud, el escudo y los potenciadores.
        Controla el movimiento del jugador según las teclas presionadas.
        
        Args:
            keys (pygame.key): Teclas presionadas en el momento de la actualización.
        '''
        speed = PLAYER_SPEED
        direction = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT]:
            direction.x = -1
        if keys[pygame.K_RIGHT]:
            direction.x = 1
        if keys[pygame.K_UP]:
            direction.y = -1
        if keys[pygame.K_DOWN]:
            direction.y = 1
        
        if direction.length_squared() != 0:
            self.last_direction = direction.normalize()

        if self.charge_status:
            speed += 2
        elif self.speed_boost > 0:
            speed += 2
            self.speed_boost -= 1
        
        if self.dashing:
            self.rect.x += int(self.last_direction.x * speed * 3)
            self.rect.y += int(self.last_direction.y * speed * 3)
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.dashing = False
        else:
            self.rect.x += int(direction.x * speed)
            self.rect.y += int(direction.y * speed)

        if self.charge_status:
            if self.charge_timer >= self.charge_duration:
                self.charge_status = False
                self.charge_timer = 0
            else:
                self.charge_timer += 1
            
        self.rect.clamp_ip(pygame.Rect(0, 0, 480, 670))

        if self.dash_cooldown > 0:
            if self.charge_status:
                self.dash_cooldown -= 4
            else:
                self.dash_cooldown -= 1

            if self.dash_cooldown < 0:
                self.dash_cooldown = 0

        if self.shoot_cooldown > 0:
            if self.charge_status:
                self.shoot_cooldown -= 6  # O incluso -3 si querés que dispare muy rápido
            else:
                self.shoot_cooldown -= 1

            if self.shoot_cooldown < 0:
                self.shoot_cooldown = 0

        if self.shield > 0:
            self.shield -= 1

        if self.charge_status:
            self.image = self.sprite_ship_overcharge # Cambia el color durante la sobrecarga
        else:
            self.image = self.sprite_ship_normal  # Vuelve al color normal

        if self.double_shot > 0:
            self.double_shot-= 1

        if self.double_points >= 0:
            self.double_points -= 1
        
    def shoot(self):
        '''
        Dispara una bala desde la posición del jugador.
        Si el jugador tiene el disparo doble o está en estado de sobrecarga, dispara dos balas en paralelo.
        Si el jugador tiene ambos potenciadores, dispara tres balas en paralelo.
        Si el jugador no tiene potenciadores, dispara una sola bala.
        La recarga de disparo se gestiona con un cooldown.
        Si el cooldown de disparo es mayor a 0, no se puede disparar.
        '''
        if self.shoot_cooldown == 0:
            if self.double_shot > 0 and self.charge_status:
                # Disparo doble: dos balas en paralelo
                bullet1 = Bullet(self.rect.centerx - 10, self.rect.top)
                bullet2 = Bullet(self.rect.centerx + 10, self.rect.top)
                bullet3 = Bullet(self.rect.centerx, self.rect.top)
                self.bullets.add(bullet1, bullet2, bullet3)
            elif self.double_shot > 0 or self.charge_status:
                # Disparo doble: dos balas en paralelo
                bullet1 = Bullet(self.rect.centerx - 10, self.rect.top)
                bullet2 = Bullet(self.rect.centerx + 10, self.rect.top)
                self.bullets.add(bullet1, bullet2)
            else:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                self.bullets.add(bullet)

            self.shoot_cooldown = 10

    def draw(self, surface):
        '''
        Dibuja al jugador y sus balas en la superficie proporcionada.
        Args:
            surface (pygame.Surface): Superficie donde se dibuja el jugador y sus balas.
        '''
        surface.blit(self.image, self.rect)
        self.bullets.draw(surface)

    def update_bullets(self):
        '''
        Actualiza las balas disparadas por el jugador.
        '''
        self.bullets.update()

    def draw_hearts(self, surface):
        '''
        Dibuja los corazones que representan la salud del jugador en la superficie proporcionada.
        Args:
            surface (pygame.Surface): Superficie donde se dibujan los corazones.
        '''
        heart_width = self.ui_icons["full_health_icon"].get_width()  # Ancho de un corazón
        spacing = 5  # Espacio entre corazones
        max_hearts = self.max_health // 20  # Ejemplo: 5 corazones si max_health = 100

        for i in range(max_hearts):
            x_pos = 45 + i * (heart_width + spacing)  # Posición horizontal
            # Dibuja corazón lleno o vacío según la vida restante
            if self.health >= (i + 1) * 20:  # Si tiene vida para este corazón
                surface.blit(self.ui_icons["full_health_icon"], (x_pos, 5))
            else:
                surface.blit(self.ui_icons["empty_health_icon"], (x_pos, 5))
        
    def draw_health_bar(self, surface):
        '''
        Dibuja la barra de salud del jugador en la superficie proporcionada.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibuja la barra de salud.
        '''
        surface.blit(self.ui_icons["health_bar_icon"], (2, 5))
    
    def draw_charge_bar(self, surface):
        '''
        Dibuja la barra de carga del jugador en la superficie proporcionada.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibuja la barra de carga.
        '''
        if self.charge == self.charge_max:
            surface.blit(self.ui_icons["charge_tank_full"], (10, SCREEN_HEIGHT - 65))
        else:
            surface.blit(self.ui_icons["charge_tank_empty"], (10, SCREEN_HEIGHT - 65))
    
    def draw_score(self, surface, score):
        '''
        Dibuja el puntaje del jugador en la superficie proporcionada.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibuja el puntaje.
            score (int): Puntaje actual del jugador.
        '''
        # Si el puntaje es negativo, se pone en 0
        if score < 0:
            score = 0
        score_str = str(score)  # Convierte el puntaje a string ("100")
        x_pos = 90  # Posición inicial (ajusta según necesites)
        y_pos = 40

        for digit in score_str:
            if digit.isdigit():
                if digit == '0':
                    digit_index = 9
                else:
                    digit_index = int(digit) - 1
                surface.blit(self.score_font[digit_index], (x_pos, y_pos))
                x_pos += self.score_font[digit_index].get_width() + 2
    
    def dash(self):
        '''
        Inicia el dash del jugador si no está en cooldown.
        El dash permite al jugador moverse rápidamente en la dirección actual.
        Si el cooldown de dash es mayor a 0, no se puede iniciar un nuevo dash.
        '''
        if self.dash_cooldown == 0:
            self.dashing = True
            self.dash_timer = self.dash_duration
            self.dash_cooldown = 30  # Frames de cooldown (~0.5s)
            
    def draw_powerup_icons(self, surface):
        '''
        Dibuja los iconos de los potenciadores activos del jugador en la superficie proporcionada.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujan los iconos de potenciadores.
        '''
        x_base = SCREEN_WIDTH - 30  # esquina derecha
        y = 10

        if self.double_shot > 0:
            icon = self.ui_icons["double_shot_icon"]
            surface.blit(icon, (x_base, y))
            y += 50

        if self.shield > 0:
            icon = self.ui_icons["shield_icon"]
            surface.blit(icon, (x_base, y))
            y += 50
            # Dibuja el sprite del escudo encima del jugador
            surface.blit(self.sprite_shield, (self.rect.centerx - self.sprite_shield.get_width() // 2, self.rect.centery - self.sprite_shield.get_height() // 2))

        if self.speed_boost > 0:
            icon = self.ui_icons["speed_icon"]
            surface.blit(icon, (x_base, y))
            y += 50
        
        if self.charge_status:
            icon = self.ui_icons["charge_icon"]
            surface.blit(icon, (x_base, y))
            y += 50
            
        if self.double_points > 0:
            icon = self.ui_icons["double_points_icon"]
            surface.blit(icon, (x_base, y))
            y += 50