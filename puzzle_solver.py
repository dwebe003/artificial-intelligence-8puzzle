#########################################################################################
#
#   File:       puzzle_solver.py
#   Author:     David Weber (dwebe003)
#   Date:       10/29/2017
#   Version:    1.0
#
#   Algorithms: Uniform Cost Search
#               A* with Manhattan
#               A* with Misplaced Tile
#
#   Contents:   This program implements three ways of solving an 8-puzzle (also capable of
#               solving any n-puzzle with a few changes in input/output code). It prompts
#               the user to input a puzzle (or use default) and then uses whichever selected
#               algorithm to find a solution. The three algorithms are chosen to demonstrate
#               the optimality of A* as well as the increased optimality given a better
#               heuristic.
#
#########################################################################################

import copy
import time

from pip._vendor.distlib.compat import raw_input

GOALSEQ = [1, 2, 3, 4, 5, 6, 7, 8, 0]
GOALIND = [(0, (2, 2)), (1, (0, 0)), (2, (0, 1)), (3, (0, 2)), (4, (1, 0)), (5, (1, 1)), (6, (1, 2)), (7, (2, 0)), (8, (2, 1))]

###########################################################################################################################
###########################################################################################################################

class Node:

	#initialize instance of node class
	def __init__(self, data):
		self.data = data  # puzzle data# g(n) aka depth
		self.child = [None, None, None, None]
		self.g_n = 0
		self.h_n = 0
		self.state = "notgoal"

	#calculate misplaced tile heuristic
	def h_n_misplaced(self):
		h_n = 0
		k = 0
		
		#determines which tiles in the goal state are somewhere distant in the current node state
		for i in range(len(self.data)):
			for j in range(len(self.data)):
				if self.data[i][j] != GOALSEQ[k] and self.data[i][j] != 0:
					h_n += 1
				k +=1

		if h_n == 0:
			self.state = "goal"
			
		self.h_n = h_n
		
		
	# calculate manhattan heuristic
	def h_n_manhattan(self):

		h_n = 0
		k = 0

		# checks that each entry matches GOALSEQ, if not then h(n) += | [x][y] - [i][i] |
		# where [x][y] is where the number should be and [i][j] is the
		# index where the number currently is
		for i in range(len(self.data)):
			for j in range(len(self.data)):
				if self.data[i][j] == 0:
					k = k + 1
					continue
				if self.data[i][j] != GOALSEQ[k]:
					num = self.data[i][j]
					x = GOALIND[num][1][0]
					y = GOALIND[num][1][1]
						  
					distance = abs(x - i) + abs(y - j)
					h_n = h_n + distance
				#endif
				k = k + 1
			#endfor
		#endfor

		if h_n == 0:
			self.state = "goal"
						  
		self.h_n = h_n
						  
		#enddef
		
						  
	def create_children(self, choice):
		#determine possible moves. create new Node for each move, add to queue
		blank_index = (0, 0)

		# ------ where is the blank? ------ #
		for i in range(len(self.data)):
			for j in range(len(self.data)):
				if self.data[i][j] == 0:
					blank_index = (i, j)

		i = blank_index[0]
		j = blank_index[1]


		#------- move blank right if legal -----------------------------------------------
		if j < (len(self.data) - 1):
			#right is possible
			self.child[3] = Node(self.data)
			self.child[3] = copy.deepcopy(self)

			#switch blank
			temp = self.child[3].data[i][j+1]
			self.child[3].data[i][j+1] = 0
			self.child[3].data[i][j] = temp

			#sets g(n)
			self.child[3].g_n = self.g_n + 1
			
			#sets h(n)
			if choice == 1:
				self.child[3].h_n = 0
			if choice == 2:
				self.child[3].h_n_misplaced()
			if choice == 3:
				self.child[3].h_n_manhattan()
		else:
			
			self.child[3] = None



		#------- move blank left if legal ------------------------------------------------
		if j != 0:
			#left is possible
			self.child[2] = Node(self.data)
			self.child[2] = copy.deepcopy(self)

			#switches blank
			temp = self.child[2].data[i][j-1]
			self.child[2].data[i][j-1] = 0
			self.child[2].data[i][j] = temp
			
			#set g(n)
			self.child[2].g_n = self.g_n + 1
			#sets h(n)
			if choice == 1:
				self.child[2].h_n = 0
			if choice == 2:
				self.child[2].h_n_misplaced()
			if choice == 3:
				self.child[2].h_n_manhattan()
		else:
			self.child[2] = None



		#------- move blank down if legal ------------------------------------------------
		if i < (len(self.data) - 1):
			#down is possible
			self.child[1] = Node(self.data)
			self.child[1] = copy.deepcopy(self)

			#switches blank
			temp = self.child[1].data[i+1][j]
			self.child[1].data[i+1][j] = 0
			self.child[1].data[i][j] = temp

			#sets g(n)
			self.child[1].g_n = self.g_n + 1
			
			#sets h(n)
			if choice == 1:
				self.child[1].h_n = 0
			if choice == 2:
				self.child[1].h_n_misplaced()
			if choice == 3:
				self.child[1].h_n_manhattan()
		else:
			self.child[1] = None
		

		#------- move blank up if legal -------------------------------------------------
		if i != 0:
			#up is possible
			self.child[0] = Node(self.data)
			self.child[0] = copy.deepcopy(self)

			#switches blank
			temp = self.child[0].data[i-1][j]
			self.child[0].data[i-1][j] = 0
			self.child[0].data[i][j] = temp

			#sets g(n)
			self.child[0].g_n = self.g_n + 1
			
			#sets h(n)
			if choice == 1:
				self.child[0].h_n = 0
			if choice == 2:
				self.child[0].h_n_misplaced()
			if choice == 3:
				self.child[0].h_n_manhattan()
		else:
			self.child[0] = None


	#calculates f(n) = g(n) + h(n)
	def f_n(self):
		fx = self.g_n + self.h_n
		return fx



	# calculate misplaced tile heuristic


###########################################################################################################################

def f(node):
	fx = node.g_n + node.h_n
	return fx

###########################################################################################################################

def goal_found(max_nodes, node_depth, count):
	print("GOOOOOOOOOOOOOOOOAL!!")
						  
	print('To solve this problem the search algorithm expanded a total of ', count, 'nodes.')
	print('The maximum numbers of nodes in the queue at any one time was ', max_nodes, '.')
	print('The depth of the goal node was ', node_depth, '.\n\n')
	
	return

###########################################################################################################################

def print_node(node):
		#print contents of current Node state
	
	if node is None:
		return
	else:
		for x in range(len(node.data)):
			s = ''
			for y in range(len(node.data)):
				s = s + str(node.data[x][y])
				s = s + ' '
			s = s + '\n'
			print(s)

###########################################################################################################################

# General (Generic) Search Algorithm
# altered to cooperate with python + this code's Node class
def solve_puzzle(puzzle, choice):
	#goal = None
	
	closed_list = []
	open_list = []
	
	open_list.append(Node(puzzle))
	
	max_nodes = 0
	count = 0

###########################################################

	while len(open_list) != 0:
		#pop front of list
		node = open_list.pop(0)


		#check it isn't a duplicate
		for m in range(len(closed_list)):
			if node.data == closed_list[m].data:
				node = open_list.pop(0)
		
		#check for success
		if node.state == "goal":
			goal_found(max_nodes, node.g_n, count)
			return


		#generate kids
		node.create_children(choice)
		count += 1

		#add non-null kids to open_list
		for x in range(4):
			if node.child[x] is not None:
					open_list.insert(0, node.child[x])
					
		#sort open_list by f(n) = g(n) + h(n)
		new = sorted(open_list, key=f)
		open_list = new
		
		if max_nodes < len(open_list):
			max_nodes = len(open_list)

		#add parent to closed_list list
		
		print('Expanding state with g(n) = ', node.g_n, ' and h(n) = ', node.h_n, '...\n')
		print_node(node)
		print('\n')

		closed_list.append(node)
	#endwhile

	print('Failure!')



###########################################################################################################################

def get_input():
	
	ret = list()
	input_type = input("input_type \"1\" to use the default puzzle, or \"2\" to enter your own: ")

	num = ['first', 'second', 'third']
	i = 0

	#default puzzle-------------------------------------------------------------------------------------------------------
	if input_type == 1:
		ret = [[1, 2, 3], [4, 8, 0], [7, 6, 5]]
		print('\n')
				
		print('Enter your choice of algorithm: \n', '1. Uniform Cost Search\n', '2. A* with Misplaced Tile heuristic')
		print('3. A* with Manhattan distance heuristic\n\n')
						
		choice = raw_input()
		choice = int(choice)
								
		print('\n')
		return ret, choice
	#enter your own puzzle-------------------------------------------------------------------------------------------------
	elif input_type == 2:
		
		#gets our input, checks number of arguments, stores into array 'ret'
		while i < 3:
			
			#prints message to obtain the numbers
			print('Enter the', num[i], 'row, separated by spaces: ')
			
			#retrieves line, forms array of literals
			arr = raw_input().split()
			
			#converts the literals into input_type int
			arr = [int(x) for x in arr]
			
			#checks the user has entered 3 numbers, quits otherwise
			if len(arr) > 3:
				print("Error: too many arguments")
				quit(1)
			if len(arr) < 3:
				print("Error: too few arguments")
				quit(1)
			
			#appends final array with the inputted numbers
			ret.append(arr)
			
			#increments i... while loop should execute exactly 3 times.
			i = i + 1
		#endwhile
		
		#checks matrix for duplicates
		sum = 0
		for x in range(3):
			sum += ret[0][x]
			sum += ret[1][x]
			sum += ret[2][x]
		
		if sum != 36:
			print("\nError: duplicate number detected... Try again.\n")
			get_input()
		
		print('\n')

		#offers choice of algorithm
		print('Enter your choice of algorithm: \n', '1. Uniform Cost Search\n', '2. A* with Misplaced Tile heuristic')
		print('3. A* with Manhattan distance heuristic\n\n')

		choice = raw_input()
		choice = int(choice)
			
		print('\n')

		return ret, choice
	else:
		print("error: invalid entry")
		quit(1)




###########################################################################################################################

def main():

	print("\n\n\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print("~~~~ THE NAME OF OUR BAR.... PUZZLES. PEOPLE WILL BE LIKE ~~~~\n~~~~     \"WHY IS IT CALLED PUZZLES?\" THAT'S THE PUZZLE.   ~~~~")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

	#gets puzzle to solve
	puzzle, choice = get_input()
	
	
	#runs through the search process
	start = time.clock()
	solve_puzzle(puzzle, choice)
	end = time.clock()
	
	algtime = end - start
	
	print 'This took ', str(algtime), ' seconds to complete.'

	print("\n")

if __name__ == '__main__':
	main()

