from zone import Zone
from gui import GameGUI
from ghost import Ghost
import threading
import random
import time
import sys

# CONFIGURAZIONE INIZIALE
score = 0                    # lo score parte SEMPRE da zero a ogni avvio
boss_fight_done = False      # flag se il boss è già apparso
boss_active = False          # flag per fermare spawn fantasmi durante il boss

# controllo modalità CLI
cli_mode = len(sys.argv) > 1 and sys.argv[1].lower() == "cli"  # True se scrivo python main.py cli

# LOGGER UNIVERSALE
# se siamo in GUI -> logger usa gui.log_event
# se siamo in CLI -> logger usa print
gui = GameGUI() if not cli_mode else None
logger = (lambda txt, tag=None: gui.log_event(txt, tag)) if not cli_mode else lambda txt, tag=None: print(txt)

# FUNZIONI PRINCIPALI
def add_score(points):  # aggiunge punti al punteggio globale
    global score
    score += points
    if not cli_mode:
        gui.update_score(score)       # aggiorna barra punteggio in GUI
    logger(f"Punti totali: {score}") # log in CLI o GUI

def check_boss():         # controlla se spawnare il boss
    global boss_fight_done, boss_active
    if score >= 200 and not boss_fight_done:  # quando arrivi a 200 punti
        boss_fight_done = True
        boss_active = True                      # blocca spawn fantasmi
        threading.Thread(target=fight_boss).start()  # avvia boss in thread separato
        return True
    return False

def fight_boss():         # combattimento boss automatico
    logger("!!! BOSS SPAWN !!! Il fantasma supremo è apparso!", "boss")
    time.sleep(3)
    boss_hp = 100
    while boss_hp > 0:
        damage = random.randint(10, 20)
        boss_hp -= damage
        logger(f"Hai colpito il boss! -{damage} HP", "boss")
        time.sleep(1.5)
    logger("BOSS SCONFITTO! 🎉", "boss")
    logger("Urban Spectral Hunting realizzato dal team UnaBomber della 4E - Iti Renato Elia 2025/2026", "boss")
    logger("Puoi chiudere la finestra o premere CTRL+C per uscire.", "zone")
    global boss_active
    boss_active = False  # il boss è morto, spawn di fantasmi può riprendere

def is_boss_active():    # funzione che serve alle zone per fermare spawn
    global boss_active
    return boss_active

# CREAZIONE DELLE ZONE
zones = [
    Zone("Centro", add_score, logger, check_boss, is_boss_active),
    Zone("Stazione", add_score, logger, check_boss, is_boss_active),
    Zone("Quartiere Antico", add_score, logger, check_boss, is_boss_active)
]

for z in zones:
    z.start()  # ogni zona parte in parallelo

# AVVIO DEL GIOCO
if cli_mode:
    print("Benvenuto in Urban Spectral Hunting CLI! Premi CTRL+C per uscire.\n")
    try:
        while True:  # loop infinito
            time.sleep(1)
    except KeyboardInterrupt:
        print("Chiusura del gioco...")
        for z in zones:
            z.stop()
else:
    gui.start()  # resta aperta finché chiudi
    for z in zones:
        z.stop()
