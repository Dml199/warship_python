import os
import random


clear = lambda: os.system("clear")




class ErrorLog:

    def __init__(self):

        self.list = [""]

    def push_error(self, error):
        self.list.append("Error log: " + error)

    def delete_prev(self):
        self.list.pop(len(self.list) - 1)

    def refresh(self, error):
        self.push_error(error)
        if len(self.list) > 5:
            self.list.pop(0)

    def displayError(self):
        print(self.list[-1])


class Board:

    error = ErrorLog()

    def __init__(self, isAiBoard):
        self.board = [[]]
        self.shipList = []

        self.isAiBoard = isAiBoard
        self.boardIsFull = False
        self.iterations = 0
        self.startQuant = {"three": 1, "two": 2, "one": 4}
        self.currentQuant = {"three": 0, "two": 0, "one": 0}
        if isAiBoard:
            self.name = "AiBoard"
            self.isRandom = True
        else:
            self.name = "PlayerBoard"
            self.isRandom = False

    def fillWithZeros(self):
        self.board = [[0 for x in range(6)] for y in range(6)]

    def displayBoard(self):

        self.renew_board()

        print("    ", end="")

        for k in range(6):
            print("|", k + 1, "| ", end="")
        print("\n")
        for i in range(6):
            for j in range(6):

                if j == 0:
                    print(i + 1, "|", end="")
                print("   " + str(self.board[j][i]) + "  ", end="")
                if j == 5:
                    print("\n")

    def checkCoordAllowence(self, ship):

        for a in range(len(ship.dotList)):
            for x in range(-1, 2, 1):
                for y in range(-1, 2, 1):
                    for k in range(len(self.shipList)):
                        for j in range(len(self.shipList[k].dotList)):
                            if (
                                ship.dotList[a].x + x == self.shipList[k].dotList[j].x
                                and ship.dotList[a].y + y
                                == self.shipList[k].dotList[j].y
                            ):
                                self.error.refresh("Too close to existing ship.")
                                self.iterations += 1
                                if self.iterations > 20:
                                    self.iterations = 0
                                    self.shipList.clear()
                                    self.nullify_quant()
                                    self.renew_board()
                                raise ValueError("Too close to existing ship.")

    def displayInfo(self):
        print("                    Game of sea warships.")
        print("_________________________________________________________________")


    def nullify_quant(self):
        self.currentQuant["three"] = 0
        self.currentQuant["two"] = 0
        self.currentQuant["one"] = 0

    def check_quantity(self):
        try:
            if self.currentQuant["three"] > self.startQuant["three"]:
                self.error.refresh("Can't place more than one of that ship.")
                raise ValueError("Can't place more than one of that ship.")
            if self.currentQuant["two"] > self.startQuant["two"]:
                self.error.refresh("Can't place more than one of that ship.")
                raise ValueError("Can't place more than two of that ship.")
            if self.currentQuant["one"] > self.startQuant["one"]:
                self.error.refresh("Can't place more than one of that ship.")
                raise ValueError("Can't place more than four of that ship.")
            if self.startQuant == self.currentQuant:
                self.boardIsFull = bool(1)

        except ValueError as e:
            print(e)

    def add_ship(self):

        try:
            type = None
            if self.isRandom:
                randInt = random.randint(1, 3)
                match randInt:
                    case 3:
                        test_type = "three"
                    case 2:
                        test_type = "two"
                    case 1:
                        test_type = "one"
            else:
                test_type = input("Enter type of ship (amount of dots - three/two/one):")

            if test_type == "three" or test_type == "two" or test_type == "one":
                type = test_type
            else:
                self.error.refresh("Type does not exist.")
                raise ValueError("Type does not exist.")

            if (
                type == "three"
                and self.currentQuant["three"] == self.startQuant["three"]
            ):
                self.error.refresh("Can't place more than already there.")
                raise ValueError("Can't place more than already there.")

            if type == "two" and self.currentQuant["two"] == self.startQuant["two"]:
                self.error.refresh("Can't place more than already there.")
                raise ValueError("Can't place more than already there.")

            if type == "one" and self.currentQuant["one"] == self.startQuant["one"]:
                self.error.refresh("Can't place more than already there.")
                raise ValueError("Can't place more than already there.")

            isHorizontal = None
            if self.isRandom:
                randInt = random.randint(1, 2)
                match randInt:

                    case 2:
                        isHorizontal = bool(int(0))
                    case 1:
                        isHorizontal = bool(int(1))

            else:
                isHorizontal = bool(
                    int(
                        input(
                            "Horizontal or vertical orientation of the ship?(1 - for horizontal / 0 - for vertical):"
                        )
                    )
                )

            if isHorizontal != True and isHorizontal != False:
                self.error.refresh("Wrong type of the variable")
                raise ValueError("Wrong type of the variable.")
            x = None
            y = None

            if self.isRandom:
                x = random.randint(1, 6)
                y = random.randint(1, 6)
            else:
                x = int(input("Enter x coordinate for the ship to be placed:"))
                y = int(input("Enter y coordinate for the ship to be placed:"))

            if (
                (x > 6 or x < 1 or y > 6 or y < 1)
                or (x >= 5 and isHorizontal == 1 and type == "three")
                or (y >= 5 and isHorizontal == 0 and type == "three")
            ) or (
                (x >= 6 and isHorizontal == 1 and type == "two")
                or (y >= 6 and isHorizontal == 0 and type == "two")
            ):
                self.error.refresh("Coordinates are outside of the field.")
                raise ValueError("Coordinates are outside of the field. ")

            ship = Ship(type, x - 1, y - 1, isHorizontal, self.isAiBoard)
            self.checkCoordAllowence(ship)
            self.shipList.append(ship)
            self.error.refresh("No error. Please continue")
            self.currentQuant[type] += 1
        except ValueError as e:
            print(e)

    def displayMyBoard(self):

        print("    ", end="")

        for k in range(6):
            print("|", k + 1, "| ", end="")
        print("\n")
        for i in range(6):
            for j in range(6):

                if j == 0:
                    print(i + 1, "|", end="")
                print("   " + str(self.board[j][i]) + "  ", end="")
                if j == 5:
                    print("\n")

    def renew_board(self):
        self.fillWithZeros()
        for k in self.shipList:
            for l in k.dotList:
                self.board[l.x][l.y] = l.type

    def generate_board(self):
        while not self.boardIsFull:
            clear()
            
            self.displayInfo()
            self.displayBoard()
            self.error.displayError()
            self.add_ship()
            self.check_quantity()
            self.renew_board()


class Ship:

    def __init__(self, type, x, y, isHorizontal, isAiBoard):

        if isAiBoard:
            self.typeOfUnit = 4
        else:
            self.typeOfUnit = 1

        self.dotList = []
        self.interval = 3 if type == "three" else 2 if type == "two" else 1

        if isHorizontal:

            for j in range(self.interval):

                self.dotList.append(Dot(x + j, y, self.typeOfUnit))

        else:

            for i in range(self.interval):

                self.dotList.append(Dot(x, y + i, self.typeOfUnit))


class Dot:

    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        if type == 1:
            self.type = "■"

        if type == 2:
            self.type = "X"

        if type == 3:
            self.type = "☒"

        if type == 4:
            self.type = "0"


class Player:

    def __init__(self, isAi):
        Player.error_log = ErrorLog()
        self.gameIsOver = False

        if isAi:
            self.aiBoard = True
            self.name = "Computer-Ai"
        else:
            self.aiBoard = False
            self.name = "User"

    def cleanerFunc(self, boardInst):
        for m in boardInst.shipList:
            if len(m.dotList) == 0:
                boardInst.shipList.remove(m)

    def checkForDotsRemaining(self, boardInst):
        if len(boardInst.shipList) == 0:
            self.gameIsOver = True
            print("Game is over. " + self.name + " has won.")

    def makeAMove(self, boardInst):
     
        if not self.aiBoard:
           
            self.coordX = int(input("Enter the coordinate X:"))
            self.coordY = int(input("Enter the coordinate Y:"))
            
            if ((self.coordX > 6 or self.coordX < 1 or self.coordY > 6 or self.coordY < 1)):
                self.error_log.refresh("Coordinates are outside of the field.")
                raise ValueError("Coordinates are outside of the field. ")
            else: self.error_log.refresh("No error.")
               
        else:
            self.coordX = random.randint(1, 6)
            self.coordY = random.randint(1, 6)

            
        if boardInst.board[self.coordX-1][self.coordY-1] == "x" or boardInst.board[self.coordX-1][self.coordY-1] == "☒":
                    if not self.aiBoard:
                        self.error_log.refresh("Cant fire the same spot")
                    raise ValueError("Cant fire the same spot.")            
        boardInst.board[self.coordX-1][self.coordY-1] = "x"
        for k in boardInst.shipList:
            for l in k.dotList:
                if l.y == self.coordY - 1 and l.x == self.coordX - 1:
                    boardInst.board[self.coordX - 1][self.coordY - 1] = "☒"
               
                    k.dotList.remove(l)
                    self.cleanerFunc(boardInst)
                    self.checkForDotsRemaining(boardInst)
    
                 


def mainLoop():

    boardInst = Board(False)
    aiBoard = Board(True)
    user = Player(False)
    ai = Player(True)
    
    boardInst.generate_board()
    aiBoard.generate_board()

    while not ai.gameIsOver and  not user.gameIsOver:
        clear()
        print("This is Users board:")
        boardInst.displayMyBoard()
        print("This is computer's board:")
        aiBoard.displayMyBoard()
        user.error_log.displayError()
        try:
          
          ai.makeAMove(boardInst)
          user.makeAMove(aiBoard)
        except ValueError as e:
            print(e)


mainLoop()
