"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 10        # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    """
    Move both player one by one starting with player
    """
    while board.check_win() == None:         
       
        empty_list = board.get_empty_squares()
    
        empty_place = empty_list.pop(random.randint(0, len(empty_list)-1 ))
        board.move(empty_place[0], empty_place[1], player)
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player): 
    
    """
    update scores as per Monte Carlo
    """
    
    board_result = board.check_win()
    
    if(board_result == provided.DRAW) :
        return
    
    board_size = board.get_dim()
    
    current_win = False
    if (player == board_result) :
        current_win = True
    
    for dummy_row in range(board_size) :
        for dummy_col in range(board_size) :
            
            if(board.square(dummy_row, dummy_col) == provided.EMPTY) :
                continue
                
            current_score = 0
            
            current_player = board.square(dummy_row, dummy_col)
            
            if(current_win) :
                if(current_player == player) :
                    current_score = SCORE_CURRENT
                else :
                    current_score = -SCORE_OTHER

            else :
                if(current_player == player) :
                    current_score = -SCORE_CURRENT
                else :
                    current_score = SCORE_OTHER
            
            scores[dummy_row][dummy_col]  += current_score

def get_best_move(board, scores):
    
    """
    Get best move by looking as scores 
    """
    
    max_score = None
    max_list = []
   
    empty_squares  = board.get_empty_squares()
    
    if len(empty_squares) == 0  :
        return 
   
    for dummy_squares in empty_squares :
        max_score = max(max_score, scores[dummy_squares[0]][dummy_squares[1]])
    
    for dummy_squares in empty_squares :
        if(max_score == scores[dummy_squares[0]][dummy_squares[1]]) :
                    max_list.append((dummy_squares[0], dummy_squares[1]))
    
        
    return max_list[random.randint(0, len(max_list)-1)]

def mc_move(board, player, trials):
    
    """
    Return best move for player after doing trials
    """
    
    board_dim = board.get_dim()
    
    scores = [[0 for dummy_col in range(board_dim)] for dummy_row in range(board_dim)]
    
    for dummy_trail in range(trials) :
        
        trail_board = board.clone()
        mc_trial(trail_board, player)
        mc_update_scores(scores , trail_board, player)
    
    return get_best_move(board, scores)
        
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.
provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
