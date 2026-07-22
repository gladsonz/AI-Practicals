 
N = 4

rows = list(range(N))

def is_safe_swap(rows, col):
	for c in range(col):
		if rows[c] == rows[col] or abs(rows[c] - rows[col]) == abs(c - col):
			return False
	return True

def solve(col):
	if col >= N:
		return True

	for i in range(col, N):
		rows[col], rows[i] = rows[i], rows[col]

		if is_safe_swap(rows, col):
			if solve(col + 1):
				return True

		rows[col], rows[i] = rows[i], rows[col]

	return False

def print_solution():
	for r in range(N):
		for c in range(N):
			if rows[c] == r:
				print("Q", end=" ")
			else:
				print(".", end=" ")
		print()

if solve(0):
	print("Solution Found:\n")
	print_solution()
else:
	print("No Solution Exists")
