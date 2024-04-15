'''Contains serializers for forest object'''

import csv
import pickle
import os
import abc

class Forest_serializer(abc.ABC):
    '''Class for serialization and deserialization forest object'''

    def __init__(self, filename):
        '''Initializes the filename field'''
        self.filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    @abc.abstractmethod
    def write_forest(self, forest):
        '''Writes a forest object to a file with name in the filename field'''
        pass
    @abc.abstractmethod
    def append_forest(self, forest):
        '''Append a forest object to a file with name in the filename field'''
        pass

    @abc.abstractmethod
    def read_forest(self):
        '''Read a forest object from a file with name in the filename field'''
        pass


class Forest_serializer_csv(Forest_serializer):
    __doc__ = Forest_serializer.__doc__ + ", using csv module"

    COLUMNS = ['type', 'total_quantity', 'healthy_quantity']

    def __init__(self, filename):
        super().__init__(filename)
        self.write_forest([])

    def write_forest(self, forest):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.COLUMNS)
            writer.writeheader()
            writer.writerows(forest)

    def append_forest(self, forest):
        with open(self.filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.COLUMNS)
            writer.writerows(forest)

    def read_forest(self):
        with open(self.filename, 'r', newline='') as file:
            reader = csv.DictReader(file)
            forest = [{'type': el['type'], 'total_quantity': int(el['total_quantity']), 'healthy_quantity': int(el['healthy_quantity'])} for el in reader]

        return forest
    
    __init__.__doc__ = Forest_serializer.__init__.__doc__
    write_forest.__doc__ = Forest_serializer.write_forest.__doc__
    append_forest.__doc__ = Forest_serializer.append_forest.__doc__
    read_forest.__doc__ = Forest_serializer.read_forest.__doc__


class Forest_serializer_pickle(Forest_serializer):
    __doc__ = Forest_serializer.__doc__ + ", using pickle module"

    def __init__(self, filename):
        super().__init__(filename)

    def write_forest(self, forest):
        with open(self.filename, 'wb') as file:
            pickle.dump(forest, file)

    def append_forest(self, forest):
        with open(self.filename, 'rb') as file:
            file_forest = pickle.load(file)

        with open(self.filename, 'wb') as file:
            pickle.dump(file_forest + forest, file)

    def read_forest(self):
        with open(self.filename, 'rb') as file:
            forest = pickle.load(file)

        return forest
    
    __init__.__doc__ = Forest_serializer.__init__.__doc__
    write_forest.__doc__ = Forest_serializer.write_forest.__doc__
    append_forest.__doc__ = Forest_serializer.append_forest.__doc__
    read_forest.__doc__ = Forest_serializer.read_forest.__doc__