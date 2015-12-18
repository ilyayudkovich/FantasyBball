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

    memo = []

    # gets the best value of players up to i with budget j
    def bestValue(i,j):
        if j/100 >= len(memo) or j < 0:
            return 0
        if i >= len(memo[j/100]) or i < 0:
            return 0
        else:
            return memo[j/100][i]

    for budget in range(0, money + 100, 100):
        memo.append([])
        for player in range(0,len(players)):
            take = players[player].FPG + bestValue(player - 1, budget - players[player].Price)
            notake = bestValue(player-1, budget)
            memo[budget/100].append(max(take, notake))

    team = []

    budget = money
    picks = len(players)

    while(budget > 0 and picks > 0):
        if bestValue(picks, budget) > bestValue(picks - 1, budget):
            team.append(players[picks])
            budget = budget - players[picks].Price
        picks = picks - 1
    
    names = map(lambda x: x.name, team)
    print "team: ", names
    print "Fantasy points: ", memo[money/100][len(players) -1]

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
	players.extend(PG)
	players.extend(SG)
	players.extend(SF)
	players.extend(PF)
	players.extend(C)
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
	knapSack(players, 60000)

main()
