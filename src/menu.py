import pygame



def menu_principal(screen, options_sound):
    '''
    Muestra el menú principal del juego.
    Permite al jugador seleccionar entre "Nuevo Juego", "Continuar" o "Salir".
    
    Args:
        screen (pygame.Surface): La superficie donde se dibuja el menú.
        options_sound (pygame.mixer.Sound): Sonido que se reproduce al seleccionar una opción.
    Returns:
        str: La opción seleccionada por el jugador ("nuevo juego", "continuar" o "salir").
        '''
    font_tittle = pygame.font.Font("assets/fonts/Orbitron-VariableFont_wght.ttf", 42)
    font = pygame.font.Font("assets/fonts/Orbitron-VariableFont_wght.ttf", 32)
    opciones = ["Nuevo Juego", "Continuar", "Salir"]
    seleccion = 0

    fondo = pygame.image.load("assets/bg/menu_main.png").convert()
    fondo = pygame.transform.scale(fondo, screen.get_size())
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"
            if event.type == pygame.KEYDOWN:
                options_sound.play()
                if event.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif event.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif event.key == pygame.K_RETURN:
                    return opciones[seleccion].lower()

        screen.blit(fondo, (0,0))
        
        titulo = font_tittle.render("Galaxy Blast", True, (255, 255, 0))
        screen.blit(titulo, (120, 220))

        for i, opcion in enumerate(opciones):
            color = (255, 255, 255) if i != seleccion else (0, 255, 0)
            texto = font.render(opcion, True, color)
            screen.blit(texto, (150, 280 + i * 50))

        pygame.display.flip()

def menu_tutorial(screen, options_sound):
    ''' 
    Muestra el menú de tutorial del juego.
    Permite al jugador ver las instrucciones de control del juego.
    
    Args:
        screen (pygame.Surface): La superficie donde se dibuja el menú.
        options_sound (pygame.mixer.Sound): Sonido que se reproduce al seleccionar una opción.
    Returns:
        bool: True si el jugador decide continuar, False si cierra el menú.
    '''
    pygame.mixer.pause()
    
    fondo = pygame.image.load("assets/bg/menu_main.png").convert()
    fondo = pygame.transform.scale(fondo, screen.get_size())
    
    font = pygame.font.Font("assets/fonts/Orbitron-VariableFont_wght.ttf", 24)
    instrucciones = [
        "Controles:",
        "Flechas: Moverse.",
        "Z: Disparar.",
        "X: Impulso.",
        "C: Sobrecarga",
        "ESC: Pausa.",
        "Presione cualquier tecla",
        "para continuar"
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                options_sound.play()
                return True

        screen.blit(fondo, (0, 0))
        for i, linea in enumerate(instrucciones):
            texto = font.render(linea, True, (255, 255, 255))
            screen.blit(texto, (50, 100 + i * 30))

        pygame.display.flip()

def menu_seleccion_fase(screen, fases_desbloqueadas, options_sound):
    '''
    Muestra el menú de selección de fase.
    Permite al jugador seleccionar una fase desbloqueada para jugar.
    
    Args:
        screen (pygame.Surface): La superficie donde se dibuja el menú.
        fases_desbloqueadas (list): Lista de fases desbloqueadas.
        options_sound (pygame.mixer.Sound): Sonido que se reproduce al seleccionar una opción.
    Returns:
        int: El número de la fase seleccionada por el jugador.
    '''
    font = pygame.font.Font("assets/fonts/Orbitron-VariableFont_wght.ttf", 28)
    seleccion = 0

    fondo = pygame.image.load("assets/bg/menu_main.png").convert()
    fondo = pygame.transform.scale(fondo, screen.get_size())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                options_sound.play()
                if event.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(fases_desbloqueadas)
                elif event.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(fases_desbloqueadas)
                elif event.key == pygame.K_RETURN:
                    return fases_desbloqueadas[seleccion]

        screen.blit(fondo, (0, 0))
        titulo = font.render("Selecciona una Fase", True, (255, 255, 0))
        screen.blit(titulo, (100, 100))

        for i, fase in enumerate(fases_desbloqueadas):
            color = (255, 255, 255) if i != seleccion else (0, 255, 0)
            texto = font.render(f"Fase {fase}", True, color)
            screen.blit(texto, (150, 160 + i * 40))

        pygame.display.flip()
        
def menu_pausa(screen, options_sound):
    '''
    Muestra el menú de pausa del juego.
    Permite al jugador reanudar el juego, acceder a la configuración o salir.
    
    Args:
        screen (pygame.Surface): La superficie donde se dibuja el menú.
        options_sound (pygame.mixer.Sound): Sonido que se reproduce al seleccionar una opción.
    Returns:
        str: La opción seleccionada por el jugador ("reanudar", "configuración" o "salir").
    '''
    font = pygame.font.Font("assets/fonts/Orbitron-VariableFont_wght.ttf", 28)
    opciones = ["Reanudar", "Configuración", "Salir"]
    seleccion = 0

    fondo = pygame.image.load("assets/bg/menu_main.png").convert()
    fondo = pygame.transform.scale(fondo, screen.get_size())
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"
            if event.type == pygame.KEYDOWN:
                options_sound.play()
                if event.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif event.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif event.key == pygame.K_RETURN:
                    return opciones[seleccion].lower()

        screen.blit(fondo, (0, 0))
        for i, opcion in enumerate(opciones):
            color = (255, 255, 0) if i == seleccion else (255, 255, 255)
            texto = font.render(opcion, True, color)
            screen.blit(texto, (150, 200 + i * 40))
        pygame.display.flip()

def game_over(screen, score_manager, lose_sound):
    '''
    Muestra el menú de Game Over.
    Permite al jugador reiniciar el juego o salir.
    
    Args:
        screen (pygame.Surface): La superficie donde se dibuja el menú.
        score_manager (ScoreManager): Objeto que gestiona el puntaje y récords.
        lose_sound (pygame.mixer.Sound): Sonido que se reproduce al perder.
    '''
    pygame.mixer.music.pause()
    lose_sound.play()
    fondo = pygame.image.load("assets/bg/menu_main.png").convert()
    fondo = pygame.transform.scale(fondo, screen.get_size())
    font_big = pygame.font.Font("assets/fonts/Orbitron-VariableFont_wght.ttf", 36)
    font_small = pygame.font.Font("assets/fonts/Orbitron-VariableFont_wght.ttf", 24)

    texto1 = font_big.render("GAME OVER", True, (255, 0, 0))
    texto2 = font_small.render(f"Puntaje: {score_manager.score}", True, (255, 255, 255))
    texto3 = font_small.render(f"Récord: {score_manager.highscore}", True, (255, 255, 0))
    texto4 = font_small.render("Presiona R para reiniciar ", True, (200, 200, 200))
    texto5 = font_small.render("o ESC para salir", True, (200, 200, 200))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.music.unpause()
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False

        screen.blit(fondo, (0, 0))
        screen.blit(texto1, (150, 200))
        screen.blit(texto2, (160, 250))
        screen.blit(texto3, (160, 280))
        screen.blit(texto4, (90, 340))
        screen.blit(texto5, (130, 370))
        pygame.display.flip()