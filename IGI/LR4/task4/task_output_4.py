from graph_interaction_square import *
from validation_functions import *


class TaskOutput:
    def __init__(self):
        '''
        Initializes a TaskOutput object.
        '''

        self.graph = GraphInteractionSquare(Square(2, 'black'), 'square')

    def input_for_radius(self):
        '''
        Prompts the user to enter the inradius for the square and validates the input.
        '''

        print(f"Enter inradius (float positive value): ", end='')
        while True:
            try:
                self.graph.square.inradius = consistent_validation(
                    input(), float_validation, positive_validation)
                break
            except ValueError as ex:
                print(ex, ", try again: ", sep='', end='')

    def input_for_color(self):
        '''
        Prompts the user to enter the color for the square and validates the input.
        '''

        print(f"Enter color: ", end='')
        while True:
            color = input()
            if color not in self.graph.available_colors:
                print("Valid colors:", ', '.join(
                    self.graph.available_colors), '\n')
                print("Invalid color", ", try again: ", sep='', end='')
                continue
            self.graph.square.color.color = color
            break

    def input_for_text(self):
        '''
        Prompts the user to enter the text/title for the plot.
        '''

        print(f"Enter text: ", end='')
        self.graph.text = input()

    def show_parametrs(self):
        '''
        Displays the parameters of the square.
        '''

        print(self.graph.square.get_parameters(), end='')

    def show_plot(self):
        '''
        Displays the plot for the square.
        '''

        self.graph.show_plot()

    def save_plot(self):
        '''
        Saves the plot for the square as a PNG file.
        '''

        self.graph.save_plot()
        print('Graph was saved', end='')
