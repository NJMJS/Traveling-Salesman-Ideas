import random
import math

MAX_X = 100
MAX_Y = 100
MAX = 5

class Point:
    x = 0
    y = 0

    def __init__(self):
        while self.x == 0:
            self.x = random.randint(0,MAX_X)

        while self.y == 0:
            self.y = random.randint(0,MAX_Y)

    def SET(self, x, y):
        self.x = x
        self.y = y

    def distance(self, p2):
        return math.sqrt((self.x-p2.x)*(self.x-p2.x) + (self.y-p2.y)*(self.y-p2.y))


nodes = []
x = 0
while x < 8:
    nodes.append(Point())
    x = x + 1

nodes[0].SET(0,0)
nodes[7].SET(1,1)
nodes[1].SET(2,1)
nodes[6].SET(3,1)
nodes[2].SET(3,0)
nodes[5].SET(2,0)
nodes[3].SET(1,0)
nodes[4].SET(0,3)

for node in nodes:
    print(str(node.x) + "," + str(node.y))
print("-----------------")

def NN():
    order = [] #Contains the order via the location of the node in the nodes list.
    order.append(0) #Starting point set to 0

    remaining = []
    x = 1
    while x < len(nodes):
        remaining.append(x)
        x = x + 1
    
    CONT = True
    while CONT:
        loc = 0
        MIN = 0
        MIN_VAL = MAX_X + MAX_Y
        
        while loc < len(remaining):
            DIST = nodes[order[len(order)-1]].distance(nodes[remaining[loc]])
            if DIST < MIN_VAL:
                MIN = loc
                MIN_VAL = DIST
            
            loc = loc + 1
        order.append(remaining[MIN])
        remaining.remove(remaining[MIN])

        if len(remaining) == 0:
            CONT = False
    order.append(0)

    tot_dist = float(0)
    loc = 1
    while loc < len(order):
        dist = nodes[order[loc-1]].distance(nodes[order[loc]])
        tot_dist += dist
        loc = loc + 1
    return tot_dist






###IDEA 2: Insert locations one at a time, dropping them in their proper slot that adds the least distance.

# Due to being based on insertion sort, the run time is essentially the same as insertion sort: O(n) = n^2
#
def new():
    order = [nodes[0],nodes[1],nodes[2], nodes[0]]
    loc = 3

    "add and order"
    while loc < len(nodes):
        INSERT_TO = 1
        d1 = nodes[loc].distance(order[0])
        d2 = nodes[loc].distance(order[1])
        LOC = 2
        while LOC < len(order):
            D1 = nodes[loc].distance(order[LOC])
            D2 = nodes[loc].distance(order[LOC-1])
            if d1+d2 > D1 + D2:
                d1 = D1
                d2 = D2
                INSERT_TO = LOC            
            LOC += 1

        hold = [order[0]]
        count = 1
        while count < len(order):
            if count == INSERT_TO:
                hold.append(nodes[loc])
            hold.append(order[count])
            count += 1

        order = hold
        loc += 1

    tot_dist = float(0)
    loc = 1
    while loc < len(order):
        dist = order[loc-1].distance(order[loc])
        tot_dist += dist
        loc = loc + 1
    return tot_dist

######################################################

NNCOUNT = 0
NEWCOUNT = 0
TIES = 0
count = 10
while count <= 100:
    NN_WIN = 0
    NEW_WIN = 0
    TIE = 0
    
    COUNT = 0
    while COUNT <= 500:
        nodes = []
        x = 0
        while x < count:
            nodes.append(Point())
            x = x + 1
            
        x = NN()
        y = new()
        if x < y:
            NN_WIN += 1
        elif y < x:
            NEW_WIN += 1
        else:
            TIE += 1
        COUNT += 1
    print("ELEMENTS: " + str(count))
    print("NN won " + str(NN_WIN))
    print("NEW won " + str(NEW_WIN))
    print("TIES: " + str(TIE))
    print()
    NNCOUNT += NN_WIN
    NEWCOUNT += NEW_WIN
    TIES += TIE
    count += 1
print("NN = " + str(NNCOUNT))
print("NEW = " + str(NEWCOUNT))
print("TIES = " + str(TIE))
