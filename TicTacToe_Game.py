
import copy
#============================== TicTacToe Game Class ==============================#
class TicTacToe:
    def __init__(self, player, board, AiUser, HumanUser, maximizer):
        self.board = board
        self.X_O_locations = self.extract_X_O_locations()
        self.player = player
        self.AiUser = AiUser
        self.HumanUser = HumanUser
        self.maximizer = maximizer

    # extract_X_O_locations function
    # Initially extract the all locations from board
    # Board is a 3x3 matrix
    # Board assumed as empty initially
    @staticmethod
    def extract_X_O_locations():
        locations = []
        symbol = '-'
        claimedBy = None
        for i in range(3):
            for j in range(3):
                locations.append((i,j,symbol))
        return locations
    
    # is_valid_move function
    # Check if the move is valid
    # if the move is valid return True, else False
    def is_valid_move(self, action):
        row, col = action.split()
        row = int(row)
        col = int(col)
        for loc in self.X_O_locations:
            if loc[0] == row and loc[1] == col:
                if loc[2] == '-':
                    return True # if that position is empty return True
                else:
                    return False # if that position is already filled return False
        if row < 0 or row > 2 or col < 0 or col > 2:
            return False # if the row or column is out of bound return False
    
    # valid_actions function
    # Return a list of valid actions that can be performed
    # Use is_valid_move function to check if the move is valid
    def valid_actions(self):
        valid_actions = []
        for loc in self.X_O_locations:
            action = f"{loc[0]} {loc[1]}"
            if self.is_valid_move(action) == True:
                valid_actions.append(action)
        return valid_actions    
    
    # performAction function
    # Update the given location's symbol in locations list
    # Update the board with the given symbol
    def performAction(self, action, player):
        row, col = action.split()
        row = int(row)
        col = int(col)
        is_valid = self.is_valid_move(action)
        if is_valid == False:
            print("Invalid move. Please try again.")
            return
        else:
            for i, loc in enumerate(self.X_O_locations):
                if loc[0] == row and loc[1] == col:
                    self.X_O_locations[i] = (row, col, player.capitalize())
            
            self.update_board(row, col, player)
   
    # update_board function
    # Update the board with the given symbol
    def update_board(self, row, col, player): 
        self.board[row*2+1][col*2+1] = player.capitalize()

    # isOWinner function
    # Used to check if O is the winner  
    def isOWinner(self):
        O_count = 0
        # Horizontal win check
        for row in range(3):
            for col in range(3):
                if self.board[row*2+1][col*2+1] == 'O':
                    O_count += 1
            if O_count == 3:
                return True
            O_count = 0
        # Vertical win check
        for col in range(3):
            for row in range(3):
                if self.board[row*2+1][col*2+1] == 'O':
                    O_count += 1
            if O_count == 3:
                return True
            O_count = 0
        # Diagonal win check
        if (self.board[1][1] == 'O' and self.board[3][3] == 'O' and self.board[5][5] == 'O') or (self.board[1][5] == 'O' and self.board[3][3] == 'O' and self.board[5][1] == 'O'):
            return True
       
        return False
    
    # isXWinner function
    # Used to check if X is the winner
    def isXWinner(self):
        X_count = 0
        # Horizontal win check
        for row in range(3):
            for col in range(3):
                if self.board[row*2+1][col*2+1] == 'X':
                    X_count += 1
            if X_count == 3:
                return True
            X_count = 0

        # Vertical win check
        for col in range(3):
            for row in range(3):
                if self.board[row*2+1][col*2+1] == 'X':
                    X_count += 1
            if X_count == 3:
                return True
            X_count = 0

        # Diagonal win check
        if (self.board[1][1] == 'X' and self.board[3][3] == 'X' and self.board[5][5] == 'X') or (self.board[1][5] == 'X' and self.board[3][3] == 'X' and self.board[5][1] == 'X'):
            return True
        
        return False
    # isBoardFull function
    # Used to check draw condition
    def isBoardFull(self):
        for row in range(3):
            for col in range(3):
                if self.board[row*2+1][col*2+1] == ' ':
                    return False
        return True
    
    # isTerminal function
    # Check if the game is over
    def isTerminal(self):
        if self.isOWinner() == True or self.isXWinner() == True or self.isBoardFull() == True:
            return True
        return False
    
    # utility function
    # Calculate the payoff of the game state at the end of the game (in terminal state)
    def utility(self,game):
        # Idea: Return a value that reflects the goodness of the state
        # Reaching winning condition with less symbols is better (will have higher score)
        # Reaching winning condition with more symbols is worse (will have lower score)
        # If the game is a draw, return 0
        # This difference in score will help the AI to choose the best move (better than directly returning 1, 0, -1)
        if game.maximizer == 'O': # Identify the maximizer
            if game.isOWinner() == True: # Maximizer and Winner same return positive result
                countO = 0
                for state in game.X_O_locations:
                    if state[2] == 'O':
                        countO += 1
                return 100 - countO
            elif game.isXWinner() == True: # Maximizer and Winner different return negative result
                countX = 0
                for state in game.X_O_locations:
                    if state[2] == 'X':
                        countX += 1
                return -100 - countX
            else:
                return 0
        # Same methodology above also applicable in here
        elif game.maximizer == 'X': # Identify the maximizer
            if game.isXWinner() == True:
                countX = 0
                for state in game.X_O_locations: # Maximizer and Winner same return positive result
                    if state[2] == 'X':
                        countX += 1
                return 100 - countX
            elif game.isOWinner() == True:
                countO = 0
                for state in game.X_O_locations: # Maximizer and Winner different return negative result
                    if state[2] == 'O':
                        countO += 1
                return -100 - countO
            else:
                return 0
        
    def announce_winner(game):
        print("===== Game Over! =====")
        if game.isOWinner():
            if game.AiUser == 'O':
                print("AI wins as O!")
            else:
                print("User wins as O!")
        elif game.isXWinner():
            if game.AiUser == 'X':
                print("AI wins as X!")
            else:
                print("User wins as X!")
        elif game.isBoardFull():
            print("The game is a draw.")
 #============================== AI Game Class ==============================#
class AI:
    def __init__(self, game):
        self.game = game
    # perform_ai_action function
    # Perform the best action based on the alpha-beta search algorithm
    # Use deepcopy to prevent changes in the original game
    def perform_ai_action(self, isAIMaximizer):
        _, best_action = self.alpha_beta_search(copy.deepcopy(self.game), float('-inf'), float('inf'), self.game.AiUser, isAIMaximizer)
        return best_action
    # alpha_beta_search function
    def alpha_beta_search(self, game, alpha, beta, player, isMaximizer):
        if game.isTerminal() == True:
            return game.utility(game), None

        if isMaximizer == True:
            best_action = None
            for action in game.valid_actions():
                new_game = copy.deepcopy(game) # Copy game to prevent changes in the original game
                new_game.performAction(action, player)
                new_player = 'O' if player == 'X' else 'X' # change player for recursive call
                value, _ = self.alpha_beta_search(new_game, alpha, beta, new_player, False) # send false to make it minimizer
                if alpha < value: # If value is greater than alpha, update alpha and best action
                    alpha = max(alpha, value)
                    best_action = action
                if beta <= alpha: # If beta is less than or equal to alpha, perform alpha pruning
                    return alpha, best_action
            return alpha, best_action
        
        elif isMaximizer == False:
            best_action = None
            for action in game.valid_actions():
                new_game = copy.deepcopy(game) # Copy game to prevent changes in the original game
                new_game.performAction(action, player)
                new_player = 'O' if player == 'X' else 'X' # change player for recursive call
                value, _ = self.alpha_beta_search(new_game, alpha, beta, new_player, True) # send true to make it maximizer
                if beta > value: # If value is less than beta, update beta and best action
                    beta = min(beta, value)
                    best_action = action
                if alpha >= beta: # If alpha is greater than or equal to beta, perform beta pruning
                    return beta, best_action
            return beta, best_action
        pass

board =[
    ['','---','---','---'],
    ['|',' ','|',' ','|',' ','|'],
    ['','---','---','---'],
    ['|',' ','|',' ','|',' ','|'],
    ['','---','---','---'],
    ['|',' ','|',' ','|',' ','|'],
    ['','---','---','---']
    ]

def print_board(board):
    print("    0   1   2")
    i=0
    for row in board:
        if row[0] == '|':
            print(i, end=' ')
            i+=1
        else:
            print(' ', end=' ')
        for col in row:
            print(col, end=' ')
        print()


def runGame():
    game = None
    AIuser = None
    ai = None
    isAIMaximizer = False
    print()
    print("===== Welcome to Tic Tac Toe Game! =====")
    print("Please press E to exit the game at any time.")
    print()
    print_board(board)
    preInput = True
    breakGame = False
    while preInput == True:

        print("Do you want to start first? (Y/N)")
        start = input() # Decide who will start first
        # The X will be given to maximizer and O will be given to minimizer
        # i.e. if user decide the start first, user will be X and AI will be O
        if start.capitalize() == 'E':
            breakGame = True
            print("Exiting the game...")
            break
        if start.capitalize() != 'Y' and start.capitalize() != 'N':
            print("Invalid input. Please enter Y or N.")
            continue
        
        if start.capitalize() == 'Y': # If user wants to start first
            user = 'X' # User is X
            AIuser = 'O' # AI is O
            game = TicTacToe(user, board, AIuser, user, user)
            isAIMaximizer = False # User is the maximizer
            ai = AI(game)
            print("You are X")
            preInput = False
        elif start.capitalize() == 'N': # If AI wants to start first
            user = 'O' # User is O
            AIuser = 'X' # AI is X
            game = TicTacToe(AIuser, board, AIuser, user, AIuser)
            isAIMaximizer = True # AI is the maximizer
            ai = AI(game)
            print("You are O")
            preInput = False

    while breakGame == False and game.isTerminal() == False:
        if start.capitalize() == 'Y':
            print("===== Your Turn =====")
            print("Current board:")
            print_board(board)
            print("Enter the row and column number to place your move.")
            print("Format: Row Column --> e.g. 0 1")
            print("Row Column:")
            action = input()
            if action.capitalize() == 'E':
                breakGame = True
                print("Exiting the game...")
                break
            print(f"User's move: Row: {action[0]}, Column: {action[2]}, Label, {user}") 
            game.performAction(action, user)
            print("Board after your action")
            print_board(board)
            start = 'N' # Change the turn to AI
        elif start.capitalize() == 'N':
            print("===== AI's turn =====")
            action = ai.perform_ai_action(isAIMaximizer)
            print(f"AI's move: Row: {action[0]}, Column: {action[2]}, Label, {AIuser}")
            game.performAction(action, AIuser)
            print_board(board)
            start = 'Y' # Change the turn to User
    
    if breakGame == False:   
        game.announce_winner()

if __name__ == "__main__":
    runGame()