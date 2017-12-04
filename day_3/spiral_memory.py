'''
--- Day 3: Spiral Memory ---

You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and then counting up while spiraling outward. For example, the first few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...
While this is very space-efficient (no squares are skipped), requested data must be carried back to square 1 (the location of the only access port for this memory system) by programs that can only move up, down, left, or right. They always take the shortest path: the Manhattan Distance between the location of the data and square 1.

For example:

Data from square 1 is carried 0 steps, since it's at the access port.
Data from square 12 is carried 3 steps, such as: down, left, left.
Data from square 23 is carried only 2 steps: up twice.
Data from square 1024 must be carried 31 steps.
How many steps are required to carry the data from the square identified in your puzzle input all the way to the access port?

Your puzzle answer was 326.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

As a stress test on the system, the programs here clear the grid and then store the value 1 in square 1. Then, in the same allocation order as shown above, they store the sum of the values in all adjacent squares, including diagonals.

So, the first few squares' values are chosen as follows:

Square 1 starts with the value 1.
Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.
Once a square is written, its value does not change. Therefore, the first few squares would receive the following values:

147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...
What is the first value written that is larger than your puzzle input?

Your puzzle input is still 361527.
'''


def create_map_of_numbers_to_coordinates(position, number_limit):
	'''
	Starting from a central point of [0,0] map numbers to coordinates by spiraling
	outwards in an anticlockwise direction.
	'''
	direction = 0
	number = 1
	counter = 1
	step = 1

	numbers_to_locations_map = {}

	for i in range(1, number_limit+1):
		numbers_to_locations_map[number] = position[:]

		counter, step, direction, number = step_and_change_position(position, counter, step, direction, number)

	return numbers_to_locations_map


def step_and_change_position(position, counter, step, direction, number):
	"""
	Sorta hacky - there is probably a better way of doing this. It works by making 'steps' around
	the grid of coordinates. The algorithm works on the logic that when spiralling outwards you make
	movements composed of steps and a direction. i.e. Starting at position [0,0] you make a movement left of 1 step.
	Next you make a movement upwards of 1 step. After making these 2 movements the number of steps
	increases by 1. When making a movement to the right you will now make 2 steps to clear position
	[0,0] underneath you. Next you move downwards 2 steps. The pattern here is that each time you
	make 2 movements in a particular direction the number of steps increases by 1. Thus you have:
	Left: 1
	Up: 1
	Right: 2
	Down: 2
	Left: 3
	Up: 3
	And so on. Counter is used to see if you have made all of the steps for the current movement.
	Once the movement is complete the counter resets and step increments.

	Args:
		position (list): Current position in the grid (starts at [0, 0])
		counter (int): Used to keep track of how many steps have been made
		step (int): How many steps need to be made in the current movement.
	"""
	if direction == 0:
		position[0]+=1
		if counter == step:
			counter = 0
			# change direction from left to up
			direction+=1
	elif direction == 1:
		position[1]+=1
		if counter == step:
			counter = 0
			# change direction from up to right
			direction+=1
			# changing direction means 1 extra step
			step+=1
	elif direction == 2:
		position[0]-=1
		if counter == step:
			counter = 0

			direction+=1
	elif direction == 3:
		position[1]-=1
		if counter == step:
			counter = 0
			#
			direction = 0
			step+=1

	counter+=1
	number +=1

	return counter, step, direction, number


def create_map_of_coordinates_to_numbers(position, number_limit):
	direction = 0
	number = 1
	counter = 1
	step = 1

	locations_to_numbers_map = {}

	for i in range(1, number_limit+1):

		locations_to_numbers_map[tuple(position)] = sum_adjacent_positions(locations_to_numbers_map, position)
		# Once we find the number we're looking for we can break the loop
		if locations_to_numbers_map[tuple(position)] > number_limit:
			return locations_to_numbers_map[tuple(position)]

		counter, step, direction, number = step_and_change_position(position, counter, step, direction, number)


def sum_adjacent_positions(locations_to_numbers_map, position):
	"""
	Sum the values of all numbers located at adjacent positions in the locations_to_numbers_map dict.
	Adjacent positions are hardcoded cos there is only 8 of them and I'm too lazy to write a fun to
	find them.
	"""
	adjacent_positions = [tuple([position[0]+1, position[1]]),
						  tuple([position[0]+1, position[1]+1]),
						  tuple([position[0]-1, position[1]]),
						  tuple([position[0]-1, position[1]-1]),
						  tuple([position[0], position[1]+1]),
						  tuple([position[0], position[1]-1]),
						  tuple([position[0]-1, position[1]+1]),
						  tuple([position[0]+1, position[1]-1])]
	# Get the sum of all adjacent positions - If a position doesn't exist default to 0
	total = sum([locations_to_numbers_map.get(pos, 0) for pos in adjacent_positions])
	# If statement here handles one case (When the dict is empty on the first run)
	return total if total > 0 else 1


def calculate_manhattan_distance(start, end):
	"""
	Caculate the manhattan distance between 2 points. Pretty simple.
	"""
	return abs(start[0] + abs(end[0])) + abs(start[1] + abs(end[1]))


if __name__ == '__main__':

	position = [0, 0]
	number_limit = 361527

	number_to_coordinate_map = create_map_of_numbers_to_coordinates(position, number_limit)

	manhattan_distance = calculate_manhattan_distance([0,0], number_to_coordinate_map[361527])
	print('Part 1: Manhattan distance: {}'.format(manhattan_distance))

	larger_adjacent_number_sum = create_map_of_coordinates_to_numbers(position, number_limit)
	print('Part 2: The first larger sum is {}'.format(larger_adjacent_number_sum))
