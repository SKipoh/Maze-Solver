class Maze:
    # The Maze is made up of a series of Nodes joined by links, which we track with "Neighbours"
    # and "Weights", which describe which direction the Neighbours are, and how hard it is to
    # traverse to that Neighbour
    class Node:
        def __init__(self, position):
            # x, y coordinates of the pixel in the image of the maze
            self.Position = position
            # Neighbours are any Nodes that are connected directly to
            # this Node in the N, S, E and W directions
            # N = 0, S = 2, E = 1, W = 3 (Clockwise around each pixel)
            self.Neighbours = [None, None, None, None]
            # Weights for getting to each neighbour, needed for
            # algorithms that care about some sort of weighting or
            # distance heuristic between nodes, follows the same 
            # "compass" as Neighbours: N S E W
            self.Weights = [None, None, None, None]
    

    def __init__(self, im):
        # We grab and store the width and height of our image as a
        # slight optimisation
        width = im.size[0]
        height = im.size[1]
        # We also store the image data as a single continuous list,
        # instead of a 2D array, which again, is "slightly" faster, though
        # this scales with the sizes of maze (i.e 15k x 15k pixels)
        data = list(im.getdata(0))

        # We have specific, tangible objects for the start and end of our maze,
        # which makes finding out if we have reach the start or end much easier.
        # Initially, we just assign these values nothing
        self.start = None
        self.end = None

        # We also store a buffer list of the nodes above us in the X axis. We multiple the
        # size of the list by the width of the maze, so that the list index corresponds to
        # coordinates in the maze (i.e. if the maze)
        topnodes = [None] * width
        # We store a count of how many Nodes we have created for each maze
        count = 0
        # We also have a variable to track the weight, or distance, between two nodes, we
        # store it so that we only calculate it once each time we need it, but can assign to
        # both nodes we are "linking"
        weight = 0


        # We look for the start of the maze, starting the search from 1 pixel
        # in, as the maze must be surrounded by black walls, and search till
        # we reach the width - 1 (the outer black wall)
        for x in range(1, width - 1):
            # If we come across a path tile (a white pixel)...
            if data[x] > 0:
                # We assign it to be the Maze's start, as a Node object at the
                # first line (0), and whereever we are along it, x
                self.start = Maze.Node((0,x))
                # We also note in the topnodes list, the start object
                topnodes[x] = self.start
                # We also increment our Node counter
                count += 1
                # Once we have found the entrance, we can break out of the loop
                # as there is only a single entrance along the top row of the image
                break
        
        # We then start our one-pass algorithm, but looking over every y value between 1,
        # and the width -1, as we can exclude the outer most walls all the way around,
        # as they must be black to be a valid maze in this program
        for y in range(1, height - 1):
            # Because our image has been prepared as a 1D array, with each line of the image
            # just placed after the last, we need a way of finding the pixel immediately
            # above and below us if the image was 2D. to do this, we calculate the row offset
            # of where we are in relation to the start
            rowoffset = y * width
            # To find the pixel above, we simple subtract the width of the image from our
            # offset
            rowaboveoffset = rowoffset - width
            # and to find the pixel below, we ADD the image width
            rowbelowoffset = rowoffset + width

            # Because of how we are going to do our corner/junction detection, we need to
            # track the previous, current, and next pixel value in our image. for the sake
            # of speed, we only look at 1 pixel, for nxt, and as we move across each line,
            # we shift the cur value to prv, and the nxt value to cur. This means we only
            # need to search our very large data list once per set of 3 pixels (mo' speed)
            prv = False
            cur = False
            nxt = data[rowoffset + 1] > 0

            # We also keep a track of the last node we created on this row, thats still on
            # a connecting path, so we can create a link between them as Neighbours
            leftnode = None

            # For each column, we search from the second row in, to the second to last row...
            for x in range(1, width - 1):
                # First thing we do is move along our 3 pointers, prv becomes cur, cur becomes
                # nxt, and nxt becomes the next pixel (the value of x, plus the offset to get
                # the current row, plus 1)
                prv = cur
                cur = nxt
                nxt = data[rowoffset + x + 1] > 0

                # List to store the current current node as a Maze.Node object
                n = None

                # If the current pixel is False, or a wall, then no take no action and move the
                # loop on to the next pixel
                if cur == False:
                    continue
                
                # Now we check over each condition for a new Node to be created...
                if prv == True:
                    if nxt == True:
                        # PATH PATH PATH
                        # In this instance, we have 3 paths in a row, so we are on a horizontal
                        # path, so we check above and below us to see if we're at a junction
                        if data[rowaboveoffset + x] > 0 or data[rowbelowoffset + x] >0:
                            # We store out current coords as a Maze.Node object in n
                            n = Maze.Node((y,x))
                            # And we also connect the last Node we created to the left
                            leftnode.Neighbours[1] = n
                            # We also set the connection of our current Node to connect to
                            # leftnode
                            n.Neighbours[3] = leftnode
                            # Calculating the weight between our current node n, and the node
                            # to our left, leftnode
                            weight = n.Position[1] - leftnode.Position[1]
                            # We also set the Weight to get from leftnode to n, and vice versa
                            n.Weights[3] = weight
                            leftnode.Weights[1] = weight
                            # We then also update the new leftnode, to be n, our current node,
                            # so we can continue searching
                            leftnode = n
                    
                    else:
                        # PATH PATH WALL
                        # Here we create a Node at the end of a corridor at our current location
                        n = Maze.Node((y,x))
                        # We then update the last node we created, leftnode, so that it's right
                        # neighbour is our new Node, n
                        leftnode.Neighbours[1] = n
                        # Setting our new Node, n's West Neighbour to be our last node, leftnode
                        n.Neighbours[3] = leftnode
                        # As we've hit a wall as the next tile, we empty leftnode, as nothing will
                        # connect to the right of our current Node n, because of the wall
                        leftnode = None
                
                else:
                    if nxt == True:
                        # WALL PATH PATH
                        # Here, we are at the start of a new corridor, so we create a new Node,
                        n = Maze.Node((y,x))
                        # and set it as leftnode as well
                        leftnode = n
                    
                    else:
                        # WALL PATH WALL
                        # In this case, we are in a vertical corridor, and only create a node if
                        # there is a Node above or below us (i.e. we are in a corner/deadend)
                        if (data[rowaboveoffset + x] == 0) or data[rowbelowoffset + x] == 0):
                            n = Maze.Node((y,x))
                
                # If we have a created a Node this loop (i.e. n is NOT None), we look to see if
                # there is a Node above it that we need to connect too
                if n != None:
                    # We check above to see if it is path pixel...
                    if (data[rowaboveoffset + x] > 0):
                        # We set "t" to be whatever Node is directly above us, which is stored
                        # in the topnodes buffer at whatever our x position is
                        t = topnodes[x]
                        # We set t's South neighbour to be our current Node n's position
                        t.Neighbours[2] = n
                        # At the same time, we set n's North Neighbour to be t, the Node
                        # directly above it
                        n.Neighbours[0] = t
                
                # We also check below us to see if there is a path...
                if (data[rowbelowoffset + x] > 0):
                    # If there is, we set our current Node n as the topnode at this x coordinate
                    topnodes[x] = n
                else:
                    # If there is not, then it is a wall, and so we have no need for a new
                    # topnode at our x coordinate
                    topnodes[x] = n
                
                # We then increase our count of total Nodes created
                count += 1
        
        # We recalcualte the rowoffset, so that we look at the bottom row 
        rowoffset = (height - 1) * width
        # Like finding the start, we look over each pixel on the final row...
        for x in range(1, width - 1):
            # When we find the white, path pixel...
            if data[rowoffset + x] > 0:
                # We set the Maze's end to be our current x coord, and the bottom row of the maze
                self.end = Maze.Node((height - 1, x))
                # We set t to the Node directly above us at our current x coord
                t = topnodes[x]
                # We set's South Neighbour to be the Maze's End Node
                t.Neighbours[2] = self.end
                # We also increase our Node count by 1
                count += 1
                break


        # We set some properties for the Maze such as Node count and the height and width of it
        self.count = count
        self.width = width
        self.height = height
