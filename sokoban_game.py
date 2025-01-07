# Constants
ROWS = 10
COLS = 10

# Every tile on the map has to be one of the following values.
class Base:
    NONE = 0
    WALL = 1
    STORAGE = 2

# A single tile of our board.
# box should only contain the value:
# - True: there exists a box here
# - False: there doesn't exist a box here
class Tile:
    def __init__(self, base=Base.NONE, box=False):
        self.base = base
        self.box = box


################################################################################
############################## PROVIDED FUNCTIONS ##############################
################################################################################

# Function to initialize the board to default values
def init_board(board):
    for i in range(ROWS):
        row = []
        for i in range(COLS):
            row.append(Tile())
        board.append(row)
    

# Helper function to print a line the width of the sokoban board
def print_line():
    print('-' * (COLS * 4 + 1))

# Helper function to print the title above the sokoban board
def print_title():
    print_line()
    title = "|             S O K O B A N             |"
    print(title)


# Function to print the current state of the sokoban board
# It will place the player on the board at position player_row, player_col
# If player position is out of bounds, it won't place a player anywhere
def print_board(board, player_row, player_col):

    print_title()
    for i in range(ROWS):
        print_line()
        for j in range(COLS):
            print("|", end="")
            tile = board[i][j]
            if i == player_row and j == player_col:
                print("^_^", end="")
            elif tile.base == Base.WALL:
                print("===", end="")
            elif tile.box == True and tile.base == Base.STORAGE:
                print("[o]", end="") 
            elif tile.box == True:
                print("[ ]", end="")
            elif tile.base == Base.STORAGE:
                print(" o ", end="")
            else:
                print("   ", end="")
        print("|")
    print_line()
 


################################################################################
############################## YOUR FUNCTIONS ##################################
################################################################################

# TODO: Your function implementations go here


################################################################################
############################## MAIN FUNCTIONS ##################################
################################################################################

def main():
    board = []
    init_board(board)
    print("=== Level Setup ===")
    while True:
        try:
            command, row, col = input().split(" ")
            row = int(row)
            col = int(col)
            if command == "w":
                board[row][col].base = Base.WALL
            elif command == "s":
                board[row][col].base = Base.STORAGE
            print_board(board, -1, -1)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
