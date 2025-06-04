import pygame

def load_music(path, bucle=-1, volume=0.5):
    '''
    Carga y reproduce música desde un archivo.
    
    Args:
        path (str): Ruta del archivo de música.
        bucle (int): Número de veces que se repetirá la música (-1 para bucle infinito).
        volume (float): Volumen de la música (0.0 a 1.0).
    '''
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)  # Ajusta el volumen según sea necesario
    pygame.mixer.music.play(bucle)  # Reproduce la música en bucle
    print(f"Música cargada y reproducida desde {path} con volumen {volume}")
