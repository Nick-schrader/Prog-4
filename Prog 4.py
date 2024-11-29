from tkinter import *
import sqlite3


class Lingo:
    def __init__(self, window):
        self.window = window
        self.window.title("Lingo!")
        self.window.geometry("500x600")
        self.window.configure(bg="#F7F7F7")  

        # Variabelen
        self.woord = None
        self.punten = 0
        self.pogingen = 0
        self.max_pogingen = 5
        self.input_letters = []
        self.feedback = []

        # Layout
        self.create_widgets()
        self.database_uitput()

    def create_widgets(self):
        # Titel
        Label(self.window, text="Lingo!", font=("Helvetica", 24, "bold"), bg="#F7F7F7", fg="#333").pack(pady=10)
        Label(self.window, text="Raad het woord van vijf letters in vijf beurten.",
              font=("Helvetica", 14), bg="#F7F7F7").pack(pady=5)

        # Score
        self.score_label = Label(self.window, text="Score: 0", font=("Helvetica", 16, "bold"), bg="#F7F7F7", fg="#007ACC")
        self.score_label.pack(pady=5)

        # Rasterframe voor de feedback
        self.grid_frame = Frame(self.window, bg="#F7F7F7")
        self.grid_frame.pack(pady=20)

        # Input en knoppen
        input_frame = Frame(self.window, bg="#F7F7F7")
        input_frame.pack(pady=10)

        Label(input_frame, text="Jouw poging:", font=("Helvetica", 14), bg="#F7F7F7").grid(row=0, column=0, padx=5)
        self.entry = Entry(input_frame, font=("Helvetica", 16), justify="center", width=10)
        self.entry.grid(row=0, column=1, padx=5)

        self.submit_button = Button(input_frame, text="Submit", command=self.validate_input, font=("Helvetica", 12),
                                    bg="#007ACC", fg="white", relief="flat", width=8)
        self.submit_button.grid(row=0, column=2, padx=5)

        # Status
        self.status_label = Label(self.window, text="", font=("Helvetica", 14), bg="#F7F7F7", fg="red")
        self.status_label.pack(pady=10)

    def reset_grid(self):
        # Maak een leeg raster met een standaardachtergrond
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        for row in range(self.max_pogingen):
            for col in range(5):
                label = Label(self.grid_frame, text="", font=("Helvetica", 18, "bold"), width=2, height=1,
                              bg="#D3D3D3", fg="white", borderwidth=2, relief="groove")
                label.grid(row=row, column=col, padx=5, pady=5)

    def update_grid(self):
        # Werk het raster bij met de huidige pogingen en feedback
        for row_index, poging in enumerate(self.input_letters):
            for col_index, letter in enumerate(poging):
                color = "#D3D3D3"  
                text_color = "white"  

                if letter == self.woord[col_index]:  # Correcte letter en plaats
                    color = "#4CAF50"  
                elif letter in self.woord:  # Correcte letter maar verkeerde plaats
                    color = "#F4A100"  
                elif letter != '_':  # Onjuiste letter
                    color = "#CC3333"  

                # Update label
                label = Label(self.grid_frame, text=letter.upper(), font=("Helvetica", 18, "bold"), width=2, height=1,
                              bg=color, fg=text_color, borderwidth=2, relief="groove")
                label.grid(row=row_index, column=col_index, padx=5, pady=5)

    def database_uitput(self):
        # Haal een willekeurig woord van 5 letters uit de database
        try:
            conn = sqlite3.connect('lingo.sqlite3')
            cursor = conn.execute('SELECT woord FROM vijfletters ORDER BY RANDOM() LIMIT 1')
            row = cursor.fetchone()
            if row:
                self.woord = row[0].lower()
                print(f"Gekozen woord: {self.woord}")  
                self.pogingen = 0
                self.input_letters = []
                self.reset_grid()
                self.update_score()
            else:
                self.status_label.config(text="Database is leeg!")
            conn.close()
        except sqlite3.Error as e:
            self.status_label.config(text=f"Databasefout: {e}")

    def validate_input(self):
        poging = self.entry.get().lower()
        self.entry.delete(0, END)

        if len(poging) != 5:
            self.status_label.config(text="Voer een woord in van precies 5 letters!")
            return

        if not self.woord:
            self.status_label.config(text="Start eerst een spel met de startknop!")
            return

        self.input_letters.append(poging)
        self.pogingen += 1
        self.update_grid()

        if poging == self.woord:
            self.punten += 1
            self.status_label.config(text=f"Hoera, je hebt gewonnen!", fg="#28A745")
            self.database_uitput()
        elif self.pogingen >= self.max_pogingen:
            self.status_label.config(text=f"Je hebt verloren! Het woord was: {self.woord}", fg="#CC3333")
            self.database_uitput()
        else:
            self.status_label.config(text="")
            self.update_score()

    def update_score(self):
        self.score_label.config(text=f"Score: {self.punten}")

# Main
root = Tk()
game = Lingo(root)
root.mainloop()