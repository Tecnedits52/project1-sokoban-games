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
def is_outofbounds(row,col):
    if (row > 9 or row < 0) or (col > 9 or col < 0):
        return True
    return False

def player_is_valid(p_row,p_col,board):
    if is_outofbounds(p_row,p_col) == True:
        return False
    else:
        if board[p_row][p_col].base == Base.WALL:
            return False
        elif board[p_row][p_col].box == True:
            return False
        else:
            return True

def set_player_location(board):
    while True:
        print("Enter player starting position:", end=" ")
        p_row, p_col = input().split(" ")
        p_row = int(p_row )
        p_col = int(p_col) 
        if player_is_valid(p_row,p_col,board) == True:
            print("\n=== Starting Sokoban! ===\n")
            print_board(board,p_row,p_col)
            return p_row, p_col
        else:
            print(f"Position ({p_row}, {p_col}) is invalid\n")
            continue
        
def move_box(p_row,p_col,board,direction):
    if direction == "w":
        if board[p_row][p_col].box == True:
            if board[(p_row-1)%ROWS][p_col].base != Base.WALL:
                board[p_row][p_col].box = False
                board[(p_row-1)%ROWS][p_col].box = True

    elif direction == "a":
        if board[p_row][p_col].box == True:
            if board[p_row][(p_col-1)%10].base != Base.WALL:
                board[p_row][p_col].box = False
                board[p_row][(p_col-1)%10].box = True

    elif direction == "s":
        if board[p_row][p_col].box == True:
            if board[(p_row+1)%ROWS][p_col].base != Base.WALL:
                board[p_row][p_col].box = False
                board[(p_row+1)%ROWS][p_col].box = True

    elif direction == "d":
        if board[p_row][p_col].box == True:
            if board[p_row][(p_col+1)%10].base != Base.WALL:
                board[p_row][p_col].box = False
                board[p_row][(p_col+1)%10].box = True


    
        

            
def move_player(board,p_row,p_col,move,p_counter):

    if move == "w":
        if board[p_row-1][p_col].base != Base.WALL and board[p_row-2][p_col].base != Base.WALL:
            p_row -= 1 
            p_counter += 1
        if p_row < 0:
            p_row = 9
        
        move_box(p_row,p_col,board,move)
    elif move == "a":
        if board[p_row][p_col-1].base != Base.WALL and board[p_row][p_col-2].base != Base.WALL:
            p_col -= 1
            p_counter += 1
        if p_col < 0:
            p_col = 9
        move_box(p_row,p_col,board,move)
        
    elif move == "s":
        if board[(p_row+1)%ROWS][p_col].base != Base.WALL and board[(p_row+2)%ROWS][p_col].base != Base.WALL:
            p_row += 1 
            p_counter += 1
        if p_row > 9:
            p_row = 0
        move_box(p_row,p_col,board,move)
        
    elif move == "d":
        if board[p_row][(p_col+1)%COLS].base != Base.WALL and board[p_row][(p_col+2)%COLS].base != Base.WALL:
            p_col += 1
            p_counter += 1
        if p_col > 9:
            p_col = 0
        move_box(p_row,p_col,board,move)

    
    return p_row, p_col, p_counter
################################################################################
############################## MAIN FUNCTIONS ##################################
###############################################################################

def main():
    board = []
    init_board(board)
    print("=== Level Setup ===")
    line = []
    while True:
        try:
            line = input("> ").split(" ")
            if line[0] == "q":
                p_row, p_col = set_player_location(board)
                break
            elif len(line) == 5:
                command = line[0]
                row1 = int(line[1])
                col1 = int(line[2])
                row2 = int(line[3])
                col2 = int(line[4])
            elif len(line) == 3:
                command = line[0]
                row = int(line[1])
                col = int(line[2])
                if is_outofbounds(row,col) == True:
                    print("Location out of bounds")
                    print_board(board, -1, -1)

                    continue
                
            else:
                continue
            
            if command == "w":
                board[row][col].base = Base.WALL
                board[row][col].box = False
            elif command == "s":
                board[row][col].base = Base.STORAGE
            elif command == "b":
                if board[row][col].base == Base.WALL:
                    board[row][col].base = Base.NONE
                    board[row][col].box = True
                else:
                    board[row][col].box = True
            elif command == "W":
                if is_outofbounds(row1,col1) and is_outofbounds(row2,col2):
                    print("Location out of bounds")
                    print_board(board, -1, -1)
                    continue
                if row1 == row2:
                    for i in range(col1,col2+1):
                        if not is_outofbounds(row1,i):
                            board[row1][i].base = Base.WALL
                            board[row1][i].box = False    
                if col1 == col2:
                    for i in range(row1, row2+1):
                        if not is_outofbounds(i,col1):
                            board[i][col1].base = Base.WALL
                            board[i][col1].box = False
                

            print_board(board, -1, -1)
        except KeyboardInterrupt:
            break
    p_counter = 0
    while True:
        try:

            command = input("> ")
            if command in ["w","a","s","d"]:
                p_row, p_col, p_counter = move_player(board,p_row,p_col,command,p_counter)
            elif command == "c":
                print(f"Number of moves so far: {p_counter}")
            print_board(board,p_row,p_col)


        except KeyboardInterrupt:
            break



if __name__ == "__main__":
    main()
