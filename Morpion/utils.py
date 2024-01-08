 

def isEmpty(p):
    return p=="" or p.strip()==""



def generate_winning_combinations(size,alignment):
    combinations = []
    
    #Combinaison gagnante en ligne
    for i in range(size):
        for j in range(size - alignment +1):
            row_combination = [(i, j+k ) for k in range(alignment)]
            combinations.append(row_combination)
            
    #Combinaison gagnante en colonne
    for i in range(size):
        for j in range(size - alignment +1):
            col_combination = [(j+k, i ) for k in range(alignment)]
            combinations.append(col_combination)     
    
    
    #Combinaison gagnante diagonale
    for i in range(size-alignment+1):
        for j in range(size - alignment+1):
            diag_combination = [(i + k, j + k ) for k in range(alignment)]
            combinations.append(diag_combination)   
            
    #Combinaison gagnante diagonale renverser
    for i in range(size-alignment+1):
        for j in range(alignment-1, size):
            diag_rev_combination = [(i + k, j - k ) for k in range(alignment)]
            combinations.append(diag_rev_combination)
            
    return combinations

def has_winner(game):
    
    winning_combinations = generate_winning_combinations(game.config.grid_size,game.config.alignment)
 
    for combination in winning_combinations:
        if all(game.board[row][col]==game.current_player.id for row,col in combination):
            return True
    return False
 
    
    
        