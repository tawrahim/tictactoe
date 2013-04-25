import webapp2
import os
import jinja2
import random

from google.appengine.api import users
from google.appengine.api import xmpp
from google.appengine.ext.webapp import xmpp_handlers

QUIT = 0
HUMAN_PLAYER = 1
COMPUTER_PLAYER = 2

HELP_MSG1 = ("Greetings!!!, Would you like to play tic toe?"
            "Start the game by typing '/play'!")

HELP_MSG2 = ("Enter the command '/move' and two numbers (x,y) for the Coordinates of your Move -e.g /move 1,1: ")
			
GAME_OVER = "Game Over"

game_started = False
boardStr = ''

jinja_environment = jinja2.Environment(autoescape=True,
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# Retrieved from: http://en.literateprograms.org/Tic_Tac_Toe_(Python)?oldid=17009
def allEqual(list):
    """returns True if all the elements in a list are equal, or if the list is empty."""
    return not list or list == [list[0]] * len(list)

# === Provided class Position from 6.00x PSet7 (modified by Benz Theodore)
class Position(object):
    """
    A Position represents a location in a two-dimensional plane.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        x: an integer > 0
        y: an integer > 0
        """
        assert(x > 0)
        assert(y > 0)

        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, x, y):
        """
        Returns: a Position object representing the new position.
        """
        return Position(self.x, self.y)

    def __str__(self):  
        return "(%d, %d)" % (self.x, self.y)


# class GameBoard by Benz Theodore
class GameBoard(object):
    """
    Define a Tic Tac Toe gameBoard Board, 3x3 by default.
    A gameBoard represents a rectangular region containing empty ('-'), X, or Y tiles.

    A board has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either empty or marked with X or Y.
    """
    def __init__(self, width = 3, height = 3):
        """
        Initializes a gameBoard with the specified width and height.
        Initially, all tiles are empty.

        width: an integer > 0
        height: an integer > 0
        """
        assert(width > 0)
        assert(height > 0)

        self.width = width
        self.height = height
        self.numTiles = width * height
        self.numEmptyTiles = self.numTiles
        self.playerXTurn = True
        self.playerType = HUMAN_PLAYER
        self.playerTilePositions = [['-','-','-'],['-','-','-'],['-','-','-']]

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height

    def getNumTiles(self):
        """
        Returns: an integer, the total number of tiles on the board.
        """
        return self.numTiles

    def getNumEmptyTiles(self):
        """
        Returns: an integer, the total number of empty tiles on the board.
        """
        return self.numEmptyTiles

    def setNumEmptyTiles(self):
        self.numEmptyTiles -= 1

    def isPlayerXTurn(self):
        return self.playerXTurn

    def setPlayerXTurn(self, toggle):
        self.playerXTurn = toggle

    def getPlayerType(self):
        return self.playerType

    def setPlayerType(self, playerType):
        self.playerType = playerType

    def getPlayerTilePositions(self, pos):
        return self.playerTilePositions[pos.getX()-1][pos.getY()-1]

    def setPlayerTilePositions(self, pos, val):
        self.playerTilePositions[pos.getX()-1][pos.getY()-1] = val

    def isTileEmpty(self, pos):
        """
        Return True if the tile at position pos is empty.
        Assumes that pos represents a valid tile on the board.

        pos.getX(): an integer
        pos.getY(): an integer
        returns: True if pos is empty, False otherwise
        """
        try:
            if self.getPlayerTilePositions(pos) == '-':
                return True
        except:
            return False

    def markTileAtPosition(self, pos):
        """
        Mark the tile under the position POS with value val ('X' or 'Y')
        Assumes that POS represents a valid position on the board.
        pos: a Position
        Returns True if the tile at position pos was marked and False otherwise.
        """
        if self.isPlayerXTurn():
            val = 'X'   #X is always a human player.
        else:
            val = 'O'   #The computer always plays as O.
            if self.getPlayerType() == COMPUTER_PLAYER:
                pos = self.getRandomComputerPosition()
                print 'Player O:\nThe computer played:',
                print str(pos.getX()) + ',' + str(pos.getY())
        
        if self.isPositionOnBoard(pos) and self.isTileEmpty(pos):
            self.setPlayerTilePositions(pos,val)

            #Toggle the players
            #self.playerXTurn = not self.playerXTurn
            self.setPlayerXTurn(not self.isPlayerXTurn())

            self.setNumEmptyTiles()
            print self
            return True
        else:
            print "Invalid Coordinate\n"
            return False

    def getRandomPosition(self):
        """
        Return a random position on the board.
        returns: a Position object.
        """
        return Position(random.randint(1,self.width),random.randint(1,self.height))

    def getRandomComputerPosition(self):
        """
        Return a random position on the board.  This is used to simulate the
        computer player.  The final solution will include a MiniMax function
        to handle computer moves.
        
        Must assume there are empty tiles!!!
        
        returns: a Position object if there is a move that can be made.
        """
#        if self.getNumEmptyTiles() > 0:
        pos = Position(random.randint(1,self.width),random.randint(1,self.height))
        while not self.isTileEmpty(pos):
            pos = Position(random.randint(1,self.width),random.randint(1,self.height))
        return pos
#        else:
#            raise ValueError('Game Over: No more spots!') 
    
    def isPositionOnBoard(self, pos):
        """
        Return True if pos is on the board.

        pos: a Position object.
        returns: True if pos is on the board, False otherwise.
        """
        if pos.getX() <= self.getWidth() and \
            pos.getY() <= self.getHeight() and \
            pos.getX() > 0 and \
            pos.getY() > 0:            
            return True
        else:
            return False

    # Retrieved from: http://en.literateprograms.org/Tic_Tac_Toe_(Python)?oldid=17009
    # (modified by Benz Theodore)
    def winner(self):
        """Determine if one player has won the game. Returns X, O or -"""
        winning_rows = [[0,1,2],[3,4,5],[6,7,8], # horizontal
                        [0,3,6],[1,4,7],[2,5,8], # vertical
                        [0,4,8],[2,4,6]]         # diagonal
        mapX = [0,1,2,0,1,2,0,1,2]
        mapY = [0,0,0,1,1,1,2,2,2]
        for row in winning_rows:
            if self.playerTilePositions[mapX[row[0]]][mapY[row[0]]] != '-' and \
                allEqual([self.playerTilePositions[mapX[i]][mapY[i]] for i in row]):
                return self.playerTilePositions[mapX[row[0]]][mapY[row[0]]]

    def isGameOver(self):
        return self.winner() in ('X', 'O') or self.getNumEmptyTiles < 1

    def __str__(self):
        global boardStr
        boardStr = ''
        for y in range(self.height, 0, -1):
            #print str(y) + '  ',
            boardStr += str(y) + '   '
            for x in range(1, self.width+1):
                #print str(self.getPlayerTilePositions(Position(x,y))),
                boardStr += str(self.getPlayerTilePositions(Position(x,y))) + ' '
            #print
            boardStr += '\n'
        #print "Y\n/ X 1 2 3"
        boardStr += 'Y\n/ X 1 2 3\n'
        return boardStr

##def playGame(playerType):
##    board = GameBoard()
##    board.setPlayerType(playerType)
##    print board
##    inputText = "Enter two numbers (x,y) for your Move Coordinate. e.g. 1,1: "
##    while True:
##        #Player X is always human and goes first.
##        if board.isPlayerXTurn():
##            print 'Player X:'
##        else:
##            # Player O may be human or computer and goes next
##            if board.getPlayerType() == HUMAN_PLAYER:
##                print 'Player O:'
##        #Get the input from the human players.
##        if board.getPlayerType() != COMPUTER_PLAYER or board.isPlayerXTurn():
##            try:
##                pos = raw_input(inputText)
##                pos = Position(int(pos[0]),int(pos[2]))
##                while not board.isPositionOnBoard(pos):
##                    print "Invalid Coordinate\n"
##                    pos = raw_input(inputText)
##            except:
##                continue
##        #Implement the move.
##        if board.markTileAtPosition(pos):
##            #Game is over if a player won or there are no more empty tiles.
##            if board.isGameOver() or board.getNumEmptyTiles() < 1: 
##                break
##        else:
##            continue
##
##    if board.winner():
##        print 'Player "%s" wins!' % board.winner()
##    elif board.winner() == None:
##        print "It's a Draw."

class XmppHandler(xmpp_handlers.CommandHandler):
    """Handler class for all XMPP activity."""

    def unhandled_command(self, message=None):
      message.reply(HELP_MSG.format(self.request.host_url))

    def play_command(self, message=None):
      if not game_started:
        global game_started
        game_started = True
        message.reply(HELP_MSG2)
      else:
        message.reply("Game in Progress")
 
    def move_command(self, message=None):
        if game_started:
            global game_started

            #Player X is always human and goes first.
            if board.isPlayerXTurn():
                 message.reply('Player X:')
            else:
                # Player O may be human or computer and goes next
                if board.getPlayerType() == HUMAN_PLAYER:
                    message.reply('Player O:')
            
            #Get the input from the human players.
            if board.getPlayerType() != COMPUTER_PLAYER or board.isPlayerXTurn():
                pos = Position(int(message.arg[0]),int(message.arg[2]))
                if not board.isPositionOnBoard(pos):
                    wrong_pos = "Invalid Coordinate"
                    message.reply(wrong_pos)
                else:
                    #Implement the move.
                    if board.markTileAtPosition(pos):
                        #print boardStr              #is this line still needed?
                        #message.reply(boardStr)     #is this line still needed?
                        #Game is over if a player won or there are no more empty tiles.
                        if board.isGameOver() or board.getNumEmptyTiles() < 1:
                            game_started = False
                            if board.winner():
                                message.reply('Player "%s" wins.' % board.winner())
                            elif board.winner() == None:
                                message.reply(GAME_OVER)
        else:
            message.reply(HELP_MSG1)

    def text_message(self, message=None):
        message.reply(HELP_MSG1)
	
    def help_command(self, message=None):
        message.reply(HELP_MSG2)
	 
    def quit_command(self, message=None):
        game_started = False
        message.reply(GAME_OVER)
	
 
app = webapp2.WSGIApplication([
 ('/_ah/xmpp/message/chat/', XmppHandler),
 ], debug=True)

 
if __name__ == "__main__":
 game_started = False


##if __name__ == "__main__":
##    while True:
##        try:
##            #ans = raw_input('\nPlay against [human = 1] or [computer = 2] or [quit = 0]: ')
##            message.reply('\nPlay against [human = 1] or [computer = 2] or [quit = 0]: ')
##            if str(HUMAN_PLAYER) in ans:
##                playGame(HUMAN_PLAYER)
##            elif ans == str(COMPUTER_PLAYER):
##                playGame(COMPUTER_PLAYER)
##            elif ans == str(QUIT):
##                break
##            else:
##                continue
##        except:
##            break
##    print 'Goodbye!'
