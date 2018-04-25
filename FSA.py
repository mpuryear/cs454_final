import os
import numpy as np
from enum import Enum
    
class Board():
    def __init__(self, filename):
        self.filename = filename
    def apply_basic_moves(moves):
        # Do Something Public
        pass
    def __apply_basic_moves(moves):
        # Do Something Private
        pass
    def __load_random_board():
        # Do Something
        pass
    def compare(board):
        # Do Something
        pass

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
    i = 0
    for b in B:
        V[b] = i
        i += 1
        
    print(V)
    # start with an undefined update graph with each Predicate Vertex
    X = []
    for a in range(len(B)):
        row = np.ones((len(B)), dtype='int')
        row *= -1
        X.append(list(row))
    
    print(X)

    for t in list(V):
        print(V[t])
        for b in range(len(B)):
            while X[V[t]][b] == -1:
                n = 1
                b_n = ['', B[b]]
                b_i = ['']
                for s in list(V):
                    print('s in V: ' + str(s))
                    # if not s === (b^n)t
                    while True:#not Oracle(s, (b_n[n], t)):
                        if n == 2:
                            break
                        n = n + 1
                        b_n.append(b_n[n-1] + B[b])
                        print(n)


                    for i in range(1, n):
                        # vertex doesnt exist in update graph, so add it
                        b_i.append(b_i[i-1] + B[b])
                    
                        V[b_i[i] + t] = len(V) # V = V union {[b^i t]}
                        # add the edge to the newly added vertex
    was_unioned = True
    while True:
        if not was_unioned:
            break
        was_unioned = False
        for t in list(V):
            print(V[t])
            for b in range(len(B)):
                while X[V[t]][b] == -1:
                    n = 1
                    b_n = ['', B[b]]
                    b_i = ['']
                    for s in list(V):
                        print('s in V: ' + str(s))
                        # if not s === (b^n)t
                        while not Oracle(s, b_n[n-1] + t):
                            n = n + 1
                            b_n.append(b_n[n-1] + B[b])


                        for i in range(1, n):
                            # vertex doesnt exist in update graph, so add it
                            b_i.append(b_i[i-1] + B[b])
                            
                            V[b_i[i] + t] = len(V) # V = V union {[b^i t]}
                            was_unioned = True 
                            # add the edge to the newly added vertex
                            '''
                            print('X: '+ str(X))
                            print('V: ' + str(V))
                            print('b_i:' + str(b_i[i]))
                            print('b_i-1: ' + str(b_i[i-1]))
                            print('i: ' + str(i))
                            print('b: ' + str(b))
                            print('t: ' + str(t))
                            print('V[b_i[i-1] + t]: ' + str(V[b_i[i-1]+t]))
                            '''
                            if len(X) <= V[b_i[i-1] + t]:
                                X.append([-1, -1, -1])
                            X[V[b_i[i-1] + t]][b] = V[b_i[i] + t]
                        '''
                        # our s === (b^n)t
                        print('t: ' + str(t))
                        print('n: ' + str(n))
                        print('b_n-1: ' + str(b_n[n-1]))
                        print('V[s] @ b_n: '+ str(V[s]))
                        print('V[b_n[n-1] + t]: ' + str(V[b_n[n-1] + t]))
                        '''
                        if len(X) <= V[b_n[n-1] + t]:
                            X.append([-1, -1, -1])
                        X[V[b_n[n-1]+t]][b] = V[s]
    print(X)
    return V, X
            

def Oracle(s, t):
    return False 




B = ['x', 'y', 'z']

'''
P = dict()
for i in B:
    for j in range(int(i), int(i) + 2):
        P.setdefault(j, []).append(i)
'''
P = []
V, X = infer(P, B, Oracle)
print("finished")
