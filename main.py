from PIL import Image
import PIL.ImageOps
from maze import Maze
import time
# For command line arguments
import argparse

# Hard coded path to the file that will be converted to an array
imgPath = './maze.png'

def solve(factory, method, input_file, output_file):

    print("Loading Image...")
    # Importing the Image using PIL
    im = Image.open(imgPath)
    # Inverting the colours on our image, so that instead of a black path on a
    # white background, we get a white path on a black background
    inv_img = PIL.ImageOps.invert(im)

    # We take the array of pixels and turn it into the a graph that is faster to
    # traverse for the searching algorithms
    print("Creating Maze Graph...")
    # We also time how long this one-pass algorithm takes
    t0 = time.time()
    # Creating our Maze Object, by parsing in our inverted Image of the maze
    maze = Maze(inv_img)
    t1 = time.time()
    # We can show some stats on how long this took, so we display the number of
    # nodes that were created for this maze...
    print("Node Count: " + maze.count)
    # As well as calculating how long this took
    total = t1 - t0
    print("Time Elapsed: " + total, "\n")


    # Creating a "solver", which chooses the algorithm we will use to try and find
    # a solution to the maze
    [title, solver] = factory.createsolver(method)


def main():
    pass