import pandas as pd
import numpy as np
import tkinter as tk
import time

n = int(input("Enter the size of the Board Game(at least 8x8): "))
if n < 8:
    raise ValueError("Board size must be at least 8.")
board_size = n

m = int(input("Enter the number of items: "))
if m >= n * n:
    raise ValueError("Items cannot be equal to or more than the board size")
num_items = m

num_players = int(input("Enter the number of players (max 5): "))
if not (2 <= num_players <= 5):
    raise ValueError("Number of players must be between 2 and 5.")

difficulty = input("Choose difficulty level (easy, medium, hard): ")
if difficulty not in ['easy', 'medium', 'hard', 'Easy', 'Medium', 'Hard', 'EASY', 'MEDIUM', 'HARD']:
    raise ValueError("Invalid difficulty level. Choose 'easy', 'medium', or 'hard'.")


board = pd.DataFrame(np.zeros((board_size, board_size), dtype=int))
player_position = [0, 0]
board.iloc[player_position[0], player_position[1]] = 1


remaining_items = num_items
item_positions = []
for _ in range(num_items):
    while True:
        x, y = np.random.randint(0, board_size, size=2)
        if board.iloc[x, y] == 0:
            board.iloc[x, y] = 2
            item_positions.append((x, y))
            break


screen = tk.Tk()
screen.title("Multiplayer Board Game")
board_canvas = tk.Canvas(screen, width=500, height=500)
board_canvas.pack()
cell_size = (500 // board_size)


player_times = []
current_player = 1
items_collected = 0
player_start_time = None


def draw_board():
    board_canvas.delete("all")
    for i in range(board_size):
        for j in range(board_size):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            if board.iloc[i, j] == 1:
                board_canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
            elif board.iloc[i, j] == 2:
                board_canvas.create_rectangle(x1, y1, x2, y2, fill="green")
            else:
                board_canvas.create_rectangle(x1, y1, x2, y2, fill="white")


def update_items():
    global item_positions
    if difficulty in ['medium', 'hard', 'Medium', 'Hard', 'MEDIUM', 'HARD'] and items_collected < num_items:
        for x, y in item_positions:
            board.iloc[x, y] = 0

        new_positions = []
        for _ in range(remaining_items):
            while True:
                x, y = np.random.randint(0, board_size, size=2)
                if board.iloc[x, y] == 0:
                    board.iloc[x, y] = 2
                    new_positions.append((x, y))
                    break

        item_positions = new_positions
        draw_board()
        if difficulty == 'medium' or difficulty == 'Medium' or difficulty == 'MEDIUM':
            screen.after(2000, update_items)
        elif difficulty == 'hard' or difficulty == 'Hard' or difficulty == 'HARD':
            screen.after(500, update_items)


def display_results():
    board_canvas.delete("all")
    player_times.sort(key=lambda x: x[1])
    fastest = player_times[0]
    slowest = player_times[-1]

    board_canvas.create_text(250, 100, text="Game Over!", font=("Arial", 24), fill="black")
    board_canvas.create_text(250, 150, text=f"Fastest: Player {fastest[0]} - {fastest[1]} seconds", font=("Arial", 16), fill="green")
    board_canvas.create_text(250, 200, text=f"Slowest: Player {slowest[0]} - {slowest[1]} seconds", font=("Arial", 16), fill="red")

    y_offset = 250
    for player, time_taken in player_times:
        board_canvas.create_text(250, y_offset, text=f"Player {player}: {time_taken} seconds", font=("Arial", 14), fill="black")
        y_offset += 30


def move_player(event):
    global player_position, items_collected, player_start_time, current_player, remaining_items

    if player_start_time is None:
        player_start_time = time.time()

    x, y = player_position
    board.iloc[x, y] = 0

    if event.keysym == 'Up' and x > 0:
        x -= 1
    elif event.keysym == 'Down' and x < board_size - 1:
        x += 1
    elif event.keysym == 'Left' and y > 0:
        y -= 1
    elif event.keysym == 'Right' and y < board_size - 1:
        y += 1

    if board.iloc[x, y] == 2:
        items_collected += 1
        remaining_items -= 1
        if items_collected == num_items:
            elapsed_time = int(time.time() - player_start_time)
            player_times.append((current_player, elapsed_time))
            if current_player == num_players:
                display_results()
                screen.after(5000, screen.destroy)
                return
            else:
                current_player += 1
                reset_for_next_player()
                return

    player_position[:] = [x, y]
    board.iloc[x, y] = 1
    draw_board()


def reset_for_next_player():
    global player_position, items_collected, player_start_time, remaining_items, item_positions

    player_position = [0, 0]
    items_collected = 0
    player_start_time = None

    board.iloc[:, :] = 0
    board.iloc[player_position[0], player_position[1]] = 1

    remaining_items = num_items
    item_positions = []
    for _ in range(num_items):
        while True:
            x, y = np.random.randint(0, board_size, size=2)
            if board.iloc[x, y] == 0:
                board.iloc[x, y] = 2
                item_positions.append((x, y))
                break

    draw_board()


def on_closing():
    print("Game closed.")
    screen.destroy()


draw_board()
if difficulty in ['medium', 'hard', 'Medium', 'Hard', 'MEDIUM', 'HARD']:
    screen.after(5000 if difficulty == 'medium' or difficulty == 'Medium' or difficulty == 'MEDIUM' else 3000, update_items)
screen.bind("<KeyPress>", move_player)
screen.protocol("WM_DELETE_WINDOW", on_closing)
screen.mainloop()
