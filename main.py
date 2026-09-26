import random
columns = 8
rows = 8
wall_limit = 4
total_boxes = columns * rows
Blue = "\033[96m"
Reset = "\033[0m"
Red = "\033[91m"
Brown = "\033[0;33m"
player_position = 0
enemy_position = 0
wall_positions = []
player = f"{Blue}<>{Reset}"
enemy = f"{Red}XX{Reset}"
wall = f"{Brown}||{Reset}"
def grid():
  for box_number in range(1, total_boxes + 1):
    if box_number == player_position:
      token = player
    elif box_number == enemy_position:
      token = enemy
    elif box_number in wall_positions:
      token = wall
    else:
      token = f"{box_number:02d}"
    if player_position > total_boxes:
      break
    if box_number % columns == 0:
        print(f"[{token}]")
    else:
        print(f"[{token}]", end=" ")
grid()
spawn = int(input("Where do you want to spawn? "))
player_position = spawn
enemy_position = random.randint(1, total_boxes)
current_column = (player_position - 1) % columns
current_row = (player_position - 1) // columns
while enemy_position == player_position:
  enemy_position = random.randint(1, total_boxes)
while True:
  if player_position > total_boxes or player_position < 1:
    print("You fell into the Abyss, doomed forever")
    break
  grid()
  move = int(input("Where would you like to move? "))
  current_column = (player_position - 1) % columns
  current_row = (player_position - 1) // columns
  target_column = (move - 1) % columns
  target_row = (move - 1) // columns
  column_difference = abs(current_column - target_column)
  row_difference = abs(current_row - target_row)
  if (column_difference + row_difference) == 1 and move != enemy_position and move not in wall_positions:
    player_position = move 
    current_column = (player_position - 1) % columns
    current_row = (player_position - 1) // columns  
  else:
    print("That is not a valid move!")
    continue
  enemy_column = (enemy_position - 1) % columns
  enemy_row = (enemy_position - 1) // columns
  next_enemy_position = enemy_position
  if enemy_column < current_column:
    next_enemy_position += 1
  elif enemy_column > current_column:
    next_enemy_position -= 1
  if next_enemy_position in wall_positions:
    random_vertical_step = random.choice([-columns, columns])
    slide_row = (enemy_position - 1) // columns
    if random_vertical_step == columns and slide_row == (rows - 1):
      next_enemy_position = enemy_position - columns
    elif random_vertical_step == -columns and slide_row == 0:
      next_enemy_position = enemy_position + columns
    else:
      next_enemy_position = enemy_position + random_vertical_step
  if next_enemy_position in wall_positions:
    next_enemy_position = enemy_position
  horiz_final_position = next_enemy_position
  next_enemy_position = enemy_position
  if enemy_row < current_row:
    next_enemy_position += columns
  elif enemy_row > current_row:
    next_enemy_position -= columns
  if next_enemy_position in wall_positions:
    random_horizontal_step = random.choice([-1, 1])
    slide_column = (enemy_position - 1) % columns
    if random_horizontal_step == 1 and slide_column == (columns - 1):
      next_enemy_position = enemy_position - 1
    elif random_horizontal_step == -1 and slide_column == 0:
      next_enemy_position = enemy_position + 1
    else:
      next_enemy_position = enemy_position + random_horizontal_step
  if next_enemy_position in wall_positions:
    next_enemy_position = enemy_position
  vert_final_position = next_enemy_position
  h_diff = horiz_final_position - enemy_position
  v_diff = vert_final_position - enemy_position
  combined_test = enemy_position + h_diff + v_diff
  if combined_test not in wall_positions:
    enemy_position = combined_test
  elif horiz_final_position not in wall_positions:
    enemy_position = horiz_final_position
  elif vert_final_position not in wall_positions:
    enemy_position = vert_final_position
  grid()
  if enemy_position == player_position:
    print("Game over, you were tagged")
    break
  place_wall = input("would you like to place a wall? ").lower()
  if place_wall == "yes":
    if len(wall_positions) < wall_limit:
      wall_place = int(input("where would you like to place the wall? "))
      wall_column = (wall_place - 1) % columns
      wall_row = (wall_place - 1) // columns
      wall_column_difference = abs(current_column - wall_column)
      wall_row_difference = abs(current_row - wall_row)
      if (wall_column_difference + wall_row_difference) == 1 and wall_place != enemy_position and wall_place not in wall_positions:
        wall_positions.append(wall_place)
    else:
      print(f"You have run out of wall, limit of {wall_limit} reached")
