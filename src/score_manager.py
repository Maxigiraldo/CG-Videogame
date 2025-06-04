import json
import os

SCORE_FILE = "score_data.json"

class ScoreManager:
    '''
    Clase para manejar el puntaje del juego.
    Esta clase permite agregar puntos, resetear el puntaje y guardar el récord en un archivo JSON.
    
    Atributos:
        score (int): Puntaje actual del jugador.
        highscore (int): Récord de puntaje guardado.
        SCORE_FILE (str): Ruta del archivo donde se guarda el récord.
    '''
    def __init__(self):
        self.score = 0
        self.highscore = 0
        self.load_score()

    def add_points(self, amount):
        '''
        Agrega puntos al puntaje actual.
        Si el puntaje se vuelve negativo, se establece en 0.
        Si el nuevo puntaje supera el récord, se actualiza el récord y se guarda.
        Args:
            amount (int): Cantidad de puntos a agregar.
        '''
        if (self.score + amount) < 0:
            self.score = 0
        else:
            self.score += amount
        if self.score > self.highscore:
            self.highscore = self.score
            self.save_score()

    def reset(self):
        '''
        Resetea el puntaje actual a 0.
        '''
        self.score = 0

    def load_score(self):
        '''
        Carga el récord de puntaje desde un archivo JSON.
        Si el archivo no existe, se inicializa el récord a 0.
        '''
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, "r") as f:
                data = json.load(f)
                self.highscore = data.get("highscore", 0)

    def save_score(self):
        '''
        Guarda el récord de puntaje en un archivo JSON.
        Si el archivo no existe, se crea uno nuevo.
        '''
        with open(SCORE_FILE, "w") as f:
            json.dump({"highscore": self.highscore}, f)
