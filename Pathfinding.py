import turtle

class node:
    IDs = -1

    def __init__(self, _x=0, _y=0):
        self.nodes = [] #neighbouring nodes
        self.weights = []
        self.marked = 0
        self.origin = -1 #node used to reach, -1 means origin
        node.IDs += 1
        self.ID = node.IDs
        self.x = _x
        self.y = _y

    def num(self, n):
        self.ID = n
        
    def add_node(self, n, d=1):
        self.nodes.append(n)
        self.weights.append(d)

    def setog(self, n):
        self.origin = n
        
    def mark(self):
        self.marked = 1
    
    def reset(self):
        self.marked = 0
        self.origin = -1
    
    def info(self):
        print("ID: %d\nLocation: %d, %d\nOrigin: %d\nMarked: %d\nNeighbours:" % (self.ID, self.x, self.y, self.origin, self.marked))
        print(self.nodes)
        print(self.weights)
        #for i in range(len(self.nodes)):
        #    print(self.nodes[i], self.weights[i])
        print("")

class network:
    nodes = []

    def add(self, x=0, y=0):
        self.nodes.append(node(x, y))

    def detatch(self, node):
        for i in self.nodes[node].nodes:
            node_index = self.nodes[i].nodes.index(node)
            self.nodes[i].weights.pop(node_index)
            self.nodes[i].nodes.pop(node_index)
        self.nodes[node].nodes = []
        self.nodes[node].weights = []
    
    def delete(self, node): #can delete topmost node. Can't delete prior nodes due to how indexing and referencing other nodes are done
        self.detatch(node)
        self.nodes.pop(node)
        self.IDs -= 1
    
    def linknode(self, n1=0, n2=1):
        d = ((self.nodes[n1].x-self.nodes[n2].x)**2+(self.nodes[n1].y-self.nodes[n2].y)**2)**0.5
        self.nodes[n1].add_node(n2, d)
        self.nodes[n2].add_node(n1, d)
        
    def unlinknode(self, n1=0, n2=1):
        node_index = self.nodes[n1].nodes.index(n2)
        self.nodes[n1].weights.pop(node_index)
        self.nodes[n1].nodes.pop(node_index)
        node_index = self.nodes[n2].nodes.index(n1)
        self.nodes[n2].weights.pop(node_index)
        self.nodes[n2].nodes.pop(node_index)

    def mark(self, node):
        self.nodes[node].mark()
    
    def info(self):
        for i in self.nodes:
            i.info()

    def generate_nodes(self, region, tile_size=1):
        #for j in range(int(region[1]/tile_size+0.5)):
        #    for i in range(int(region[0]/tile_size+0.5)):
        for j in range(math.ceil(region[1]/tile_size)):
            for i in range(math.ceil(region[0]/tile_size)):
                #print(i, j, i*tile_size, j*tile_size)
                self.add((i+0.5)*tile_size, (j+0.5)*tile_size)
                if (i*tile_size > 0):
                    self.linknode(coords2index((i+0.5)*tile_size,(j+0.5)*tile_size,region,tile_size), coords2index((i-0.5)*tile_size,(j+0.5)*tile_size,region,tile_size))
                if (j*tile_size > 0):
                    self.linknode(coords2index((i+0.5)*tile_size,(j+0.5)*tile_size,region,tile_size), coords2index((i+0.5)*tile_size,(j-0.5)*tile_size,region,tile_size))
                #self.gotoscale(i, (j), turtle=turtle)

    def trace(self, end=0):
        path = [end]
        xs = [self.nodes[end].x]
        ys = [self.nodes[end].y]
        while self.nodes[path[len(path)-1]].origin > -1:
            #print(path)
            path.append(self.nodes[path[len(path)-1]].origin)
            xs.append(self.nodes[path[len(path)-1]].x)
            ys.append(self.nodes[path[len(path)-1]].y)
        print(path)
        return path, xs, ys

    def bfs(self, start=0, end=1):
        for i in self.nodes:
            i.reset()
        
        queue = [start]
        tweight = [0]
        
        #print(queue)
        while ((len(queue) > 0) & (queue[0] != end)):
        #while (len(queue) > 0): # Sometimes you want to do the full map. Eg. A to C via B can be done by searching at B and then joining paths A B and B to C

            self.nodes[queue[0]].mark()
            #print(self.nodes[queue[0]].nodes)
            
            #BFS
            for i in self.nodes[queue[0]].nodes:
                if ((self.nodes[i].marked == 0) & (i not in queue)):
                    self.nodes[i].setog(queue[0])
                    queue.append(i)
            #print(queue)
            queue.pop(0)
        
        return self.trace(end)
    
    def djikstra(self, start=0, end=1):
        for i in self.nodes:
            i.reset()
        
        queue = [start]
        tweight = [0]
        
        #print(queue)
        #while ((len(queue) > 0) & (queue[0] != end)):
        while (len(queue) > 0): # Sometimes you want to do the full map. Eg. A to C via B can be done by searching at B and then joining paths A B and B to C

            self.nodes[queue[0]].mark()
            #print(self.nodes[queue[0]].nodes)

            #allnodes[queue[0]] = details of first node
            #allnodes[queue[0]].nodes[i] = node for ith neighbouring node
            #allnodes[allnodes[queue[0]].nodes[i]] = node details for ith neighbouring node
            #allnodes[queue[0]].weights[i] = ith weight for neighbouring node
            #DJIKSTRA
            for i in range(len(self.nodes[queue[0]].nodes)): #go through all neighbouring node
                if (self.nodes[self.nodes[queue[0]].nodes[i]].marked == 0): #if neighbouring node is not marked
                    tempw = tweight[0] + self.nodes[queue[0]].weights[i] #get distance for node from origin
                    search = 1
                    j = 0
                    if (self.nodes[queue[0]].nodes[i]) in queue: #if neighbouring node exists in queue
                        if (tempw < tweight[queue.index(self.nodes[queue[0]].nodes[i])]): #neighbouring node index for tweight value
                            tweight.pop(queue.index(self.nodes[queue[0]].nodes[i]))
                            queue.pop(queue.index(self.nodes[queue[0]].nodes[i]))
                        else:
                            search = 0
                            j = len(queue) + 2
                    while search == 1:
                        search = 0
                        if (j < len(queue)):
                            if(tweight[len(tweight)-1-j] > tempw):
                                j += 1
                                search = 1
                    if (j <= len(queue) + 1):
                        queue.insert(len(tweight)-j, self.nodes[queue[0]].nodes[i])
                        tweight.insert(len(tweight)-j, tempw)
                        self.nodes[self.nodes[queue[0]].nodes[i]].origin = queue[0]
                #print("queue")
                #print(queue)
                #print(tweight)
            tweight.pop(0)
            queue.pop(0)
        
        return self.trace(end)

    # Used to change heurestic to measure estimated distance remaining. abs(x2-x1)+abs(y2-y1) is another option eg. for cartesian movement
    def get_eweight(self, x=0, y=0, n1=0):
        #return abs(self.nodes[n1].x-x)+abs(self.nodes[n1].y-y)) # Taxicab distance
        return ((self.nodes[n1].x-x)**2+(self.nodes[n1].y-y)**2)**0.5 # Straight line distance

    def astar(self, start=0, end=1):
        for i in self.nodes:
            i.reset()

        endx = self.nodes[end].x
        endy = self.nodes[end].y
        
        queue = [start]
        tweight = [0]
        eweight = [self.get_eweight(endx, endy, start)]
        
        #print(queue)
        while ((len(queue) > 0) & (queue[0] != end)):

            self.nodes[queue[0]].mark()
            #print(self.nodes[queue[0]].nodes)

            #allnodes[queue[0]] = details of first node
            #allnodes[queue[0]].nodes[i] = node for ith neighbouring node
            #allnodes[allnodes[queue[0]].nodes[i]] = node details for ith neighbouring node
            #allnodes[queue[0]].weights[i] = ith weight for neighbouring node
            #DJIKSTRA
            for i in range(len(self.nodes[queue[0]].nodes)): #go through all neighbouring node
                if (self.nodes[self.nodes[queue[0]].nodes[i]].marked == 0): #if neighbouring node is not marked
                    tempw = tweight[0] + self.nodes[queue[0]].weights[i] #get distance for node from origin 
                    tempe = tempw + self.get_eweight(endx, endy, self.nodes[queue[0]].nodes[i]) #get estimated distance of route
                    search = 1
                    j = 0
                    if (self.nodes[queue[0]].nodes[i]) in queue: #if neighbouring node exists in queue
                        if (tempw < tweight[queue.index(self.nodes[queue[0]].nodes[i])]): #neighbouring node index for tweight value
                            tweight.pop(queue.index(self.nodes[queue[0]].nodes[i]))
                            eweight.pop(queue.index(self.nodes[queue[0]].nodes[i]))
                            queue.pop(queue.index(self.nodes[queue[0]].nodes[i]))
                        else:
                            search = 0
                            j = len(queue) + 2
                    #Astar
                    while search == 1:
                        search = 0
                        if (j < len(queue)):
                            if(eweight[len(eweight)-1-j] > tempe):
                            #if(tweight[len(tweight)-1-j] > tempw):
                                j += 1
                                search = 1
                    if (j <= len(queue) + 1):
                        #queue.insert(len(tweight)-j, self.nodes[queue[0]].nodes[i])
                        queue.insert(len(eweight)-j, self.nodes[queue[0]].nodes[i])
                        tweight.insert(len(tweight)-j, tempw)
                        eweight.insert(len(eweight)-j, tempe)
                        self.nodes[self.nodes[queue[0]].nodes[i]].origin = queue[0]
                #print("queue")
                #print(queue)
                #print(tweight)
                #print(eweight)
            tweight.pop(0)
            eweight.pop(0)
            queue.pop(0)
        
        return self.trace(end)
        
    def redraw(self, turtle=turtle):
        turtle.color('#000000')
        turtle.clear()
        for i in self.nodes:
            turtle.pu()
            turtle.goto(i.x, i.y)
            turtle.pd()
            turtle.dot(5)
            turtle.write(i.ID)
            for j in i.nodes:
                if j > i.ID:
                    print(j)
                    turtle.goto(self.nodes[j].x, self.nodes[j].y)
                    turtle.pd()
                    turtle.goto(i.x, i.y)
                    turtle.pu()
            turtle.pu()

allnodes = network()
allnodes.add()
allnodes.add(100, -100)
allnodes.add(100, 100)
allnodes.add(-100, -100)
allnodes.add(-200, 100)
allnodes.add(-100, 100)
allnodes.linknode(0, 1)
allnodes.linknode(0, 2)
allnodes.linknode(0, 3)
allnodes.linknode(3, 4)
allnodes.linknode(4, 5)
allnodes.linknode(0, 5)

turtle.setup(1.0, 1.0, 0, 0)
turtle.title("Breath First Search.py")
turtle.speed(0)

allnodes.info()

allnodes.redraw()
start = int(input("Starting Node? "))
end = int(input("End Node? "))

while 1:
    path, xs, ys = allnodes.bfs(start, end)
    
    turtle.color('#FF0000')
    for i in range(len(xs)):
        turtle.goto(xs[i], ys[i])
        turtle.pd()
        turtle.dot(5)
    turtle.pu()
        
    path, xs, ys = allnodes.djikstra(start, end)
    turtle.color('#00FF00')
    for i in range(len(xs)):
        turtle.goto(xs[i], ys[i])
        turtle.pd()
        turtle.dot(5)
    turtle.pu()
        
    path, xs, ys = allnodes.astar(start, end)
    turtle.color('#0000FF')
    for i in range(len(xs)):
        turtle.goto(xs[i], ys[i])
        turtle.pd()
        turtle.dot(5)
    turtle.pu()
    
    print(path)
    start = int(input("Starting Node? "))
    end = int(input("End Node? "))
    allnodes.redraw()
