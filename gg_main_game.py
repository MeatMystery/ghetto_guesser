# GhettoGusser - Remake of 'Ghetto Price is Right' from 2022 CCOMP-11p class
# Originally by Story on the Programming Discord, re-made Chase Varvayanis
# ChatGPT used to help resolve syntax issues & make docstring format prettier,
# linted w/ FLAKE8, spellchecked w/ StreetSideSoftware's Spell Checker

# gg_main_game generates the game based on round data and

# last revision 11-14-2024

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # For image Processing
import requests
from io import BytesIO
from round_data_maker import make_round_data
from link_file_maker import generate_listings_file

# Constant Game Data
ROUNDS = 5  # Number of rounds
MAX_SCORE = 10000  # Maximum score per round
PLAYER_COUNT = 4  # Number of players


class GhettoGusserGame:
    def __init__(self, master, round_data):
        self.master = master
        self.master.title("GhettoGusser Game")
        self.master.configure(bg="white")

        # Game initial state
        self.round_data = round_data
        self.current_round = 0
        self.scores = [0] * PLAYER_COUNT
        self.entries = []

        # Setup GUI
        self.create_widgets()

    def create_widgets(self):
        # Listing title
        self.title_label = tk.Label(
            self.master,
            text="",
            font=("Times New Roman", 16),
            anchor="w",
            bg="white",
            wraplength=500
            )
        self.title_label.grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            padx=10,
            pady=5
            )

        # Horizontal line under title
        self.title_separator = tk.Label(
            self.master,
            text="-" * 120,
            bg="white",
            font=("Times New Roman", 12)
            )
        self.title_separator.grid(
            row=1,
            column=0,
            columnspan=4,
            sticky="ew",
            padx=10,
            pady=5
            )

        # Image
        self.image_label = tk.Label(self.master, bg="white")
        self.image_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

        # Description
        self.description_label = tk.Label(
            self.master,
            text="",
            font=("Times New Roman", 12),
            wraplength=200,
            justify="left",
            anchor="nw",
            bg="white"
            )
        self.description_label.grid(
            row=2,
            column=3,
            sticky="n",
            padx=10,
            pady=5
            )

        # Player input boxes
        self.entries_frame = tk.Frame(self.master, bg="white")
        self.entries_frame.grid(row=4, column=0, columnspan=4, pady=10)

        for i in range(PLAYER_COUNT):
            player_label = tk.Label(
                self.entries_frame,
                text=f"Player {i + 1}'s Guess:",
                font=("Times New Roman", 12),
                bg="white"
                )
            player_label.grid(row=0, column=i, padx=5, pady=5)

            entry = tk.Entry(
                self.entries_frame,
                font=("Times New Roman", 12),
                bg="lightgrey")
            entry.grid(row=1, column=i, padx=5, pady=5)
            self.entries.append(entry)

        # Buttons
        self.button_frame = tk.Frame(self.master, bg="white")
        self.button_frame.grid(row=5, column=0, columnspan=4, pady=10)

        self.submit_button = tk.Button(
            self.button_frame,
            text="Submit Guesses",
            command=self.submit_guesses,
            bg="purple", fg="white",
            font=("Times New Roman", 12)
            )
        self.submit_button.grid(row=0, column=0, padx=20)

        self.next_round_button = tk.Button(
            self.button_frame,
            text="Next Round",
            command=self.next_round,
            bg="grey",
            fg="black",
            font=("Times New Roman", 12)
            )
        self.next_round_button.grid(row=0, column=1, padx=20)
        self.next_round_button.config(state=tk.DISABLED)

        # Horizontal line below buttons
        self.buttons_separator = tk.Label(
            self.master,
            text="-" * 120,
            bg="white",
            font=("Times New Roman", 12)
            )
        self.buttons_separator.grid(
            row=6,
            column=0,
            columnspan=4,
            sticky="ew",
            padx=10,
            pady=5
            )

        # Score display
        self.score_label = tk.Label(
            self.master,
            text="",
            font=("Times New Roman", 12),
            anchor="w",
            justify="left",
            bg="white"
            )
        self.score_label.grid(
            row=7,
            column=0,
            columnspan=4,
            sticky="w",
            padx=10,
            pady=5
            )

        # Start first round
        self.display_round()

    def display_round(self):
        """Display the current round's listing."""
        if self.current_round < len(self.round_data):
            listing = self.round_data[self.current_round]

            # Set title
            self.title_label.config(text=f"{listing['title']}")

            # Load and display image
            image_url = listing['photo']
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            # image = image.resize((300, 200))
            photo = ImageTk.PhotoImage(image)

            self.image_label.config(image=photo)
            self.image_label.image = photo

            # Display description
            self.description_label.config(
                text=f"{listing['description']}"
                )
        else:
            self.end_game()

    def submit_guesses(self):
        """Process guesses and calculate scores for the current round."""
        listing = self.round_data[self.current_round]
        actual_price = listing['price']

        try:
            guesses = [int(entry.get()) for entry in self.entries]
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numeric guesses."
                )
            return

        # Calculate scores #TODO Make better scoring system.
        round_details = f"Actual Price: ${actual_price}\nOriginal Listing: {listing['url']}\n\n"
        for i, guess in enumerate(guesses):
            difference = abs(actual_price - guess)
            score = max(0, MAX_SCORE - difference)
            self.scores[i] += score

            round_details += f"Player {i + 1}'s Guess: ${guess} | Difference: ${difference} | Score: {score}\n"

        # Update score label
        total_scores = "\n".join([f"Player {i + 1}: {self.scores[i]} points" for i in range(PLAYER_COUNT)])
        self.score_label.config(text=f"{round_details}\n\nTotal Scores:\n{total_scores}")

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
        scores_text = "\n".join(
            [f"Player {i + 1}: {self.scores[i]} points" for i in range(PLAYER_COUNT)]
            )
        messagebox.showinfo(
            "Game Over",
            f"Final Scores:\n\n{scores_text}\n\nPlayer {winner + 1} won!"
            )
        self.master.quit()


generate_listings_file("https://stockton.craigslist.org/search/sss")


def main():
    # Generate round data
    round_data = make_round_data('cl_listings_file.txt')

    # Ensure enough listings in round data, never seen this in play test
    # hopefully I never will but just in case
    if len(round_data) < ROUNDS:
        messagebox.showerror(
            "Insufficient Data",
            "Not enough valid listings for game."
            )
        return

    # Start game
    root = tk.Tk()
    game = GhettoGusserGame(root, round_data)
    root.mainloop()
    # I do not know why this is needed, works without it but throws syntax error?
    game


if __name__ == "__main__":
    main()
