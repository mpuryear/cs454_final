import os
import numpy as np
import random
import copy
import time


num_senses = 0
num_experiments = 0
num_moves = 0


class Board():

    back = 0
    left = 1
    bottom = 2
    right = 3
    top = 4
    front= 5

    def __init__(self):
        self.board = []
        # white green red blue orange pink
        colors = ['W', 'G', 'R', 'B', 'O', 'Y']
        for color in colors:
            face = [[], [], []]
            for i in range(3):
                for j in range(3):
                    face[i].append(color)
            self.board.append(face)

    def apply_basic_moves(self,moves):
        # Do Something Public
        for move in moves:
            self.__apply_basic_move(move)

    def __apply_basic_move(self, move):
        # Do Something Private
        if move == 'x':
            self.__x_move()
        elif move == 'y':
            self.__y_move()
        elif move == 'z':
            self.__z_move()

            #print('illegal move: ' + move)

    def __x_move(self):
        # rotate on the x axis
        # rotate the top/bottom
        # move every other face ccw
        board = self.board
        temp = board[Board.front]
        board[Board.front] = board[Board.left]
        board[Board.left] = board[Board.back]
        board[Board.back] = board[Board.right]
        board[Board.right] = temp
        board[Board.bottom] = np.rot90(board[Board.bottom]).tolist()
        board[Board.top] = np.rot90(board[Board.top]).tolist()
        self.board = board

    def __y_move(self):
        # rotate on the y axis
        board = self.board
        temp = board[Board.front]
        board[Board.front] = board[Board.bottom]
        board[Board.bottom] = board[Board.back]
        board[Board.back] = board[Board.top]
        board[Board.top] = temp
        board[Board.left] = np.rot90(board[Board.left]).tolist()
        board[Board.right] = np.rot90(board[Board.right]).tolist()
        self.board = board

    def __z_move(self):
        # rotate on the z axis
        board = self.board
        bottom_row = []

        # remove the bottom rows and store them in a list
        bottom_row.append(board[Board.left].pop())
        bottom_row.append(board[Board.bottom].pop())
        bottom_row.append(board[Board.right].pop())
        bottom_row.append(board[Board.top].pop())

        # move the last element to the front
        bottom_row.insert(0, bottom_row.pop())

        # replace our now moved bottom rows back into their original positions
        board[Board.top].append(bottom_row.pop())
        board[Board.right].append(bottom_row.pop())
        board[Board.bottom].append(bottom_row.pop())
        board[Board.left].append(bottom_row.pop())

        board[Board.front] =np.rot90(board[Board.front]).tolist()
        
        return board

    def load_random_board(self):
        board = self.__load_random_board()

    def __load_random_board(self):
        Dmax = 54
        num_moves = Dmax
        # choose with 50% chance to do nothing, and the other 50% chance to
        # make a random move. 
        r = ''.join(random.choice(['', '', '','x', 'y', 'z']) for x in range(num_moves))
        self.apply_basic_moves(r)
        pass

    def get_predicate(self):
        one = self.board[Board.front][1][1] # center piece
        two = self.board[Board.front][1][2] # center right
        three = self.board[Board.front][2][2] # bottom right
        return [one + two + three]
                           
    def __eq__(self, other):
        return self.__dict__ == other.__dict__




    
# Formally, an FSA M is a 6-tuple
# ξ = <Q, B, P, q0, ẟ, γ)
'''
Params:
Q : is a finite, nonempty, set of states
B : is a finite, nonempty, set of input symbols. Also called basic actions
P : is a finite, nonempty, set of predicate symbols, also called sensations
q0: a member of Q, the initial state.
ẟ : is a function from QxB into Q, ẟ is called the next-state function.
γ : is a function from QxP into {true,false}

returns: 
bool 
'''
def build_fsa(Q, B, P, q0, ẟ, γ):
    FSA = {}
    FSA['Q'] = Q
    FSA['B'] = B
    FSA['q0'] = q0
    FSA['delta'] = ẟ
    FSA['gamma'] = γ
    
    return FSA


def infer(P, B, Oracle):
    '''
    Inputs:
    P - set of predicates
    B - set of basic actions
    O - Oracle for testing is s===t for any tests s and t
    
    Outputs:
    V - set of equivalance classes
    X - VxB -> V such that X([t], b) == [bt]
    '''

    '''
    initially V consists of one equivalence class for each of the
    predicates.
    '''

    # let V be a lookup table of the form:
    # V{'x'} = 0
    # V{'y'} = 1
    # V{'z'} = 2
    # V{'xt'} = V{'x'} = 0 for some equiv class x == xt
    V = {}
    for i in range(len(P)):
        V[P[i]] = i
        
    print(V)
    # start with an undefined update graph with each Predicate Vertex
    X = []


    row_to_append = [-1 for f in range(len(B))]
    for a in range(len(V)):
        X.append(list(row_to_append))

    print(X)
    global num_experiments
    num_outerloop = 0
    global num_moves
    global num_sesnes
    was_unioned = True
    while True:
        num_outerloop += 1
        if not was_unioned:
            break
        was_unioned = False
        for t in list(V):
            for b in range(len(B)):
                if X[V[t]][b] == -1:
                    n = 1
                    b_n = ['', B[b]]
                    b_i = ['']
                    s = ['']
                    while True:
                        found_equiv = False
                        for s_ in V:
                            s = s_
                
                            # if not s === (b^n)t
                            num_experiments += 1
                            if not Oracle(s, b_n[n] + t):
                                found_equiv = False
                            else:
                                found_equiv = True
                                num_moves += n
                                break
                        if found_equiv:
                            break
                        else:
                            b_n.append(b_n[n] + B[b])
                            n = n+1

                    for i in range(1, n):
                        # vertex doesnt exist in update graph, so add it
                        b_i.append(b_i[i-1] + B[b])
                        
                        V[b_i[i] + t] = len(V) # V = V union {[b^i t]}
                        was_unioned = True 
                        # add the edge to the newly added vertex
                        if len(X) <= V[b_i[i-1] + t]:
                            X += [[-1,-1,-1]]

                        X[V[b_i[i-1] + t]][b] = V[b_i[i] + t]

                    # our s === (b^n)t
                    if len(X) <= V[b_n[n-1] + t]:
                        X += [[-1,-1,-1]]
                    X[V[b_n[n-1]+t]][b] = V[s]

#    print('V: ' + str(V))
#    print('X: ' + str(X))
    print('X.shape : ' + str(np.array(X).shape))
    print('num experiments: ' + str(num_experiments))
    print('num senses: ' + str(num_senses))
    print('num_moves: ' + str(num_moves))
    return V, X
            


def Oracle(s, t):
    '''
    determine if s and t are equivilant
    '''

    '''
    Here is the algorithm for testing if s and t are equivalent:
(1) Find a path A in the update graph from some predicate’s equivalence class
[p] to [s].
(2) Get the environment into some random state q.
(3) Execute p and at (simultaneously) to find their values in q: If qp != qat,
then halt and conclude s != t.
(4) Repeat steps (2) and (3) until confident that s === t.
    '''

    # rule 4
    Dmax = 2
    global num_senses
    num_senses += 1
    start = time.time()
    val = True
    t = t[:-3]


    for i in range(Dmax):
        
        # find path A in X
        # (2) 
        q = Board()
        q.load_random_board()
        q2 = copy.deepcopy(q)

    
        q.apply_basic_moves(s)

        # len(t) - 3 = num_moves applied
        q2.apply_basic_moves(t)

    a = q.get_predicate()
    b = q2.get_predicate()
        # sense occurs
        #val |= a == b


    #    print('Found: ' + str(a == b))
    #print('time to compare s ==t : ' + str(time.time() - start))
    #return q == q2
    return a == b



def main():
    B = ['x', 'y', 'z']

    start = time.time()
    # our predicates are each visible color.
    start_board = Board()
    start_board.load_random_board()

    P = start_board.get_predicate()
    V, X = infer(P, B, Oracle)

    print('time: ' + str(time.time() - start))


    '''
    board = Board()
    board.load_random_board()
    print(board.board)
    board2 = copy.deepcopy(board)
    print()
    board2.apply_basic_moves('x')
    print(board2.board)

    print(board.board[Board.back])
    print()
    print(board2.board[Board.left])
    print("finished")
    '''



if __name__== '__main__':
    main()
