# Artifical Intelligence -- 8-puzzle Solver (n-puzzle capable)

## Algorithms: 
	Uniform Cost Search
	A* with Manhattan
	A* with Misplaced Tile

## Contents:   
	This program implements three ways of solving an 8-puzzle (also capable of
	solving any n-puzzle with a few tweaks in input/output code). It prompts
	the user to input a puzzle (or use default) and then uses whichever selected
	algorithm to find a solution. The three algorithms are chosen to demonstrate
	the optimality of A* as well as the increased optimality given a better
	heuristic.
	
## Author:
	David Weber

## Date:
	October 2017
	
## TO RUN THIS PROGRAM:
	1) Open Terminal/Command Prompt
	2) Navigate to folder containing puzzleSolver.py (using cd commands)
	3) Type what is contained in these quotations: "python puzzleSolver.py"
	
## Test cases:
	Here are some test cases for you to try, other than the default:
	
	1 3 2		1 2 3		0 1 2		8 7 1		
	4 8 0		4 8 0		4 5 3		6 0 2
	7 5 6		7 6 5		7 8 6		5 4 3
	
	The one below is impossible to solve, and the AI will evaluate every node (~100,000)
	before reporting failure.
	
	1 2 3
	4 5 6
	8 7 0
