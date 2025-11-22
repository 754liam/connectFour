def my_agent(obs, config):
    import numpy as np
    import random

    def drop_piece(grid, col, piece, config):
        next_grid = grid.copy()
        for row in range(config.rows-1, -1, -1):
            if next_grid[row][col] == 0:
                break
        next_grid[row][col] = piece
        return next_grid

    def check_winning_move(obs, config, col, piece):
        grid = np.asarray(obs.board).reshape(config.rows, config.columns)
        next_grid = drop_piece(grid, col, piece, config)
        
        # horizontal
        for r_loop in range(config.rows):
            for c_loop in range(config.columns-(config.inarow-1)):
                window = list(next_grid[r_loop, c_loop:c_loop+config.inarow])
                if window.count(piece) == config.inarow:
                    return True
        # vertical
        for r_loop in range(config.rows-(config.inarow-1)):
            for c_loop in range(config.columns):
                window = list(next_grid[r_loop:r_loop+config.inarow, c_loop])
                if window.count(piece) == config.inarow:
                    return True
        # positive diagonal
        for r_loop in range(config.rows-(config.inarow-1)):
            for c_loop in range(config.columns-(config.inarow-1)):
                window = list(next_grid[range(r_loop, r_loop+config.inarow), range(c_loop, c_loop+config.inarow)])
                if window.count(piece) == config.inarow:
                    return True
        # negative diagonal
        for r_loop in range(config.inarow-1, config.rows):
            for c_loop in range(config.columns-(config.inarow-1)):
                window = list(next_grid[range(r_loop, r_loop-config.inarow, -1), range(c_loop, c_loop+config.inarow)])
                if window.count(piece) == config.inarow:
                    return True
        return False
    def count_windows(grid, num_discs, piece, config):
        count = 0
        
        for row in range(config.rows):
            for col in range(config.columns-(config.inarow-1)):
                window = list(grid[row, col:col+config.inarow])
                if window.count(piece) == num_discs and window.count(0) == config.inarow-num_discs:
                    count += 1
        
        for row in range(config.rows-(config.inarow-1)):
            for col in range(config.columns):
                window = list(grid[row:row+config.inarow, col])
                if window.count(piece) == num_discs and window.count(0) == config.inarow-num_discs:
                    count += 1
        
        for row in range(config.rows-(config.inarow-1)):
            for col in range(config.columns-(config.inarow-1)):
                window = list(grid[range(row, row+config.inarow), range(col, col+config.inarow)])
                if window.count(piece) == num_discs and window.count(0) == config.inarow-num_discs:
                    count += 1
        
        for row in range(config.inarow-1, config.rows):
            for col in range(config.columns-(config.inarow-1)):
                window = list(grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
                if window.count(piece) == num_discs and window.count(0) == config.inarow-num_discs:
                    count += 1
        return count

    def get_heuristic(grid, mark, config):
        #my defined heuristic values; A for 4 way next case, B for three way next case, C for 2 way next case, D for 2 way opp next case, E for 3 way opp next case
        A = 1000000 
        B = 100     
        C = 1       
        D = -100    
        E = -1000000 
        
        my_piece = mark
        opp_piece = mark % 2 + 1
        
        num_threes = count_windows(grid, 3, my_piece, config)
        num_twos = count_windows(grid, 2, my_piece, config)
        
        num_threes_opp = count_windows(grid, 3, opp_piece, config)
        num_fours_opp = count_windows(grid, 4, opp_piece, config) 
        
        score = B*num_threes + C*num_twos + D*num_threes_opp + E*num_fours_opp
        return score
        
    grid = np.asarray(obs.board).reshape(config.rows, config.columns)
    valid_moves = [c for c in range(config.columns) if 0 in grid[:, c]]
    
    # Check for winning moves
    for c in valid_moves:
        if check_winning_move(obs, config, c, obs.mark):
            return c
            
    # Check for blocking moves
    opponent_mark = 3 - obs.mark
    for c in valid_moves:
        if check_winning_move(obs, config, c, opponent_mark):
            return c
            
    # Heuristics for finding the best move
    best_score = -float("inf")
    best_move = random.choice(valid_moves) #if and only if all scores are equal
    for col in valid_moves:
        #simulation
        temp_grid = drop_piece(grid,col,obs.mark,config)
        score = get_heuristic(temp_grid,obs.mark,config)
        if score >best_score:
            best_score = score
            best_move = col
    return best_move