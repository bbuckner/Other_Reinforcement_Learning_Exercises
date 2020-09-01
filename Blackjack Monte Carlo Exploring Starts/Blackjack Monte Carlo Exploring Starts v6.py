import random
from copy import deepcopy

"""
Blackjack, Every Visit Monte Carlo, Exploring Starts
Starts are always random due to the nature of blackjack.
As the number of episodes approaches infinity, all states will be visited.
Cards are drawn with replacement to simulate an infinitely large deck, this prevents counting cards.
No splitting your hand.
Since there is only 1 agent playing against 1 dealer, I did not create a player or dealer class.
"""

class Agent():

	def __init__(self, dealerSticks, episodes):
		self.episodes = episodes
		self.ua_policy, self.nua_policy = Agent.train(dealerSticks, episodes)

	@staticmethod
	def train(dealerSticks, episodes):
		env = BJE(dealerSticks)
		q = {}
		p = {}
		for i in range(episodes):
			states, actions, returns = env.episode()
			g = 0
			for j in range(len(states) - 1, -1, -1):
				g = returns[j]
				s = " ".join(str(i) for i in states[j])
				q[s] = q.get(s, {"stick" : [0,0], "hit" : [0,0]})
				a = actions[j]
				q[s][a][1] += 1
				q[s][a][0] = q[s][a][0] + ((g - q[s][a][0]) / q[s][a][1])
		for s in q:
			if q[s]["stick"][0] > q[s]["hit"][0]:
				p[s] = "stick"
			else:
				p[s] = "hit"

		ua_policy = [[0 for i in range(1, 11)] for j in range(1, 22)]
		nua_policy = [[0 for i in range(1, 11)] for j in range(1, 22)]

		for s, a in p.items():
			s = s.split(" ")
			if s[0] == "Ace":
				dealerShowing = 1
			else:
				dealerShowing = int(s[0])
			playerSum = int(s[1])
			useableAce = s[2]
			if useableAce == "True":
				ua_policy[playerSum - 1][dealerShowing - 1] = a
			else:
				nua_policy[playerSum - 1][dealerShowing - 1] = a

		return deepcopy(ua_policy), deepcopy(nua_policy)

# Short for Blackjack_Environment
class BJE():

	deck = []
	face_cards = ["Ace", 10, 10, 10]
	number_cards = []
	for i in range(2, 11):
		number_cards.append(i)
	deck = (face_cards + number_cards) * 4
	del(face_cards, number_cards)

	playerChoices = ["hit", "stick"]

	def __init__(self, dealerSticks):
		self.dealerSticks = dealerSticks

	def episode(self):
		states = []
		actions = []
		returns = []
		# Set up 1 hand

		dealerShowing = random.choice(BJE.deck)

		playerCards = [random.choice(BJE.deck), random.choice(BJE.deck)]
		playerSum = 0
		useableAce = False
		for card in playerCards:
			playerSum, useableAce, over21 = BJE.process_card(playerSum, useableAce, card)
		states.append([dealerShowing, playerSum, useableAce])

		# Play 1 hand
		while True:
			# Every player choice is equally probably to maintain exploring starts.
			playerChoice = random.choice(BJE.playerChoices)
			actions.append(playerChoice)

			if playerChoice == "hit":
				card = random.choice(BJE.deck)
				playerSum, useableAce, over21 = BJE.process_card(playerSum, useableAce, card)
				if over21:
					returns.append(-1)
					return states, actions, returns
				states.append([dealerShowing, playerSum, useableAce])
				returns.append(0)
			else:
				break

		# Dealer finishes his hand according to parameter self.dealerSticks, no policy required.
		useableAce = False
		dealerSum = 0
		dealerSum, useableAce, over21 = BJE.process_card(dealerSum, useableAce, dealerShowing)
		while dealerSum < self.dealerSticks:
			card = random.choice(BJE.deck)
			dealerSum, useableAce, over21 = BJE.process_card(dealerSum, useableAce, card)
		if over21:
			returns.append(1)
		elif dealerSum < playerSum:
			returns.append(1)
		elif dealerSum == playerSum:
			returns.append(0)
		elif dealerSum > playerSum:
			returns.append(-1)

		return states, actions, returns

	@staticmethod
	def process_card(currentSum, useableAce, card):
		if card == "Ace":
			if currentSum + 11 <= 21:
				useableAce = True
				currentSum += 11
			else:
				currentSum += 1
		else:
			currentSum += card
		over21 = False
		if currentSum > 21:
			if useableAce:
				useableAce = False
				currentSum -= 10
			else:
				over21 = True
		return currentSum, useableAce, over21

def main():
	agent1 = Agent(17, 1000000)

	for i in range(20, 10, -1):
		print(agent1.ua_policy[i])

	print()

	for i in range(20, 10, -1):
		print(agent1.nua_policy[i])

main()














