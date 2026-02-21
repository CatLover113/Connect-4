from Board import Board
from MCTS import MCTS
from Node import Node
import time



def human_play(game, currentplayer):
    print("Make a move by choosing your coordinates to play.")
    print("enter column (1-7) or ask for hint by typing 'hint or 'q' to quit:")
    userInput = input()
    if userInput == 'hint':
        best_move = get_hint(game, currentplayer)
        print("Best move according to the AI would be: ", best_move)
        return int(input("Enter column (1-7): ")) - 1
    elif userInput == 'q':
        return -1
    else:
        return int(userInput) - 1

def get_hint(game, currentplayer):
        temporaryGame = game
        root = Node(temporaryGame, None) #Current game after player makes move
        mcts = MCTS(root, currentplayer)
        best_node = mcts.best_move()
        move = best_node.board.last_move_column
        return move + 1



def human_vs_human():
    game = Board()
    player = "X"
    game_is_over = False

    while not game.is_board_full() and not game_is_over:
        player = "O" if player == "X" else "X"
        game.print_board()
        print(f"It is now {player}'s turn!")
        col = human_play(game, player)

        if col == -1:
            break

        if not game.is_legal_move(col):
            print("\nWarning: Invalid Move. Try again!")
        else:
            game.make_move(col, player)

        game_is_over = game.is_won(col, player)
        
    game.print_board()
    if col == -1:
        print("Match abandonded")

    elif game.is_tie():
        print("It's a tie!")
    
    else:
        print(f"Player {player} has won!\n")
        

def ai_vs_human():
    game = Board()
    ai = "O"
    human = "X"
    humanplay = True # False for AI first, True for HUMAN first

    game_is_over = False 

    while not game.is_board_full() and not game_is_over:
        player = human if humanplay else ai
        game.print_board()
        print(f"It is now {player}'s turn!")

        if humanplay:
            move = human_play(game, player)
            if not game.is_legal_move(move):
                print("\nWarning: Invalid Move. Try again!")
            else:
                game.make_move(move, human)

        else:
            root = Node(game, None) #Current game after player makes move
            mcts = MCTS(root, ai)
            start = time.time()
            best_node = mcts.best_move()
            end = time.time()
            move = best_node.board.last_move_column
            if mcts.gameOver:
                print("AI chose column :", move + 1)
                print(f"Time taken: {end - start:.2f}")
                break
            
            game.make_move(move, ai)
            print("AI chose column :", move + 1)
            print(f"Time taken: {end - start:.2f}")
        
        # After game is won
        game_is_over = game.is_won(move, player)
        humanplay = False if humanplay else True

    game.print_board()
    if game.is_tie():
        print("It's a tie!")
    else:
        print(f"Player {player} has won!\n")

def ai_vs_ai():
    game = Board()
    x = "X"
    o = "O"
    playerX = True # False for O first, True for X first

    game_is_over = False

    while (not game.is_board_full() and not game_is_over) or game.is_tie():
        currentplayer = x if playerX else o
        game.print_board()
        print(f"It is now {currentplayer}'s turn!")

# N sei se a arvore do MCTS vai fzr update do root para preservar as vitórias ou cirar um árvore de zero
        if playerX:
            root = Node(game, None)
            mcts = MCTS(root, x)
            start = time.time()
            best_node = mcts.best_move()
            move = best_node.board.last_move_column
            end = time.time()
            if mcts.gameOver:
                print("X chose column :", move + 1)
                print(f"Time taken: {end - start:.2f}")
                break
    
        else:
            root = Node(game, None)
            mcts = MCTS(root, o)
            start = time.time()
            best_node = mcts.best_move()
            move = best_node.board.last_move_column
            end = time.time()
            if mcts.gameOver:
                print("O chose column :", move + 1)
                print(f"Time taken: {end - start:.2f}")
                break

        game.make_move(move, currentplayer)
        print(f"{currentplayer} chose column :", move + 1)
        print(f"Time taken : {end - start:.2f}")
        playerX = False if playerX else True

    # After game is won
    game.print_board()
    if game.is_tie():
        print("It's a tie!")
    else:
        print(f"Player {currentplayer} has won!\n")


def run():
    print("Choose a game mode:")
    print("1. Human vs Human")
    print("2. AI vs Human")
    print("3. AI vs AI")
    game_mode = int(input("Enter the game mode number: "))

    if game_mode == 1:
        human_vs_human()
    elif game_mode == 2:
        ai_vs_human()
    elif game_mode == 3:
        ai_vs_ai()
    else:
        print("Invalid game mode selected!")
