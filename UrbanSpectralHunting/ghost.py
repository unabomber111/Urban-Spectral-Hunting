import time            # serve per far passare il tempo
import random          # serve per numeri casuali

class Ghost:           # classe che rappresenta un fantasma
    def __init__(self, name):
        self.name = name                      # nome/tipo del fantasma
        self.points = random.choice([5, 10, 15])   # punti bassi → progressione lenta
        self.life_time = random.randint(5, 15)     # tempo in secondi prima che sparisca
        self.alive = True                     # stato del fantasma (vivo o catturato)

    def exist(self):
        time.sleep(self.life_time)            # il fantasma "vive" per un po'
        self.alive = False                    # poi sparisce
