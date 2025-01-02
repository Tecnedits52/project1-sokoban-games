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
    def _init_(self, base=Base.NONE, box=False):
        self.base = base
        self.box = box


################################################################################
############################## PROVIDED FUNCTIONS ##############################
################################################################################

# Function to initialize the board to default values
def init_board(board):
    pass
    
# Helper function to print a line the width of the sokoban board
def print_line():
    print('-' * (COLS * 4 + 1))

# Helper function to print the title above the sokoban board
def print_title():
    print_line()
    title = "S O K O B A N"
    pass

# Function to print the current state of the sokoban board
# It will place the player on the board at position player_row, player_col
# If player position is out of bounds, it won't place a player anywhere
def print_board(board, player_row, player_col):
    print_title()
    pass


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

    # TODO: add your code (and remove this todo)

    # prints the board with no player, you might want to delete this...
    print_board(board, -1, -1)

if __name__ == "__main__":
    main()