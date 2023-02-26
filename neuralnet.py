import random
import json
import shutil
import math
tablebase = []
class node():
	self_id = 0
	inputs = {}
	weights = {}
	bias = 0
	outputs = []
	total = 0
	threshold = 0
	ishidden = False

	def __init__(this, currentid, ih):
		this.inputs = {}
		this.weights = {}
		this.outputs = []
		this.self_id = currentid
		this.ishidden = ih
		this.bias = random.random()*2 - 1
		#print(f'\tnode {this.self_id} started')
		#print(this.self_id)

	def process(this, a):
		this.total = 0
		for i in this.inputs:
			this.total += this.inputs[i] * this.weights[i]
			#if a and this.self_id == 20:
				#print(f'({this.inputs[i]}, {this.weights[i]})', end = '')
		#if a and this.self_id == 20:
			#print(f' this.total: {this.total}')
		if this.ishidden:
			this.total = 1 / (1 + math.pow(math.e, -1 * this.total))
			this.total += this.bias
	
	def propagate(this):
		for i in this.outputs:
			i.inputs[this.self_id] = this.total
			#continue
			#if this.total > this.threshold:
			#	i.inputs[this.self_id] = 1
			#else:
			#	i.inputs[this.self_id] = 0


class neuralnet():
	inputlayer = []
	midlayer = []
	outputlayer = []
	currentid = 0
	netid = 0

	def __init__(this, netid):
		this.inputayer = []
		this.midlayer = []
		this.outputlayer = []
		this.currentid = 0
		this.netid = netid
		#print(f'net {this.netid} setup started#############################')
		this.setup()


	def createinputlayer(this):
		for i in range(9):
			temp = node(this.currentid, False)
			this.currentid += 1
			this.inputlayer.append(temp)

	def createmidlayer(this):
		for i in range(9):
			temp = node(this.currentid, True)
			this.currentid += 1
			this.midlayer.append(temp)
			for j in this.inputlayer:
				j.outputs.append(temp)
				temp.weights[j.self_id] = random.random() * 2 - 1

	def createoutputlayer(this):
		for i in range(9):
			temp = node(this.currentid, False)
			this.currentid += 1
			this.outputlayer.append(temp)
			for j in this.midlayer:
				j.outputs.append(temp)
				temp.weights[j.self_id] = random.random() * 2 - 1

	def setup(this):
		this.createinputlayer()
		this.createmidlayer()
		this.createoutputlayer()

	def play(this, table, a):
		for i in range(9):
			this.inputlayer[i].total = table[i]
		for i in this.inputlayer:
			i.propagate()
		for i in this.midlayer:
			i.process(False)
			i.propagate()
		for i in this.outputlayer:
			i.process(a)
			#print(i.total)

		move = None
		weight = None
		for i in range(9):
			if table[i] != -1:
				continue
			if move == None:
				move = i
				weight = this.outputlayer[i].total
				if a:
					#print(id(this.outputlayer))
					print(id(this.outputlayer[i]))
					print(weight)
				continue
			if weight < this.outputlayer[i].total:
				move = i
				weight = this.outputlayer[i].total
		#print(move)
		return move

	def saveweights(this):
		output = [[], []]

		for i in this.midlayer:
			output[0].append([i.bias, i.weights.copy()])
		for i in this.outputlayer:
			output[1].append([i.bias, i.weights.copy()])

		with open(f'weights{this.netid}.json', 'w') as f:
			f.write(json.dumps(output))

	def setweights(this, fid = None, mutation = 0):
		if fid == None:
			fname = f'weights{this.netid}.json'
		elif fid == -1:
			fname = f'weights.json'
		else:
			fname = f'weights{fid}.json'
		l = None
		with open(fname) as f:
		#with open(f'weights.json') as f:
			l = json.loads(f.read())
		for i in range(9):
			this.midlayer[i].bias = l[0][i][0] + (random.random()*2-1)*mutation
			for j in this.midlayer[i].weights:
				this.midlayer[i].weights[j] = l[0][i][1][str(j)] + (random.random()*2-1)*mutation

		for i in range(9):
			this.outputlayer[i].bias = l[1][i][0] + (random.random()*2-1)*mutation
			for j in this.outputlayer[i].weights:
				this.outputlayer[i].weights[j] = l[1][i][1][str(j)] + (random.random()*2-1)*mutation

	def evaluate(this):
		correct = 0
		a = False
		for i in tablebase:
			table = i[0]
			moves = i[1]
			move = this.play(table, a)
			if move in moves:
				correct += 1
			a = False
		#print(correct)
		return correct


def train():
	gen = 10
	numofnets = 10
	mutationrate = 0.1
	nets = []
	bestweights = None
	scores = []
	average = 0
	#nets.append(None)
	for i in range(numofnets):
		net = neuralnet(i)
		nets.append(net)
		net.saveweights()
		net.setweights()
		print(f'net {i} setup')
	
	print('setup finished')

	for i in range(gen):
		best = 0
		score = 0
		scores = []

		for j in range(numofnets):
			temp = nets[j].evaluate()
			#print(nets[j].midlayer[0].weights)
			print(temp)
			scores.append(temp)
			if temp > score:
				score = temp
				best = j
		shutil.copy(f'G:\\New folder\\projects\\TicTacToeAI\\weights{best}.json', f'G:\\New folder\\projects\\TicTacToeAI\\weights.json')
		for j in range(numofnets):
			shutil.copy(f'G:\\New folder\\projects\\TicTacToeAI\\weights.json', f'G:\\New folder\\projects\\TicTacToeAI\\weights{j}.json')
			nets[j].setweights(-1, mutationrate*j/numofnets)
		#with open('weights2.json') as f:
		#	print(f.read())
		average = sum(scores) / numofnets
		print(f'\nGen {i} Best net: {best}, with score: {score}, average: {average}')



if __name__ == '__main__':
	with open('tablebase.json') as f:
		n = json.load(f)
		for k, v in n.items():
			tablebase.append(v)
	#net = neuralnet(0)
	#net.setup()
	#net.saveweights()
	#net.setweights()
	#t = [-1,0,0,1,1,0,1,-1,-1]
	#net.play(t)
	train()
	print(f'out of {len(tablebase)}')
	print('terminated')