"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Iterate through the list to count how many X's & O's 
    X_count = 0
    O_count = 0

    for i in range(0,len(board)):
        for j in range(0, len(board)):
            if board[i][j] == "X":
                X_count += 1
            elif board[i][j] == "O":
                O_count += 1

    # Return X when equal count or less than O
    if O_count < X_count: return "O"  
    else: return "X"

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board. i are the rows
    """
    actions = set()

    for i in range(0,len(board)):
        for j in range(0, len(board)):

            # Check whether the field is still empty
            if board[i][j] is None:
                actions.add((i, j))

    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    # Copy current board
    board_state = copy.deepcopy(board)
    print("RESULT FUNC State & action", board_state, action)
    # Add the action to the board for the player who's turn it is
    board_state[action[0]][action[1]] = player(board)

    # Return the new board
    return board_state

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # It would be more efficient to only iterate through fields connected to the last move
    # We would need to include the action as an arg to winner

    # Iterate through rows:
    for i in range(0,len(board)):
        j = 0
        symbol = board[i][j]

        # Save time if it's None
        if symbol is None:
            continue

        while True:
            j += 1
            if board[i][j] != symbol:
                break
            if j == (len(board) - 1): 
                print("ROW WINS")
                return board[i][j]
    
    # Iterate through columns:
    for i in range(0,len(board)):
        j = 0
        symbol = board[j][i]

        # Save time if it's None
        if symbol is None:
            continue

        while True:
            j += 1
            if board[j][i] != symbol:
                break
            if j == (len(board) - 1): 
                print("COL WINS")
                return board[j][i]

    # Iterate through diagonals: 
    i = 0
    j = 0
    symbol = board[i][j]

    if symbol is not None:
        while True:
            j += 1
            i += 1
            if board[i][j] != symbol:
                break
            if j == (len(board) - 1): 
                print("DIAG1 WINS")
                return board[j][i]

    i = len(board) - 1
    j = 0
    symbol = board[i][j]

    if symbol is not None:
        while True:
            i -= 1
            j += 1
            if board[i][j] != symbol:
                break
            if j == (len(board) - 1): 
                print("DIAG2 WINS")
                return board[j][i]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Check if somebody has won
    print("Checking winner;")
    if winner(board) is not None:
        print("Winner returned true")
        return True

    print("Winner is None")
    # Check if draw by checking for remaining actions
    if len(actions(board)) == 0: 
        print("ACTIONS are 0")
        return True
    print("Actions are not 0")

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == "X":
        print("Returning 1")
        return 1
    elif winner(board) == "O":
        print("Returning -1")
        return -1
    else:
        print("Returning 0")
        return 0

    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    We will have to call the function itself again
    """

    # Get the utility for the board 
    if terminal(board) == True:
        return utility(board)

    # Get solve with Alpha -20 & Beta 20
    action = solve(board, -20, 20)[1]

    print("Proposed action: ", action)

    return action



def solve(board, alpha, beta): 


    if terminal(board) == True:
        v_list = [utility(board), None]
        return v_list

    print("Determining player")
    # Find out who is the current player:
    if player(board) == "X":

        # We make v a list of the score and the action
        v_max = [-20, None]

        for action in actions(board):

            # Store the utility of the current action
            util = solve(result(board,action), alpha, beta)[0]

            print("UtilX: ", util)

            # We only update v if this action improves our result!
            if util > v_max[0]:
                v_max[0] = util
                v_max[1] = action

                alpha = max(util, alpha)

                if alpha >= beta:
                    break


        return v_max


    if player(board) == "O":

        v_min = [20, None]

        for action in actions(board):
            
            # Store the utility of the current action
            util = solve(result(board, action), alpha, beta)[0]


            print("UtilO: ", util)

            # We only update v if this action improves our result -- which shall be smaller!!
            if util < v_min[0]:
                v_min[0] = util
                v_min[1] = action

                beta = min(util, beta)
                if alpha >= beta:
                    break

        return v_min

    
            