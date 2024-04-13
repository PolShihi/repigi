from square import *
import matplotlib.pyplot as plt
from matplotlib import colors
import os


class GraphInteractionSquare:
    def __init__(self, square: Square, text):
        '''
        Initializes a GraphInteractionSquare object.

        Parameters:
        square (Square): The Square object to interact with.
        text (str): The text/title for the plot.
        '''

        self.square = square
        self.text = text
        self.available_colors = list(colors.CSS4_COLORS.keys())

    def get_plot(self):
        '''
        Generates the plot for the square.
        '''

        plt.figure(num=self.text)
        side_length = 2 * self.square.inradius
        x = [0, 0, side_length, side_length, 0]
        y = [0, side_length, side_length, 0, 0]

        plt.plot(x, y, color='none')
        plt.fill(x, y, self.square.color.color)
        plt.title(self.text)

    def show_plot(self):
        '''
        Displays the plot for the square.
        '''

        self.get_plot()
        plt.show()

    def save_plot(self):
        '''
        Saves the plot for the square as a PNG file.
        '''

        self.get_plot()
        plt.savefig(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), self.text + '.png'))
