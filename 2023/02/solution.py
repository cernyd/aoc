# Red, green, blue
cube_limits = [12, 13, 14]

games_possible = 0
set_powers = 0
with open("cubes.txt", "r") as file:
    for game_id, game in enumerate(map(str.strip, file.readlines()), start=1):
        if not game:
            continue

        # Red, green, blue
        cubes_counted = [0, 0, 0]
        _, cubes = game.split(":")

        token_value = 0
        for token_i, token in enumerate(cubes.split()):
            # Even tokens represent cube counts
            if token_i % 2 == 0:
                token_value = int(token)
            # Odd tokens represent colors
            else:
                # Not bothering with parsing the colors precisely,
                # will just check for the presence of target words
                if "red" in token:
                    cubes_counted[0] = max(cubes_counted[0], token_value)
                elif "green" in token:
                    cubes_counted[1] = max(cubes_counted[1], token_value)
                elif "blue" in token:
                    cubes_counted[2] = max(cubes_counted[2], token_value)
                else:
                    raise ValueError()

                token_value = 0

        # If no cube counts are greater than cube limits (part 1)
        if not any([cnt > limit for cnt, limit in zip(cubes_counted, cube_limits)]):
            print(f"POSSIBLE game {game_id}: {cubes_counted} {cubes}")
            games_possible += game_id
        else:
            print(f"IMPOSSIBLE game {game_id}: {cubes_counted} {cubes}")

        # Power of minimum cube counts that could be in the bag (part 2)
        set_powers += cubes_counted[0] * cubes_counted[1] * cubes_counted[2]


print(f"Games possible sum: {games_possible}")
print(f"Set powers: {set_powers}")
