import random
import math
class Game:

    
    def __init__(self):
        A = random.randint(1, 1000000)
        B = random.randint(1, 1000000)



        S = A * B

        while S > 1000000:
            A = random.randint(1, 1000000)
            B = random.randint(1, 1000000)
            S = A * B

        matrix = []

        for i in range(A):
            matrix.append([0] * B)
            


        randA = random.randint(0, A - 1)
        randB = random.randint(0, B - 1)
        matrix[randA][randB] = 1
        self.goal = (randA, randB)
        randA = random.randint(0, A - 1)
        randB = random.randint(0, B - 1)
        self.start = (randA, randB)
        self.matrix = matrix
        self.S = S
        self.A = A
        self.B = B
        self.moves = ['right', 'left', 'up', 'down']


    def is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n) + 1)):
            if n % i == 0:
                return False
        return True

    def next_prime(self, n):
        while True:
            n += 1
            if self.is_prime(n):
                return n

    def is_found(self, i, j, matrix):
        if matrix[i][j] == 1:

            return True

        return False

    def traverse(self):
        current = self.start
        
        move = 'right'
        current_moves_r = 2
        current_moves_d = 3
        R, D = 0, 0
        for k in range(35*self.S):

            i, j = current

            if self.is_found(i, j, self.matrix):
                self.k = k

                return True
            
            if k % 35 == 0:
                current = self.move_up(current)
                continue
            

            match move:
                case 'right':
                    if R == current_moves_r:
                        move = 'down'
                        R = 0
                        current_moves_d = self.next_prime(current_moves_d)
                    else:
                        current = self.move_right(current)
                        R += 1
                
                case 'down':
                    if D == current_moves_d:
                        move = 'right'
                        D = 0
                        current_moves_r = self.next_prime(current_moves_r)
                    else:
                        current = self.move_down(current)
                        D += 1
    
                
                
        return False
    
    def move_right(self, current):
        i, j = current
        j = (j +1)%self.B
        return (i, j)


    def move_up(self, current):
        i, j = current
        i  = (i - 1)%self.A
        return (i, j)

    def move_down(self, current):
        i, j = current
        i = (i + 1)%self.A
        return (i, j)




if __name__ == '__main__':
    passed = 0
    average = 0
    highest = 0
    for i in range(10):
        game = Game()
        if game.traverse():
            passed += 1
            res = int(game.k//game.S)
            if res > highest:
                highest = res
        else:
            print(game.A, game.B, game.S)   
            print("Failed")

    print("Passed: ", passed, " out of 10")
    print("Highest step count (x * S); x: ", highest)

