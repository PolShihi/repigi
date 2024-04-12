import math
import statistics


class FunctionCalculation:
    STEP = 0.1
    EPS = 0.1

    @staticmethod
    def math_func(x: float) -> float:
        '''
        This function returns a value that is approximated by the Taylor series. It calculates the natural logarithm of (1 - x) using the math.log function.

        Parameters:
        x (float): The input value for the function. It represents the argument of the natural logarithm.

        Returns:
        float: The result of the function, which is the approximation of the natural logarithm of (1 - x) using the Taylor series.
        '''

        return math.log(1 - x)

    @staticmethod
    def get_series_members(x: float, n: int) -> float:
        '''
        This function returns a list of the members of the Taylor series for the given input value and the number of terms.

        Parameters:
        x (float): The input value for the Taylor series.
        n (int): The number of terms in the Taylor series.

        Returns:
        list: The list of Taylor series members.
        '''

        return [-(x ** i / i) for i in range(1, n + 1)]

    @staticmethod
    def calculate_series_sum_with_eps(x: float) -> float:
        '''
        This function calculates the sum of the Taylor series for the given input value until the absolute difference between the series sum and the true function value is less than or equal to the predefined epsilon (EPS).

        Parameters:
        x (float): The input value for the Taylor series.

        Returns:
        float: The sum of the Taylor series that approximates the true function value.
        '''

        n = 1
        while True:
            series_sum = sum(FunctionCalculation.get_series_members(x, n))
            if abs(series_sum - FunctionCalculation.math_func(x)) <= FunctionCalculation.EPS:
                return series_sum
            n += 1

    @staticmethod
    def calculate_additional_parameters(sequence: list) -> dict:
        '''
        This function calculates additional statistical parameters for a given sequence.

        Parameters:
        sequence (list): The input sequence of numeric values.

        Returns:
        dict: A dictionary containing the calculated parameters:
            ['mean'] (float): The arithmetic mean of the sequence.
            ['median'] (float): The median value of the sequence.
            ['mode'] (list): A list of the mode(s) of the sequence.
            ['variance'] (float): The variance of the sequence.
            ['std_deviation'] (float): The standard deviation of the sequence.
        '''

        parameters = {}
        parameters['mean'] = statistics.mean(sequence)
        parameters['median'] = statistics.median(sequence)
        parameters['mode'] = statistics.multimode(sequence)
        parameters['variance'] = statistics.variance(sequence)
        parameters['std_deviation'] = statistics.stdev(sequence)

        return parameters

    @staticmethod
    def get_range(start, end) -> list:
        '''
        This function generates a list of values within a specified range.

        Parameters:
        start (float): The starting value of the range.
        end (float): The ending value of the range.

        Returns:
        list: A list of values within the specified range, generated with a step size of STEP.
        '''

        values = []
        while start <= end:
            values.append(start)
            start += FunctionCalculation.STEP

        return values

    @staticmethod
    def get_x_y_values() -> tuple:
        '''
        This function generates x and y values for plotting a graph.

        Returns:
        tuple: A tuple containing:
            x_points (list): The x-coordinates of the points.
            y_points_series (list): The y-coordinates of the points calculated using the Taylor series.
            y_points_func (list): The y-coordinates of the points calculated using the true function.
        '''

        x_points = FunctionCalculation.get_range(-1, 1)
        x_points.pop(0)
        x_points.pop(-1)
        y_points_func = [FunctionCalculation.math_func(x) for x in x_points]
        y_points_series = [
            FunctionCalculation.calculate_series_sum_with_eps(x) for x in x_points]

        return x_points, y_points_series, y_points_func
