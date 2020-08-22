class Maze:
    # The maze is made up of nodes, which have an x,y position, and
    # a way of knowing if it has any neighbours, and which direction
    # they are (using  directions)
    class Node:
        def __init__(self, position):
            self.Position = position
            self.Neighbours = [None, None, None, None]

    def __init__(self, im):
        # We store the size of maze, using the image's size,
        # as well as the full list of the pixel data
        width = im.size[0]
        height = im.size[1]
        data = list(im.getdata(0))

        # These are specific objects in memory for storing the
        # Entrance and Exit of the maze, so the searching algorithms
        # know when they have reached the end
        self.start = None
        self.end = None

        # Top Row Buffer
        topnodes = [None] * width
        count = 0

        # Finding the Start of the maze
        # We loop over the first row of the array
        for x in range(1, width - 1):
            # If the pixel value at where we are looking is 0,
            if data[x] > 0:
                # We set the coordinates of the start node as 0, and
                # where we are on x
                self.start = Maze.Node((0,x))
                # We also note in topNodes, where the start is
                topnodes[x] = self.start
                # We then increment a counter
                count += 1
                break

        for y in range(1, height - 1):

            rowoffset = y * width
            rowaboveoffset = rowoffset - width
            rowbelowoffset = rowoffset + width

            # Initialising the previous, current, and next values
            prv = False
            cur = False
            nxt = data[rowoffset + 1] > 0

            # As we are working top left to bottom right, we store the last node
            # on the left we created for whatever row we are looking over
            leftnode = None

            for x in range(1, width - 1):
                # First, we move prev, current and next onwards, so we only read
                # from the image data once per pixel, not 3
                prv = cur
                cur = nxt
                nxt = data[rowoffset + x + 1] > 0

                # Variable to store the current location in the maze as a
                # Maze.Node object
                n = None

                # If the current pixel we are on is "False", or 0,
                # we are on a wall, so no action is taken
                if cur == False:
                    continue

                # Here, we check for each of the conditions for a Node,
                if prv == True:
                    if nxt == True:
                        # PATH PATH PATH
                        # Here we have 3 Path's in a row, so we only
                        # create a new Node if there is a path above
                        # or below us
                        if data[rowaboveoffset + x] > 0 or data[rowbelowoffset + x] > 0:
                            # Setting n to be a Maze Node at our current coords
                            n = Maze.Node((y,x))
                            # Setting the leftnode's neighbour to be our current
                            # coords, n
                            leftnode.Neighbours[1] = n
                            # Setting n's neighbour on the right (3) to be our current leftnode
                            n.Neighbours[3] = leftnode
                            # Then lastly we update leftnode to be our current node
                            leftnode = n

                    else:
                        # PATH PATH WALL
                        # Here we create a node at the end of a corridor by storing our location
                        # in n as a Maze.Node object
                        n = Maze.Node((y,x))
                        # We then set our last leftnode's Right Neighbour (1) to be our location n
                        leftnode.Neighbours[1] = n
                        # Setting our n Node's left neighbour to the last node we made on the left
                        n.Neighbours[3] = leftnode
                        # We then set leftnode to nothing, as we've hit a wall, and if we found 
                        # another path, there would be a wall between them, and so no link
                        leftnode = None

                else:
                    # WALL PATH PATH
                    # Here we are checking we are at the start or end of a corridor
                    if nxt == True:
                        # We store the current coords in n as a Maze.Node object
                        n = Maze.Node((y,x))
                        # and we set leftnode to be n
                        leftnode = n

                    else:
                        # WALL PATH WALL
                        # Here we are in a vertical corridor, and only create a node
                        # if there is a wall above or below (i.e. a deadend)
                        if (data[rowaboveoffset + x] == 0) or (data[rowbelowoffset + x] == 0):
                            n = Maze.Node((y.x))

                # If node isn't None, we assume we can make a North-South connection somewhere
                if n != None:
                    # We check above, and if it is clear...
                    if (data[rowaboveoffset + x] > 0):
                        # We set "t" to be a topnodes at location x
                        t = topnodes[x]
                        # We set t's neighbour South neighbour to be our current node n
                        t.Neighbours[2] = n
                        # and also set our current n's North neighbour to be t's location
                        n.Neighbours[0] = t

                    # We check below, and if it clear...
                    if (data[rowbelowoffset + x] > 0):
                        # We put this new node n into the topnodes list at position x
                        topnodes[x] = n
                    else:
                        # Otherwise, it is not clear (i.e. A wall), we put None into topnodes at x
                        topnodes[x] = None

                    count +=1

        # Handling the bottom row, we update the rowoffset for the bottom row
        rowoffset = (height - 1) * width
        # We loop over ever pixel in the bottom row, until we find a path pixel (white pixel)
        for x in range(1, width - 1):
            if data[rowoffset + x] > 0:
                # If we find a path, we make the Maze's end object to be a Maze.Node at the bottom
                # of the maze and at location x
                self.end = Maze.Node((height - 1, x))
                # We then store our current location in t as a topnodes object at location x
                t = topnodes[x]
                # We set t's South neighbour to be our End node
                t.Neighbours[2] = self.end
                # and we also set out end node's North neighbour to be our current t
                self.end.Neighbours[0] = t
                # We add one count to our node count
                count += 1
                break

        # some properties to track the number of nodes we have created for this maze,
        # and the width and height of the image
        self.count = count
        self.width = width
        self.height = height
