'''Allows you to view forest information downloaded from a file: \
total number of trees, number of healthy trees, relative number of diseased trees, detailed information about a specific type of tree
lr: 4
version: 1.1.0
FIO: Lyamtsev H. K.
date of development: 11.04.2024'''

from serializers import *
from validation_functions import *
from forest_calc import *

def input_for_add(forest: Forest_calc):
    '''This function prompts the user to input information about a tree and adds the tree to the forest using the add_tree method of a Forest_calc object. \
It validates the user input for the tree type, total quantity of trees, and healthy quantity of trees before adding the tree to the forest.

Parameters:
forest (Forest_calc): The Forest_calc object representing the forest to which the tree will be added.'''

    print("Enter type of tree (string with letters and spaces): ", end='')

    while True:
        tree_type = input()
        if all(char.isalpha() or char.isspace() for char in tree_type):
            break
        print("Try again: ", end='')

    print("Enter total quantity of trees (positive integer): ", end='')

    while True:
        try:
            total_quantity = consistent_validation(
                input(), int_validation, positive_validation)
            break
        except ValueError as ex:
            print(ex, ", try again: ", sep='', end='')

    print("Enter total quantity of healthy trees (positive integer, less than total quantity): ", end='')

    while True:
        try:
            healthy_quantity = consistent_validation(
                input(), int_validation, positive_validation)
            if healthy_quantity > total_quantity:
                raise ValueError(
                    "healthy quantity can not be greater than total")
            break
        except ValueError as ex:
            print(ex, ", try again: ", sep='', end='')

    forest.add_tree({
        'type': tree_type,
        'total_quantity': total_quantity,
        'healthy_quantity': healthy_quantity,
    })


def input_for_type(forest: Forest_calc):
    '''This function prompts the user to input a tree type and retrieves information about that tree type from the forest using the get_type_info method of a Forest_calc object. \
If the tree type exists in the forest, it returns formatted information about the tree type. \
If the tree type is not found in the forest, it returns the string "There is no such type of tree in the forest".

Parameters:
forest (Forest_calc): The Forest_calc object representing the forest from which to retrieve tree type information.

Returns:
str: formatted information about the tree type, including its type, total quantity, and healthy quantity, \
or a message indicating that the tree type does not exist in the forest.'''

    print("Enter type of tree (string with letters and spaces): ", end='')

    while True:
        tree_type = input()
        if all(char.isalpha() or char.isspace() for char in tree_type):
            break
        print("Try again: ", end='')

    tree = forest.get_type_info(tree_type)

    if tree is None:
        return "There is no such type of tree in the forest"

    return f"\nTree Type: {tree['type']}\nTotal Quantity: {tree['total_quantity']}\nHealthy Quantity: {tree['healthy_quantity']}"


def output_for_detailed(forest: Forest_calc):
    '''This function retrieves detailed disease information for trees in the forest using the disease_trees_detailed_percent method of a Forest_calc object. \
It formats the information for each tree type, including the tree type and the disease percentage, and returns a string with the formatted details joined by line breaks.

Parameters:
forest (Forest_calc): The Forest_calc object representing the forest from which to retrieve detailed disease information.

Returns:
str: The formatted details about each tree type in the forest, including the tree type and the corresponding disease percentage. \
The details are joined by line breaks in the returned string.'''

    details = forest.disease_trees_detailed_percent()

    return '\n'.join([f"Tree Type: {detail[0]}, disease percentage: {detail[1]:.1f}" for detail in details])


trees = [
    {'type': 'birch', 'total_quantity': 100, 'healthy_quantity': 70},
    {'type': 'oak', 'total_quantity': 150, 'healthy_quantity': 50},
    {'type': 'spruce', 'total_quantity': 70, 'healthy_quantity': 10},
]

TASKS = {
    1: Forest_calc.show_forest_info,
    2: input_for_add,
    3: Forest_calc.upload_function(Forest_serializer_csv("forest.csv")),
    4: Forest_calc.load_function(Forest_serializer_csv("forest.csv")),
    5: Forest_calc.upload_function(Forest_serializer_pickle("forest.pickle")),
    6: Forest_calc.load_function(Forest_serializer_pickle("forest.pickle")),
    7: Forest_calc.total_trees_num,
    8: Forest_calc.healthy_trees_num,
    9: Forest_calc.disease_trees_percent,
    10: output_for_detailed,
    11: input_for_type,
    12: Forest_calc.clear_forest
}


def execute(forest):
    print('-' * 50, "1 - show forest info", "2 - add tree", "3 - upload to CSV file", "4 - load from CSV file", "5 - upload to pickle file",
          "6 - load from pickle file", "7 - total number of trees in the forest", "8 - total number of healthy trees in the forest",
          "9 - percentage of diseased trees in the forest", "10 - percentage of diseased trees for each tree type in the forest",
          "11 - information about a specific tree type in the forest", "12 - clear forest", sep='\n')
    
    print('\n' , f"Enter the number of action (1 to {len(TASKS)}): ", end='', sep='')
    
    while True:
        try:
            func_number = consistent_validation(input(), int_validation)
            if func_number < 1 or func_number > len(TASKS):
                raise ValueError("Invalid number")
            break
        except ValueError as exc:
            print(exc, ", try again: ", end='', sep='')
            continue
        
    print('=' * 50, '\n')
    
    res = TASKS[func_number](forest)
    if res is not None:
        print(res, '\n')


if __name__ == "__main__":
    forest = Forest_calc()
    while True:
        execute(forest)
