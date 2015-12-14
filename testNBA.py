import csv
import time

# gets the current date
def printTime():
	now = time.localtime(time.time())
	print time.strftime("%m/%d/%y", now)

class Player(object):
	name = ""
	FPG = 0
	Price = 0
	Posn = ""
	Opp = ""

	"""docstring for Player"""
	def __init__(self, Name, FPG, Price, Posn, Opp):
		self.name = Name
		self.FPG = float(FPG)
		self.Price = Price
		self.Posn = Posn
		self.Opp = Opp

	def toString(self):
		string = ""
		string += self.name + " "
		string += self.Posn + " "
		string += str(self.FPG) + " "
		string += str(self.Price)
		string += " vs " + self.Opp
		return string

	def dollarPerPoint(self):
		return round(self.Price / self.FPG, 2)

	def targetGoal(self):
		target = self.Price * 4.5 / 1000
		return target

	def reachGoal(self):
		return self.targetGoal() < self.FPG

	def percentValue(player):
		FPG = player.FPG
		print round(FPG * 100/ player.Price, 4)

def knapSack(players, money):

	def bestValue(i, j):
		if i == 0: return 0
		value, weight = players[i - 1].FPG, players[i - 1].Price
		if weight > j:
			return bestValue(i - 1, j)
		else:
			return max(bestValue(i - 1, j),
						bestValue(i - 1, j - weight) + value)
	j = money
	result = []
	for i in range(0, len(players)):
		if bestValue(i, j) != bestValue(i -1, j):
			result.append(players[i - 1])
			j -= players[i - 1][1]
	return result.reverse()



def main():
	PG = []
	SG = []
	SF = []
	PF = []
	C = []
	f =  open('NBA125.csv', 'rb')
	reader = csv.reader(f)
	reader.next()
	for row in reader:
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
	PG.sort()
	SG.sort()
	SF.sort()
	PF.sort()
	C.sort()
	players = []
	players.append(PG)
	players.append(SG)
	players.append(SF)
	players.append(PF)
	players.append(C)
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


# main()
printTime()
