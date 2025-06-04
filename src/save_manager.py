import json
import os

SAVE_FILE = "save_data.json"

class SaveManager:
    '''
    Clase para manejar el guardado y carga de datos del juego.
    Esta clase permite guardar el estado del juego, incluyendo la fase actual y las fases desbloqueadas.
    
    Atributos:
        fase_actual (int): Fase actual del juego.
        fases_desbloqueadas (list): Lista de fases desbloqueadas.
    '''
    def __init__(self):
        self.fase_actual = 1
        self.fases_desbloqueadas = [1]
        self.load()

    def load(self):
        '''
        Carga los datos guardados desde el archivo JSON.
        Si el archivo no existe, se inicializan los valores por defecto.
        '''
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                self.fase_actual = data.get("fase_actual", 1)
                self.fases_desbloqueadas = data.get("fases_desbloqueadas", [1])

    def save(self):
        '''
        Guarda el estado actual del juego en un archivo JSON.
        Incluye la fase actual y las fases desbloqueadas.
        '''
        data = {
            "fase_actual": self.fase_actual,
            "fases_desbloqueadas": self.fases_desbloqueadas
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=4)