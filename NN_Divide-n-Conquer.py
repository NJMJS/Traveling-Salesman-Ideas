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

nodes[0].SET(6,3)
nodes[1].SET(10,10)
nodes[2].SET(2,10)
nodes[3].SET(6,4)
nodes[4].SET(2,8)
nodes[5].SET(7,10)
nodes[6].SET(2,3)
nodes[7].SET(2,2)

#for node in nodes:
#    print(str(node.x) + "," + str(node.y))
#print()

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






###IDEA 1: Divide into smaller groups and connect them on the way back. Better until case sizes around 20

# G(n) = 2n + 2*G(n/2)                    where n is even
# G(n) = 2n + G((n/2)-.5) + G((n/2)+.5)   where n is odd
# G(1) = 1
# G(2) = 1

# Equates to around O(n) = 2 * n * log(2,n) + 1
# Is better than NN to around 22 locations (50/50 split)
def new():
    def reverse(l):
        ret = []
        x = len(l)-1
        while x >=0:
            ret.append(l[x])
            x = x - 1
        return ret

    def solve(G1,G2):
        d00 = G1[0].distance(G2[0])
        d01 = G1[0].distance(G2[len(G2)-1])
        d10 = G1[len(G1)-1].distance(G2[0])
        d11 = G1[len(G1)-1].distance(G2[len(G2)-1])
        ret = []
        
        if d00 < d01 and d00 < d10 and d00 < d11:
            #Connect G1[0] and G2[0]
            G1 = reverse(G1)
            ret = G1
            for node in G2:
                ret.append(node)

        elif d01 < d10 and d01 < d11:
            #Connect G1[0] and G2[Last]
            G1 = reverse(G1)
            G2 = reverse(G2)
            ret = G1
            for node in G2:
                ret.append(node)

        elif d10 < d11:
            #Connect G1[Last] and G2[0]
            ret = G1
            for node in G2:
                ret.append(node)

        else:
            #Connect G1[Last] and G2[Last]
            ret = G1
            G2 = reverse(G2)
            for node in G2:
                ret.append(node)
        return ret
    
    def group(items):
        if len(items) == 2 or len(items) == 1:
            return items #Already connected list.
        else:
            "Split to two groups; divide based on the range of x and y, whichever is smaller is the divide."
            g1 = []
            g2 = []
            x_min = MAX_X
            y_min = MAX_Y
            x_max = 0
            y_max = 0

            for node in items:
                if node.x < x_min:
                    x_min = node.x
                elif node.x > x_max:
                    x_max = node.x

                if node.y < y_min:
                    y_min = node.y
                elif node.y >y_max:
                    y_max = node.y

            if x_max - x_min > y_max - y_min:
                div_x = float(x_max - (x_max-x_min)/2)
                put_in = False
                for node in items:
                    if node.x < div_x:
                        g1.append(node)
                    elif node.x > div_x:
                        g2.append(node)
                    elif put_in:
                        g1.append(node)
                        put_in = False
                    else:
                        g2.append(node)
                        put_in = True
                if len(g1) == 0 or len(g2) == 0:
                    if len(g1) == 0:
                        return g2
                    return g1
                
                G1 = group(g1)
                G2 = group(g2)
                return solve(G1,G2)
            else:
                div_y = float(y_max - (y_max-y_min)/2)
                put_in = True
                for node in items:
                    if node.y < div_y:
                        g1.append(node)
                    elif node.y > div_y:
                        g2.append(node)
                    elif put_in:
                        g1.append(node)
                        put_in = False
                    else:
                        g2.append(node)
                        put_in = True
                if len(g1) == 0 or len(g2) == 0:
                    if len(g1) == 0:
                        return g2
                    return g1

                G1 = group(g1)
                G2 = group(g2)
                return solve(G1,G2)

    order = group(nodes)
    order.append(order[0])
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
