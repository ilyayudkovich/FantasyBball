import csv
import time
import urllib2


# gets the current date
# this will be used to automate the process for getting the csv file
def printTime():
	now = time.localtime(time.time())
	print time.strftime("%m/%d/%y", now)

# the players object
class Player(object):
	name = "" # the string name of the player
	FPG = 0 # the average fantasy points the player earns
	Price = 0 # the price that the player costs
	Posn = "" # what position the player plays
	Opp = "" # who the opponent is

	"""docstring for Player
		intialize the values for each player
	"""
	def __init__(self, Name, FPG, Price, Posn, Opp):
		self.name = Name 
		self.FPG = float(FPG)
		self.Price = Price
		self.Posn = Posn
		self.Opp = Opp

	# a toString method that prints 
	# a players name, posn, FPG, Price, Opponent
	def toString(self):
		string = ""
		string += self.name + " "
		string += self.Posn + " "
		string += str(self.FPG) + " "
		string += str(self.Price)
		string += " vs " + self.Opp
		return string

	# the amount of dollars per point spent on a player
	def dollarPerPoint(self):
		return round(self.Price / self.FPG, 2)

	# the target goal for the player
	def targetGoal(self):
		target = self.Price * 4.5 / 1000
		return target

	# does the player reach the targetGoal
	def reachGoal(self):
		return self.targetGoal() < self.FPG

# the knapsack algorithm that will be used in determining the optimal lineup
def knapSack(players, money):

	# determines the best value between a player and the amount of money 
	# allowed to be spent
	def bestValue(i, j):
		# if i is empty, just return
		if i == 0: return 0
		# set the tuple value, weight to be FPG, Price
		value, weight = players[i - 1].FPG, players[i - 1].Price
		# if the weight is > than j
		if weight > j:
			# do not include this player
			return bestValue(i - 1, j) 
		# otherwise 
		else:
			# return the bestValue between choosing this 
			# player and not choosing this player
			return max(bestValue(i - 1, j),
						bestValue(i - 1, j - weight) + value)
	# set j to be the total money we can spend 
	j = money
	# an intialization of the final list of players
	result = []
	# for all the players
	for i in range(0, len(players)):
		# check to see if we include the final player
		if bestValue(i, j) != bestValue(i -1, j):
			# add them to the result array
			result.append(players[i - 1])
			# subtract his cost 
			j -= players[i - 1].Price
	# return the result
	return result


# the main method
def main():
	# initialize all 5 positional arrays
	PG = []
	SG = []
	SF = []
	PF = []
	C = []
	# open the csv file with all the players
	f =  open('NBA125.csv', 'rb')
	reader = csv.reader(f)
	# skip the first row because that contains all the category names
	reader.next()
	# for each player in the file
	for row in reader:
		# get all the values for each player needed and add them to the 
		# correct positional array
		Posn = row[1]
		player = Player(row[2] + " " + row[3], row[4], int(row[6]), Posn, row[9])
		if (Posn == "PG"):
			PG.append(player)
		elif (Posn == "SG"):
			SG.append(player)
		elif (Posn == "SF"):
			SF.append(player)
		elif (Posn == "PF"):
			PF.append(player)
		else:
			C.append(player)
	# sort the positional arrays based on name
	PG.sort()
	SG.sort()
	SF.sort()
	PF.sort()
	C.sort()
	# create a new array that contains all the players
	players = []
	players.append(PG)
	players.append(SG)
	players.append(SF)
	players.append(PF)
	players.append(C)
	# start printing all the players based on position
	# only if they reach their goal
	print "Printing PG's"
	for player in PG:
		if (player.reachGoal()):
			print player.toString()
			print player.dollarPerPoint()

	print "\nPrinting SG's"
	for player in SG:
		if (player.reachGoal()):
			print player.toString()
			print player.dollarPerPoint()
	print "\nPrinting SF's"
	for player in SF:
		if (player.reachGoal()):
			print player.toString()
			print player.dollarPerPoint()
	print "\nPrinting PF's"
	for player in PF:
		if (player.reachGoal()):
			print player.toString()
			print player.dollarPerPoint()
	print "\nPrinting C's"
	for player in C:
		if (player.reachGoal()):
			print player.toString()
			print player.dollarPerPoint()
	print  "\n"
	# print the result of the knapsack algorithm
	print knapsack(players, 60000)

main()
printTime()
