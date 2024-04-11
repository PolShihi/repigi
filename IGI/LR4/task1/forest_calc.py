from serializers import *

class Forest_calc:
    '''For a given forest in the form of a list of dictionaries with keys: type, total_quantity, healthy_quantity - can provide various information'''

    def __init__(self, forest = []):
        '''Initializes the Forest_calc object with the provided forest.
Parameters:
forest (list of dictionaries): A list of dictionaries representing the forest.'''

        self.forest = forest

    def show_forest_info(self):
        '''Returns information about the trees in a forest. \
It iterates  over the trees in the forest and creates a formatted string for each tree, \
including its type, total quantity, and healthy quantity. \
The formatted strings are then joined together with line breaks and returned. \
If the forest is empty, it returns the string "Forest is empty".

Returns:
str: The formatted information about the trees in the forest or a message indicating that the forest is empty.
    '''
        formatted_info = []
        for tree in self.forest:
            info = f"Tree Type: {tree['type']}\nTotal Quantity: {tree['total_quantity']}\nHealthy Quantity: {tree['healthy_quantity']}"
            formatted_info.append(info)

        if not formatted_info:
            return "Forest is empty"

        return '\n\n'.join(formatted_info)

    def add_tree(self, tree):
        '''Adds a tree to the forest. It takes a tree object as a parameter and appends it to the list of trees in the forest.'''

        self.forest.append(tree)

    def clear_forest(self):
        "Clear the forest"

        self.forest = []

    def total_trees_num(self):
        '''Returns the total number of trees in the forest.

Returns:
int: The total number of trees in the forest.'''

        return sum([tree['total_quantity'] for tree in self.forest])

    def healthy_trees_num(self):
        '''Returns the total number of healthy trees in the forest.

Returns:
int: The total number of healthy trees in the forest.'''

        return sum([tree['healthy_quantity'] for tree in self.forest])

    def disease_trees_percent(self):
        '''Returns the percentage of diseased trees in the forest.

Returns:
float: The percentage of diseased trees in the forest.'''

        return 100 - self.healthy_trees_num() * 100 / self.total_trees_num()

    def disease_trees_detailed_percent(self):
        '''Returns the percentage of diseased trees for each tree type in the forest.

Returns:
list of tuples: A list of tuples where each tuple contains the tree type and its corresponding percentage of diseased trees.'''

        return [(tree['type'], 100 - tree['healthy_quantity'] * 100 / tree['total_quantity']) for tree in self.forest]

    def get_type_info(self, type):
        '''Returns information about a specific tree type in the forest.

Parameters:
tree_type (str): The type of tree to get information about.

Returns:
dictionary: A dictionary containing information about the specified tree type, including its 'type', 'total_quantity', and 'healthy_quantity'.'''

        trees = [tree for tree in self.forest if tree['type'] == type]
        if not trees:
            return None

        return trees[0]

    @staticmethod
    def upload_function(ser: Forest_serializer):
        '''This function returns an inner function upload_from, which is responsible for uploading the forest data using a Forest_serializer object. \
The upload_from function calls the write_forest method of the Forest_serializer object to write the forest data.

Parameters:
ser (Forest_serializer): The Forest_serializer object used to serialize the forest data.

Returns:
function: The returned function upload_from can be called to upload the forest data.'''

        def upload_from(self):
            ser.write_forest(self.forest)

        return upload_from

    @staticmethod
    def load_function(ser: Forest_serializer):
        '''This function returns an inner function load_to, which is responsible for loading the forest data using a Forest_serializer object. \
The load_to function attempts to read the forest data using the read_forest method of the Forest_serializer object. If the file is not found, it returns the string "File doesn't exist".

Parameters:
ser (object): The Forest_serializer object used to deserialize the forest data.

Returns:
function: The returned function load_to can be called to load the forest data or check if the file exists. If the file doesn't exist, it returns the corresponding message.'''
        def load_to(self):
            try:
                self.forest = ser.read_forest()
            except FileNotFoundError:
                return "File doesn't exist"

        return load_to