import random
import time

"""
Blackjack, Every Visit Monte Carlo, Exploring Starts
Starts are always random due to the nature of blackjack.
As the number of episodes approaches infinity, all states will be visited.
Cards are drawn with replacement to simulate an infinitely large deck, this prevents counting cards.
No splitting your hand.
Since there is only 1 agent playing against 1 dealer, I did not create a player or dealer class.
"""

class Card:
	def __init__(self, kind):
		self.kind = kind
	def __str__(self):
		return str(self.kind)

class Blackjack_Environment():

	def __init__(self, dealerSticks):
		self.dealerSticks = dealerSticks
		self.playerChoices = ["hit", "stick"]
		self.deck = self.create_deck()

	def create_deck(self):
		face_cards = ["Ace", 10, 10, 10]
		number_cards = []
		for i in range(2, 11):
			number_cards.append(i)
		kinds = face_cards + number_cards
		deck = []
		for i in range(4):
			for kind in kinds:
				deck.append(Card(kind))
		return deck

	def process_card(self, currentSum, useableAce, card):
		if card.kind == "Ace":
			if currentSum + 11 <= 21:
				useableAce = True
				currentSum += 11
			else:
				currentSum += 1
		else:
			currentSum += card.kind
		over21 = False
		if currentSum > 21:
			if useableAce:
				useableAce = False
				currentSum -= 10
			else:
				over21 = True
		return currentSum, useableAce, over21

	def episode(self):
		states = []
		actions = []
		returns = []
		# Set up 1 hand
		dealerShowing = random.choice(self.deck)

		playerCards = [random.choice(self.deck), random.choice(self.deck)]
		playerSum = 0
		useableAce = False
		for card in playerCards:
			playerSum, useableAce, over21 = self.process_card(playerSum, useableAce, card)
		states.append([dealerShowing.kind, playerSum, useableAce])

		# Play 1 hand
		while True:
			playerChoice = random.choice(self.playerChoices)
			actions.append(playerChoice)

			if playerChoice == "hit":
				card = random.choice(self.deck)
				playerSum, useableAce, over21 = self.process_card(playerSum, useableAce, card)
				if over21:
					returns.append(-1)
					return states, actions, returns
				states.append([dealerShowing.kind, playerSum, useableAce])
				returns.append(0)
			else:
				break

		# Dealer finishes his hand according to parameter self.dealerSticks, no other policy required.
		useableAce = False
		dealerSum = 0
		dealerSum, useableAce, over21 = self.process_card(dealerSum, useableAce, dealerShowing)
		while dealerSum < self.dealerSticks:
			card = random.choice(self.deck)
			dealerSum, useableAce, over21 = self.process_card(dealerSum, useableAce, card)
		if over21:
			returns.append(1)
		elif dealerSum < playerSum:
			returns.append(1)
		elif dealerSum == playerSum:
			returns.append(0)
		elif dealerSum > playerSum:
			returns.append(-1)

		return states, actions, returns


env = Blackjack_Environment(17)
gamma = 1
q = {}
p = {}
for i in range(50000):
	states, actions, returns = env.episode()
	g = 0
	for j in range(len(states) - 1, -1, -1):
		g = (gamma * g) + returns[j]
		s = " ".join(str(i) for i in states[j])
		q[s] = q.get(s, {"stick" : [0,0], "hit" : [0,0]})
		a = actions[j]
		q[s][a][1] += 1
		q[s][a][0] += (g - q[s][a][0]) / q[s][a][1]
		if q[s]["stick"][0] > q[s]["hit"][0]:
			p[s] = "stick"
		else:
			p[s] = "hit"

for s, a in p.items():
	print(s, a)






