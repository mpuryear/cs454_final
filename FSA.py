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


    def __rotate_list(self, l):
        m = copy.deepcopy(l)
        for i in range(len(l[0])):
            for j in range(len(l)-1,  -1):
                m[i][len(l) - 1- j] = l[j][i]

        return m

    
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
        board[Board.bottom] = np.rot90(board[Board.bottom], k=3).tolist()
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
        board[Board.left] = np.rot90(board[Board.left], k=3).tolist()
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

        board[Board.front] = np.rot90(board[Board.front]).tolist()
        
        return board
    
    def load_random_board(self):
        board = self.__load_random_board()

    def __load_random_board(self):
        Dmax = 8
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

def fig4(P, B, Oracle):
    V = {}
    for i in range(len(P)):
        V[P[i]] = i
        
    print(V)
    # start with an undefined update graph with each Predicate Vertex
    X = []
    row_to_append = [-1 for f in range(len(B))]
    for a in range(len(V)):
        X.append(list(row_to_append))


    was_union = True
    while True:
        if not was_union:
            break
        was_union = False
        for t in list(V):
            for b in range(len(B)):
                #print('t: ' + str(t))
                #print('b: ' + str(b))
                #print('X: ' + str(X))
                while X[V[t]][b] == -1:
                    was_equiv = False
                    for s in V:
                        if Oracle(s, B[b] + t):
#                            print('s: ' + str(s))
                            X[V[t]][b] = V[s]
                            was_equiv = True
                            break
                    if not was_equiv:
                        # V = V union {[bt]}
                        V[B[b] + t] = len(V) # V = V union {[b^i t]}
                        was_union = True
                        X.append([-1,-1,-1])
#                        print('union: ' + str(V[B[b] +t]))
                        X[V[t]][b] = V[B[b] + t]
    print('v: ' + str(V))
    print('x.shape: ' + str(np.array(X).shape))
    return V, X

def infer(P, B, Oracle, start_board):
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

    T = []
    for t in V:
        T.append(t)
    row_to_append = [-1 for f in range(len(B))]
    for a in range(len(V)):
        X.append(list(row_to_append))

    print(X)

    global num_experiments
    
    for t in T:
        # O(n^2)
        print(len(T))
        for b in range(len(B)):
            while X[V[t]][b] == -1:
                num_experiments += 1
                start_s = time.time()

                s,n = while_for_all(X, V, B, B[b], t, Oracle)

                X,V = from_one_to_n(X, V, B, T, n, b, t)
                        
                # our s === (b^n)t
                if len(X) <= V[(B[b] * (n-1)) + t]:
                    X += [[-1,-1,-1]]
                X[V[(B[b] * (n - 1))+t]][b] = V[s]

                
    print('X.shape : ' + str(np.array(X).shape))
    return V, X
            

def random_walk_in_X(X, B):

    Dmax = 54
    q = 0
    w = ''

    for d in range(Dmax):
        b = random.randint(0, len(X[0]))
        if b == len(X[0]):
            break
        if q != -1: # undefined state
            q = X[q][b] # get next state 
            w = B[b] + w # append the edge to our walk
    return w

def from_one_to_n(X, V, B, T, n, b, t):

    for i in range(1, n):
        # vertex doesnt exist in update graph, so add it
        
        V[(B[b] * i) + t] = len(V) # V = V union {[b^i t]}
                  
        # add the edge to the newly added vertex
        if len(X) <= V[(B[b] * (i - 1)) + t]:
            X += [[-1,-1,-1]]
            
        T.append((B[b] * i) + t)
        X[V[(B[b] * (i - 1)) + t]][b] = V[(B[b] * i) + t]

    return X, V


def while_for_all(X, V, B, b, t, Oracle):

    
    n = 0
    list_V = list(V.keys())
    found_equiv = False
    while not found_equiv:
        # O(n^3)
        n += 1 # start with n = 1
        for s in V:
            # if not s === (b^n)t
            if Oracle(X, B, s, (b * n) + t, list_V):
                found_equiv = True
                break


    return s, n


    
def Oracle(X, B, s, t, list_V):
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
    start_time = time.time()
    Dmax = 1
    global num_senses
    global num_moves
    global num_experiments

    
    t = t[:-3] # remove the predicate from t

    num_moves += len(t)
    random_board = Board()
    # get environment into random state q
    random_board.load_random_board()


    new_start = time.time()
    # find path A in X
    # (2)
    #a = list_V[a]
    #a = a * 2
    for d in range(Dmax):
        a = random_walk_in_X(X, B)
        a_t = a+t
        a_s = a+s
        new_start = time.time()
        q = copy.deepcopy(random_board)
        q2 = copy.deepcopy(q)

        new_start = time.time()
        # apply as and at
        # O(a_s + a_t)
        q.apply_basic_moves(a_s)
        q2.apply_basic_moves(a_t)
    
        new_start = time.time()
        # compare qas and qat
        # O(1)
        a = q.get_predicate()
        b = q2.get_predicate()

        # Sense
        num_senses += 1
        if not a == b:
            return False
    new_start = time.time()

    
    return a == b




'''
Bottom of the paper
'''
def other_infer(E, V, B):
    '''
    E = environment, (V, B, delta, q0)
    V = set of equiv classes
    B = set of basic actions

    output = delta table
    '''

    S = []



def main():
    B = ['x', 'y', 'z']

    start_board = Board()
    start_board.load_random_board()
    start = time.time()
    # our predicates are each visible color.
    '''
    start_board.load_random_board()
    delta = time.time() - start
    print('time to random a board: ' + str(delta))

    start = time.time()
    b = copy.deepcopy(start_board)
    delta = time.time() - start
    print('time to copy a board: ' + str(delta))

    
    
    Dmax = 54
    num_moves = Dmax
    # choose with 50% chance to do nothing, and the other 50% chance to
    # make a random move.
    r = ''.join(random.choice(['', '', '','x', 'y', 'z']) for x in range(num_moves))
    start = time.time()
    b.apply_basic_moves(r)
    delta = time.time() - start

    print('time to apply moveset: '+ str(delta))
    
    '''
    P = start_board.get_predicate()
    V, X = infer(P, B, Oracle, start_board)
#    V, X = fig4(P, B, Oracle)
    global num_experiments
    global num_senses
    global num_moves
    print('num experiments: ' + str(num_experiments))
    print('num senses: ' + str(num_senses))
    print('num_moves: ' + str(num_moves))

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
