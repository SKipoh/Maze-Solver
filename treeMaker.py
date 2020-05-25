import cv2
import numpy as np
import matplotlib.pyplot as plt
import graph as graph


def img2array():
    # Hard coded path to the file that will be converted to an array
    imgPath = 'C:/Users/jack_/OneDrive/Documents/_Code/Maze Solver/maze.png'

    # Converting the image to a numpy array
    img = cv2.imread(imgPath, 0)
    # Inverting the black and white colours
    img_inverted = (255.0 - img)
    # Normalising the values to be between 0 and 1
    new_img = img_inverted / 255.0

    #print(type(new_img))

    plt.imshow(new_img, cmap="Greys_r")
    plt.show()

    # Returning the numpy array
    return new_img

    


def createGraph(imgArray):
    # Creating a variable to track if we've
    # found the start of the Maze
    startFound = False



    # Next we find the number of dimensions in the array
    # (which should only be 2 in this case). This needs
    # to be stored, as nparray.shape is just a function
    # that returns a list each time it is called
    aDims = imgArray.shape
    # Next we instantiate an instance of the graph object
    # to store the eventual graph
    mazeGraph = graph()

    for y in range(aDims[0]):
        # First, we check if we're looking at the first row
        # in the Maze
        if y == 0:
            # If it is, we then scan the first line for the 
            # start of the maze
            for x in range(aDims[1]):
                # We check for the one White pixel that signals
                # the start of the Maze
                if imgArray[y, x] == 1:
                    # Once we find the start, we add it to the
                    # graph labeled as "Start", then we can exit
                    # out of the loop, as there will only ever be
                    # one Start point on the top of the maze
                    mazeGraph.add_vertex("Start")
            
        # After we find the start of the maze, we can loop over each
        # row of the maze to check if we've found 
        for x in range(aDims[1]):
            # We check if the current pixel is white (part of the path)
            if imgArray[y, x] == 1:
                if imgArray



    if fLine == True:
        mazeGraph.add_edge("Start")
        startFound = True




def main():
    # Grabbing our hardcoded file and returning a
    # Numpy array
    a = img2array()
    print(type(a))
    # Creating some variables to store the size
    # of the maze and the shape
    aRows, aCols = a.shape
    aDims = a.shape
    print(aDims[0])

    createGraph(a)


    print()
    print(aRows)
    print(aCols)


main()
