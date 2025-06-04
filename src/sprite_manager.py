import pygame

def cortar_sprite(sheet, columnas, filas, escala=1):
    '''
    Corta un sprite sheet en múltiples sprites individuales.
    
    Args:
        sheet (pygame.Surface): La imagen del sprite sheet.
        columnas (int): Número de columnas en el sprite sheet.
        filas (int): Número de filas en el sprite sheet.
        escala (float): Factor de escala para redimensionar los sprites (1.0 = sin escala).
    Returns:
        list: Lista de sprites cortados.
    '''
    ancho = sheet.get_width() // columnas
    alto = sheet.get_height() // filas
    sprites = []

    for y in range(filas):
        for x in range(columnas):
            rect = pygame.Rect(x * ancho, y * alto, ancho, alto)
            image = sheet.subsurface(rect)
            if escala != 1:
                image = pygame.transform.scale(image, (int(ancho * escala), int(alto * escala)))
            sprites.append(image)
    
    return sprites

def cargar_sprites(nombre_archivo, columnas, filas, escala=1):
    ''' 
    Carga un sprite sheet y lo corta en múltiples sprites.
    
    Args:
        nombre_archivo (str): Ruta del archivo del sprite sheet.
        columnas (int): Número de columnas en el sprite sheet.
        filas (int): Número de filas en el sprite sheet.
        escala (float): Factor de escala para redimensionar los sprites (1.0 = sin escala).
    Returns:
        list: Lista de sprites cortados.
    '''
    try:
        sheet = pygame.image.load(nombre_archivo).convert_alpha()
        return cortar_sprite(sheet, columnas, filas, escala)
    except pygame.error as e:
        print(f"Error al cargar el sprite sheet: {e}")
        return []
    
def extraer_sprite(sheet, x, y, ancho, alto, escala=1):
    '''
    Extrae un sprite específico de un sprite sheet.
    
    Args:
        sheet (pygame.Surface): La imagen del sprite sheet.
        x (int): Coordenada X del sprite en el sprite sheet.
        y (int): Coordenada Y del sprite en el sprite sheet.
        ancho (int): Ancho del sprite a extraer.
        alto (int): Alto del sprite a extraer.
        escala (float): Factor de escala para redimensionar el sprite (1.0 = sin escala).
    Returns:
        pygame.Surface: El sprite extraído y redimensionado.
    '''
    image = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), pygame.Rect(x, y, ancho, alto))
    if escala != 1:
        image = pygame.transform.scale(image, (int(ancho * escala), int(alto * escala)))
    return image

def animar_sprites(sprites, velocidad):
    '''
    Crea una animación a partir de una lista de sprites.
    Cada sprite se redimensiona según la velocidad especificada.

    Args:
        sprites (list): Lista de sprites a animar.
        velocidad (float): Factor de escala para redimensionar los sprites (1.0 = sin escala).
    Returns:
        list: Lista de sprites animados redimensionados.
    '''
    animacion = []
    for sprite in sprites:
        animacion.append(pygame.transform.scale(sprite, (sprite.get_width() * velocidad, sprite.get_height() * velocidad)))
    return animacion