from scipy.stats.distributions import poisson
import numpy as np

class JCR():
	max_cars = 20
	gamma = .9
	rental_reward = 10
	move_reward = -2

class JCR_L():

	def __init__(self, rental_lam, return_lam):
		self.rental_lam = rental_lam
		self.return_lam = return_lam
		self.poisson_rental_probs = poisson_support(JCR.max_cars + 1, self.rental_lam)
		self.poisson_return_probs = poisson_support(JCR.max_cars + 1, self.return_lam)

# Location initialization
# cLX stands for "car location X" where X is a number
def main():
	global cL1, cL2, value, policy, poisson_probs
	cL1 = JCR_L(3, 3)
	cL2 = JCR_L(4, 2)
	value = np.zeros((JCR.max_cars + 1, JCR.max_cars + 1))
	policy = value.copy().astype(int)

	theta = 50
	while True:
		policy_evaluation(theta)
		p = policy_improvement()
		if p == True:
			print("Policy is stable")
			print(policy)
			break
		theta /= 10

def poisson_support(search_until, lam):
	poisson_probs = {}
	for i in range(0, search_until):
		temp = poisson.pmf(i, lam)
		if temp > .01:
			poisson_probs[i] = temp
	return poisson_probs

def expected_reward(s_curr, action):
	global cL1, cL2, value, policy, poisson_probs
	print(".", end = "")
	"""
	state : A pair of integers, # of cars at cL1 and cL2 respectively
	action : # of cars transferred from cL1 to cL2, -5 <= action <= 5
	"""

	# Account for the effect of the action taken on the current state
	s_next_temp = [max(min(s_curr[0] - action, JCR.max_cars), 0),
			       max(min(s_curr[1] + action, JCR.max_cars), 0)]

	# Account for moving penalty
	r = JCR.move_reward * abs(action) # Reward variable first initialization

	"""
	There are 4 discrete random variables that determine the probability
	distribution of the next state and associated reward.  Those being:

	cars rented at location 1
	cars rented at location 2
	cars returned at location 1
	cars returned at location 2

	In order to consider all possible next states, we must go through the permutation of
	these 4 variables and add each outcomes weighted reward to the overall expected reward.

	To be all encompassing of every meaningful number of returns and rentals possible on
	any given day, you can start from 0 (negative value in a poisson dist are 0 probability)
	and loop through the max number of cars allowed at the locations.  Cars returned 
	or rented in excess of the max number of cars are ignored for the purposes of this 
	problem (there is no negative reward associated with that) so their probabilities do 
	not contribute to the expected reward.  However it is much more efficent to only check
	possibilities where the probability of the occurance is greater than .01.
	"""
	s_next = [0,0]
	for rentals_cL1 in cL1.poisson_rental_probs:
		for rentals_cL2 in cL2.poisson_rental_probs:
			for returns_cL1 in cL1.poisson_return_probs:
				for returns_cL2 in cL2.poisson_return_probs:
					"""
					Probabilitiy of this outcome (events are independent so
					you can multiply them to get the overall probability.
					"""
					p  = cL1.poisson_rental_probs[rentals_cL1]
					p *= cL2.poisson_rental_probs[rentals_cL2]
					p *= cL1.poisson_return_probs[returns_cL1]
					p *= cL2.poisson_return_probs[returns_cL2]

					valid_rentals_cL1 = min(s_next[0], rentals_cL1)
					valid_rentals_cL2 = min(s_next[1], rentals_cL2)

					temp_r = (valid_rentals_cL1 + valid_rentals_cL2) * 10
					"""
					Calculate next state based on outcomes of the 4 events
					as well as the action that you are currently taking (latter
					is already done before the for loops)
					"""
					s_next[0] = max(min(s_next_temp[0] - valid_rentals_cL1 + returns_cL1, JCR.max_cars), 0)
					s_next[1] = max(min(s_next_temp[1] - valid_rentals_cL2 + returns_cL2, JCR.max_cars), 0)

					# Bellmans equation
					r += p * (temp_r + (JCR.gamma * value[s_next[0]][s_next[1]]))

	return r

def policy_evaluation(theta):
	global cL1, cL2, value, policy
	while True:
		max_delta = 0
		for i in range(len(value[0])):
			for j in range(len(value[1])):
				prev_value = value[i][j]
				"""
				Change the value of the state at i, j to the expected reward
				of that state given that you are in that state and taking
				action policy[i][j]
				"""
				value[i][j] = expected_reward([i,j], policy[i][j])
					
				max_delta = max(max_delta, abs(value[i][j] - prev_value))
		print(max_delta, theta)
		if max_delta < theta:
			break

def policy_improvement():
	global cL1, cL2, value, policy
	policy_stable = True
	for i in range(policy.shape[0]):
		for j in range(policy.shape[1]):

			prev_action = policy[i][j]

			max_action_value = None
			max_action = None

			# Make sure you cant move more cars than you have at one location to the other
			cL1_max_move = min(i, 5)
			cL2_max_move = -min(j, 5)
			for action in range(cL2_max_move, cL1_max_move + 1):
				v = expected_reward([i,j], action)
				if max_action_value == None:
					max_action_value = v
					max_action = action
				elif max_action_value < v:
					max_action_value = v
					max_action = action

			policy[i][j] = max_action

			if prev_action != policy[i][j]:
				policy_stable = False

	return policy_stable

main()















