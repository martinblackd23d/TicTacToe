import random
import GameTree
import json


def display(table):
	print('-----------------------------')
	for i in range(9):
		if table[i] != -1:
			print(table[i], end='')
		if (i+1)%3 == 0:
			print('\n',end='')
		else:
			print('\t', end = '')
	print('-----------------------------')

def iswin(table):
	for i in range(3):
		if table[i*3] == table[i*3+1] == table[i*3+2]:
			return table[i*3]
		if table[i] == table[i+3] == table[i+6]:
			return table[i]
	if (table[0] == table[4] == table[8]) or (table[2] == table[4] == table[6]):
		return table[4]
	if -1 not in table:
		return 2
	return -1

class player:
	playerid = -1
	def play(this, table):
		return 0

class player_tree(player):
	def buildtree():
		pass

class player_random():
	def play(this, table):
		count = 0
		for i in range(9):
			if table[i] == -1:
				count += 1
		rnd = random.randrange(count)
		count = 0
		for i in range(9):
			if table[i] == -1:
				if count == rnd:
					return i
				count += 1

class player_perfect(player):
	def isfork(this, table, player):
		count = 0
		for i in range(9):
			if table[i] != -1:
				continue
			temp_table = table.copy()
			temp_table[i] = player
			if iswin(temp_table) == player:
				count += 1
		if count >= 2:
			return True
		else:
			return False

	def numofforks(this, table, player):
		count = 0
		for i in range(9):
			if table[i] != -1:
				continue
			temp_table = table.copy()
			temp_table[i] = player
			if this.isfork(temp_table,player):
				count += 1
		return count

	def hastwo(this, table, player):
		for i in range(9):
			if table[i] != -1:
				continue
			temp_table = table.copy()
			temp_table[i] = player
			if iswin(temp_table) == player:
				return [True, i]
		return [False, 0]

	def play(this, table):
		own = this.playerid
		opp = (this.playerid+1)%2
		ret = []
		#if own not in table and opp not in table:
		#	return 0

		for i in range(9):
			if table[i] != -1:
				continue
			temp_table = table.copy()
			temp_table[i] = own
			if iswin(temp_table) == own:
				ret.append(i)
		if len(ret) != 0:
			return ret

		for i in range(9):
			if table[i] != -1:
				continue
			temp_table = table.copy()
			temp_table[i] = opp
			if iswin(temp_table) == opp:
				ret.append(i)
		if len(ret) != 0:
			return ret

		for i in range(9):
			if table[i] != -1:
				continue
			temp_table = table.copy()
			temp_table[i] = own
			if this.isfork(temp_table, own):
				ret.append(i)
		if len(ret) != 0:
			return ret

		num = this.numofforks(table.copy(), opp)
		if num == 1:
			for i in range(9):
				if table[i] != -1:
					continue
			if this.numofforks(table.copy(), opp) == 0:
				#print('breakpoint 0')
				ret.append(i)
		if len(ret) != 0:
			return ret

		if num >= 1:
			for i in range(9):
				if table[i] != -1:
					continue
				temp_table = table.copy()
				temp_table[i] = own
				if this.numofforks(temp_table, opp) == 0 and this.hastwo(temp_table, own)[0]:
					#print('breakpoint 1')
					ret.append(i)
			if len(ret) != 0:
				return ret

			for i in range(9):
				if table[i] != -1:
					continue
				temp_table = table.copy()
				temp_table[i] = own
				temp_result = this.hastwo(temp_table, own)
				temp_table[temp_result[1]] = opp
				if temp_result[0] and not this.isfork(temp_table, opp):
					#print('breakpoint 2')
					ret.append(i)
			if len(ret) != 0:
				return ret


		if table[4] == -1:
			return [4]

		for corners in [{table[0]:0,table[8]:8}, {table[2]:2,table[6]:6}]:
			if -1 in corners and opp in corners:
				#print('break')
				ret.append(corners[-1])
		if len(ret) != 0:
			return ret
		for i in [0,2,6,8,1,3,5,7]:
			if table[i] == -1:
				ret.append(i)
		if len(ret) != 0:
			return ret

		print('no move found')
		return None
	
class player_human(player):
	def play(this, table):
		display(table)
		return input(f'\nPlayer{this.playerid}\'s move:')

class player_tablebase(player):

	def play(this, table)

def game():
	table = []
	for i in range(9):
		table.append(-1)

	player0 = player_perfect()
	player0.playerid = 0
	player1 = player_random()
	player1.playerid = 1
	players = [player0, player1]
	#table[0] = 0
	current = 0
	while True:
		#display(table.copy())
		move = int(players[current].play(table.copy()))
		if table[move] == -1:
			table[move] = current
		else:
			#print(f'\ninvalid move: {move}\n')
			break
		result = iswin(table.copy())
		if result == -1:
			pass
		else:
			#display(table.copy())
			if result == 2:
				#print('\nThe game has ended in a tie')
				return True
			if result == 0 or result == 1:
				#print(f'Player{current} has won')
				return False
			break
		current = (current+1)%2

def stats():
	result = []
	count = 0
	for i in range(1,100000000):
		icount = 0
		while not game():
			icount += 1
		count += icount
		#if game():
		#	count +=1
		#result.append(count)
	#print(sum(result)/len(result))
		print(count/i)

#stats()
#game()
if __name__ == '__main__':
	n = GameTree.node()
	n.table = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
	n.build()
	n.findmoves()
	#n.tablebase()
	#GameTree.nodes[GameTree.getid(n.table)] = n
	#n.show(True)
	#print(GameTree.numofnodes)
	#n.traverse()
	#p = player_perfect()
	#print(GameTree.nodes)
	#count = 0
	#for i in GameTree.nodes:
	#	moves = p.play(GameTree.nodes[i][0].copy())
	#	if moves != None:
	#		GameTree.nodes[i].append(moves.copy())
	#		count += 1
	#	else:
	#		break
	#with open(f'tablebase.json', 'w') as f:
	#	f.write(json.dumps(GameTree.nodes))
	#print(count)
	#print("tablebase created")


	#GameTree.check()

