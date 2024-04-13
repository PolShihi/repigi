from abc import ABC, abstractmethod


class GeometricShape(ABC):
    @abstractmethod
    def calculate_area(self):
        '''
        Abstract method to calculate the area of a geometric shape. Subclasses must implement this method.
        '''

        pass
