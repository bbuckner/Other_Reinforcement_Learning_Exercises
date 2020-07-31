def main():
	global world1, world2, rows, cols

	rows, cols = (4, 4)

	def create_world_grid(initial_value):
		return [[initial_value.copy() for i in range(cols)] for j in range(rows)]

	world1 = [[0 for i in range(cols)] for j in range(rows)]
	world2 = [[0 for i in range(cols)] for j in range(rows)]

	rewards = [[-1 for i in range(cols)] for j in range(rows)]
	for i in range(3):
		rewards[0][i + 1] = -10
		rewards[2][i] = -10

	action_probs = {"Up" : .25, "Down": .25, "Left" : .25, "Right" : .25}
	policy1 = create_world_grid(action_probs)
	policy1[0][0] = {"Up" : 0, "Down": 0, "Left" : 0, "Right" : 0}

	policy_iteration(rewards, policy1, 2)

def iterative_policy_evaluation(rewards, policy, theta = .001):
	global world1, world2, rows, cols
	max_delta = 1
	while (max_delta > theta):
		max_delta = 0
		for i in range(rows):
			for j in range(cols):

				# Handling edge cases to avoid array out of bounds
				up = True
				down = True
				left = True
				right = True
				if i - 1 < 0:
					up = False
				if i + 1 > rows - 1:
					down = False
				if j - 1 < 0:
					left = False
				if j + 1 > cols - 1:
					right = False

				# Update world2 using uniform random prob
				temp = 0
				if up:
					temp += policy[i][j]["Up"] * (world1[i - 1][j] + rewards[i - 1][j])
				else:
					temp += policy[i][j]["Up"] * (world1[i][j] + rewards[i][j])

				if down:
					temp += policy[i][j]["Down"] * (world1[i + 1][j] + rewards[i + 1][j])
				else:
					temp += policy[i][j]["Down"] * (world1[i][j] + rewards[i][j])

				if left:
					temp += policy[i][j]["Left"] * (world1[i][j - 1] + rewards[i][j - 1])
				else:
					temp += policy[i][j]["Left"] * (world1[i][j] + rewards[i][j])

				if right:
					temp += policy[i][j]["Right"] * (world1[i][j + 1] + rewards[i][j + 1])
				else:
					temp += policy[i][j]["Right"] * (world1[i][j] + rewards[i][j])

				# Don't update the destination node
				if (i == 0 and j == 0):
					continue
				else:
					world2[i][j] = temp
					delta = abs(world2[i][j] - world1[i][j])
					if delta > max_delta:
						max_delta = delta

		world1 = [row[:] for row in world2]

def iterative_policy_improvement(rewards, policy):
	global world1, world2, rows, cols

	for i in range(rows):
		for j in range(cols):

			# Don't update the destination node
			if (i == 0 and j == 0):
				continue

			# Handling edge cases to avoid array out of bounds
			up = True
			down = True
			left = True
			right = True
			if i - 1 < 0:
				up = False
			if i + 1 > rows - 1:
				down = False
			if j - 1 < 0:
				left = False
			if j + 1 > cols - 1:
				right = False

			# Update policies greedily (choose the direction with the least negative reward)
			# In this function, greedy ties are broken randomly
			if up:
				up_val = world2[i - 1][j] + rewards[i - 1][j]
			else:
				up_val = world2[i][j] + rewards[i][j]

			if down:
				down_val = world2[i + 1][j] + rewards[i + 1][j]
			else:
				down_val = world2[i][j] + rewards[i][j]

			if left:
				left_val = world2[i][j - 1] + rewards[i][j - 1]
			else:
				left_val = world2[i][j] + rewards[i][j]

			if right:
				right_val = world2[i][j + 1] + rewards[i][j + 1]
			else:
				right_val = world2[i][j] + rewards[i][j]

			action_vals = [up_val, down_val, left_val, right_val]
			maxVal = max(action_vals)
			maxIndicies = [i for i, val in enumerate(action_vals) if val == maxVal]
			prob = 1 / len(maxIndicies)
			action_probs = {"Up" : 0, "Down": 0, "Left" : 0, "Right" : 0}

			for index in maxIndicies:
				if index == 0:
					action_probs["Up"] = prob
				if index == 1:
					action_probs["Down"] = prob
				if index == 2:
					action_probs["Left"] = prob
				if index == 3:
					action_probs["Right"] = prob

			policy[i][j] = action_probs.copy()


def print_grid(grid):
	for row in grid:
		print(row)

def reformat_policy(policy):
	lite_view = [row[:] for row in policy]
	for i in range(rows):
		for j in range(cols):
			temp = ""
			if policy[i][j]["Left"]:
				temp += "<"
			if policy[i][j]["Up"]:
				temp += "^"
			if policy[i][j]["Right"]:
				temp += ">"
			if policy[i][j]["Down"]:
				temp += "v"
			lite_view[i][j] = temp
	return lite_view

def policy_iteration(rewards, policy, iter):
	global world2
	for i in range(iter):
		iterative_policy_evaluation(rewards, policy)
		print_grid(world2)
		iterative_policy_improvement(rewards, policy)
		print_grid(reformat_policy(policy))
		print()

main()