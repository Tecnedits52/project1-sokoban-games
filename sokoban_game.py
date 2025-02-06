# Constants
ROWS = 10
COLS = 10

# Variables
stack_move = [] 
link_groups = {}
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

class Player:
    def __init__(self,p_row,p_col,p_counter = 0):
        self.p_col = p_col
        self.p_row = p_row
        self.p_counter = p_counter
    


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


 
def move_player(board,move,player):
    deltas = {
        "w":(-1,0),
        "s":(1,0),
        "a":(0,-1),
        "d":(0,1)
    }
    undo = copy_board(board)
    player1 = Player(player.p_row,player.p_col,player.p_counter) 
    stack_move.append((undo,player1))
        
    # cari new_row dan new_col
    delta_row, delta_col = deltas[move]
    new_row = (player.p_row + delta_row)%ROWS
    new_col = (player.p_col + delta_col)%COLS
    
    target_tile = board[new_row][new_col]
    
    if target_tile.box:
        newgroup = []
        box = (new_row,new_col)
        group = link_groups.get(box, [box])
        for r,c in group:
            box_move = []
            box_new_row = (r+delta_row)%ROWS
            box_new_col = (c+delta_col)%COLS
            box_target_tile = board[box_new_row][box_new_col]

            box_move.append((r,c))
            box_move.append((box_new_row,box_new_col))
            while box_target_tile.box:  
                box_new_row = (box_new_row+delta_row)%ROWS
                box_new_col = (box_new_col+delta_col)%COLS   
                box_target_tile = board[box_new_row][box_new_col]
                box_move.append((box_new_row,box_new_col))
            print(box_move)
            box_move.pop()

            if box_target_tile.base == Base.WALL:
                continue
            
            for i in range(len(box_move)-1,-1,-1):
                next_row = (box_move[i][0] + delta_row)%10
                next_col = (box_move[i][1] + delta_col)%10
                board[next_row][next_col].box = True

                if i == 0:
                    board[box_move[i][0]][box_move[i][1]].box = False
            r = (delta_row+r) % ROWS
            c = (delta_col+c) % COLS
            new_pos = (r,c)
            newgroup.append(new_pos)

            if r == new_row and c == new_col:
                player.p_counter += 1
                player.p_row = new_row
                player.p_col = new_col
                
        for pos in group:
            del link_groups[pos]
        for i in newgroup:
            link_groups[i] = newgroup
            
        print(link_groups)
    elif target_tile.base == Base.WALL:
        stack_move.pop()
        return
    else:
        player.p_counter += 1
        

def link_boxes(board, row1, col1, row2, col2):
    box1 = row1,col1
    box2 = row2,col2

    if board[row1][col1].box == False:
        print("Invalid Location(s)\n")
        return 
    elif board[row2][col2].box == False:
        print("Invalid Location(s)\n")
        return         
    
    group1 = link_groups.get(box1, [box1])
    group2 = link_groups.get(box2, [box2])
    group = group1+group2

    for i in group:
        link_groups[i] = group

    print(f"Linked boxes at {box1} and {box2}")
    print(link_groups)

def check_win_condition(board):
    correct = 0
    num_box = 0
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j].box == True and board[i][j].base == Base.STORAGE:
                    correct += 1
            if board[i][j].box == True:
                    num_box += 1
    if num_box == correct:
        return True
    else:
        return False

def copy_board(board):
    copyboard = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):  
            tile = board[i][j]
            new_tile = Tile(tile.base,tile.box)
            row.append(new_tile)
        copyboard.append(row)
    return copyboard

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
                player = Player(p_row,p_col)
                board_setup = copy_board(board)
                player_row = p_row
                player_col = p_col

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
            elif command == "l":
                link_boxes(board, row1, col1, row2, col2)
            
            print_board(board, -1, -1)
            

        except KeyboardInterrupt:
            break
    

    while True:
        try:
            command = input("> ")
            if command in ["w","a","s","d"]:
                
                move_player(board,command,player)
                if check_win_condition(board):  
                    if player.p_counter == 1:
                        print(f"=== Level Solved in {player.p_counter} Move! ===")
                    else:
                        print(f"=== Level Solved in {player.p_counter} Moves! ===")
                    
            elif command == "c":
                print(f"Number of moves so far: {player.p_counter}")
            elif command == "r":
                board = board_setup
                player.p_row = player_row
                player.p_col = player_col
                player.p_counter = 0
                board_setup = copy_board(board)
            elif command == "u":
                if player.p_counter>0:
                     player.p_counter -= 1
                else:
                    player.p_counter = 0
                previous_board,previous_player = stack_move.pop()
                board = previous_board
                player = previous_player

            print_board(board,player.p_row,player.p_col)


        except KeyboardInterrupt:
            break
                                                                                                                                                                                                                                                                                                                 


if __name__ == "__main__":
    main()



