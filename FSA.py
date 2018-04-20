import numpy as np

from enum import Enum
class Action(Enum):
    x_rotate = 'x'
    y_rotate = 'y'
    z_rotate = 'z'
    


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
    X - VxB -> V such that x([t], b) == [bt]
    '''
    V = P

    X = [[None]]

    print(np.array(X).shape)
    print(X)
    t = 0
    b = 0
    while X[t][b] is None:
        n = 0
        for s in V:
            if not Oracle(s, (B[n], V[t])):
                n = n + 1
                if n >= len(B):
                    break
        for i in range(0, n):
            print(B[i])
            print(V[t])
            V.append([B[i] + V[t]])
            X[B[i-1]t][b] = b[i]t
        #X[b[n-1]t][b] = s
    return V, X
            

def Oracle(a, bt):
    b = bt[0]
    t = bt[1]
    return False




B = ['x', 'y', 'z']

P = ['x']
V, X = infer(P, B, Oracle)
print("finished")
