import random

# Create a deck of cards, only kind is needed for blackjack
class Card:
	def __init__(self, kind):
		self.kind = kind
	def __str__(self):
		return str(self.kind)

face = ["Ace", 10, 10, 10]
numbers = []
for i in range(2, 11):
	numbers.append(i)
kinds = face + numbers
deck = []
for i in range(4):
	for kind in kinds:
		deck.append(Card(kind))

"""
Starts are always random due to the nature of blackjack.
As the number of episodes approaches infinity, all states will be visited.
Cards are drawn with replacement to simulate an infinitely large deck.
No splitting your hand, no counting cards.
2 policys are being learned, one without a useable ace and one with a useable ace.
Since there is only 1 agent playing against 1 dealer, I did not create a player or dealer class.
"""

# Helper parameter and function
dealerSticks = 17

# For playing multiple hands
while True:
	# Set up game
	dealerShowing = random.choice(deck)

	playerCards = [random.choice(deck), random.choice(deck)]
	playerSum = 0
	useableAce = False
	for card in playerCards:
		if card.kind == "Ace":
			if playerSum + 11 <= 21:
				useableAce = True
				playerSum += 11
			else:
				playerSum += 1
		else:
			playerSum += card.kind

	print("The dealer is showing: " + str(dealerShowing))
	print("Your sum is: " + str(playerSum))
	print("Player has useable ace: " + str(useableAce))

	# Start playing
	while True:
		playerChoice = input("Would you like to hit or stick: ").lower()
		while playerChoice != "hit" and playerChoice != "stick":
			playerChoice = input("Please enter 'hit' or 'stick: ").lower()

		if playerChoice == "hit":
			card = random.choice(deck)
			if card.kind == "Ace":
				if playerSum + 11 <= 21:
					useableAce = True
					playerSum += 11
				else:
					playerSum += 1
			else:
				if playerSum + card.kind > 21:
					if useableAce:
						useableAce = False
						playerSum -= 10
				playerSum += card.kind
			print("You got: " + str(card.kind))
			print("Your sum is: " + str(playerSum))
			print("Player has useable ace: " + str(useableAce))
		else:
			break
		if playerSum > 21:
			if useableAce:
				playerSum -= 10
				useableAce = False
			else:
				print("You Lose")
				break

	if playerSum <= 21:
		useableAce = False
		dealerSum = 0
		if dealerShowing.kind == "Ace":
			useableAce = True
			dealerSum += 11
		else:
			dealerSum += dealerShowing.kind
		while dealerSum < dealerSticks:
			card = random.choice(deck)
			if card.kind == "Ace":
				if dealerSum + 11 <= 21:
					useableAce = True
					dealerSum += 11
				else:
					dealerSum += 1
			else:
				dealerSum += card.kind
		print("Dealers sum is: " + str(dealerSum))
		if dealerSum > 21:
			print("You Win")
		elif dealerSum < playerSum:
			print("You Win")
		elif dealerSum == playerSum:
			print("Draw")
		elif dealerSum > playerSum:
			print("You Lose")

	keepPlaying = input("Enter 'yes' to play again: ").lower()
	if keepPlaying != "yes":
		print("Goodbye")
		break
	print()











