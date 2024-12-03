



import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
from round_data_maker import make_round_data  # Import the make_round_data function

# Constants
ROUNDS = 5
MAX_SCORE = 10000  # Maximum score per round
PLAYER_COUNT = 4


class GhettoGusserGame:
    def __init__(self, master, round_data):
        self.master = master
        self.master.title("GhettoGusser Game")

        # Game state
        self.round_data = round_data
        self.current_round = 0
        self.scores = [0] * PLAYER_COUNT
        self.entries = []

        # UI setup
        self.create_widgets()

    def create_widgets(self):
        # Listing information
        self.title_label = tk.Label(self.master, text="", font=("Arial", 16), wraplength=400)
        self.title_label.pack(pady=10)

        self.image_label = tk.Label(self.master)
        self.image_label.pack(pady=10)

        self.description_label = tk.Label(self.master, text="", font=("Arial", 12), wraplength=400, justify=tk.LEFT)
        self.description_label.pack(pady=10)

        # Player inputs
        self.entries_frame = tk.Frame(self.master)
        self.entries_frame.pack(pady=10)

        for i in range(PLAYER_COUNT):
            player_label = tk.Label(self.entries_frame, text=f"Player {i + 1}'s Guess:")
            player_label.grid(row=i, column=0, padx=5, pady=5)

            entry = tk.Entry(self.entries_frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries.append(entry)

        # Buttons
        self.submit_button = tk.Button(self.master, text="Submit Guesses", command=self.submit_guesses)
        self.submit_button.pack(pady=10)

        self.next_round_button = tk.Button(self.master, text="Next Round", command=self.next_round)
        self.next_round_button.pack(pady=10)
        self.next_round_button.config(state=tk.DISABLED)

        self.score_label = tk.Label(self.master, text="", font=("Arial", 12))
        self.score_label.pack(pady=10)

        # Start first round
        self.display_round()

    def display_round(self):
        """Display the current round's listing."""
        if self.current_round < len(self.round_data):
            listing = self.round_data[self.current_round]

            # Set title
            self.title_label.config(text=listing['title'])

            # Load and display image
            image_url = listing['photo']
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            image = image.resize((300, 200))
            photo = ImageTk.PhotoImage(image)

            self.image_label.config(image=photo)
            self.image_label.image = photo

            # Display description
            self.description_label.config(text=f"Description:\n{listing['description']}")
        else:
            self.end_game()

    def submit_guesses(self):
        """Process guesses and calculate scores for the current round."""
        listing = self.round_data[self.current_round]
        actual_price = listing['price']

        try:
            guesses = [int(entry.get()) for entry in self.entries]
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric guesses.")
            return

        # Calculate scores
        for i, guess in enumerate(guesses):
            difference = abs(actual_price - guess)
            score = max(0, MAX_SCORE - difference)
            self.scores[i] += score

        # Display scores
        scores_text = "\n".join([f"Player {i + 1}: {self.scores[i]} points" for i in range(PLAYER_COUNT)])
        self.score_label.config(text=scores_text)

        # Disable submit button and enable next round button
        self.submit_button.config(state=tk.DISABLED)
        self.next_round_button.config(state=tk.NORMAL)

    def next_round(self):
        """Advance to the next round."""
        self.current_round += 1

        # Clear inputs
        for entry in self.entries:
            entry.delete(0, tk.END)

        # Disable next round button and enable submit button
        self.next_round_button.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.NORMAL)

        # Display next round
        self.display_round()

    def end_game(self):
        """Display the final scores and determine the winner."""
        winner = max(range(PLAYER_COUNT), key=lambda i: self.scores[i])
        scores_text = "\n".join([f"Player {i + 1}: {self.scores[i]} points" for i in range(PLAYER_COUNT)])
        messagebox.showinfo("Game Over", f"Final Scores:\n\n{scores_text}\n\nWinner: Player {winner + 1}!")
        self.master.quit()


def main():
    # Generate round data
    round_data = make_round_data('cl_listings_file.txt')

    # Ensure enough data
    if len(round_data) < ROUNDS:
        messagebox.showerror("Insufficient Data", "Not enough valid listings for the game.")
        return

    # Start game
    root = tk.Tk()
    game = GhettoGusserGame(root, round_data)
    root.mainloop()


if __name__ == "__main__":
    main()
