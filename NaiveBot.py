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
            
    # If no available "informed" moves are available, select random choice in valid moves
    if len(valid_moves) != 0:
        return random.choice(valid_moves)
        
    # Base Case (no moves available)
    return 0