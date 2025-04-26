import tkinter as tk
from tkinter import messagebox
from game import Game
import pygame
import time

# Initialize pygame for sound
pygame.mixer.init()

class CityRunGameGUI:
    def __init__(self, window):
        self.window = window
        self.game = Game(window)

        # Set up UI components
        self.energy_label = tk.Label(window, text="Energy: 100%", font=('Arial', 14))
        self.energy_label.pack()

        self.distance_label = tk.Label(window, text="Distance: 0 meters", font=('Arial', 14))
        self.distance_label.pack()

        self.message_label = tk.Label(window, text="Start the game!", font=('Arial', 16))
        self.message_label.pack()

        # Quit button
        self.quit_button = tk.Button(window, text="Quit", command=self.quit_game, font=('Arial', 14))
        self.quit_button.pack()

        # Create start button
        self.start_button = tk.Button(window, text="Start Game", command=self.start_game, font=('Arial', 14))
        self.start_button.pack()

        # Initially hide the game control buttons until game starts
        self.hide_game_buttons()

        # Track the time to update the distance continuously
        self.last_time = time.time()

        # Track player movement (in pixels)
        self.distance_in_pixels = 0  # Initial pixel distance
        self.pixels_per_meter = 8  # Let's assume 8 pixels = 1 meter for simplicity

        # Set up key bindings for moving left and right
        self.window.bind("<a>", self.move_left)
        self.window.bind("<Left>", self.move_left)
        self.window.bind("<d>", self.move_right)
        self.window.bind("<Right>", self.move_right)

        # Bind the spacebar to restart the game
        self.window.bind("<space>", self.reset_game)


    def start_game(self):
        """Start the game when the start button is clicked."""
        self.game = Game(self.window)  # Reset game
        self.message_label.config(text="Game Started!")
        self.show_game_buttons()
        self.update_game()  # Start the automatic updates

    def reset_game(self, event=None):
        """Reset the game when spacebar is pressed."""
        self.game = Game(self.window)  # Reset game instance
        self.message_label.config(text="Game Reset! Start again.")
        self.update_labels()  # Update the UI
        self.hide_game_buttons()  # Hide game buttons
        self.update_game()  # Start the game updates again

    def show_game_buttons(self):
        """Show game control buttons (Quit)."""
        self.quit_button.pack()
        self.start_button.pack_forget()  # Hide start button after game starts

    def hide_game_buttons(self):
        """Hide game control buttons."""
        self.quit_button.pack_forget()
        self.start_button.pack_forget()

    def update_labels(self):
        energy, distance, obstacles, energy_drinks, lane = self.game.get_stats()
        self.energy_label.config(text=f"Energy: {energy}%")
        self.distance_label.config(text=f"Distance: {distance} meters")  # Distance counter

    def update_game(self):
        """Start running the game automatically."""
        if self.game.is_game_over:
            self.game_over_sound.play()
            messagebox.showinfo("Game Over", f"You ran {self.game.distance} meters! Game Over.")
            self.quit_game()
            return

        # Track the player's movement based on pixels
        self.game.move_character()  # Move character logic

        # Display updated labels
        self.update_labels()

        # Update the game every 100ms
        self.window.after(100, self.update_game)

    def move_left(self, event=None):
        """Move the character to the left."""
        message = self.game.move_left()
        self.message_label.config(text=message)

    def move_right(self, event=None):
        """Move the character to the right."""
        message = self.game.move_right()
        self.message_label.config(text=message)

    def quit_game(self):
        """Quit the game and close the window."""
        self.window.quit()


def main():
    # Set up the main window
    window = tk.Tk()

    # Initialize the game GUI
    game_gui = CityRunGameGUI(window)

    # Start the Tkinter loop
    window.mainloop()


if __name__ == "__main__":
    main()

