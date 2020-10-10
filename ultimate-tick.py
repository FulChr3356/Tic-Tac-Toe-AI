'''
  ultimate-tick-alpha.py
  Author: Paul Talaga
  Date: Nov 8, 2018
  Description: Implements the Ultimate Tic Tac Toe game, but no AI is implemented.
               See the getAIMove to add an AI player.
  Works with Python 2.X and 3.X
'''


'''A board state is an array of 81 strings, where each string is either X, O, or a space.
   The inBox, getMiniBoard, getHighBoard, and minToBig functions allow this big state to
   be analyzed as a normal 3x3 board.'''

def inBox(box, x, y):
  #boxes are labeled 0 1 2    3 4 5    6 7 8
  return int(x / 3) == int(box % 3) and int(y / 3) == int(box / 3)
  
def getMiniBoard(big, box):
  (x,y) = (box%3, int(box / 3) )
  indexes = []
  indexes += map(lambda a: x*3 + a + y *27,range(3))
  indexes += map(lambda a: x*3 + a + y *27 + 9,range(3))
  indexes += map(lambda a: x*3 + a + y *27 + 18,range(3))
  # make subboard
  subboard = []
  for i in indexes:
    subboard.append(big[i])
  return subboard
  
  
def getHighBoard(big):
  ret = []
  for box in range(9):
    (x,y) = (box%3, int(box / 3) )
    indexes = []
    indexes += map(lambda a: x*3 + a + y *27, range(3))
    indexes += map(lambda a: x*3 + a + y *27 + 9, range(3))
    indexes += map(lambda a: x*3 + a + y *27 + 18, range(3))
    # make subboard
    subboard = []
    for i in indexes:
      subboard.append(big[i])
    if miniScorePlayer(subboard,'X') == 1: # If X won this miniboard, fill all with Xs
      ret.append('X')
    elif miniScorePlayer(subboard,'O') == 1:# If O won this miniboard, fill with all Os
      ret.append('O')
    elif isFull(subboard):  # No win, but a Tie
      ret.append('T')
    else:
      ret.append(' ')
  return ret
    
def minToBig(index, box):
  (x,y) = (box%3, int(box / 3) )
  return x*3 + (index % 3) + y *27 + int(index/3) * 9

def printState(state):
  (big, box) = state
  # Print the large board
  print("Large board state.  You must play on the . locations.")
  print("Box: %d" % box)
  for y in range(9):
    line = ""
    for x in range(9):
      if big[x + y * 9] == " " and inBox(box,x,y):
         line += "."
      else:
        line += big[x + y * 9]
      if (x + 1) % 3 == 0 and x != 8:
        line += "|"
    print( line)
    if (y+1) % 3 == 0 and y != 8:
      print("-" * 11)
  print("")
  print("Who is winning each small board:")
  mini = getHighBoard(big)
  for y in range(3):
    line = ""
    for x in range(3):
      line += mini[x + y * 3] 
      if x < 2:
        line += "|"
    print( line)
    if y < 2:
      print("-----")
  print("Score for O: " + str(score(state)))
  print("")
  
def printNumberHelp():
  state = list("0123456789")
  print("Index Helper:")
  for y in range(3):
    line = ""
    for x in range(3):
      line += state[x + y * 3] 
      if x < 2:
        line += "|"
    print( line )
    if y < 2:
      print("-----")
  print("\n")


def miniScorePlayer(mini, c):
  # horizontal
  for y in range(3):
    r = y * 3
    if mini[r] == c and mini[r+1] == c and mini[r+2] == c:
      return 1
  # vertical
  for x in range(3):
    if mini[x] == c and mini[x+3] == c and mini[x+6] == c:
      return 1
  # diag down to right
  if mini[0] == c and mini[4] == c and mini[8] == c:
    return 1
  # diag down to left
  if mini[2] == c and mini[4] == c and mini[6] == c:
    return 1
  return 0
  
def validMove(state, pos): # Pos is 0-8 for a small 3x3 board.
  (big, box) = state
  miniboard = getMiniBoard(big, box)
  if pos < 0 or pos > 8:
    return False
  return miniboard[pos] == " "
  
def score(state):
  (big, box) = state
  mini = getHighBoard(big)
  x = miniScorePlayer(mini,'X')
  o = miniScorePlayer(mini,'O')
  if x == o:
    return 0
  if x > o:
    return 1
  if x < o:
    return -1
    
def isFull(minBoard):
  return not " " in minBoard
  
def isBigFull(state):
  (big, box) = state
  return isFull(getHighBoard(big))
  
def generateSuccessors(state, player):
  # Returns a tuple, (index, new state)
  # if player = 1, O, if -1, X
  player_character = ''
  if player == 1:
    player_character = "O"
  else:
    player_character = "X"
  ret = []
  (big, box) = state
  if isFull(getMiniBoard(big,box)) or miniScorePlayer(getMiniBoard(big,box),'X') == 1 or  miniScorePlayer(getMiniBoard(big,box),'X') == 1:  #full or someone won
    # get to pick a random other board... lets just pick the next one that is free
    box = -1
    for i in range(9):
      if not isFull(getMiniBoard(big,i)) and miniScorePlayer(getMiniBoard(big,box),'X') == 0 and  miniScorePlayer(getMiniBoard(big,box),'X') == 0:
        box = i
        break
  state = (state[0], box)
  for i in range(9):
    if validMove(state,i):
      (big, box) = state
      newBig = big[:]
      newBig[minToBig(i,box)] = player_character
      ret.append((i, (newBig, i)))
  if len(ret) == 0:
    print("no options!")
  return ret
  
'''This is called in the game play.  Substitute your own function to change the AI method.
   This needs to return a move, which is an index to place their character.'''
def getAIMove(state):
  # As an example pick the first available spot to play
  options = generateSuccessors(state, 1)

  return options[0][0]
  
# AI aspect: Insert your AI functions below


#  -------------- Run the Game! -------------------

state = ([" "] * 81, 0)   # (full board, next subboard to play)


play = True
while play:
  print("")
  printNumberHelp()
  printState(state)
  move = input('Enter O placement:')
  move = int(move)
  if not validMove(state,move):
    print("That move is not valid, try again.")
    continue
  (big, box) = state
  state[0][minToBig(move, box)] = "O"
  state = (state[0], move)
  (big, box) = state
  if score(state) == -1:
    printState(state)
    print("You Won!!!!")
    play = False
    break
  if isFull(getHighBoard(big)):
    printState(state)
    print("Tie!")
    play = False
    break
  move = getAIMove(state)  # This will call the AI agent
  (big, box) = state
  state[0][minToBig(move, box)] = "X"
  state = (state[0], move)
  (big, box) = state
  if score(state) == 1:
    printState(state)
    print("Computer Won.  ;-(")
    play = False
    break
  if isFull(getHighBoard(big)):
    printState(state)
    print("Tie!")
    play = False
    break


