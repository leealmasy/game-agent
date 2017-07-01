"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass
"""
===============================================================================
"""

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    This should be the best heuristic function for your project submission.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    xown,yown= game.get_player_location(player)
    xopp,yopp = game.get_player_location(game.get_opponent(player))
    ymid = -(-game.height//2) 
    xmid = -(-game.width//2) 
    # euclidean distance 2D to center
    dist_own = ((xown-xmid)**2+(yown-ymid)**2)**0.5
    dist_opp = ((xopp-xmid)**2+(yopp-ymid)**2)**0.5   
    cust1 = (dist_own-2*dist_opp)
    cust2 = custom_score2(game,player)
    cust3 = custom_score3(game_player)
    cust = 0.5*cust1  +0.25*cust2+0.25*cust3
    return float(cust)
   
    
"""
===============================================================================
"""

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    x_own,y_own = game.get_player_location(player)
    x_opp,y_opp = game.get_player_location(game.get_opponent(player))
    ymid = -(-game.height//2) 
    xmid = -(-game.width//2) 
    
    if x_own >= xmid:
        xown = game.width - x_own
    else:
        xown = x_own -game.width
    if y_own >= ymid:
        yown = game.height - y_own
    else:
        yown = y_own -game.height        
    if x_opp >= xmid:
        xopp = game.width - x_opp
    else:
        xopp = x_pp -game.width
    if y_opp >= ymid:
        yopp = game.height - y_opp
    else:
        yopp = y_opp -game.height   
        
    # determine players' manhattan distance from outter edge
    dist_own = (abs(xown)+ abs(yown))
    dist_opp = (abs(xopp)+ abs(yopp))
    
    return float(dist_own-2*dist_opp)      

"""
===============================================================================
"""

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    own_cnt =0
    opp_cnt =0
    
    own = game.get_legal_moves(player)
    for z in own:
        x,y = z
        print('xy',x,y)
        if x>=2 and x<=6 and y>=2 and y<=6:
            own_cnt += 1
    
    opp = game.get_legal_moves(game.get_opponent(player))
    for z in opp:
        x,y = z
        if x>=2 and x<=6 and y>=2 and y<=6:
            opp_cnt += 1 
    
    
    return float(own_cnt-opp_cnt)   
"""
===============================================================================
"""

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.
    ********************  DO NOT MODIFY THIS CLASS  ********************
    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)
    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.
    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

"""
===============================================================================
"""

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************
        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.
        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move
    
    def minimax(self, game, depth):    
        """Implement depth-limited minimax search algorithm as described in
        the lectures.
        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md
        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.
            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        #TODO: finish this function!
        legal_moves = game.get_legal_moves()
        
        best_score = float("-inf")
        best_move= (-1,-1)

        for move in legal_moves:
            score = self.min_value(game.forecast_move(move),depth-1)
            if score>best_score:
                best_score = score
                best_move = move
                
        return best_move

       
    def max_value(self,game,depth):
       if self.time_left() < self.TIMER_THRESHOLD:
           raise SearchTimeout()

       legal_moves = game.get_legal_moves()

       if depth==0 or not legal_moves:
           return self.score(game,self)
      
       best_score = float("-inf")
       for move in legal_moves:
           score = self.min_value(game.forecast_move(move),depth-1)
           if score >= best_score:
               best_score = score
       return best_score
   
           
    def min_value(self,game,depth):     
       if self.time_left() < self.TIMER_THRESHOLD:
           raise SearchTimeout()
       
       legal_moves = game.get_legal_moves()
       
       if depth==0 or not legal_moves:
           return self.score(game,self)
       
       best_score = float("inf")
       for move in legal_moves:
           score = self.max_value(game.forecast_move(move),depth-1)
           if score <= best_score:
               best_score = score       
       return best_score

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """
    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.
        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.
        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        
        self.time_left = time_left

        move = (-1,-1)

        try:
            depth = 1
            while True:
                move = self.alphabeta(game, depth)
                depth += 1
        except SearchTimeout:
            return move
        return move
        
        
    def alphabeta(self, game, depth):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.
        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md
        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers
            Initial values of alpha =-inf  beta =+inf
        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.
            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
    
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        
        # TODO: finish this function!
        best_move = (-1,-1) 
        best_score= float("-inf")

        
        alpha = float("-inf")
        beta = float("inf")

        legal_moves = game.get_legal_moves()
        if not legal_moves: 
            return best_move
        new_score= float("-inf")
        for move in legal_moves:  
            alpha = max(alpha,new_score)
            new_score = self.min_value2(game.forecast_move(move),depth-1,alpha,beta)
    
            if new_score >= best_score:
                best_score = new_score
                best_move = move
                
        return best_move

    def max_value2(self,game,depth,alpha,beta):
        
        if self.time_left() < self.TIMER_THRESHOLD: raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        
        #if not legal_moves: return self.score(game,self)
           
        if depth == 0: return self.score(game,self)

        new_score = float("-inf")
        
        for move in legal_moves:
            new_score = max(new_score,self.min_value2(game.forecast_move(move),depth-1,alpha,beta))

            if new_score >= beta:
                return new_score
            alpha = max(alpha,new_score)
        return new_score
        
        
    def min_value2(self,game,depth,alpha,beta):
        if self.time_left() < self.TIMER_THRESHOLD: raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        
        #if not legal_moves: return self.score(game,self)
           
        if depth == 0: return self.score(game,self)

        new_score = float("inf")
        
        for move in legal_moves:
            new_score = min(new_score,self.min_value2(game.forecast_move(move),depth-1,alpha,beta))

            if new_score <= alpha:
                return new_score
            beta = min(beta,new_score)
        return new_score