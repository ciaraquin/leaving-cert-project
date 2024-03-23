import random
import time
import csv
import os
import matplotlib.pyplot as plt


colors = {
  "reset": "\033[00m",
  "red": "\033[91m",
  "blue": "\033[94m",
}


def clear(seconds=0): #function to clear console
  time.sleep(seconds)
  os.system('clear')

def output_board(board): #function for printing board
  row = ['A','B','C','D','E','F']
  collum = 1
  print(' ', *row, sep=' ')
  for i in board:
    print(collum, (" ").join(i))
    collum = collum + 1

print(colors['blue'])
print('Welcome to battleship !\nPlease select an option from the menu below\n')
print(colors['reset'])


def single_player():
  game_type = 'single-player' #for data collection later

  print('Welcome to single-player mode!\n\nHere the computer will select a pre-set layout with three one-block ships on it\nYou must find these ships and sink them within 20 guesses in order to win\n\nGood luck !\n')

  input("\nPress Enter to continue...")
  clear(1)
  
  board = []
  pre_set_board = []

  row = ['A','B','C','D','E','F']

  #initialise hits and misses
  hit = 0
  miss = 0
  
  for j in range(len(row)): #add '....' to board
    board.append(["."] * len(row))
    pre_set_board.append(["."] * len(row))

  #coordinates for preset ships
  pre_set_boards = [[[3, 4], [0, 5], [5, 3]], [[0, 1], [5, 5], [1, 4]], [[1, 2], [5, 1], [2, 3]]] 
  board_selection = random.randint(0, 2)

  pre_set_board[pre_set_boards[board_selection][0][1]][pre_set_boards[board_selection][0][0]] = "1"
  pre_set_board[pre_set_boards[board_selection][1][1]][pre_set_boards[board_selection][1][0]] = "1"
  pre_set_board[pre_set_boards[board_selection][2][1]][pre_set_boards[board_selection][2][0]] = "1"

  guesses_left = 20 #initialise number of guesses that use has

  print("Status: Waiting for coordinate\nGuesses left:", guesses_left) #displays guesses the user has
  print('Hits:', hit)
  print('Misses:', miss)
  print('\n')
  output_board(board)
  print()
  while hit < 3 and hit + miss < 20: #while loop keeps going until hits > 3 and guesses > 20 
    guess_row = (input("\nEnter guess collumn (A-F): "))

    #data validation
    while (guess_row.upper()) not in row:
      print('Invalid entry')
      guess_row = (input("Enter guess collumn (A-F): "))
    #data validation
    while True:
      guess_col = (input("Enter guess row (1-6) : "))
      try:
        guess_col = int(guess_col)
      except ValueError:
        print('Enter a valid number')
        continue
      if 1 <= guess_col <= 6:
        break
      else:
        print('Enter a valid number: 1-6')

    #put coordinate into correct form for computer to understand
    guess_row = guess_row.upper()
    guess_row = (row.index(guess_row))
    guess_col = guess_col - 1

    #checks if coordinate has been hit previously
    if board[guess_col][guess_row] == "X" or board[guess_col][guess_row] == "1":
      clear(1)
      print("You've already guessed this coordinate !")
      print("Guesses left:", guesses_left)
      print('Hits:', hit)
      print('Misses:', miss)
      output_board(board)

    #checks for a hit
    elif guess_row == pre_set_boards[board_selection][0][0] and guess_col == pre_set_boards[board_selection][0][1] or guess_row == pre_set_boards[board_selection][1][0] and guess_col == pre_set_boards[board_selection][1][1] or guess_row == pre_set_boards[board_selection][2][0] and guess_col == pre_set_boards[board_selection][2][1]:
      clear(1)
      hit += 1
      guesses_left -= 1
      print("Status: Hit!")
      print("Guesses left:", guesses_left)
      print('Hits:', hit)
      print('Misses:', miss)
      print(colors['blue'])
      board[guess_col][guess_row] = "1"
      output_board(board)
      print(colors['reset'])

    else: #deals with all other cases
      if (guess_row < 0 or guess_row > 5) or (guess_col < 0 or guess_col > 5):
        clear(1)
        print("Oops, that's not even in the ocean.\n")
        print("Guesses left:", guesses_left)
        print('Hits:', hit)
        print('Misses:', miss)
        output_board(board)
      else:
        clear(1)
        miss += 1
        guesses_left -= 1
        print("Status: Miss!")
        print("Guesses left:", guesses_left)
        print('Hits:', hit)
        print('Misses:', miss)
        print(colors['red'])
        board[guess_col][guess_row] = "X"
        output_board(board)
        print(colors['reset'])

  #if player wins
  if hit == 3:
    print("\nYou won !")
    print('You had...\nHits:', hit, '\nMisses:', miss)
    result = 'won'
    clear(5)
  else:
    clear(2)
    print(
      'You ran out of ammo :(\nBetter luck next time\nHere were the locations of the ships\n'
    )
    result = 'lost'
    output_board(pre_set_board)
    print('You had...\nHits:', hit, '\nMisses:', miss)
    input("\nPress Enter to continue...")
    clear(2)

  #adding data to csv file
  file = open('battleship.csv', 'a')
  db = csv.writer(file)
  db.writerow([game_type, 'N/A', miss, hit, board_selection, result])
  file.close()


#------------------------------------------------------------------------



def multi_player(): #function for multiplayer
  game_type = 'multi-player' #for data collection later
  print('\nWelcome to multi-player mode!\n\nHere the each player will make their own layout with three ships on it\nYou must find these ships and sink them within 20 guesses in order to win\n\nGood luck !\n')
  input("\nPress Enter to continue...")
  clear(2)
  u1board = []
  u2board = []
  row = ['A', 'B', 'C', 'D', 'E', 'F']

  for i in range(len(row)):
    u1board.append(["."] * len(row))
    u2board.append(["."] * len(row))

  #create ship location nested lists
  board_u1 = [[], [], []]
  board_u2 = [[], [], []]
  print('Hi Player one! Here you are going to input the locations of your three ships!(dw we\'ll clear the screen after so player two doesen\'t see!)\n')
  output_board(u1board)

  for i in range(3): #loop for player entering ships
    print('\nEnter ship number:', i + 1)
    u1_input_row = (input("Enter collumn (A-F): "))
    
    while (u1_input_row.upper()) not in row: #input validation
      print('Invalid entry.')
      u1_input_row = (input("Enter collumn (A-F): "))

    while True:
      u1_input_col = (input("Guess row (1-6) : "))
      try:
        u1_input_col = int(u1_input_col)
      except ValueError:
        print('Enter a valid number.')
        continue
      if 1 <= u1_input_col <= 6:
        break
      else:
        print('Enter a valid number: 1-6')
    u1_input_row = (row.index(u1_input_row.upper()))
    u1_input_col = u1_input_col - 1

    board_u1[i].append(u1_input_row) #append ships to list
    board_u1[i].append(u1_input_col)
    u1board[u1_input_col][u1_input_row] = '1'
  clear(1) #clear board
  print('Here are the location of your ships:\n')
  output_board(u1board)
  input("\nPress Enter to continue and pass over to player 2...")
  clear(1) #clear board

  print('Hi Player two! Here you are going to input the locations of your three ships!(dw we\'ll clear the screen after so player one doesen\'t see!)\n')
  output_board(u2board)
  for i in range(3):
    print('\nEnter ship number:', i + 1)
    u2_input_row = input("Input collumn (A-F): ")
    while (u2_input_row.upper()) not in row:
      print('Invalid entry.')
      u2_input_row = (input("Guess collumn (A-F): "))

    while True:
      u2_input_col = (input("Guess row (1-6) : "))
      try:
        u2_input_col = int(u2_input_col)
      except ValueError:
        print('Enter a valid number.')
        continue
      if 1 <= u2_input_col <= 6:
        break
      else:
        print('Enter a valid number: 1-6')

    u2_input_row = (row.index(u2_input_row.upper()))
    u2_input_col = u2_input_col - 1

    board_u2[i].append(u2_input_row)
    board_u2[i].append(u2_input_col)

    u2board[u2_input_col][u2_input_row] = '1'
  clear(2)
  print('\nHere are the location of your ships:\n')
  output_board(u2board)
  input("\nPress Enter to continue and pass back to player 1...")
  clear(2)

  u1board = []
  u2board = []
  for x in range(len(row)):
    u1board.append(["."] * len(row))
    u2board.append(["."] * len(row))

  print('Player 1! You will now start the game. Enter coordinates to skink player twos\'s ships!\n')
  input("\nPress Enter to continue...")
  clear(1)

  u1hit = 0
  u1miss = 0
  u2hit = 0
  u2miss = 0
  row = ['A', 'B', 'C', 'D', 'E', 'F']
  guesses_leftu1 = 20
  guesses_leftu2 = 20

  while (guesses_leftu1>0 and guesses_leftu2>0) and (u1hit < 3 and u2hit < 3):
    print('Player 1 :\n')
    print("Status: Waiting for coordinate\nGuesses left:", guesses_leftu1)
    print('Hits:', u1hit)
    print('Misses:', u1miss)
    print('\n')
    output_board(u2board)
    print('\n')
    u1guess_row = (input("\nGuess collumn (A-F): "))
    while (u1guess_row.upper()) not in row:
      print('Invalid entry')
      u1guess_row = (input("Guess collumn (A-F): "))

    while True:
      u1guess_col = (input("Guess row (1-6) : "))
      try:
        u1guess_col = int(u1guess_col)
      except ValueError:
        print('Enter a valid number')
        continue
      if 1 <= u1guess_col <= 6:
        break
      else:
        print('Enter a valid number: 1-6')

    u1guess_row = u1guess_row.upper()
    u1guess_row = (row.index(u1guess_row))
    u1guess_col = u1guess_col - 1

    if u2board[u1guess_col][u1guess_row] == "X" or u2board[u1guess_col][u1guess_row] == "1":
      clear(1)
      print("You've already guessed this coordinate !")
      print("Guesses left:", guesses_leftu1)
      print('Hits:', u1hit)
      print('Misses:', u1miss)
      print('\n')
      output_board(u2board)
      clear(4)

    elif u1guess_row == board_u2[0][0] and u1guess_col == board_u2[0][
        1] or u1guess_row == board_u2[1][0] and u1guess_col == board_u2[1][
          1] or u1guess_row == board_u2[2][0] and u1guess_col == board_u2[2][1]:
      clear(1)
      u1hit += 1
      guesses_leftu1 -= 1
      print("Status: Hit!")
      print("Guesses left:", guesses_leftu1)
      print('Hits:', u1hit)
      print('Misses:', u1miss)
      print(colors['blue'])
      u2board[u1guess_col][u1guess_row] = "1"
      output_board(u2board)
      print(colors['reset'])
      clear(4)

    else:
      clear(1)
      u1miss += 1
      guesses_leftu1 -= 1
      print("Status: Miss!")
      print("Guesses left:", guesses_leftu1)
      print('Hits:', u1hit)
      print('Misses:', u1miss)
      print(colors['red'])
      u2board[u1guess_col][u1guess_row] = "X"
      output_board(u2board)
      print(colors['reset'])

    clear(3) #clear board between turns
    if u1hit > 3:
      break

    #--------------------------------------
    print('Player 2 :\n')

    print("Status: Waiting for coordinate\nGuesses left:", guesses_leftu2)
    print('Hits:', u2hit)
    print('Misses:', u2miss)
    print('\n')
    output_board(u1board)
    print('\n')
    u2guess_row = (input("\nGuess collumn (A-F): "))
    while (u2guess_row.upper()) not in row:
      print('Invalid entry')
      u2guess_row = (input("Guess collumn (A-F): "))

    while True:
      u2guess_col = (input("Guess row (1-6) : "))
      try:
        u2guess_col = int(u2guess_col)
      except ValueError:
        print('Enter a valid number')
        continue
      if 1 <= u2guess_col <= 6:
        break
      else:
        print('Enter a valid number: 1-6')

    u2guess_row = u2guess_row.upper()
    u2guess_row = (row.index(u2guess_row))
    u2guess_col = u2guess_col - 1

    if u1board[u2guess_col][u2guess_row] == "X" or u1board[u2guess_col][u2guess_row] == "1":
      clear(1)
      print("You've already guessed this coordinate !")
      print("Guesses left:", guesses_leftu2)
      print('Hits:', u2hit)
      print('Misses:', u2miss)
      print('\n')
      output_board(u1board)
      clear(4)

    elif u2guess_row == board_u1[0][0] and u2guess_col == board_u1[0][1] or u2guess_row == board_u1[1][0] and u2guess_col == board_u1[1][1] or u2guess_row == board_u1[2][0] and u2guess_col == board_u1[2][1]:
      clear(1)
      u2hit += 1
      guesses_leftu2 -= 1
      print("Status: Hit!")
      print("Guesses left:", guesses_leftu2)
      print('Hits:', u2hit)
      print('Misses:', u2miss)
      print(colors['blue'])
      u1board[u2guess_col][u2guess_row] = "1"
      output_board(u1board)
      print(colors['reset'])
      clear(4)

    else:
      clear(1)
      u2miss += 1
      guesses_leftu2 -= 1
      print("Status: Miss!")
      print("Guesses left:", guesses_leftu2)
      print('Hits:', u2hit)
      print('Misses:', u2miss)
      print(colors['red'])
      u1board[u2guess_col][u2guess_row] = "X"
      output_board(u1board)
      print(colors['reset'])
      clear(4)

  #determine winner
  if u1hit > u2hit:
    clear(2)
    print('Player 1 wins !')
    print('\nPlayer 1 had...\nHits:', u1hit, '\nMisses:', u1miss)
    print('\nPlayer 2 had...\nHits:', u2hit, '\nMisses:', u2miss)
    result = 'P1 win'
    input("\nPress Enter to continue...")
    clear(2)
  elif u1hit < u2hit:
    clear(2)
    print('Player 2 wins !')
    print('\nPlayer 1 had...\nHits:', u1hit, '\nMisses:', u1miss)
    print('\nPlayer 2 had...\nHits:', u2hit, '\nMisses:', u2miss)
    result = 'P2 win'
    input("\nPress Enter to continue...")
    clear(2)
  elif u1hit == u2hit:
    clear(2)
    print('Draw !')
    result = 'tie'
    print('\nPlayer 1 had...\nHits:', u1hit, '\nMisses:', u1miss)
    print('\nPlayer 2 had...\nHits:', u2hit, '\nMisses:', u2miss)
    input("\nPress Enter to continue...")
    clear(2)

  file = open('battleship.csv', 'a')
  db = csv.writer(file)
  db.writerow([game_type, 'P1', u1miss, u1hit, 'n/a', result])
  db.writerow([game_type, 'P2', u2miss, u2hit, 'n/a', result])
  file.close()


#-------------------------------------------------------
def simulation():
  game_type = 'simulation' #for data collection later
  print('\nWelcome to simulation play!\n\n')
  repeats = int(input('Enter the number of times youd like simulation play to run: ')) #times simulation will run
  
  row = ['A', 'B', 'C', 'D', 'E', 'F']
  sim_wins = 0
  sim_losses = 0

  for i in range(repeats):
    print('Game number:', i) #game count
    guesses_left = 30 #VARIABLE CHANGED FOR PARAMETER CHANGES
    board = []
    hit = 0
    miss = 0

    for x in range(len(row)):
      board.append(["O"] * len(row))

    pre_set_boards = [[[3, 4], [0, 5], [5, 3]], [[0, 1], [5, 5], [1, 4]],
                      [[1, 2], [5, 1], [2, 3]]]
    
    board_selection = random.randint(0, 2)

    while hit < 3 and hit + miss < 30:
      guess_row = random.choice(row)
      guess_col = random.randint(0, 5)
      guess_row = (row.index(guess_row))

      if board[guess_col][guess_row] == "X" or board[guess_col][guess_row] == "1":
        hit = hit
      elif guess_row == pre_set_boards[board_selection][0][0] and guess_col == pre_set_boards[board_selection][0][1] or guess_row == pre_set_boards[board_selection][1][0] and guess_col == pre_set_boards[board_selection][1][1] or guess_row == pre_set_boards[board_selection][2][0] and guess_col == pre_set_boards[board_selection][2][1]:
        hit += 1
        guesses_left -= 1

      else:
        miss += 1
        guesses_left -= 1

    if hit == 3:
      print("Computer wins !")
      result = 'won'
      sim_wins += 1
    else:
      print('Computer ran out of ammo :(')
      result = 'lost'
      sim_losses += 1
    
    file = open('battleship3.csv', 'a')
    db = csv.writer(file)
    db.writerow([game_type, 'N/A', miss, hit, board_selection, result])
    file.close()

    
  print('Summary...\nOut of', repeats, 'games, the computer won', sim_wins,
        'game(s) and lost', sim_losses, 'game(s)')
  input("\nPress Enter to continue...")
  clear(2)


while True:
  while True:
    option = input(
      "MENU \n====================\n1: Single-player \n2: Multi-player \n3: Simulation play \n====================\n\nChoose which option you would like to view: "
    )
    try:
      option = int(option)
    except ValueError:
      print('Enter a valid number.1-3')
      clear(2)
      continue
    if 1 <= option <= 3:
      break
    else:
      print('Enter a valid number: 1-3')
      clear(2)
  if option == 1:
    clear(2)
    single_player()
  elif option == 2:
    clear(2)
    multi_player()
  elif option == 3:
    clear(2)
    simulation()


################### graphs and statistical analysis

# files= open("battleship.csv","r")
# data = list(csv.reader(files))
# files.close()

# sim_misses=[]
# for row in data[1:]:
#   if row[0]=='simulation':
#     sim_misses.append(int(row[2]))

# import statistics

# mean = statistics.mean(sim_misses)
# print('Mean of simulation misses',mean)

# frequency = {}

# # iterating over list
# for item in sorted(sim_misses):
#    # checking element in dict
#    if item in frequency:
#       # increasing counter
#       frequency[item] += 1
#    else:
#       # initialising count
#       frequency[item] = 1

# # print frequency
# print(frequency)


files= open("battleship3.csv","r")
data = list(csv.reader(files))
files.close()



labels_pie = ['Wins','Losses']

data_pie =[]
data_pie2 =[]

data_pie_lay1 = []
data_pie_lay2 = []
data_pie_lay3 = []

stacked_bar_hits = []

wins = 0
losses = 0
wins_lay1 = 0
losses_lay1 = 0
wins_lay2 = 0
losses_lay2 = 0
wins_lay3 = 0
losses_lay3 = 0

for row in data[1:]:
  if row[0]=='simulation':
    data_pie.append(row[-1]) 
    if row[-2]=='0':
      data_pie_lay1.append(row[-1])
    if row[-2]=='1':
      data_pie_lay2.append(row[-1])
    if row[-2]=='2':
      data_pie_lay3.append(row[-1])


for i in range(len(data_pie)):
  if data_pie[i] == 'won':
    wins+=1
  elif data_pie[i] != 'won':
    losses+=1

for i in range(len(data_pie_lay1)):
  if data_pie_lay1[i] == 'won':
    wins_lay1+=1
  elif data_pie_lay1[i] != 'won':
    losses_lay1+=1

for i in range(len(data_pie_lay2)):    
  if data_pie_lay2[i] == 'won':
    wins_lay2+=1
  elif data_pie_lay2[i] != 'won':
    losses_lay2+=1
    
for i in range(len(data_pie_lay3)):
  if data_pie_lay3[i] == 'won':
    wins_lay3+=1
  elif data_pie_lay3[i] != 'won':
    losses_lay3+=1
  


data_pie2.append(wins)
data_pie2.append(losses)
data_pie_lay1 = []
data_pie_lay2 = []
data_pie_lay3 = []

data_pie_lay1 = [wins_lay1,losses_lay1]
data_pie_lay2 = [wins_lay2,losses_lay2]
data_pie_lay3 = [wins_lay3,losses_lay3]

figure, axis = plt.subplots(2, 2)
explode = [0,0.1]
colours = ['#778CA8','#1D3F6E']
axis[0, 0].pie(data_pie2, explode = explode, autopct = '%.2f',labels = labels_pie, shadow = True, startangle = 90, colors=colours)
axis[0, 0].set_title("1. Total Wins vs losses", fontsize=8)



axis[0, 1].pie(data_pie_lay1, explode = explode, autopct = '%.2f',labels = labels_pie, shadow = True, startangle = 90, colors=colours)
axis[0, 1].set_title("2. Preset Layout 1, Wins vs losses", fontsize=8)

axis[1,0].pie(data_pie_lay2, explode = explode, autopct = '%.2f',labels = labels_pie, shadow = True, startangle = 90, colors=colours)
axis[1, 0].set_title("3. Preset Layout 2, Wins vs losses", fontsize=8)

axis[1,1].pie(data_pie_lay3, explode = explode, autopct = '%.2f',labels = labels_pie, shadow = True, startangle = 90, colors=colours)
axis[1, 1].set_title("4. Preset Layout 3, Wins vs losses", fontsize=8)
figure.suptitle('Figure 3: Ratio of Wins to Losses Simulation when total_guesses = 30', fontsize=12)
plt.savefig("graphs/fig4simulation_wins_vs_losses_guesses30.png", dpi = 100)
plt.show()

files= open("battleship2.csv","r")
data = list(csv.reader(files))
files.close()


labels_pie = ['Wins','Losses']

data_pie =[]
data_pie2 =[]

data_pie_lay1 = []
data_pie_lay2 = []
data_pie_lay3 = []

stacked_bar_hits = []

wins = 0
losses = 0
wins_lay1 = 0
losses_lay1 = 0
wins_lay2 = 0
losses_lay2 = 0
wins_lay3 = 0
losses_lay3 = 0

for row in data[1:]:
  if row[0]=='simulation':
    data_pie.append(row[-1]) 
    if row[-2]=='0':
      data_pie_lay1.append(row[-1])
    if row[-2]=='1':
      data_pie_lay2.append(row[-1])
    if row[-2]=='2':
      data_pie_lay3.append(row[-1])


for i in range(len(data_pie)):
  if data_pie[i] == 'won':
    wins+=1
  elif data_pie[i] != 'won':
    losses+=1

for i in range(len(data_pie_lay1)):
  if data_pie_lay1[i] == 'won':
    wins_lay1+=1
  elif data_pie_lay1[i] != 'won':
    losses_lay1+=1

for i in range(len(data_pie_lay2)):    
  if data_pie_lay2[i] == 'won':
    wins_lay2+=1
  elif data_pie_lay2[i] != 'won':
    losses_lay2+=1
    
for i in range(len(data_pie_lay3)):
  if data_pie_lay3[i] == 'won':
    wins_lay3+=1
  elif data_pie_lay3[i] != 'won':
    losses_lay3+=1
  


data_pie2.append(wins)
data_pie2.append(losses)
data_pie_lay1 = []
data_pie_lay2 = []
data_pie_lay3 = []

data_pie_lay1 = [wins_lay1,losses_lay1]
data_pie_lay2 = [wins_lay2,losses_lay2]
data_pie_lay3 = [wins_lay3,losses_lay3]

figure, axis = plt.subplots(2, 2)
explode = [0,0.1]
colours = ['#778CA8','#1D3F6E']
axis[0, 0].pie(data_pie2, explode = explode, autopct = '%.2f',labels = labels_pie, shadow = True, startangle = 90, colors=colours)
axis[0, 0].set_title("1. Total Wins vs losses", fontsize=8)



axis[0, 1].pie(data_pie_lay1, explode = explode, autopct = '%.2f',labels = labels_pie, shadow = True, startangle = 90, colors=colours)
axis[0, 1].set_title("2. Preset Layout 1, Wins vs losses", fontsize=8)

axis[1,0].pie(data_pie_lay2, explode = explode, autopct = '%.2f',labels = labels_pie, shadow = True, startangle = 90, colors=colours)
axis[1, 0].set_title("3. Preset Layout 2, Wins vs losses", fontsize=8)

axis[1,1].pie(data_pie_lay3, explode = explode, autopct = '%.2f',labels = labels_pie, shadow = True, startangle = 90, colors=colours)
axis[1, 1].set_title("4. Preset Layout 3, Wins vs losses", fontsize=8)
figure.suptitle('Figure 2: Ratio of Wins to Losses Simulation when total_guesses = 25', fontsize=12)
plt.savefig("graphs/fig3simulation_wins_vs_losses_guesses25.png", dpi = 100)
plt.show()


  
files= open("battleship.csv","r")
data = list(csv.reader(files))
files.close()


labels_pie = ['Wins','Losses']

data_pie =[]
data_pie2 =[]

data_pie_lay1 = []
data_pie_lay2 = []
data_pie_lay3 = []

stacked_bar_hits = []

wins = 0
losses = 0
wins_lay1 = 0
losses_lay1 = 0
wins_lay2 = 0
losses_lay2 = 0
wins_lay3 = 0
losses_lay3 = 0

for row in data[1:]:
  if row[0]=='simulation':
    data_pie.append(row[-1]) 
    if row[-2]=='0':
      data_pie_lay1.append(row[-1])
    if row[-2]=='1':
      data_pie_lay2.append(row[-1])
    if row[-2]=='2':
      data_pie_lay3.append(row[-1])


for i in range(len(data_pie)):
  if data_pie[i] == 'won':
    wins+=1
  elif data_pie[i] != 'won':
    losses+=1

for i in range(len(data_pie_lay1)):
  if data_pie_lay1[i] == 'won':
    wins_lay1+=1
  elif data_pie_lay1[i] != 'won':
    losses_lay1+=1

for i in range(len(data_pie_lay2)):    
  if data_pie_lay2[i] == 'won':
    wins_lay2+=1
  elif data_pie_lay2[i] != 'won':
    losses_lay2+=1
    
for i in range(len(data_pie_lay3)):
  if data_pie_lay3[i] == 'won':
    wins_lay3+=1
  elif data_pie_lay3[i] != 'won':
    losses_lay3+=1
  


data_pie2.append(wins)
data_pie2.append(losses)
data_pie_lay1 = []
data_pie_lay2 = []
data_pie_lay3 = []

data_pie_lay1 = [wins_lay1,losses_lay1]
data_pie_lay2 = [wins_lay2,losses_lay2]
data_pie_lay3 = [wins_lay3,losses_lay3]

figure, axis = plt.subplots(2, 2)
explode = [0,0.1]
colours = ['#778CA8','#1D3F6E']
axis[0, 0].pie(data_pie2, explode = explode, autopct = '%.2f',labels = labels_pie, shadow = True, startangle = 90, colors=colours)
axis[0, 0].set_title("1. Total Wins vs losses", fontsize=8)



axis[0, 1].pie(data_pie_lay1, explode = explode, autopct = '%.2f',labels = labels_pie, shadow = True, startangle = 90, colors=colours)
axis[0, 1].set_title("2. Preset Layout 1, Wins vs losses", fontsize=8)

axis[1,0].pie(data_pie_lay2, explode = explode, autopct = '%.2f',labels = labels_pie, shadow = True, startangle = 90, colors=colours)
axis[1, 0].set_title("3. Preset Layout 2, Wins vs losses", fontsize=8)

axis[1,1].pie(data_pie_lay3, explode = explode, autopct = '%.2f',labels = labels_pie, shadow = True, startangle = 90, colors=colours)
axis[1, 1].set_title("4. Preset Layout 3, Wins vs losses", fontsize=8)
figure.suptitle('Figure 1: Ratio of Wins to Losses Simulation when total_guesses = 20', fontsize=12)
plt.savefig("graphs/fig1simulation_wins_vs_losses.png", dpi = 100)
plt.show()



####################################



all_hits = []
all_hits_counted = []

board0_hits = []
board0_hits_all = []

board1_hits = []
board1_hits_all = []

board2_hits = []
board2_hits_all = []

for row in data[1:]:
  all_hits.append(row[3])
  if row[4]=='0':
    board0_hits_all.append(row[3])
  elif row[4]=='1':
    board1_hits_all.append(row[3])
  elif row[4]=='2':
    board2_hits_all.append(row[3])


board0_hits.append(board0_hits_all.count('0'))
board0_hits.append(board0_hits_all.count('1'))
board0_hits.append(board0_hits_all.count('2'))
board0_hits.append(board0_hits_all.count('3'))

board1_hits.append(board1_hits_all.count('0'))
board1_hits.append(board1_hits_all.count('1'))
board1_hits.append(board1_hits_all.count('2'))
board1_hits.append(board1_hits_all.count('3'))

board2_hits.append(board2_hits_all.count('0'))
board2_hits.append(board2_hits_all.count('1'))
board2_hits.append(board2_hits_all.count('2'))
board2_hits.append(board2_hits_all.count('3'))

all_hits_counted.append(all_hits.count('0'))
all_hits_counted.append(all_hits.count('1'))
all_hits_counted.append(all_hits.count('2'))
all_hits_counted.append(all_hits.count('3'))

#
import numpy as np
print(board0_hits)

x = np.array(["0", "1", "2", "3"])
figure, axis = plt.subplots(2, 2)

axis[0,0].bar(x, all_hits_counted, color = '#1D3F6E', width=.8)
axis[0,0].set_title('1. Total Hits', fontsize=8)

axis[0,0].xaxis.set_tick_params(labelsize=5)
axis[0,0].yaxis.set_tick_params(labelsize=5)
axis[0,0].grid(linestyle='-', linewidth='0.5', alpha=0.4)

axis[0,1].bar(x, board0_hits, color = '#1D3F6E', width=.8)
axis[0,1].set_title('2. Preset Layout 1 Hits', fontsize=8)

axis[0,1].xaxis.set_tick_params(labelsize=5)
axis[0,1].yaxis.set_tick_params(labelsize=5)
axis[0,1].grid(linestyle='-', linewidth='0.5', alpha=0.4)

axis[1,0].bar(x, board1_hits, color = '#1D3F6E', width=.8)
axis[1,0].set_title('3. Preset Layout 2 Hits', fontsize=8)

axis[1,0].xaxis.set_tick_params(labelsize=5)
axis[1,0].yaxis.set_tick_params(labelsize=5)
axis[1,0].grid(linestyle='-', linewidth='0.5', alpha=0.4)

axis[1,1].bar(x, board2_hits, color = '#1D3F6E', width=.8)
axis[1,1].set_title('4. Preset Layout 3 Hits', fontsize=8)

axis[1,1].xaxis.set_tick_params(labelsize=5)
axis[1,1].yaxis.set_tick_params(labelsize=5)
axis[1,1].grid(which='major',linestyle='-', linewidth='0.5', alpha=0.4)


figure.supxlabel('Hits')
figure.supylabel('Number of Occurances')
figure.suptitle('Figure 4: Number of Hits by Preset Layout', fontsize=12)

plt.savefig("graphs/fig2num_hits.png", dpi = 100)
figure.show()

