solution1 = 0
solution2 = 0


def line_generator():
    with open("input.txt", "r") as file:
        yield from map(str.strip, file.readlines())


for line in line_generator():
    # PUT YOUR CODE HERE
    # put solution to part 1 to variable solution1
    # put solution to part 2 to variable solution2
    print(line)


print("=== SOLUTIONS ===")
print(f"Solution 1: {solution1}")
print(f"Solution 2: {solution2}")
