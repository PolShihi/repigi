from geometric_shape import *
from color import *


class Square(GeometricShape):
    SHAPE_NAME = "Square"

    def __init__(self, inradius, color):
        '''
        Initializes a Square object.

        Parameters:
        inradius (float): The inradius of the square.
        color (str): The color of the square.
        '''

        self.inradius = inradius
        self.color = Color(color)

    def calculate_area(self):
        '''
        Calculates the area of the square.

        Returns:
        float: The area of the square.
        '''

        return (self.inradius * 2) ** 2

    def get_parameters(self):
        '''
        Retrieves the parameters and details of the square.

        Returns:
        str: A string containing the shape name, inradius, color, and area of the square.
        '''

        return f"Shape: {self.SHAPE_NAME}, inradius: {self.inradius}, color: {self.color.color}, area: {self.calculate_area()}"

    @classmethod
    def get_shape_name(cls):
        '''
        Retrieves the name of the square shape.

        Returns:
        str: The name of the square shape.
        '''

        return cls.SHAPE_NAME
