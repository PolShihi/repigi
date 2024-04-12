from graph_interaction import *
from function_calculation import *
from validation_functions import *


class TaskOutput:
    @staticmethod
    def input_for_epsilon():
        '''
        Prompts the user to enter the value for epsilon/precision and validates it.
        '''

        print("Enter epsilon/prexision (positive float value): ", end='')
        while True:
            try:
                FunctionCalculation.EPS = consistent_validation(
                    input(), float_validation, positive_validation)
                break
            except ValueError as ex:
                print(ex, ", try again: ", sep='', end='')

    @staticmethod
    def input_for_step():
        '''
        Prompts the user to enter the value for the step and validates it.
        '''

        print("Enter step (float value between 0 and 1, 0 excluded): ", end='')

        while True:
            try:
                FunctionCalculation.STEP = consistent_validation(
                    input(), float_validation, between_0_and_1_validation)
                break
            except ValueError as ex:
                print(ex, ", try again: ", sep='', end='')

    @staticmethod
    def show_plots():
        '''
        Generates and displays the plot of the series and the true function.
        '''

        GraphInteraction.get_plot(*FunctionCalculation.get_x_y_values())
        GraphInteraction.show_plot()

    @staticmethod
    def save_plot():
        '''
        Generates and saves the plot of the series and the true function as an image file.
        '''

        GraphInteraction.get_plot(*FunctionCalculation.get_x_y_values())
        GraphInteraction.save_plot()

    @staticmethod
    def show_statistics():
        '''
         Calculates and returns various statistical parameters based on the y-values of the series.

        Returns:
        str: A formatted string containing the calculated statistical parameters.
        '''

        y_values_series = FunctionCalculation.get_x_y_values()[1]
        values_info = FunctionCalculation.calculate_additional_parameters(
            y_values_series)
        answer_list = []
        answer_list.append(f"Arithmetic mean value: {values_info['mean']}")
        answer_list.append(f"Median value: {values_info['median']}")
        answer_list.append(
            f"Mode value: {values_info['mode'][0]}, has no meaning")
        answer_list.append(f"Variance value: {values_info['variance']}")
        answer_list.append(
            f"Standart deviation value: {values_info['std_deviation']}")

        return '\n'.join(answer_list)
