import random
from copy import deepcopy
from Node import Node

class MCTS:
    def __init__(self, initial_state, current_player, simulation_limit=10000):
        self.root = initial_state
        self.simulation_limit = simulation_limit
        self.current_player = current_player
        self.gameOver = False


    def selection(self):
        # Traverse the tree starting from the root, choosing the best child
        # using UCT (Upper Confidence Bound) until a leaf node is reached.
        node = self.root
        while node.children:
            node = node.best_child()
        
        return node


    def expansion(self, node):
        current_player = self.current_player
        for board in node.board.get_possible_moves(current_player):
            new_node = Node(board, parent=node)
            node.add_child(new_node)


    def simulation(self, node):
        # Simulate a random playout from the given node until the game ends.
        # The simulation follows random moves until there's a winner or a tie.
        sim_board = deepcopy(node.board)
        player = "O" if self.current_player == "X" else "X"
#       sim_board.print_board()


        while not sim_board.is_board_full():            
            legal_moves = [i for i in range(sim_board.board_width) if sim_board.is_legal_move(i)]
            move = random.choice(legal_moves)
            sim_board.make_move(move, player)
#            sim_board.print_board()

            if sim_board.is_won(move, player):
#                print(player, "WON")
                return player  # Return the winner

            # Switch players
            player = "O" if player == "X" else "X"

        return "."  # It's a tie (draw)


    def backpropagation(self, node, result):
        while node is not None:
            node.visits += 1
            if result == self.current_player:
                node.wins += 1 
            elif result == ".":
                node.wins += 0.5 
            node = node.parent


    def check_for_win(self, leaf) -> bool:
        possible_moves = [i for i in range(leaf.board.board_width) if leaf.board.is_legal_move(i)]

        for i in possible_moves:
            nodeCopy = deepcopy(leaf)
            nodeCopy.board.make_move(i, self.current_player)
            if nodeCopy.board.is_won(i, self.current_player):
                leaf.board.make_move(i, self.current_player)
                self.gameOver = True
                return True
        
        return False
    
    def best_move(self):  # Main MCTS loop: run simulations, expand, simulate, backpropagate
        leaf = self.selection()
        if not leaf.children:
            self.expansion(leaf)

        if self.check_for_win(leaf):
            return leaf
            
        
        for child in leaf.children: # Visits all children at least once, remember children is a node
            result = self.simulation(child)
            self.backpropagation(child, result)

        children = leaf.children #Turn the leaf.children into a static variable

        for i in range(7, self.simulation_limit + 1):
            leaf = random.choice(children)
            result = self.simulation(leaf)
            self.backpropagation(leaf, result)

# ---------------------------------------------------
    
        for idx, child in enumerate(children):

            print(f"NODE {idx + 1} VISITS: ", child.visits)
            print(f"NODE {idx + 1} WINS: ", child.wins)
            print(f"NODE {idx + 1} UCT: ", child.get_uct_value())
    

        best_node = self.root.best_child()
     
        print("Simulations: ", i)
        print("BEST NODE VISITS: ", best_node.visits)
        print("BEST NODE WINS", best_node.wins)
        print("BEST UCT : ", best_node.get_uct_value())
        # After all simulations, return the child with the highest win rate
    

        return self.root.best_child()

