import random
"""
Acronyms
MC = Monte Carlo
TD = Temporal Difference
For this project the environment was so small I just integrated it into the Agent class on the init. 
"""
def main():
	r = [0, 0, 0, 0, 0, 0, 1]
	q = [0, .5, .5, .5, .5, .5, 0]
	gamma = 1
	alpha = .5
	episodes = 2
	agent1 = Agent("Monte Carlo", 1, q, r, 1, 0.5)
	print(agent1.q)

class Agent():

	def __init__(self, algorithm, episodes, q, r, gamma, alpha):
		self.algorithm = algorithm
		self.episodes = episodes
		self.gamma = gamma
		self.alpha = alpha
		self.q = q
		self.r = r
		if algorithm == "Monte Carlo":
			self.train_MC()
		else:
			self.train_TD()

	def train_TD(self):
		for i in range(self.episodes):
			s_ = 3
			while True:
				s = s_
				a = random.randint(0,1)
				if a == 0:
					s_ = s + 1
				else:
					s_ = s - 1
				self.q[s] += self.alpha * (self.r[s_] + (self.gamma * self.q[s_]) - self.q[s])
				if s_ == 0 or s_ == 6:
					break

	def train_MC(self):
		for i in range(self.episodes):
			states = set()
			g = 0
			s = 3
			while True:
				states.add(s)
				a = random.randint(0,1)
				if a == 0:
					s += 1
				else:
					s -= 1
				g += (self.gamma * self.r[s])
				if s == 0 or s == 6:
					break
			for s in states:
				self.q[s] += self.alpha * (g - self.q[s])

main()




