import pygame
import random
import math
from src.sprite_manager import extraer_sprite

class Boss(pygame.sprite.Sprite):
    '''
    Clase para los jefes del juego por fase.
    Esta clase maneja la lógica de movimiento, disparo y daño del jefe.
    Se encarga de crear y gestionar las balas disparadas por el jefe.
    Además, implementa diferentes patrones de ataque como espiral, anillo y bola cargada.
    También maneja la entrada del jefe desde la parte superior de la pantalla.
    
    Atributos:
        image (pygame.Surface): Imagen del jefe.
        rect (pygame.Rect): Rectángulo que define la posición y tamaño del jefe.
        health (int): Salud del jefe.
        speed (int): Velocidad de movimiento del jefe.
        direction (int): Dirección de movimiento del jefe (-1 o 1).
        bullets (pygame.sprite.Group): Grupo de balas disparadas por el jefe.
        shoot_timer (int): Temporizador para controlar el tiempo entre disparos.
        entrando (bool): Indica si el jefe está entrando en la pantalla.
    '''
    def __init__(self):
        '''
        Inicializa el jefe con sus sprites, posición inicial y atributos básicos.
        Carga las imágenes de los sprites del jefe y las balas.
        Configura la posición inicial del jefe para que entre desde la parte superior de la pantalla.
        '''
        super().__init__()
        sheet = pygame.image.load("assets/boss/SpaceShip_Boss-0001.png").convert_alpha()
        bullets_sprites = pygame.image.load("assets/bullet/Bullets-0001.png").convert_alpha()
        boss_sprites_1 = [
            extraer_sprite(sheet, 3, 36, 105, 105, 1.5), 
            extraer_sprite(sheet, 3, 157, 105, 105, 1.5), 
            extraer_sprite(sheet, 3, 288, 105, 105, 1.5),
            
        ]
        boss_sprites_2 = [
            extraer_sprite(sheet, 138, 36, 105, 105, 1.5), 
            extraer_sprite(sheet, 138, 157, 105, 105, 1.5), 
            extraer_sprite(sheet, 138, 288, 105, 105, 1.5),
        ]
        
        self.bullets_sprites = [
            extraer_sprite(bullets_sprites, 16, 80, 17, 22, 1.5),  # Bullet sprite
            extraer_sprite(bullets_sprites, 16, 16, 17, 22, 1.5),   # Alternate bullet sprite
        ]
        
        self.image = random.choice(boss_sprites_1)
        self.rect = self.image.get_rect(midtop=(240, -100))  # Entra desde arriba
        self.health = 1500
        self.speed = 3
        self.direction = 1
        self.bullets = pygame.sprite.Group()
        self.shoot_timer = 0
        self.entrando = True

    def update(self, time_factor=1.0):
        '''
        Actualiza la posición del jefe y maneja el disparo de balas.
        Si el jefe está entrando, se mueve hacia abajo hasta alcanzar una posición específica.
        Una vez que ha entrado, se mueve horizontalmente y dispara balas según un patrón aleatorio.
        
        Args:
            time_factor (float): Factor de tiempo para ajustar la velocidad de movimiento y disparo.
        '''
        if self.entrando:
            self.rect.y += 1
            if self.rect.top >= 50:
                self.entrando = False
        else:
            self.rect.x += int(self.speed * time_factor) * self.direction
            if self.rect.left <= 0 or self.rect.right >= 480:
                self.direction *= -1

            # Disparar cada 60 frames SOLO cuando no está entrando
            self.shoot_timer += 1
            if self.shoot_timer >= 60:  # Dispara cada segundo
                attack_pattern = random.choice([
                    self.shoot,          # Ataque básico original
                    self.shoot_spiral,
                    self.shoot_ring,
                    self.shoot_charged_ball
                ])
                attack_pattern()
                self.shoot_timer = 0

    def shoot(self):
        '''
        Dispara una bala hacia abajo desde la posición del jefe.
        Selecciona aleatoriamente un sprite de bala del grupo de balas.
        '''
        bullet = random.choice(self.bullets_sprites)
        rect = bullet.get_rect(midtop=(self.rect.centerx, self.rect.bottom))
        self.bullets.add(BossBullet(bullet, rect))

    def draw(self, surface):
        '''
        Dibuja el jefe y sus balas en la superficie proporcionada.
        Args:
            surface (pygame.Surface): Superficie donde se dibuja el jefe y sus balas.
        '''
        surface.blit(self.image, self.rect)
        self.bullets.draw(surface)

    def hit(self, damage):
        '''
        Metodo para recibir daño.
        Reduce la salud del jefe en la cantidad de daño recibido.
        Si la salud del jefe llega a 0 o menos, se elimina del grupo de sprites.
        
        Args:
            damage (int): Cantidad de daño recibido por el jefe.
        '''
        self.health -= damage
        if self.health <= 0:
            self.kill()  # Esto saca al jefe del grupo automáticamente
    
    def shoot_spiral(self):
        '''
        Dispara balas en un patrón espiral.
        Crea 8 balas que se dispersan en un patrón espiral alrededor del jefe.
        Cada bala se crea con un ángulo inicial basado en el tiempo actual del juego.
        El ángulo de cada bala se incrementa en 45 grados para crear el efecto espiral.
        '''
        angle = pygame.time.get_ticks() % 360
        for i in range(8):
            bullet = random.choice(self.bullets_sprites)
            rect = bullet.get_rect(center=(self.rect.centerx, self.rect.centery))
            self.bullets.add(SpiralBullet(bullet, rect, angle + i*45))

    def shoot_ring(self, bullets=12):
        '''
        Dispara balas en un patrón de anillo.
        Crea un número específico de balas que se dispersan en un círculo alrededor
        del jefe. Cada bala se crea con un ángulo calculado en función de su posición en el círculo.
        
        Args:
            bullets (int): Número de balas a disparar en el patrón de anillo.
        '''
        for i in range(bullets):
            angle = 360 / bullets * i
            bullet = random.choice(self.bullets_sprites)
            rect = bullet.get_rect(center=(self.rect.centerx, self.rect.centery))
            self.bullets.add(BossBullet(bullet, rect, angle))  # Ahora acepta 3 parámetros

    def shoot_charged_ball(self):
        '''
        Dispara una bola cargada que explota después de un tiempo.
        Crea una bala grande que se mueve hacia abajo y explota después de un tiempo,
        creando 8 balas más pequeñas que se dispersan en todas direcciones.
        Esta bala tiene un efecto de pulso visual y se escala para simular una carga.
        También utiliza un sprite aleatorio de las balas disponibles.
        '''
        big_bullet = pygame.transform.scale(
            random.choice(self.bullets_sprites), 
            (40, 40)
        )
        rect = big_bullet.get_rect(center=(self.rect.centerx, self.rect.bottom))
        self.bullets.add(ChargedBullet(big_bullet, rect, self.bullets_sprites))


class BossBullet(pygame.sprite.Sprite):
    '''
    Clase para las balas disparadas por el jefe.
    Esta clase maneja el movimiento y la actualización de las balas.
    Las balas pueden ser disparadas en diferentes ángulos y patrones.
    
    Atributos:
        image (pygame.Surface): Imagen de la bala.
        rect (pygame.Rect): Rectángulo que define la posición y tamaño de la bala.
        speed (int): Velocidad de movimiento de la bala.
        angle (float): Ángulo en radianes en el que se mueve la bala.
        vel_x (float): Componente horizontal de la velocidad.
        vel_y (float): Componente vertical de la velocidad.
    '''
    def __init__(self, image, rect, angle=90):  # 90° = hacia abajo por defecto
        super().__init__()
        self.image = image
        self.rect = rect
        self.speed = 5
        self.angle = math.radians(angle)  # Convierte a radianes
        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed

    def update(self, time_factor=1.0):
        '''
        Actualiza la posición de la bala según su velocidad y ángulo.
        Mueve la bala en la dirección especificada por su ángulo.
        '''
        self.rect.x += int(self.vel_x * time_factor)
        self.rect.y += int(self.vel_y * time_factor)
        if self.rect.top > 670:
            self.kill()

class SpiralBullet(BossBullet):
    '''
    Clase para las balas que se mueven en un patrón espiral.
    Esta clase extiende BossBullet y añade un comportamiento de movimiento en espiral.
    
    Atributos:
        image (pygame.Surface): Imagen de la bala.
        rect (pygame.Rect): Rectángulo que define la posición y tamaño de la bala.
        angle (float): Ángulo en radianes en el que se mueve la bala.
        speed (int): Velocidad de movimiento de la bala.
        radius (float): Radio del movimiento en espiral.
        center_x (int): Coordenada x del centro del espiral.
        center_y (int): Coordenada y del centro del espiral.
    '''
    def __init__(self, image, rect, angle):
        super().__init__(image, rect)
        self.angle = math.radians(angle)
        self.speed = 3
        self.radius = 0
        self.center_x = rect.centerx
        self.center_y = rect.centery

    def update(self, time_factor=1.0):
        '''
        Actualiza la posición de la bala en un patrón espiral.
        Aumenta el radio del movimiento en espiral y actualiza la posición de la bala
        según su ángulo y radio.
        Si el radio supera un límite, la bala se elimina.
        
        Args:
            time_factor (float): Factor de tiempo para ajustar la velocidad de movimiento.
        '''
        self.radius += 0.5 * time_factor
        self.rect.x = self.center_x + math.cos(self.angle) * self.radius
        self.rect.y = self.center_y + math.sin(self.angle) * self.radius
        if self.radius > 300:
            self.kill()

class ChargedBullet(BossBullet):
    '''
    Clase para las balas cargadas que explotan después de un tiempo.
    Esta clase extiende BossBullet y añade un comportamiento de explosión.
    
    Atributos:
        image (pygame.Surface): Imagen de la bala cargada.
        rect (pygame.Rect): Rectángulo que define la posición y tamaño de la bala.
        speed (int): Velocidad de movimiento de la bala.
        timer (int): Temporizador para controlar el tiempo antes de la explosión.
        glow_timer (float): Temporizador para el efecto de pulso visual.
        scale_factor (float): Factor de escala para el efecto de pulso.
    '''
    def __init__(self, image, rect, bullets_sprites):
        super().__init__(image, rect, 90)  # Siempre dispara hacia abajo
        self.original_image = image
        self.speed = 2
        self.timer = 0
        self.glow_timer = 0
        self.scale_factor = 1.0
        self.bullets_sprites = bullets_sprites

    def update(self, time_factor=1.0):
        '''
        Actualiza la posición de la bala cargada y maneja el efecto de pulso.
        Aumenta el temporizador y escala la imagen para crear un efecto de pulso.
        Si el temporizador alcanza un límite, la bala explota y se crean balas secundarias.
        También mueve la bala hacia abajo según su velocidad.
        
        Args:
            time_factor (float): Factor de tiempo para ajustar la velocidad de movimiento y el efecto de pulso.
        '''
        # Efecto de pulso
        self.glow_timer += 0.1 * time_factor
        self.scale_factor = 1 + 0.1 * math.sin(self.glow_timer)
        self.image = pygame.transform.scale(
            self.original_image,
            (int(self.original_image.get_width() * self.scale_factor),
             int(self.original_image.get_height() * self.scale_factor))
        )
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)
        
        # Movimiento y explosión
        self.timer += 1 * time_factor
        self.rect.y += int(self.speed * time_factor)
        
        if self.timer >= 60:  # Explota después de 1 segundo
            self.explode()
            self.kill()

    def explode(self):
        '''
        Crea 8 balas secundarias que se dispersan en todas direcciones al explotar
        '''
        for angle in range(0, 360, 45):  # 8 direcciones
            bullet_img = random.choice(self.bullets_sprites)
            rect = bullet_img.get_rect(center=self.rect.center)
            new_bullet = BossBullet(bullet_img, rect, angle)
            new_bullet.speed = 3  # Velocidad para las balas secundarias
            self.groups()[0].add(new_bullet)  # Añade al mismo grupo de sprites