"""
Rock Paper Scissors game with GUI using Tkinter
"""
import tkinter as tk
from tkinter import ttk, messagebox
import random

class RockPaperScissorsGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Rock Paper Scissors")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        
        # Game variables
        self.choices = ["rock", "paper", "scissors"]
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.total_rounds = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.window, text="Rock Paper Scissors", 
                              font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Detailed Scoreboard Frame
        scoreboard_frame = tk.LabelFrame(self.window, text="Detailed Scoreboard", 
                                        font=("Arial", 12, "bold"), padx=10, pady=5)
        scoreboard_frame.pack(pady=10, padx=20, fill="x")
        
        # Score statistics
        self.player_wins_label = tk.Label(scoreboard_frame, text="Player Wins: 0", 
                                         font=("Arial", 11), fg="green")
        self.player_wins_label.grid(row=0, column=0, sticky="w", pady=2)
        
        self.computer_wins_label = tk.Label(scoreboard_frame, text="Computer Wins: 0", 
                                           font=("Arial", 11), fg="red")
        self.computer_wins_label.grid(row=1, column=0, sticky="w", pady=2)
        
        self.ties_label = tk.Label(scoreboard_frame, text="Ties: 0", 
                                  font=("Arial", 11), fg="orange")
        self.ties_label.grid(row=2, column=0, sticky="w", pady=2)
        
        self.total_rounds_label = tk.Label(scoreboard_frame, text="Total Rounds: 0", 
                                          font=("Arial", 11), fg="blue")
        self.total_rounds_label.grid(row=0, column=1, sticky="w", padx=20, pady=2)
        
        self.win_rate_label = tk.Label(scoreboard_frame, text="Win Rate: 0%", 
                                      font=("Arial", 11), fg="purple")
        self.win_rate_label.grid(row=1, column=1, sticky="w", padx=20, pady=2)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(pady=20)
        
        # Choice buttons
        rock_btn = tk.Button(buttons_frame, text="🪨 Rock", 
                            command=lambda: self.play_round("rock"),
                            font=("Arial", 12), width=8, height=2)
        rock_btn.grid(row=0, column=0, padx=5)
        
        paper_btn = tk.Button(buttons_frame, text="📄 Paper", 
                             command=lambda: self.play_round("paper"),
                             font=("Arial", 12), width=8, height=2)
        paper_btn.grid(row=0, column=1, padx=5)
        
        scissors_btn = tk.Button(buttons_frame, text="✂️ Scissors", 
                                command=lambda: self.play_round("scissors"),
                                font=("Arial", 12), width=8, height=2)
        scissors_btn.grid(row=0, column=2, padx=5)
        
        # Result display
        self.result_label = tk.Label(self.window, text="Choose your move!", 
                                    font=("Arial", 14))
        self.result_label.pack(pady=20)
        
        # Computer choice display
        self.computer_label = tk.Label(self.window, text="", 
                                      font=("Arial", 12))
        self.computer_label.pack(pady=5)
        
        # Reset and Quit buttons
        control_frame = tk.Frame(self.window)
        control_frame.pack(pady=10)
        
        reset_btn = tk.Button(control_frame, text="Reset Score", 
                             command=self.reset_game,
                             font=("Arial", 10))
        reset_btn.grid(row=0, column=0, padx=5)
        
        quit_btn = tk.Button(control_frame, text="Quit", 
                            command=self.window.quit,
                            font=("Arial", 10))
        quit_btn.grid(row=0, column=1, padx=5)
    
    def update_scoreboard(self):
        """Update all scoreboard displays"""
        self.player_wins_label.config(text=f"Player Wins: {self.player_score}")
        self.computer_wins_label.config(text=f"Computer Wins: {self.computer_score}")
        self.ties_label.config(text=f"Ties: {self.ties}")
        self.total_rounds_label.config(text=f"Total Rounds: {self.total_rounds}")
        
        # Calculate win rate
        if self.total_rounds > 0:
            win_rate = (self.player_score / self.total_rounds) * 100
            self.win_rate_label.config(text=f"Win Rate: {win_rate:.1f}%")
        else:
            self.win_rate_label.config(text="Win Rate: 0%")
    
    def play_round(self, player_choice):
        computer_choice = random.choice(self.choices)
        self.total_rounds += 1
        
        # Display computer choice
        computer_emojis = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
        self.computer_label.config(text=f"Computer chose: {computer_emojis[computer_choice]} {computer_choice.title()}")
        
        # Determine winner
        if player_choice == computer_choice:
            result = "It's a tie!"
            self.ties += 1
        elif (player_choice == "rock" and computer_choice == "scissors") or \
             (player_choice == "paper" and computer_choice == "rock") or \
             (player_choice == "scissors" and computer_choice == "paper"):
            result = "You win!"
            self.player_score += 1
        else:
            result = "Computer wins!"
            self.computer_score += 1
        
        # Update displays
        self.result_label.config(text=result)
        self.update_scoreboard()
        
        # Check for game end (optional: first to 10 wins)
        if self.player_score == 10:
            messagebox.showinfo("Game Over", "Congratulations! You won the match!")
            self.reset_game()
        elif self.computer_score == 10:
            messagebox.showinfo("Game Over", "Computer won the match! Better luck next time!")
            self.reset_game()
    
    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.total_rounds = 0
        self.update_scoreboard()
        self.result_label.config(text="Choose your move!")
        self.computer_label.config(text="")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = RockPaperScissorsGUI()
    game.run()