# CS 454 Final Project

## Team:
Mathew Puryear, Dulce Palacios, Hayley Gerard, Boaz Cogan

## Project Description:
Through a diversity-based algorithm, our goal is infer the structure of a finite-state automaton from its input/output. Specifically we aim to replicate the results found by R, L. RIVEST AND R. E. SCHAPIRE at MIT Laboratory for Computer Science, Cambridge, Massachusetts. 

We can apply this algorithm to help a robot solve a Rubik’s Cube. We limit its interaction with the cube by only allowing it to observe three of the fifty-four tiles (a corner, edge and center tile) all from the front face. The robot is able to manipulate the front face, as well as rotate the entire cube along the x and y axes. This process will require the robot to learn from its initial moves and traverse through various states before reaching the final accepting state, where it finds the solution to the cube.

![Figure 7](https://i.imgur.com/041ehZS.png)

# Disclaimer:

## References:
[Diversity-based inference of finite automata](https://www.cs.princeton.edu/~schapire/papers/diversity-based-inference.pdf)
[Inference of Finite Automata Using Homing Sequences](https://pdfs.semanticscholar.org/9a62/d26420afc77543c8f17bae1b482bcb28dc66.pdf)