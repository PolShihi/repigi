import numpy as np


class MatrixCalculation:
    def __init__(self, n, m):
        '''
        Initialize a MatrixCalculation object.

        Parameters:
        n (int): The number of rows in the matrix.
        m (int): The number of columns in the matrix.
        '''

        self.__n = n
        self.__m = m
        self.__matrix = np.zeros((n, m))
        self.__rand_min = 0
        self.__rand_max = 100

    @property
    def n(self):
        '''
        int: The number of rows in the matrix.
        '''

        return self.__n

    @property
    def m(self):
        '''
        int: The number of columns in the matrix.
        '''

        return self.__m

    @property
    def rand_min(self):
        '''
        int: The minimum value for random number generation.
        '''

        return self.__rand_min

    @property
    def rand_max(self):
        '''
        int: The maximum value for random number generation.
        '''

        return self.__rand_max

    @property
    def matrix(self):
        '''
        numpy.ndarray: The matrix for calculations.
        '''

        return self.__matrix

    @n.setter
    def n(self, value):
        '''
        Set the number of rows in the matrix.

        Parameters:
        value (int): The number of rows in the matrix.
        '''

        self.__n = value
        self.__matrix = np.zeros((self.__n, self.__m))

    @m.setter
    def m(self, value):
        '''
        Set the number of columns in the matrix.

        Parameters:
        value (int): The number of columns in the matrix.
        '''

        self.__m = value
        self.__matrix = np.zeros((self.__n, self.__m))

    @rand_min.setter
    def rand_min(self, value):
        '''
        Set the minimum value for random number generation.

        Parameters:
        value (int): The minimum value for random number generation.

        Raises:
        ValueError: If the minimum value is greater than or equal to the maximum value.
        '''

        if value >= self.__rand_max:
            raise ValueError("min >= max")
        self.__rand_min = value

    @rand_max.setter
    def rand_max(self, value):
        '''
        Set the maximum value for random number generation.

        Parameters:
        value (int): The maximum value for random number generation.

        Raises:
        ValueError: If the maximum value is less than or equal to the minimum value.
        '''

        if value <= self.__rand_min:
            raise ValueError("min >= max")
        self.__rand_max = value

    def generate_matrix(self):
        '''
        Generate a random matrix.

        Returns:
        numpy.ndarray: The generated matrix.
        '''

        self.__matrix = np.random.randint(
            self.__rand_min, self.__rand_max, size=(self.__n, self.__m))
        return self.__matrix

    def sum_below_diagonal(self):
        '''
        Calculate the sum of elements below the main diagonal of the matrix.

        Returns:
        int or float: The sum of elements below the main diagonal.
        '''

        return np.sum(self.__matrix[np.tril_indices(n=self.__n, m=self.__m, k=-1)])

    def diagonal_std_deviation(self):
        '''
        Calculate the standard deviation of the elements on the main diagonal of the matrix.

        Returns:
        float: The calculated standard deviation.
        '''

        diagonal = np.diagonal(self.__matrix)
        return np.round(np.std(diagonal), 2)

    def diagonal_std_deviation_formula(self):
        '''
        Calculate the standard deviation of the elements on the main diagonal of the matrix.

        Returns:
        float: The calculated standard deviation.
        '''

        diagonal = np.diagonal(self.__matrix)
        mean = np.mean(diagonal)
        squared_diff = np.square(diagonal - mean)
        variance = np.mean(squared_diff)
        std_deviation = np.sqrt(variance)
        return np.round(std_deviation, 2)
