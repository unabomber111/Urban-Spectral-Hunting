import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class GameGUI:
    def __init__(self):
        self.root = tk.Tk()                        # creo la finestra
        self.root.title("Urban Spectral Hunting 👻") 
        self.root.geometry("600x400")               # dimensioni finestra

        self.score_label = tk.Label(self.root, text="Score: 0", font=("Arial", 16))
        self.score_label.pack(pady=10)

        self.log = ScrolledText(self.root, height=15)
        self.log.pack(padx=10, pady=10)

        self.log.tag_config("spawn", foreground="blue")    # fantasmi spawnati
        self.log.tag_config("catch", foreground="green")   # fantasmi catturati
        self.log.tag_config("boss", foreground="red")      # boss
        self.log.tag_config("zone", foreground="black")    # log generali

    def update_score(self, score):
        self.score_label.config(text=f"Score: {score}")   # aggiorna punteggio

    def log_event(self, text, tag="zone"):
        self.log.insert(tk.END, text + "\n", tag)        # aggiunge testo colorato
        self.log.see(tk.END)                              # scrolla in fondo automaticamente

    def start(self):
        self.root.mainloop()                              # avvia il ciclo principale di tkinter
