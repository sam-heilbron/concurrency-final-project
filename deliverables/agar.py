import sys
import threading
import time

BOARD_WIDTH = 10
BOARD_HEIGHT = 10

##########################
###### Player Class ######
##########################
class Player():
    def __init__(self, starting_row, starting_col, player_id):
        self.is_alive = threading.Semaphore(1)
        self.row = starting_row
        self.col= starting_col
        self.size = 1
        self.ID = player_id

    def start_moving(self, gameboard):
        if self.ID == 1:
            self.move("right", gameboard)
        elif self.ID == 3:
            self.move("left", gameboard)
    
    def move(self, direction, gameboard):
        old_row = self.row
        old_col = self.col
        if direction == "right":
            self.col += 1
        elif direction == "left":
            self.col -= 1
        elif direction == "up":
            self.row -= 1
        elif direction == "down":
            self.row += 1
        
        self.eat(gameboard, old_row, old_col)

    def eat(self, gameboard, old_row, old_col):
        print self.ID, "is waiting..."
        while not gameboard.board[self.row][self.col].is_alive.acquire(False):
            print "someone is already eating this blob..try again"
        print self.ID, "acquired the lock"
        gameboard.update_board(self, old_row, old_col, self.row, self.col)

     

#############################
###### Gameboard Class ######
#############################
class Gameboard():
    def __init__(self):
        self.board = [[0 for col in range(BOARD_WIDTH)] for row in range(BOARD_HEIGHT)]
    
    def place_players(self, players):
        for player in players:
            self.board[player.row][player.col] = player 
    
    def update_board(self, player, old_row, old_col, new_row, new_col):
        time.sleep(0.0005)
        self.board[new_row][new_col] = player
        self.board[old_row][old_col] = 0
        print("after moving: \n")
        for row in range(BOARD_WIDTH):
            for col in range(BOARD_HEIGHT):
                if self.board[row][col] == 0:
                    print 0,
                else:
                    print self.board[row][col].ID,
            print "\n"

        print "done updating"

def main(args):
    
    num_players = args[1]
    player1 = Player(0, 0, 1)
    player2 = Player(0, 1, 2)
    player3 = Player(0, 2, 3)

    players = [player1, player2, player3]

    gameboard = Gameboard()

    gameboard.place_players(players)

    print("before moving: \n")
    for row in range(BOARD_WIDTH):
        for col in range(BOARD_HEIGHT):
            if gameboard.board[row][col] == 0:
                print 0,
            else:
                print gameboard.board[row][col].ID,
        print "\n"

    threads = []
    for player in players:
        t = threading.Thread(target=player.start_moving, args=(gameboard,))
        threads.append(t)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main(sys.argv)


