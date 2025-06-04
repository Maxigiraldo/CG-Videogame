import pygame
import random
import sys

from src.player import Player
from src.enemy import Enemy
from src.boss import Boss

from src.powerup import PowerUp
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.score_manager import ScoreManager
from src.menu import menu_principal, menu_tutorial, menu_seleccion_fase, menu_pausa, game_over
from src.save_manager import SaveManager
from src.music_manager import load_music

pygame.init()
pygame.mixer.init()

# Configuración de la pantalla -------------------------------------------------------------------------
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Galaxy Blast")
clock = pygame.time.Clock()

fondo = pygame.image.load("assets/bg/Background_Full-0001.png").convert()
fondo = pygame.transform.scale(fondo, (SCREEN_WIDTH, SCREEN_HEIGHT))
scroll = 0

# Inicialización de música y efectos de sonido ---------------------------------------------------
volume_music = 0.8  # Volumen de la música y efectos de sonido
menu_music = "assets/music/menu-soundtrack.mp3"
main_music = "assets/music/main-music-soundtrack.mp3"
boss_music = "assets/music/boss-soundtrack.mp3"

shoot_sound = pygame.mixer.Sound("assets/sounds/laser-shoot.wav")
options_sound = pygame.mixer.Sound("assets/sounds/option-change-sound.wav")
powerup_sound = pygame.mixer.Sound("assets/sounds/powerup-sound.wav")
lose_sound = pygame.mixer.Sound("assets/sounds/lose.wav")
victory_sound = pygame.mixer.Sound("assets/sounds/victory.wav")
warning_sound = pygame.mixer.Sound("assets/sounds/warning.wav")
volume_sound = 0.4  # Volumen de los efectos de sonido

# Inicialización de objetos y variables ---------------------------------------------------------------
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
score_boss = 1000

# Inicialización del gestor de guardado y puntuación -----------------------------------------------
save_manager = SaveManager()
fase_actual = save_manager.fase_actual
fases_desbloqueadas = save_manager.fases_desbloqueadas

# Inicialización del jefe y estado del juego ----------------------------------------------------------
boss = None
boss_defeated = False
score_manager = ScoreManager()
mostrar_alerta_boss = False
contador_alerta = 0
duracion_alerta = 180  # ~3 segundos a 60 FPS

# Bucle principal del juego ---------------------------------------------------------------------------
running = True
load_music(menu_music, bucle=-1, volume=volume_music)  # Cargar música del menú

# Mostrar menú principal y manejar la selección de juego ------------------------------------------------
inicio = menu_principal(screen, options_sound)
if inicio == "salir": # Si el usuario elige salir del juego
    running = False
    pygame.quit()
    sys.exit()  # Termina el programa correctamente
else:
    if inicio == "nuevo juego": # Si el usuario elige iniciar un nuevo juego
        # Reiniciar el juego y cargar la fase inicial
        player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        enemies.empty()
        powerups.empty()
        enemy_bullets.empty()
        score_manager.reset()
        score_manager.save_score()
        fase_actual = 1
        fases_desbloqueadas = [1]
        save_manager.fase_actual = fase_actual
        save_manager.fases_desbloqueadas = fases_desbloqueadas
        save_manager.save()
        run = menu_tutorial(screen, options_sound) # Mostrar tutorial si se elige una fase nueva
        if not run:
            running = False
    elif inicio == "continuar": # Si el usuario elige continuar un juego guardado
        # Cargar el juego guardado
        save_manager.load()
        fases_desbloqueadas = save_manager.fases_desbloqueadas
        fase_elegida = menu_seleccion_fase(screen, fases_desbloqueadas, options_sound)
        if fase_elegida is not None:
            fase_actual = fase_elegida
        else:
            running = False
        score_manager.load_score()
        player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        enemies.empty()
        powerups.empty()
        enemy_bullets.empty()
    load_music(main_music, bucle=-1, volume=volume_music)  # Cargar música principal del juego

score_boss *= fase_actual  # Ajustar el puntaje del jefe según la fase actual

# Evento para generar enemigos cada segundo ----------------------------------------------------------
SPAWN_EVENT = pygame.USEREVENT + 1
base_difficulty = 1800  # Dificultad 
difficulty = max(400, base_difficulty - (fase_actual - 1) * 150)  # Aumentar dificultad con cada fase, mínimo 400ms
pygame.time.set_timer(SPAWN_EVENT, difficulty)  

# Bucle principal del juego -----------------------------------------------------------------------
while running:
    clock.tick(FPS) # Controlar la velocidad de fotogramas
    time_factor = 0.4 if player.charge_status else 1.0 # Factor de tiempo para la velocidad de enemigos y balas
    
    keys = pygame.key.get_pressed() # Obtener las teclas presionadas

    # Manejo de eventos del juego ---------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                player.shoot()
                shoot_sound.play()
                shoot_sound.set_volume(volume_sound)  # Ajustar volumen del sonido de disparo
            elif event.key == pygame.K_x:
                player.dash()
            elif event.key == pygame.K_c and player.charge == player.charge_max:
                player.charge_status = True
                player.charge = 0  # Reiniciar carga al activar sobrecarga
            elif event.key == pygame.K_ESCAPE:  # Pausar con tecla P
                pygame.mixer.music.pause()  # Pausar música
                resultado = menu_pausa(screen, options_sound)
                pygame.mixer.music.unpause()  # Reanudar música
                if resultado == "salir":
                    running = False
                elif resultado == "configuración":
                    pass
        if event.type == SPAWN_EVENT and boss is None and not boss_defeated:
            enemies.add(Enemy())
        
    # Actualizar el jugador y sus balas ----------------------------------------------------------
    player.update(keys)
    player.update_bullets()

    # Colisiones: balas del jugador vs enemigos ---------------------------
    for bullet in player.bullets:
        hits = pygame.sprite.spritecollide(bullet, enemies, False) # Colisión con enemigos
        
        if hits:
            for enemy in hits:
                enemy.hit(10)
            bullet.kill()
            if player.charge_status:
                score_manager.add_points(200)
            if player.double_points > 0:
                score_manager.add_points(100)  # Por cada enemigo destruido
            else:
                score_manager.add_points(50)
            player.charge = min(player.charge_max, player.charge + 5)  # Incrementar carga al destruir enemigos
            if random.random() < 0.1:  # 20% de probabilidad de generar un power-up
                powerup = PowerUp(bullet.rect.centerx, bullet.rect.centery)
                powerups.add(powerup)

    # Actualizar power-ups ---------------------------------------------------
    powerups.update(time_factor)
    
    # Colisiones: jugador vs powerups --------------------------------
    colision_powerups = pygame.sprite.spritecollide(player, powerups, True)
    for p in colision_powerups:
        powerup_sound.play()
        powerup_sound.set_volume(volume_sound)
        if p.tipo == "health":
            player.health = min(player.max_health, player.health + 20)
        elif p.tipo == "shoot":
            player.double_shot = FPS * 5  # 5 segundos de disparo doble
        elif p.tipo == "speed":
            player.speed_boost = FPS * 3  # 3 segundos
        elif p.tipo == "overcharge":
            player.charge = min(player.charge_max, player.charge + 25)
        elif p.tipo == "shield":
            player.shield = FPS * 2  # 5 segundos de inmunidad
        elif p.tipo == "double_points":
            player.double_points = FPS * 5  # 5 segundos de puntos dobles

    # Actualizar enemigos y sus balas --------------------------------
    for enemy in enemies:
        enemy.update(player, time_factor, enemy_bullets)
    
    # Colisiones: jugador vs enemigos --------------------------------
    collisions = pygame.sprite.spritecollide(player, enemies, True)
    if collisions:
        if player.dashing:
            if player.double_points > 0:
                score_manager.add_points(200)
            else:
                score_manager.add_points(100)
            player.charge = min(player.charge_max, player.charge + 10)  # Incrementar carga al parry
            print("¡Parry exitoso!")
        else:
            if player.shield <= 0:
                player.health -= 10
                score_manager.add_points(-20)  # Penalización por daño
    
    # Colisiones: balas de enemigos vs jugador -----------------------
    enemy_bullets.update()
    
    for bullet in enemy_bullets:
        if player.rect.colliderect(bullet.rect):
            if not player.dashing:
                if player.shield <= 0:
                    player.health -= 10
                    score_manager.add_points(-10)  # Penalización por daño
            else:
                if player.double_points > 0:
                    score_manager.add_points(200)
                else:
                    score_manager.add_points(100)
                player.charge = min(player.charge_max, player.charge + 10)
            bullet.kill()
    
    # Generación del jefe ------------------------------------------------
    if score_manager.score >= score_boss and boss is None and not boss_defeated and not mostrar_alerta_boss:
        mostrar_alerta_boss = True
        contador_alerta = duracion_alerta

    if mostrar_alerta_boss:
        contador_alerta -= 1
        if contador_alerta <= 0:
            load_music(boss_music, bucle=-1, volume=volume_music)  # Cambiar música al jefe
            mostrar_alerta_boss = False
            boss = Boss()
            boss_group.add(boss)

    
    # Fase del jefe ------------------------------------------------
    if boss_group:  # Verificar si hay jefe activo
        boss_group.update(time_factor)
        boss_group.draw(screen)  # Dibujar todo el grupo

        for boss in boss_group:  # Iterar por si hay múltiples jefes (opcional)
            for bullet in player.bullets.copy():
                if boss.rect.top >= 50 and boss.rect.colliderect(bullet.rect):
                    bullet.kill()
                    boss.hit(10)
                    if player.double_points > 0:
                        score_manager.add_points(200)
                    else:
                        score_manager.add_points(100)
                    player.charge = min(player.charge_max, player.charge + 5)

        # Colisión balas del jefe vs jugador ------------------------
        for boss in boss_group:
            boss.bullets.update(time_factor)
            for bullet in boss.bullets:
                if player.rect.colliderect(bullet.rect):
                        if not player.dashing:
                            if player.shield <= 0:
                                player.health -= 10
                                score_manager.add_points(-50)  # Penalización por daño
                        else:
                            if player.double_points > 0:
                                score_manager.add_points(200)
                            else:
                                score_manager.add_points(100)
                            player.charge = min(player.charge_max, player.charge + 10)  # Incrementar carga al parry
                        bullet.kill()

        # Verificar si el jefe ha sido derrotado -------------------
        if not boss_group:  # Más pythonico para verificar grupo vacío
            boss_defeated = True
            boss = None
            
    # Dibujar todo en la pantalla ---------------------------------------------------------------
    if not player.charge_status:
        scroll += 6  # velocidad del fondo (ajustable)
    else:
        scroll += 3
    if scroll >= SCREEN_HEIGHT:
        scroll = 0

    screen.blit(fondo, (0, scroll - SCREEN_HEIGHT))
    screen.blit(fondo, (0, scroll))


    # Dibujar objetos del juego ------------------------------------------------
    player.draw(screen)
    powerups.draw(screen)
    player.bullets.draw(screen)
    enemies.draw(screen)
    if boss:
        boss.draw(screen)
    enemy_bullets.draw(screen)
    
    # Dibujar HUD y puntuación ------------------------------------------------
    player.draw_hearts(screen)
    player.draw_health_bar(screen)
    player.draw_charge_bar(screen)
    player.draw_powerup_icons(screen)
    player.draw_score(screen, score_manager.score)

    # Mostrar alerta de jefe si corresponde --------------------------------
    if mostrar_alerta_boss:
        warning_sound.play()
        warning_sound.set_volume(volume_sound)  # Ajustar volumen del sonido de alerta
        alerta_font = pygame.font.Font("assets/fonts/airstrike.ttf", 30)
        alerta_text = alerta_font.render("¡ALERTA!", True, (255, 100, 50))
        screen.blit(alerta_text, (int(SCREEN_WIDTH * 0.35), int(SCREEN_HEIGHT * 0.5)))
    
    # Verificar si el jefe ha sido derrotado y desbloquear fase ------------------------
    if boss_defeated and score_manager.score > 0:
        score_manager.add_points(500)
        victory_sound.play()
        victory_sound.set_volume(volume_sound)  # Ajustar volumen del sonido de victoria
        if fase_actual + 1 not in fases_desbloqueadas:
            fases_desbloqueadas.append(fase_actual + 1)
            fase_actual += 1
            save_manager.fase_actual = fase_actual
            save_manager.fases_desbloqueadas = fases_desbloqueadas
            save_manager.save()
        
        # Resetear estado de batalla
        boss_group.empty()  
        enemies.empty()
        enemy_bullets.empty()
        powerups.empty()
        player.bullets.empty()
        player.charge = 0  # Reiniciar carga al completar fase
        player.charge_status = False  # Reiniciar estado de sobrecarga
        pygame.time.set_timer(SPAWN_EVENT, 0)  # Desactivar generación de enemigos
        
        # Mostrar mensaje de fase completada
        font = pygame.font.Font("assets/fonts/airstrike.ttf", 30)
        texto = font.render("¡Fase Completada!", True, (0, 255, 0))
        screen.blit(texto, (100, 300))
        pygame.display.flip()
        pygame.time.delay(2000)
        screen.fill((0, 0, 0))  # Limpiar pantalla
        player.charge_status = False  # Reiniciar estado de sobrecarga
        player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        texto_fase = font.render(f"Fase {fase_actual} Comienza", True, (255, 255, 0))
        screen.blit(texto_fase, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 20))
        pygame.display.flip()
        pygame.time.delay(2000)
        score_boss += score_manager.score  # Aumentar el puntaje del jefe para la siguiente fase
        difficulty = max(400, base_difficulty - (fase_actual - 1) * 150)  # Aumentar dificultad con cada fase, mínimo 400ms
        pygame.time.set_timer(SPAWN_EVENT, difficulty)  # Reiniciar temporizador de generación de enemigos
        boss_defeated = False
        load_music(main_music, bucle=-1, volume=volume_music)  # Volver a la música principal
    
    # Verificar si el jugador ha perdido --------------------------------
    if player.health <= 0:
        resultado = game_over(screen, score_manager, lose_sound)
        if resultado:
            # Reiniciar juego
            player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
            enemies.empty()
            enemy_bullets.empty()
            powerups.empty()
            if boss:
                boss_group.empty()
            boss = None
            boss_defeated = False
            if mostrar_alerta_boss:
                mostrar_alerta_boss = False
            score_manager.reset()
            player.charge = 0
            player.charge_status = False
            player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
            # Evitar duplicados
            pygame.time.set_timer(SPAWN_EVENT, 0)  # Desactivarlo primero
            pygame.time.set_timer(SPAWN_EVENT, difficulty)  # Activarlo de nuevo
            load_music(main_music, bucle=-1, volume=volume_music)  # Volver a la música principal

        else:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
