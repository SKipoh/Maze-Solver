class Maze:
    # The Maze is made up of a series of Nodes joined by 
    class Node:
        def __init__(self, position):
            # x, y coordinates of the pixel in the image of the maze
            self.Position = position
            # Neighbours are any Nodes that are connected directly to
            # this Node in the N, S, E and W directions
            # N, S, E, W
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

        # We also store a buffer list of the top nodes
        topnodes = [None] * width
        # We store a count of how many Nodes we have created for each maze
        count = 0