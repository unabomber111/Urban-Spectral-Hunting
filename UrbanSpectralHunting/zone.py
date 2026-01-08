import threading
import time
import random
from ghost import Ghost

class Zone(threading.Thread):
    def __init__(self, name, add_score_callback, logger, check_boss_callback, boss_active_flag):
        super().__init__()
        self.name = name                                # nome della zona tipo "Centro"
        self.add_score = add_score_callback            # funzione che aggiunge punti allo score
        self.logger = logger                            # funzione per loggare messaggi (GUI o CLI)
        self.check_boss = check_boss_callback          # funzione per controllare il boss
        self.boss_active_flag = boss_active_flag       # funzione che dice se il boss è attivo
        self.running = True                             # flag per fermare il thread se voglio chiudere

    def run(self):
        while self.running:                            # ciclo infinito della zona
            if self.boss_active_flag():                # se il boss sta combattendo
                time.sleep(1)                          # pausa 1 secondo e riprovo
                continue                               # non generare fantasmi nuovi

            # creo un fantasma casuale
            ghost = Ghost(f"Fantasma {random.randint(1,100)}")

            # log dell'apparizione
            self.logger(f"[{self.name}] Fantasma apparso: {ghost.name}", "spawn")

            # attendo per la durata del fantasma
            time.sleep(ghost.life_time)

            # catturo automaticamente il fantasma
            if ghost.alive:
                ghost.alive = False                     # ora è catturato
                self.add_score(ghost.points)           # aggiungo i punti
                self.logger(f"[{self.name}] Fantasma catturato! +{ghost.points}", "catch")

            # controllo se devo spawnare il boss
            self.check_boss()

            # pausa casuale tra un fantasma e l'altro
            time.sleep(random.randint(1,3))

    def stop(self):
        self.running = False                             # quando chiudo la finestra o CLI, fermo il thread
