# CS 454 Final Project

## Team:
Mathew Puryear, Dulce Palacios, Hayley Gerard, Boaz Cogan

## Project Description:
Through a diversity-based algorithm, our goal is infer the structure of a finite-state automaton from its input/output. Specifically we aim to replicate the results found by R, L. RIVEST AND R. E. SCHAPIRE at MIT Laboratory for Computer Science, Cambridge, Massachusetts. 

We can apply this algorithm to help a robot solve a Rubik’s Cube. We limit its interaction with the cube by only allowing it to observe three of the fifty-four tiles (a corner, edge and center tile) all from the front face. The robot is able to manipulate the front face, as well as rotate the entire cube along the x and y axes. This process will require the robot to learn from its initial moves and traverse through various states before reaching the final accepting state, where it finds the solution to the cube.

![Figure 7](https://i.imgur.com/041ehZS.png)

# Disclaimer:


## Algorithm:
### Basic Definitions and Examples
We will use an FSA instead of DFA:  
A finite-state automaton ξ is a 6-tuple (Q, B, P, q0, ẟ, γ) where:
— Q is a finite nonempty set of states. 
— B is a finite nonempty set of input symbols, also called basic actions. 
— P is a finite nonempty set of predicate symbols, also called sensations. 
— q0 a member of Q, is the initial state. 
— ẟ is a function from Q x B into Q; ẟ is called the next-state function. 
— γ is a function from Q x P into {true, false}.

An inference algorithm for permutation environments:

### Input:
P - set of predicates
B - set of basic actions
Oracle for testing if s ≡ t for any tests s and t

### Output:
V - set of equivalence classes
χ :  V x B →V such that χ([t], b) = [bt]

### Procedure:
V ← {[p] | p ∈ P}
while χ ([t], b) is undefined for some [t] ∈ V, b ∈ B do
n ← l
while (∀[s] ∈  V) bnt not ≡ s do
n ← n+l
for 1 <= i < n
V ← V ∪ {[bit]}
χ([bi-1t], b) ← [bit]
χ([bn-1t], b) ← [s] 	{where s ≡ bnt and [s] ∈  V}
end

## References:
[Diversity-based inference of finite automata](https://www.cs.princeton.edu/~schapire/papers/diversity-based-inference.pdf)
[Inference of Finite Automata Using Homing Sequences](https://pdfs.semanticscholar.org/9a62/d26420afc77543c8f17bae1b482bcb28dc66.pdf)

![Rubiks cube](https://ruwix.com/pics/mathematics-of-the-rubiks-cube-permutation-group.jpg)

![Rubiks cube](https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Rubik%E2%80%99s_cube_colors.svg/453px-Rubik%E2%80%99s_cube_colors.svg.png)
