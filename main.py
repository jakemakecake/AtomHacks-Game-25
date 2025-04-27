import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import shutil
from game import Game

class CityRunGameGUI:
    def __init__(self, window):
        self.window = window
        self.game = Game(window)

        # Create Canvas
        self.canvas = tk.Canvas(window, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Load background image
        self.set_background()

        # UI Labels (these are now placed outside the canvas)
        self.energy_label = tk.Label(window, text="Energy: 100%", font=('Arial', 14), fg="black", bg="white")
        self.energy_label.place(x=10, y=10)

        self.distance_label = tk.Label(window, text="Distance: 0 meters", font=('Arial', 14), fg="black", bg="white")
        self.distance_label.place(x=10, y=40)

        self.message_label = tk.Label(window, text="Start the game!", font=('Arial', 16), bg="white")
        self.message_label.place(x=300, y=10)

        # Buttons
        self.start_button = tk.Button(window, text="Start Game", command=self.start_game, font=('Arial', 14))
        self.start_button.place(x=350, y=550)

        self.quit_button = tk.Button(window, text="Quit", command=self.quit_game, font=('Arial', 14))
        self.quit_button.place(x=700, y=550)

        # Key bindings
        self.window.bind("<a>", self.move_left)
        self.window.bind("<Left>", self.move_left)
        self.window.bind("<d>", self.move_right)
        self.window.bind("<Right>", self.move_right)
        self.window.bind("<space>", self.reset_game)

        self.last_time = time.time()

    def set_background(self):
        """Set background image."""
        self.background_image = Image.open('background.png')  # Assuming the image is in the same folder
        self.background_image = self.background_image.resize((800, 600))
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

    def start_game(self):
        self.game = Game(self.window)
        self.message_label.config(text="Game Started!")
        self.update_game()

    def reset_game(self, event=None):
        self.game = Game(self.window)
        self.message_label.config(text="Game Reset! Start again.")
        self.update_labels()
        self.update_game()

    def update_labels(self):
        energy, distance, _, _, _ = self.game.get_stats()
        self.energy_label.config(text=f"Energy: {energy}%")
        self.distance_label.config(text=f"Distance: {distance} meters")

    def update_game(self):
        if self.game.is_game_over:
            messagebox.showinfo("Game Over", f"You ran {self.game.distance} meters! Game Over.")
            self.quit_game()
            return
        self.game.move_character()
        self.update_labels()
        self.game.draw_obstacles(self.canvas)  # Draw obstacles
        self.game.draw_energy_drinks(self.canvas)  # Draw energy drinks
        self.game.draw_character(self.canvas)  # Draw character
        self.window.after(100, self.update_game)

    def move_left(self, event=None):
        message = self.game.move_left()
        self.message_label.config(text=message)

    def move_right(self, event=None):
        message = self.game.move_right()
        self.message_label.config(text=message)

    def quit_game(self):
        return
        self.window.quit()

def main():
    window = tk.Tk()
    window.geometry("800x600")
    window.title("City Run Game")
    game_gui = CityRunGameGUI(window)
    if False:
        def motion(event):
            x, y = event.x, event.y
            print('{}, {}'.format(x, y))

        window.bind('<Motion>', motion)
    window.mainloop()

if __name__ == "__main__":
    main()