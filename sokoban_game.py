import copy



# Constants
ROWS = 10
COLS = 10

# Variables
stack_move = [] 
link_groups = {}
move_box_line = []
update_group_box = []
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

def find_box_line(board,row,col, delta_row, delta_col):
    tile = board[row][col]  # 0,1                               2,3
    boxes = []  # [(0,1)]                                       [(2,3)]
    update_group = [] # [(0,1)]                                 [(2,3)]

    # link_group = [{(0, 1): [], (2, 3): []}]
    while tile.box:
        box_pos = (row, col) # 0,1          (2,3)
        boxes.append(box_pos)
        link_pos = link_groups.get(box_pos,[]) # [(2, 3)]           []    

        if link_pos:

            link_pos.remove(box_pos)
            update_group.append(box_pos)
            for r,c in link_pos:
                if (delta_col == 1 or delta_col) == -1 and r==row and abs(r-row)==1:
    
                    break
                if (delta_row == 1 or delta_row) == -1 and c==col and abs(c-col)==1:
                    break
                box_line = find_box_line(board,r,c,delta_row,delta_col)
                move_box_line.append(box_line) # move_box_line = [[(2,3)], ]
            
        next_row = (row+delta_row)%10
        next_col = (col+delta_col)%10
        tile = board[next_row][next_col]
        row = next_row 
        col = next_col
        
    if tile.base == Base.WALL:
        # link_pos = link_pos + boxes
        link_pos.extend(boxes)      # [1,2,3] + [9,1] = [1,2,3,9,1]
        return []
    else:
        update_group_box.extend(update_group) # [(2,3), (0,1)]
        return boxes

        


def copy_link_groups(link_groups):
    copy = {}

    for key in link_groups.keys():
        values = []
        for position in link_groups[key]:
            p = (position[0],position[1])
            values.append(p)
        copy[key] = values        
    print(f"copy link group = {copy}")
    return copy
    

# {(0,1): [(0,1),(2,3)], (2,3): [(0,1),(2,3)], (2,8): []}
        
        

    
 
def move_player(board,move,player):

    global move_box_line
    global update_group_box
    
    deltas = {
        "w":(-1,0),
        "s":(1,0),
        "a":(0,-1),
        "d":(0,1)
    }
    undo = copy_board(board)
    player1 = Player(player.p_row,player.p_col,player.p_counter) 
    copy_link_group = copy.deepcopy(link_groups)
    stack_move.append((undo,player1,copy_link_group))
    
    
    # cari new_row dan new_col
    delta_row, delta_col = deltas[move]
    new_row = (player.p_row + delta_row)%ROWS
    new_col = (player.p_col + delta_col)%COLS
    
    # b 0 1
    # b 2 3
    # l 0 1 2 3
    # q
    # 0 0
    # d
    target_tile = board[new_row][new_col] # 0,1
    
    if target_tile.box:
        move_box_line = []
        update_group_box = []
        box_line = find_box_line(board,new_row,new_col,delta_row,delta_col) # [(0,1)] 
        move_box_line.append(box_line)  # move_box_line = [[(2,3)], [(0,1)] ]
        
        print(f"link group = {link_groups}")
        print(f"move box line = {move_box_line}")
        print(f"update group box = {update_group_box}") # [(2,3), (0,1)]

        if box_line:
            player.p_row = new_row
            player.p_col = new_col
            player.p_counter += 1
        is_stack_pop = True 
        for box_to_move in move_box_line:
            box_to_move = reversed(box_to_move)
            
            for row, col in box_to_move:
                next_row = (row+delta_row)%10
                next_col = (col+delta_col)%10
                board[next_row][next_col].box = True
                board[row][col].box = False
                is_stack_pop = False
        if is_stack_pop:
            stack_move.pop()
        # Perbarui `link_group` dengan posisi baru
        #  update_group_box=[(2,3), (0,1)]  -> new_values=[(2,4), (0,2)]
        if len(update_group_box) > 0:
            values = link_groups.get(update_group_box[0])
            new_values = list(values)
            for key in update_group_box:
                del link_groups[key]
                
                r, c = key
                new_key = (r + delta_row) % ROWS, (c + delta_col) % COLS
                new_values.append(new_key)

            for key in new_values:
                link_groups[key] = new_values



        # if update_group_box:
        #     values = link_groups.get(update_group_box[0])
        #     new_values = list[values]
        #     for key in update_group_box:
        #         new_key = ((key[0] + delta_row)%10, (key[1] + delta_col)%10)
        #         new_values.append(new_key)
        #         del link_groups[key]

        #     for key in new_values:
        #         link_groups[key] = new_values
        # update_group_box = []
        # move_box_line = []
        

    elif target_tile.base == Base.WALL:
        stack_move.pop()
        return
    else:
        player.p_counter += 1
        player.p_row = new_row
        player.p_col = new_col

def undo(player,board,stack_move):
    if player.p_counter>0:
            player.p_counter -= 1        
    else:
        player.p_counter = 0

    if stack_move:
        print("ewdweferger")
        board.clear()
        global link_groups
        previous_board,previous_player, prev_link_groups= stack_move.pop()
        board += previous_board
        player.p_row = previous_player.p_row
        player.p_col = previous_player.p_col
        link_groups = prev_link_groups 

    else:
        print("No moves to undo!")

# def setup_level1():
# def setup_level2():
# def setup_level3():

def link_boxes(board, row1, col1, row2, col2):
    box1 = row1,col1
    box2 = row2,col2

    if board[row1][col1].box == False:
        print("Invalid Location(s)\n")
        return 
    elif board[row2][col2].box == False:
        print("Invalid Location(s)\n")
        return         
    
    group1 = link_groups.get(box1, [box1])  # [(0,1)]
    group2 = link_groups.get(box2, [box2])  # [(2,3)]
    group = group1+group2   # [(0,1), (2,3)]

    # {(0,1): [(0,1), (2,3)], (2,3): [(0,1), (2,3)]}
    for i in group:
        link_groups[i] = group

    print(f"Linked boxes at {box1} and {box2}")
    print(f"link group = {link_groups}")

def check_win_condition(board):
    correct = 0
    num_storage = 0
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j].box == True and board[i][j].base == Base.STORAGE:
                    correct += 1
            if board[i][j].base == Base.STORAGE:
                    num_storage += 1
    if num_storage == correct:
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

# w 3 2
# w 3 7
# W 2 2 2 7
# W 4 2 4 7
# s 3 6
# b 3 4
# q
# 3 3
# d
# d
def setup_level1(board):
    preset1 = [
        'w 3 2',
        'w 3 7',
        'W 2 2 2 7',
        'W 4 2 4 7',
        's 3 6',
        'b 3 4',
        'q 3 3'
    ]

    i = 0
    while i < len(preset1):  
        command = preset1[i][0]
        if command in ['W', 'l']:
            row1 = int(preset1[i][2])
            col1 = int(preset1[i][4])
            row2 = int(preset1[i][6])
            col2 = int(preset1[i][8])
        elif command in ["w","b","s"]:
            row = int(preset1[i][2])
            col = int(preset1[i][4])
        elif command == "q":
            p_row = int(preset1[i][2])
            p_col = int(preset1[i][4])

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
        i += 1

    data_reset = ()                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    player = Player(p_row,p_col)
    board_setup = copy_board(board)
    data_reset = (board_setup,p_row,p_col)
    return (player,data_reset)

def manual_setup(board):
    line = []
    player = None
    data_reset = ()
    while True:
        try:
            line = input("> ").split(" ")
            if line[0] == "q":
                p_row, p_col = set_player_location(board)
                player = Player(p_row,p_col)
                board_setup = copy_board(board)
                player_row = p_row
                player_col = p_col
                data_reset = (board_setup,player_row,player_col)
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
    return (player, data_reset)

def play_game(board,player,data_reset):
    board_setup = data_reset[0]
    player_row = data_reset[1]
    player_col = data_reset[2]
    while True:
        try:
            command = input("> ")
            if command in ["w","a","s","d"]:
                
                move_player(board,command,player)
                if check_win_condition(board):  
                    if player.p_counter == 1:
                        print(f"=== Level Solved in {player.p_counter} Move! ===")
                        print_board(board,player.p_row,player.p_col)
                        break
                    else:
                        print(f"=== Level Solved in {player.p_counter} Moves! ===")
                        print_board(board,player.p_row,player.p_col)
                        break
            elif command == "c":
                print(f"Number of moves so far: {player.p_counter}")
            elif command == "r":
                board = board_setup
                player.p_row = player_row
                player.p_col = player_col
                player.p_counter = 0
                board_setup = copy_board(board)
            elif command == "u":
                undo(player,board,stack_move)

            print_board(board,player.p_row,player.p_col)
        except KeyboardInterrupt:
            break
                                

################################################################################
############################## MAIN FUNCTIONS ##################################
###############################################################################

def main():
    
    board = []
    init_board(board)
    print("=== Level Setup ===")
    # player, data_reset = manual_setup(board)

    player, data_reset = setup_level1(board)
    play_game(board,player,data_reset)
    # player, data_reset = setup_level2()
    # play_game(board,player,data_reset)
    # player, data_reset = setup_level3() 
    # play_game(board,player,data_reset)                                                                                                                                                                                                                                                                                              


if __name__ == "__main__":
    main()



