from random import shuffle
import numpy as np
from enum import Enum

SIZE = 3


class Player(Enum):
    computer = 1
    human = -1
    empty = 0


# Print the game grid
def print_grid(grid):
    symbols = {Player.human.value: "X", Player.computer.value: "O", Player.empty.value: " "}
    print("\n" + "\n".join(["|" + "".join([f"{symbols[cell]}|" for cell in row]) for row in grid]))


def equal(row):
    return row.count(row[0]) == len(row)


# Check if there is a victory of the given player
def check_victory(grid, last):
    if equal([grid[i][last[1]] for i in range(SIZE)]):
        return True
    if equal([grid[last[0]][i] for i in range(SIZE)]):
        return True
    if last[0] == last[1] and equal([grid[i][i] for i in range(SIZE)]):
        return True
    if last[0] + last[1] == SIZE - 1 and \
            equal([grid[i][j] for i in range(SIZE) for j in range(SIZE) if i + j == SIZE - 1]):
        return True
    return False


# Get the indexes of the empty cells
def get_empty_cells(grid):
    return [tuple(x) for x in np.transpose(np.where(grid == Player.empty.value))]


# Get the move of the human player
def human_move(grid):
    move = int(input("\nSelect a cell: ")) - 1
    index = (int(move / SIZE), move % SIZE)
    if grid.item(index) == Player.empty.value:
        grid.itemset(index, Player.human.value)
    else:
        print("The cell is not empty!")
        human_move(grid)


# Return the move of the AI
def computer_move(grid):
    empty_cells = get_empty_cells(grid)
    shuffle(empty_cells)
    move, best_result = None, 1

    for index in empty_cells:
        new_grid = np.copy(grid)
        new_grid.itemset(index, Player.computer.value)
        result = mini_max(new_grid, Player.human.value, index)

        if result < best_result:
            best_result = result
            move = index
            if result == -1:
                break

    if best_result == -1:
        print("AI: You are going to lose!")
    if move:
        grid.itemset(move, Player.computer.value)
        return move


# Get the score of the game
def mini_max(grid, player, last):
    if check_victory(grid, last):
        return grid.item(last) * player

    move, score = None, -2
    for index in [(i, j) for i in range(SIZE) for j in range(SIZE)]:
        if grid.item(index) == Player.empty.value:
            new_grid = np.copy(grid)
            new_grid.itemset(index, player)
            move_score = -mini_max(new_grid, -player, index)
            if move_score > score:
                score = move_score
                move = index
    if not move:
        return 0
    return score


def main():
    print("Invincible Tic-tac-toe AI")
    grid = np.zeros((SIZE, SIZE), np.int8)
    print_grid(grid)

    while True:
        human_move(grid)
        move = computer_move(grid)
        print_grid(grid)

        if not move:
            print("\nThe game ended in a draw.")
            break
        if check_victory(grid, move):
            print("\nThe computer AI wins!")
            break


if __name__ == "__main__":
    main()
