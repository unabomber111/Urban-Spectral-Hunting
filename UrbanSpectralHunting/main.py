from zone import Zone
from gui import GameGUI
from ghost import Ghost
import threading
import random
import time

score = 0                                    # lo score parte SEMPRE da zero a ogni avvio
boss_fight_done = False                      # flag se il boss è già apparso
boss_active = False                          # flag per fermare spawn fantasmi durante il boss

gui = GameGUI()                              # creo la finestra

def add_score(points):                        # aggiunge punti al punteggio globale
    global score
    score += points                           # incremento solo con i punti del fantasma catturato
    gui.update_score(score)                    # aggiorno barra punteggio

def check_boss():                             # controlla se spawnare il boss
    global boss_fight_done, boss_active
    if score >= 200 and not boss_fight_done:   # se punti >= 1000 e boss non apparso
        boss_fight_done = True
        boss_active = True                     # fermo spawn dei fantasmi
        threading.Thread(target=fight_boss).start()  # avvio boss in thread separato
        return True
    return False

def fight_boss():
    gui.log_event("!!! BOSS SPAWN !!! Il fantasma supremo è apparso!", "boss")  # log spawn boss
    time.sleep(3)                            # pausa prima del combattimento
    boss_hp = 100                            # vita boss
    while boss_hp > 0:                       
        damage = random.randint(10, 20)     # danno casuale
        boss_hp -= damage
        gui.log_event(f"Hai colpito il boss! -{damage} HP", "boss")  # log danno
        time.sleep(1.5)
    gui.log_event("BOSS SCONFITTO! 🎉", "boss")  # boss morto
    gui.log_event(
        "Urban Spectral Hunting realizzato dal team UnaBomber della 4E - Iti Renato Elia 2025/2026",
        "boss"
    )
    gui.log_event("Puoi chiudere la finestra quando vuoi.", "zone")

def is_boss_active():                      # funzione che serve alle zone per fermare spawn
    global boss_active
    return boss_active

zones = [
    Zone("Centro", add_score, gui, check_boss, is_boss_active),
    Zone("Stazione", add_score, gui, check_boss, is_boss_active),
    Zone("Quartiere Antico", add_score, gui, check_boss, is_boss_active)
]

for z in zones:
    z.start()                               # ogni zona parte in parallelo

gui.start()                                 # resta aperta finché chiudi

for z in zones:
    z.stop()                                # ferma tutti i thread quando chiudi la finestra
