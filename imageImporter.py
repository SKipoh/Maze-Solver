import cv2
import numpy as np
import matplotlib.pyplot as plt

def img2array(imgPath):

    # Converting the image to a numpy array
    img = cv2.imread(imgPath, 0)
    # Inverting the black and white colours
    img_inverted = (255.0 - img)
    # Forcing the value ranges to be be between 0 and 1
    new_img = img_inverted / 255.0

    plt.imshow(new_img, cmap="Greys_r")
    plt.show()

    print(new_img.shape)
    return new_img
