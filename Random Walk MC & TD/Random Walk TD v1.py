import random
def main():
	train_MC()

def train_TD():
	r = [0, 0, 0, 0, 0, 0, 1]
	q = [0, .5, .5, .5, .5, .5, 0]
	actions1 = [0, 0, 1, 1, 0, 0, 0] # Delete when TD algorithm is correct
	actions2 = [1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1] # Delete when TD algorithm is correct
	episodes = 2
	gamma = 1
	alpha = .5
	for i in range(episodes):
		test = 0
		s_ = 3
		while True:
			s = s_
			# a = random.randint(0,1)
			if i == 0:
				a = actions1[test]
			elif i == 1:
				a = actions2[test]
			if a == 0:
				s_ = s + 1
			else:
				s_ = s - 1
			
			q[s] += alpha * (r[s_] + (gamma * q[s_]) - q[s])

			if s_ == 0 or s_ == 6:
				break

			test += 1

		print(q)

def train_MC():
	r = [0, 0, 0, 0, 0, 0, 1]
	q = [0, .5, .5, .5, .5, .5, 0]
	actions1 = [0, 0, 1, 1, 0, 0, 0] # Delete when TD algorithm is correct
	actions2 = [1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1] # Delete when TD algorithm is correct
	episodes = 2
	gamma = 1
	alpha = .5
	for i in range(episodes):
		test = 0
		states = set()
		returns = []
		g = 0
		s = 3
		while True:
			states.add(s)

			# a = random.randint(0,1)
			if i == 0:
				a = actions1[test]
			elif i == 1:
				a = actions2[test]

			if a == 0:
				s += 1
			else:
				s -= 1
			

			g += (gamma * r[s])

			if s == 0 or s == 6:
				break

			test += 1

		for s in states:
			q[s] += alpha * (g - q[s])

		print(q)

main()





