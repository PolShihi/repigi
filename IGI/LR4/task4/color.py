class Color:
    def __init__(self, color):
        '''
        Initializes a Color object.

        Parameters:
        color(str): String representing the color value.
        '''

        self.__color = color

    @property
    def color(self):
        '''
        Getter method for accessing the color value.

        Returns:
        str: String representing the color value.
        '''

        return self.__color

    @color.setter
    def color(self, value):
        '''
        Setter method for modifying the color value.

        Parameters:
        value(str): String representing the new color value.
        '''

        self.__color = value
