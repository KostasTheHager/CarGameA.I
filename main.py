import tkinter as tk
import random

class MainMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Game - Main Menu")

        # Load high score
        self.high_score = self.load_high_score()

        # Display high score
        self.high_score_label = tk.Label(master, text="High Score: " + str(self.high_score))
        self.high_score_label.pack()

        # Player name entry
        self.name_label = tk.Label(master, text="Enter your name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(master)
        self.name_entry.pack()

        # Start game button
        self.start_button = tk.Button(master, text="Start Game", command=self.start_game)
        self.start_button.pack()

    def start_game(self):
        name = self.name_entry.get()
        self.master.destroy()  # Close main menu window
        game_window = tk.Tk()
        game_window.title("Car Game - " + name)
        game = CarGame(game_window, name)
        game.main_loop()  # Start the main game loop
        game_window.mainloop()

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                high_score_str = file.read().strip()
                return int(high_score_str)
        except (FileNotFoundError, ValueError):
            return 0

class CarGame:
    def __init__(self, master, player_name):
        self.master = master
        self.canvas = tk.Canvas(master, width=400, height=300)
        self.canvas.pack()
        self.canvas.focus_set()  # Set focus to the canvas

        self.player_name = player_name

        # Create the car
        self.car = self.canvas.create_rectangle(180, 240, 220, 280, fill="blue")

        # Bind arrow key events
        master.bind('<Left>', self.move_left)
        master.bind('<Right>', self.move_right)
        master.bind('<Up>', self.move_up)
        master.bind('<Down>', self.move_down)

        self.dx = 0
        self.dy = 0

        # Initialize score
        self.score = 0
        self.score_label = tk.Label(master, text="Score: 0")
        self.score_label.pack()

        # Create obstacles
        self.obstacles = []
        self.create_obstacle()

        # Game over flag
        self.game_over_flag = False

    def move_left(self, event):
        self.dx = -5
        self.canvas.move(self.car, self.dx, self.dy)  # Move the car
        self.check_collision()

    def move_right(self, event):
        self.dx = 5
        self.canvas.move(self.car, self.dx, self.dy)  # Move the car
        self.check_collision()

    def move_up(self, event):
        self.dy = -5
        self.canvas.move(self.car, self.dx, self.dy)  # Move the car
        self.check_collision()

    def move_down(self, event):
        self.dy = 5
        self.canvas.move(self.car, self.dx, self.dy)  # Move the car
        self.check_collision()

    def create_obstacle(self):
        x = random.randint(0, 380)
        y = 0
        obstacle = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="red")
        self.obstacles.append(obstacle)
        self.move_obstacles()
        self.master.after(1000, self.create_obstacle)  # Generate new obstacle every second

    def move_obstacles(self):
        for obstacle in self.obstacles:
            self.canvas.move(obstacle, 0, 5)  # Increase the vertical speed to 5 (adjust as needed)
            if self.canvas.coords(obstacle)[1] > 300:  # If obstacle moves beyond the window, remove it
                self.canvas.delete(obstacle)
                self.obstacles.remove(obstacle)

    def check_collision(self):
        car_coords = self.canvas.coords(self.car)
        for obstacle in self.obstacles:
            obstacle_coords = self.canvas.coords(obstacle)
            if (car_coords[0] < obstacle_coords[2] and car_coords[2] > obstacle_coords[0] and
                    car_coords[1] < obstacle_coords[3] and car_coords[3] > obstacle_coords[1]):
                self.game_over()
                return
        # Increment score if no collision occurred
        self.score += 1
        self.score_label.config(text="Score: " + str(self.score))  # Update score label

    def game_over(self):
        self.save_high_score()
        self.canvas.create_text(200, 150, text="Game Over", font=("Helvetica", 24), fill="red")
        self.game_over_flag = True  # Set game over flag to True

    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.score))

    def main_loop(self):
        if not self.game_over_flag:
            # Update game logic
            self.update()
            self.master.after(50, self.main_loop)  # Call main_loop again after 50 milliseconds
        else:
            # Keep the window open after the game is over
            self.master.mainloop()  # Enter Tkinter event loop

    def update(self):
        # Update game state
        self.move_obstacles()
        self.check_collision()
        # Add more update logic as needed

def main():
    root = tk.Tk()
    main_menu = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
