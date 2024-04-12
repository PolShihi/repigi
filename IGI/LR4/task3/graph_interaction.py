import matplotlib.pyplot as plt
from function_calculation import *
import os


class GraphInteraction:
    @staticmethod
    def get_plot(x_points, y_points_series, y_points_func):
        '''
        This function generates a plot of the series and the function ln(1-x).

        Parameters:
        x_points (list): The x-coordinates of the points.
        y_points_series (list): The y-coordinates of the points calculated using the Taylor series.
        y_points_func (list): The y-coordinates of the points calculated using the ln(1-x) function.
        '''

        plt.figure(num="Series and function")
        plt.plot(x_points, y_points_func, color='red', label='ln(1-x)')
        plt.plot(x_points, y_points_series,
                 color='blue', label='series ln(1-x)')

        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)

        plt.legend()

        plt.text(0.3, -1.1, 'ln(1-x)', color='red')
        plt.text(-0.3, -0.3, 'series ln(1-x)', color='blue')
        plt.annotate('Start of coordinates', xy=(0, 0), xytext=(0.2, 0.18),
                     arrowprops=dict(facecolor='black', arrowstyle='->'))

    @staticmethod
    def show_plot():
        '''
        This function displays the generated plot.
        '''

        plt.show()

    @staticmethod
    def save_plot():
        '''
        This function saves the generated plot as an image file.
        '''

        plt.savefig(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'series_and_function.png'))
