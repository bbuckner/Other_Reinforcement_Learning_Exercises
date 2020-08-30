import random
import time

"""
Starts are always random due to the nature of blackjack.
As the number of episodes approaches infinity, all states will be visited.
Cards are drawn with replacement to simulate an infinitely large deck.
No splitting your hand, no counting cards.
Since there is only 1 agent playing against 1 dealer, I did not create a player or dealer class.
"""

# Create a deck of cards, only kind is needed for blackjack
class Card:
	def __init__(self, kind):
		self.kind = kind
	def __str__(self):
		return str(self.kind)

class Blackjack_Environment():

	def __init__(self, dealerSticks):
		self.dealerSticks = dealerSticks
		self.deck = self.create_deck()

	def create_deck(self):
		face = ["Ace", 10, 10, 10]
		numbers = []
		for i in range(2, 11):
			numbers.append(i)
		kinds = face + numbers
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

	def play_hand(self):
		states = []
		actions = []
		returns = []
		# Set up game
		dealerShowing = random.choice(self.deck)

		playerCards = [random.choice(self.deck), random.choice(self.deck)]
		playerSum = 0
		useableAce = False
		for card in playerCards:
			playerSum, useableAce, over21 = self.process_card(playerSum, useableAce, card)
		states.append((dealerShowing.kind, playerSum, useableAce))

		print("The dealer is showing: " + str(dealerShowing))
		print("Your sum is: " + str(playerSum))
		print("Player has useable ace: " + str(useableAce))
		time.sleep(2)

		# Start playing
		while True:
			playerChoices = ["hit", "stick"]
			playerChoice = random.choice(playerChoices)
			print(playerChoice)
			actions.append(playerChoice)

			if playerChoice == "hit":
				time.sleep(2)
				card = random.choice(self.deck)
				playerSum, useableAce, over21 = self.process_card(playerSum, useableAce, card)
				print("You got: " + str(card.kind))
				print("Your sum is: " + str(playerSum))
				print("Player has useable ace: " + str(useableAce))
				if over21:
					print("You Lose")
					returns.append(-1)
					return states, actions, returns
				states.append((dealerShowing.kind, playerSum, useableAce))
				returns.append(0)
			else:
				time.sleep(2)
				break

		useableAce = False
		dealerSum = 0
		dealerSum, useableAce, over21 = self.process_card(dealerSum, useableAce, dealerShowing)
		while dealerSum < self.dealerSticks:
			card = random.choice(self.deck)
			dealerSum, useableAce, over21 = self.process_card(dealerSum, useableAce, card)
		print("Dealers sum is: " + str(dealerSum))
		if over21:
			print("You Win")
			returns.append(1)
		elif dealerSum < playerSum:
			print("You Win")
			returns.append(1)
		elif dealerSum == playerSum:
			print("Draw")
			returns.append(0)
		elif dealerSum > playerSum:
			print("You Lose")
			returns.append(-1)

		time.sleep(2)
		print()
		return states, actions, returns


env = Blackjack_Environment(17)
states, actions, returns = env.play_hand()
print(states)
print(actions)
print(returns)



