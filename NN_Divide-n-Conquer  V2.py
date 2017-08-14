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

nodes[0].SET(13,5)
nodes[1].SET(19,15)
nodes[2].SET(6,6)
nodes[3].SET(4,8)
nodes[4].SET(18,12)
nodes[5].SET(20,1)
nodes[6].SET(2,3)
nodes[7].SET(17,7)

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






###IDEA 1: Divide 4 groups, work your ways back up from them. 

# G(n) = 2n + 4G(n/4)   ***roughly***
# G(1) = 1
# G(2) = 1
# G(3) = 1
# G(4) = 1

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


    def groups(items):
        g1 = []
        g2 = []
        g3 = []
        g4 = []
        Ymin = MAX_Y
        Ymax = 0
        Xmin = MAX_X
        Xmax = 0

        #Gets min/max of x and y
        for node in items:
            if node.x < Xmin:
                Xmin = node.x
            elif node.x > Xmax:
                Xmax = node.x
            if node.y < Ymin:
                Ymin = node.y
            elif node.y < Ymax:
                Ymax = node.y

        #Splits into 4 groups based on midpoint of YMID and XMID
        XMID = float((Xmin+Xmax)/2)
        YMID = float((Ymin+Ymax)/2)
        for node in items:
            if node.x < XMID:
                if node.y < YMID:
                    g1.append(node)
                else:
                    g2.append(node)
            else:
                if node.y < YMID:
                    g3.append(node)
                else:
                    g4.append(node)
        return [g1,g2,g3,g4]


    def connect_point(G1,G2):
        "Return 00,01,10,11 and distance."
        d00 = G1[0].distance(G2[0])
        d01 = G1[0].distance(G2[len(G2)-1])
        d10 = G1[len(G1)-1].distance(G2[0])
        d11 = G1[len(G1)-1].distance(G2[len(G2)-1])
        ret = []

        if d00 < d01 and d00 < d10 and d00 < d11:
            G1 = reverse(G1)
            ret = G1
            for node in G2:
                ret.append(node)
            return(d00,ret)
        
        elif d01 < d10 and d01 < d11:
            G1 = reverse(G1)
            G2 = reverse(G2)
            ret = G1
            for node in G2:
                ret.append(node)
            return(d01,ret)
            
        elif d10 < d11:
            ret = G1
            for node in G2:
                ret.append(node)
            return(d10,ret)
                
        else:
            ret = G1
            G2 = reverse(G2)
            for node in G2:
                ret.append(node)
            return(d11,ret)

        
    def connect(G1,G2,G3,G4):
        min1_2 = connect_point(G1,G2)
        min1_3 = connect_point(G1,G3)
        min1_4 = connect_point(G1,G4)
        min2_3 = connect_point(G2,G3)
        min2_4 = connect_point(G2,G4)
        min3_4 = connect_point(G3,G4)

        if (min1_2[0] < min1_3[0] and min1_2[0] < min1_4[0] and min1_2[0] < min2_3[0] and
            min1_2[0] < min2_4[0] and min1_2[0] < min3_4):
            return connect(min1_2[1],G3,G4)
            
        elif (min1_3[0] < min1_4[0] and min1_3[0] < min2_3[0] and min1_3[0] < min2_4[0] and
            min1_3[0] < min2_4[0]):
            hold = connect(G1,G3)
            return connect(min1_3[1],G2,G4)

        elif (min1_4[0] < min2_3[0] and min1_4[0] < min2_4[0] and min1_4[0] < min2_3[0]):
            hold = connect(G1,G4)
            return connect(min1_4[1],G2,G3)

        elif (min2_3[0] < min2_4[0] and min2_3[0] < min3_4[0]):
            hold = connect(G2,G3)
            return connect(min2_3[1],G1,G4)

        elif (min2_4[0] < min3_4[0]):
            hold = connect(G2,G4)
            return connect(min2_4[1],G1,G3)

        else:
            hold = connect(G3,G4)
            return connect(min3_4[1],G1,G2)

        
    def connect(G1,G2,G3):
        min1_2 = connect_point(G1,G2)
        min1_3 = connect_point(G1,G3)
        min2_3 = connect_point(G2,G3)

        if min1_2[0] < min1_3[0] and min1_2[0] < min2_3[0]:
            return connect(min1_2[1],G3)
        
        elif min1_3[0] < min2_3[0]:
            return connect(min1_3[1], G2)
        
        else:
            return connect(min2_3[1],G1)

        
    def connect(G1,G2):
        hold = connect_point(G1,G2)
        return hold[1]
    
    ###################################
    
    def solve2(G1,G2):
        if G1 == []:
            return G2
        elif G2 == []:
            return G1

        if len(G1) > 2:
            hold1 = groups(G1)
            G1 = solve4(hold1[0],hold1[1],hold1[2],hold1[3])
        if len(G2) > 2:
            hold2 = groups(G2)
            G2 = solve4(hold2[0],hold2[1],hold2[2],hold2[3])
        return connect(G1,G2)


    def solve3(G1,G2,G3):
        count = 0
        if G1 == []:
            count += 1
        if G2 == []:
            count += 1
        if G3 == []:
            count += 1

        if count == 2:
            if G1 != []:
                return G1
            elif G2 != []:
                return G2
            else:
                return G3
            
        elif count == 1:
            if G1 == []:
                return solve2(G2,G3)
            elif G2 == []:
                return solve2(G1,G3)
            else:
                return solve2(G2,G3)

        if len(G1) > 2:
            hold1 = groups(G1)
            G1 = solve4(hold1[0],hold1[1],hold1[2],hold1[3])
        if len(G2) > 2:
            hold2 = groups(G2)
            G2 = solve4(hold2[0],hold2[1],hold2[2],hold2[3])
        if len(G3) > 2:            
            hold3 = groups(G3)
            G3 = solve4(hold3[0],hold3[1],hold3[2],hold3[3])
        return connect(G1,G2,G3)


    def solve4(G1,G2,G3,G4):
        count = 0
        if G1 == []:
            count += 1
        if G2 == []:
            count += 1
        if G3 == []:
            count += 1
        if G4 == []:
            count += 1

        if count == 3:
            if G1 != []:
                return G1
            elif G2 != []:
                return G2
            elif G3 != []:
                return G3
            else:
                return G4

        if count == 2:
            if G1 == [] and G2 == []:
                return solve2(G3,G4)
            elif G1 == [] and G3 == []:
                return solve2(G2,G4)
            elif G1 == [] and G4 == []:
                return solve2(G2,G3)
            elif G2 == [] and G3 == []:
                return solve2(G1,G4)
            elif G2 == [] and G4 == []:
                return solve2(G1,G3)
            else:
                return solve2(G1,G2)

        if count == 1:
            if G1 == []:
                return solve3(G2,G3,G4)
            elif G2 == []:
                return solve3(G1,G3,G4)
            elif G3 == []:
                return solve3(G1,G2,G4)
            else:
                return solve3(G1,G2,G3)

        if len(G1) > 2:
            hold1 = groups(G1)
            G1 = solve4(hold1[0],hold1[1],hold1[2],hold1[3])
        if len(G2) > 2:
            hold2 = groups(G2)
            G2 = solve4(hold2[0],hold2[1],hold2[2],hold2[3])
        if len(G3) > 2:
            hold3 = groups(G3)
            G3 = solve4(hold3[0],hold3[1],hold3[2],hold3[3])
        if len(G4) > 2:
            hold4 = groups(G4)
            G4 = solve4(hold4[0],hold4[1],hold4[2],hold4[3])
        return connect(G1,G2,G3,G4)


    
    def find_route(items):
        hold = groups(items)
        return solve4(hold[0],hold[1],hold[2],hold[3])
        

    order = find_route(nodes)
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
