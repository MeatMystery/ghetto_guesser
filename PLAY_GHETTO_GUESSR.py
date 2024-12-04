# GhettoGusser - Remake of 'Ghetto Price is Right' from 2022 CCOMP-11p class
# Originally by Story on the Programming Discord, re-made Chase Varvayanis
# ChatGPT used to help resolve syntax issues & make docstrings format prettier,
# linted w/ FLAKE8, spellchecked w/ StreetSideSoftware's Spell Checker. Stack
# Overflow used where referenced

# gg_main_game generates the game based on data previously acquired and creates GUI,
# handles end of game window with option for player to play again or quit, did
# not have time to implement a launcher window with options as planned

# last revision 11-14-2024

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
from round_data_maker import make_round_data
from link_file_maker import generate_listings_file

# Constant Game data for gameplay tuning purposes
ROUNDS = 5  # Number of rounds
MAX_SCORE = 10000  # Maximum score per round
PLAYER_COUNT = 4  # Number of players


class GhettoGusserGame:
    def __init__(self, master, round_data):
        """
        Initialize the GhettoGusserGame with GUI elements and game state.

        Args:
            master (tk.Tk): The root window for the GUI.
            round_data (list): List of dictionaries containing round data.
        """
        self.master = master
        self.master.title("GhettoGusser")
        self.master.configure(bg="white")

        # Game initial state
        self.round_data = round_data
        self.current_round = 0
        self.scores = [0] * PLAYER_COUNT
        self.entries = []

        # Setup GUI and elements
        self.create_widgets()

    def create_widgets(self):
        """
        Create the GUI elements for the game, labels, buttons,
        and input fields for player guesses.
        """
        # Listing title
        self.title_label = tk.Label(
            self.master,
            text="",
            font=("Times New Roman", 16),
            anchor="w",
            justify="left",
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

        # Submit guesses button
        self.submit_button = tk.Button(
            self.button_frame,
            text="Submit Guesses",
            command=self.submit_guesses,
            bg="purple", fg="white",
            font=("Times New Roman", 12)
            )
        self.submit_button.grid(row=0, column=0, padx=20)

        # Next Round Button
        self.next_round_button = tk.Button(
            self.button_frame,
            text="Next Round ->",
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
            text="-" * 150,
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
        """
        Display the details of the current round's craigslist listing, title,
        description, and cover image
        """
        if self.current_round < len(self.round_data):
            listing = self.round_data[self.current_round]

            # Set title
            self.title_label.config(text=f"{listing['title']}")

            # Load and process the image
            image_url = listing['photo']
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))

            # Scale down the image if its height is greater than a certain size
            if image.height > 300:
                aspect_ratio = image.width / image.height
                new_height = 300
                new_width = int(new_height * aspect_ratio)
                image = image.resize((new_width, new_height))

            # Convert to PhotoImage object for Tkinter
            photo = ImageTk.PhotoImage(image)

            # Display the image
            self.image_label.config(image=photo)
            self.image_label.image = photo

            # Display the description
            self.description_label.config(text=f"{listing['description']}")
        else:
            # End game at last round
            self.end_game()

    def submit_guesses(self):
        """
        Process guesses and calculate scores for the current round.
        """
        listing = self.round_data[self.current_round]
        actual_price = listing['price']

        try:
            # Replace empty entries with 0 and and int-cast inputs
            guesses = [
                int(entry.get()) if entry.get().strip() else 0
                for entry in self.entries
                ]
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numeric guesses."
                )
            return

        # Calculate scores, no points if over actual price
        round_details = f"Actual Price: ${actual_price}\nOriginal Listing: {listing['url']}\n\n"
        for i, guess in enumerate(guesses):
            if guess == 0 or guess > actual_price:
                # No points for guesses over the actual price or zero
                score = 0
            else:
                # Calculate score for guesses under or equal to actual price
                ratio = guess / actual_price
                # Scale score based on ratio, closer to actual price gets more points
                score = int(MAX_SCORE * ratio)

            self.scores[i] += score
            round_details += f"Player {i + 1}'s Guess: ${guess} | Score: {score}\n"

        # Update score label
        total_scores = "\n".join([f"Player {i + 1}: {self.scores[i]} points" for i in range(PLAYER_COUNT)])
        self.score_label.config(text=f"{round_details}\n\nTotal Scores:\n{total_scores}")

        # Disable submit button and enable next round button
        self.submit_button.config(state=tk.DISABLED)
        self.next_round_button.config(state=tk.NORMAL)

    def next_round(self):
        """
        Proceed to the next round, resetting input fields and updating the
        interface for the new round.
        """
        self.current_round += 1

        # Clear inputs
        for entry in self.entries:
            entry.delete(0, tk.END)

        # Clear the score details for the current round
        self.score_label.config(text="")

        # Disable next round button and enable submit button during round
        self.next_round_button.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.NORMAL)

        # Display next round
        self.display_round()

    def end_game(self):
        """Display the end game window with final scores and determine the winner."""
        max_score = max(self.scores)
        winners = [i + 1 for i, score in enumerate(self.scores) if score == max_score]

        # Format scores for display
        scores_text = "\n".join(
            [f"Player {i + 1}: {self.scores[i]} points" for i in range(PLAYER_COUNT)]
            )

        if len(winners) > 1:
            # Handle tie case
            winners_text = ", ".join(f"Player {winner}" for winner in winners)
            # Tie ending message
            final_message = (
                f"Final Scores:\n\n{scores_text}\n\nIt's a tie!\n"
                f"Winners: {winners_text}"
                )
        else:
            # Normal winner ending message
            final_message = (
                f"Final Scores:\n\n{scores_text}\n\nPlayer {winners[0]} won!\n"
                f"Congratulations!"
                )

        # Create end-game window
        end_window = tk.Toplevel(self.master)
        end_window.title("Game Over")
        end_window.configure(bg="white")

        # Display final message
        message_label = tk.Label(
            end_window,
            text=final_message,
            font=("Times New Roman", 12),
            bg="white",
            justify="left",
            wraplength=400
            )
        message_label.pack(padx=20, pady=20)

        # Play Again button
        play_again_button = tk.Button(
            end_window,
            text="Play Again",
            bg="green",
            fg="white",
            font=("Times New Roman", 12),
            command=lambda: self.restart_game(end_window)
            )
        play_again_button.pack(pady=10)

        # Add Quit button
        quit_button = tk.Button(
            end_window,
            text="Quit",
            bg="red",
            fg="white",
            font=("Times New Roman", 12),
            command=self.master.quit
            )
        quit_button.pack(pady=10)

        # Center the window
        # Used ChatGPT to get this working right, could not figure out syntax and truthfully still can't
        end_window.geometry("+%d+%d" % (
            self.master.winfo_rootx() + 50,
            self.master.winfo_rooty() + 50
        ))

    def restart_game(self, end_window):
        """Restart the game, generating new data and resetting scores."""
        end_window.destroy()  # Close the end-game window

        # Regenerate the link file
        generate_listings_file("https://stockton.craigslist.org/search/sss")

        # Generate new round data
        round_data = make_round_data('cl_listings_file.txt')

        # Check if there are enough listings
        # Really should never be seen unless something goes really wrong
        if len(round_data) < ROUNDS:
            messagebox.showerror(
                "Insufficient Data",
                "Not enough valid listings for game."
                )
            self.master.quit()
            return

        # Reset game state
        self.round_data = round_data  # Update with new round data
        self.scores = [0] * PLAYER_COUNT  # Reset scores
        self.current_round = 0  # Reset round counter
        self.display_round()  # Start game

    # I think this is a duplicate, but removing it seems to break regeneration of round data
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
