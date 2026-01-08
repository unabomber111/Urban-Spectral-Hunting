import threading
import time
import random
from ghost import Ghost

class Zone(threading.Thread):
    def __init__(self, name, add_score_callback, gui, check_boss_callback, boss_active_flag):
        super().__init__()
        self.name = name                                # nome della zona
        self.add_score = add_score_callback            # funzione per aggiungere punti
        self.gui = gui                                  # riferimento alla GUI
        self.check_boss = check_boss_callback          # funzione per spawn boss
        self.boss_active_flag = boss_active_flag       # funzione che dice se il boss è attivo
        self.running = True                             # flag per fermare il thread

    def run(self):
        while self.running:
            if self.boss_active_flag():                # se il boss è attivo
                time.sleep(1)                          # pausa breve e riprovo
                continue                               # non generare nuovi fantasmi

            ghost = Ghost(f"Fantasma {random.randint(1,100)}")    # creo fantasma casuale
            self.gui.log_event(f"[{self.name}] Fantasma apparso: {ghost.name}", "spawn")  # log spawn

            time.sleep(ghost.life_time)               # attende il tempo di vita del fantasma

            if ghost.alive:                              # se il fantasma non è stato catturato
                ghost.alive = False                       # ora è catturato
                self.add_score(ghost.points)             # aggiunge solo i suoi punti
                self.gui.log_event(f"[{self.name}] Fantasma catturato! +{ghost.points}", "catch")  # log cattura

            self.check_boss()                            # controlla se spawnare il boss

            time.sleep(random.randint(1, 3))            # pausa tra un fantasma e l'altro

    def stop(self):
        self.running = False                             # ferma il thread
