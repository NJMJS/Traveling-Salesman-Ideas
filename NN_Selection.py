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






###IDEA 2: Select the best one to add at the time, and put it in.
# Due to being based on selection sort, the run time is similar.
# Due to having to check everything in the list to find the inseriton point,
#   multiply by an extra n: O(n) = n^3

# N^3 disqualifies it to start with, but it never even won 1/5 of the cases on any number of nodes

def new():
    def insert(slot, node, order):
        loc = 0
        hold = []
        while loc < len(order):
            if loc == slot:
                hold.append(node)
            hold.append(order[loc])
            loc += 1
        return hold
        
    order = [nodes[0],nodes[1],nodes[2], nodes[0]]

    loc = 3
    remaining = []
    while loc < len(nodes):
        remaining.append(nodes[loc])
        loc += 1

    while len(remaining) > 0:
        SELECT = 0
        SLOT = 1
        d1 = order[0].distance(remaining[0])
        d2 = order[1].distance(remaining[0])
        LOC = 0
        while LOC < len(remaining):
            slot = 1
            while slot < len(order):
                D1 = order[slot].distance(remaining[LOC])
                D2 = order[slot-1].distance(remaining[LOC])
                if D1 + D2 < d1 + d2:
                    d1 = D1
                    d2 = D2
                    SLOT = slot
                    SELECT = LOC
                slot += 1
            LOC += 1
                
        order = insert(SLOT,remaining[SELECT],order)
        remaining.remove(remaining[SELECT])
    
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
