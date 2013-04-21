#Benz Theodore 4/20/2013    Basic Tic, Tac, Toe game

import random

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
        self.playerTilePositions = [['-','-','-'],['-','-','-'],['-','-','-']]
##        for y in range(height, 0, -1):
##            #print 'range height:', range(height, 0, -1)
##            #print y
##            for x in range(1, width+1):
##                #print 'range width:', range(1, width+1)
##                #print x
###                self.setPlayerTilePositions(Position(x,y),'-')
##                self.playerTilePositions[x][y] = '-'
##        print self.playerTilePositions.values()
                
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

    def isPlayerOTurn(self):
        return not self.playerXTurn

    def setPlayerXTurn(self):
        self.playerXTurn = True

    def setPlayerOTurn(self):
        self.playerXTurn = False

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
        if self.isPositionOnBoard(pos) and self.isTileEmpty(pos):
            if self.isPlayerXTurn():
                val = 'X'
            else:
                val = 'O'
            self.setPlayerTilePositions(pos,val)
            self.playerXTurn = not self.playerXTurn
            self.setNumEmptyTiles()
            print board
            return True
        else:
            print "Invalid Coordinate"
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
        for y in range(self.height, 0, -1):
##            print 'range height:', range(self.height, 0, -1)
##            print y
            print str(y) + '  ',
            for x in range(1, self.width+1):
##                print 'range width:', range(1, self.width+1)
##                print x
                print str(self.getPlayerTilePositions(Position(x,y))),
            print
        print "Y"
        print "/ X 1 2 3"
        return ''

if __name__ == "__main__":
    board = GameBoard()
    print board
    while True:
        try:
            pos = raw_input("Enter two numbers (x,y) for the Coordinates of your Move -e.g 1,1: ")
            pos = Position(int(pos[0]),int(pos[2]))
            while not board.isPositionOnBoard(pos):
                print "Invalid Coordinate"
                pos = raw_input("Enter two numbers (x,y) for the Coordinates of your Move -e.g 1,1: ")
        except:
            continue
        if board.markTileAtPosition(pos):   #Human player
            if board.isGameOver(): 
                break
        else:
            continue
        print board.getNumEmptyTiles()
        if board.getNumEmptyTiles() < 1:
            break
        if board.markTileAtPosition(board.getRandomComputerPosition()): #Computer player
            if board.isGameOver(): 
                break
        else:
            continue
    print
    print board
    if board.winner():
        print 'Player "%s" wins.' % board.winner()
    elif board.winner() == None:
        print 'Game over'
#    print 'Game over'

    # Some code for testing

##pos = Position(2,2)
##board = GameBoard()
##
##print 'board.getWidth():', board.getWidth()
##
##print 'board.getHeight():', board.getHeight()
##
##print 'board.getPlayerTilePositions(Position(1,1)):', board.getPlayerTilePositions(Position(1,1))
##
##print 'board.getNumTiles():', board.getNumTiles()
##
##print 'board.getNumEmptyTiles():', board.getNumEmptyTiles()
##
##print 'board.getPlayerTilePositions(pos):', board.getPlayerTilePositions(pos)
##
##print 'board.getNumEmptyTiles():', board.getNumEmptyTiles()
##
##print 'board.isTileEmpty(2,1):', board.isTileEmpty(Position(2,1))
##
##print 'board.isTileEmpty(2,2):', board.isTileEmpty(pos)
##
###print 'getRandomPosition():', board.getRandomPosition()
##
##print 'board.isPositionOnBoard(Position(2,3)):', board.isPositionOnBoard(Position(2,3))
##print 'board.isPositionOnBoard(Position(5,4)):', board.isPositionOnBoard(Position(5,4))
##
##print "board.markTileAtPosition(Position(2,2)):", board.markTileAtPosition(Position(2,2))
##print "board.markTileAtPosition(Position(2,2)):", board.markTileAtPosition(Position(2,2))
##print "board.markTileAtPosition(Position(2,2)):", board.markTileAtPosition(Position(2,2))
##print "board.markTileAtPosition(Position(1,1)):", board.markTileAtPosition(Position(1,1))
##print "board.markTileAtPosition(Position(1,3)):", board.markTileAtPosition(Position(1,3))
##print "board.markTileAtPosition(Position(3,1)):", board.markTileAtPosition(Position(3,1))
##print board.isTileEmpty(Position(2,2))
##print board
###board.markTileAtPosition(board.getRandomComputerPosition())
