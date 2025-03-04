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