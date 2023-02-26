from binascii import a2b_base64
import TicTacToeAI

numofnodes = [0,0,0,0,0,0,0,0,0,0]		#number of unique nodes
nodes = {}
current = None

#def rotate(table):
#	'''rotates table 90 degrees clockwise, returns new list'''
#	temp_table = table.copy()
#	temp_table = [temp_table[6], temp_table[3], temp_table[0], temp_table[7], temp_table[4], temp_table[1], temp_table[8], temp_table[5], temp_table[2]]
#	return temp_table
#
#def mirror(table):
#	'''mirrors table along vertical axis, returns new list'''
#	temp_table = table.copy()
#	temp_table = [temp_table[2], temp_table[1], temp_table[0], temp_table[5], temp_table[4], temp_table[3], temp_table[8], temp_table[7], temp_table[6]]
#	return temp_table
#
#def getid(table):
#	'''returns unique id for table'''
#	ids = []
#	temp_id = 0
#	temp_table = table.copy()
#	for i in range(4):		#get id, mirror, get id, rotate, repeat 4 times, get smallest id
#		temp_id = 0
#		for i in temp_table:
#			temp_id = temp_id * 10 + i + 1
#		ids.append(temp_id)
#
#		temp_id = 0
#		temp_table = mirror(temp_table)
#		for i in table:
#			temp_id = temp_id * 10 + i + 1
#		ids.append(temp_id)
#		mirror(temp_table)
#		temp_table = rotate(temp_table)
#	return min(ids)

def getid(table):
	num = 0
	for i in table:
		num *= 10
		num += i + 1
	return num

class node():
	#id = 0
	table = []
	children = []
	#canforcewin = -1
	probofwin = -1
	nextplayer = 0
	depth = 0
	best_move = None
	#worst_moves = []

	def __init__(this):		#creates new instances of default variables
		this.table = []
		this.children = []
		this.worst_moves = []
		#this.best_move = []

	def show(this, isrecursive):
		'''prints data about node, if isrecursive == True, then displays all descendand nodes as well'''
		if isrecursive:
			print('\n')
			for i in range(this.depth):
				print('\t', end = '')
			print('Table: ' + str(this.table))

			for i in range(this.depth):
				print('\t', end = '')
			print('Probability of win: ' + str(this.probofwin))

			for i in range(this.depth):
				print('\t', end = '')
			print('Next player: ' + str(this.nextplayer))

			for i in range(this.depth):
				print('\t', end = '')
			print('Depth: ' + str(this.depth))

			for i in range(this.depth):
				print('\t', end = '')
			print('Best move: ' + str(this.best_move))

			for i in range(this.depth):
				print('\t', end = '')
			print('Num of Children: ' + str(len(this.children)))
			for i in this.children:
				i.show(True)
			return

		print('Current table:')
		TicTacToeAI.display(this.table)
		print('Probability of win: ' + str(this.probofwin))
		print('Next player: ' + str(this.nextplayer))
		print('Depth: ' + str(this.depth))
		print('Best move: ' + str(this.best_move))
		print('Worst moves: ' + str(this.worst_moves))
		for i in this.children:
			for j in range(this.depth):
				print('\t', end = '')
			#print(nodes[i].table)
			print(i.table)
		print('\n')

	def traverse(this):
		'''allows user to traverse tree'''
		while True:
			this.show(False)
			which = int(input())
			if which == -1:
				return
			#nodes[this.children[which]].traverse()
			this.children[which].traverse()

	def getmove(this, table):
		for i in range(9):
			if this.table[i] != table[i]:
				return i

#	def findmoves(this):
#		'''finds best move for each game state'''
#		global nodes
#		numofchildren = len(this.children)
#		losing_moves = 0
#		chance = 0
#		if this.probofwin != -1:
#			return
#
#		for i in this.children:
#			temp = nodes[i]
#			#if temp.probofwin == -1:
#			#	temp.findmoves()
#			if temp.probofwin == this.nextplayer:
#				losing_moves += 1
#				continue
#			if temp.probofwin == (this.nextplayer+1)%2:
#				this.probofwin = (this.nextplayer+1)%2
#				this.best_move = i
#				return
#			if this.best_move == None:
#				this.best_move = i
#			#if abs(nodes[this.best_move].probofwin - (this.nextplayer+1)%2) > abs(temp.probofwin - (this.nextplayer+1)%2):
#			#	this.best_move = i
#			#chance += temp.probofwin
#		if losing_moves == numofchildren:
#			this.probofwin = this.nextplayer
#			this.best_move = this.children[0]
#			return
#		#this.probofwin = chance / numofchildren
#		this.probofwin = 0.5
#
#	def findmovesall(this):
#		global nodes
#		for j in range(9, -1, -1):
#			for i in nodes:
#				if nodes[i].depth == j:
#					nodes[i].findmoves()



#	def compare(this, table):
#		'''compares two tables, not accounting for rotation or mirroring'''
#		for i in range(9):
#			if this.table[i] != table[i]:
#				return False
#		return True
#	
#	def ismirror(this, table):
#		temp = [table[2],table[1],table[0],table[5],table[4],table[3],table[8],table[7],table[6]]
#		if this.compare(temp):
#			return True
#		return False
#
#	def isrotation(this, table):
#		temp = table.copy()
#		for i in range(4):
#			temp = [temp[6],temp[3],temp[0],temp[7],temp[4],temp[1],temp[8],temp[5],temp[2]]
#			if this.compare(temp):
#				return True
#			if this.ismirror(temp):
#				return True
#		return False

#	def build(this):
#		'''builds node and all subnodes recursively'''
#		global numofnodes
#		global nodes
#		numofnodes += 1
#		if TicTacToeAI.iswin(this.table) != -1:		#stop branch when reaching a win
#			this.probofwin = (this.nextplayer+1)%2
#			return
#		if -1 not in this.table:
#			this.probofwin = 0.5
#			return
#		#if this.depth == 2:
#		#	return
#		count = 0
#		for i in range(9):		#create possible next moves
#			if this.table[i] == -1:
#				count += 1
#		for i in range(count):
#			#if i > 0:
#			#	continue
#			#isduplicate = False
#			j = 0
#			temp = this.table.copy()
#			for k in range(9):
#				if temp[k] == -1:
#					if j == i:
#						temp[k] = this.nextplayer
#						break
#					j += 1
#			#for k in this.children:		#prune duplicate branches
#			#	if k.isrotation(temp):
#			#		isduplicate = True
#			#		break
#			#if isduplicate:
#			#	continue
#			if getid(temp) in this.children:
#				continue
#			if getid(temp) in nodes:
#				this.children.append(getid(temp))
#				continue
#			child = node()		#create child
#			child.table = temp
#			child.depth = this.depth + 1
#			child.nextplayer = (this.nextplayer+1)%2
#			#child.id = this.id + 1
#			child.build()
#			nodes[getid(temp)] = child
#			this.children.append(getid(temp))\
	def findmoves(this):
		for i in this.children:
			i.findmoves()
		if len(this.children) == 0 or this.probofwin != -1:
			return
		losing_moves = 0
		for i in this.children:
			if i.probofwin == i.nextplayer:
				losing_moves += 1
				continue
			if i.probofwin == this.nextplayer:
				#if this.probofwin != this.nextplayer:
				#	this.best_move = []
				#this.best_move.append(this.getmove(i.table))
				this.best_move = i.table
				this.probofwin = this.nextplayer
				return
			#if this.probofwin != this.nextplayer:
			#	this.best_move.append(this.getmove(i.table))
			this.best_move = i.table
		if losing_moves == len(this.children):
			this.probofwin = i.nextplayer


	def build(this):
		global numofnodes
		#global nodes
		numofnodes[this.depth] += 1
		if TicTacToeAI.iswin(this.table) != -1 and TicTacToeAI.iswin(this.table) != 2:
			this.probofwin = (this.nextplayer+1)%2
			return
		count = 0
		for i in range(9):
			if this.table[i] == -1:
				count += 1
		for i in range(count):
			j = 0
			temp = this.table.copy()
			for k in range(9):
				if temp[k] != -1:
					continue
				if j == i:
					temp[k] = this.nextplayer
					break
				j += 1
			child = node()
			child.table = temp
			child.depth = this.depth + 1
			child.nextplayer = (this.nextplayer+1)%2
			child.build()
			this.children.append(child)
			#nodes[getid(child.table)] = child.table

	def tablebase(this):
		global nodes
		#print(len(this.children))
		#print(this.nextplayer)
		#print(this.probofwin)
		#print(getid(this.table))
		if len(this.children) == 0:
			return
		if this.nextplayer != 1 and this.probofwin != 1:
			nodes[getid(this.table)] = [this.table]
		for i in this.children:
			i.tablebase()



	def play(this, table):
		pass




def check():
	print('-----------')
	l = []
	return
	for i in nodes:
		#l.append(i)
		#continue
		temp_table = []
		for j in range(9):
			temp_table.insert(0, i%10 - 1)
			i = int(i/10)
		print(temp_table)
		TicTacToeAI.display(temp_table)
	return
	print(len(l))
	for i in range(len(l)):
		for j in range(i + 1, len(l)):
			if j == i:
				print('duplicate found')
		if i >= 1000000000:
			print('number too large')







