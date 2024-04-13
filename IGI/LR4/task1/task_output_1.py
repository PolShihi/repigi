from serializers import *
from validation_functions import *
from forest_calc import *

class TaskOutput:
    @staticmethod
    def input_for_add(forest: Forest_calc):
        '''
        This function prompts the user to input information about a tree and adds the tree to the forest using \
the add_tree method of a Forest_calc object. \
It validates the user input for the tree type, total quantity of trees, and healthy quantity of trees before adding the tree to the forest.

        Parameters:
        forest (Forest_calc): The Forest_calc object representing the forest to which the tree will be added.
        '''

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

    @staticmethod
    def input_for_type(forest: Forest_calc):
        '''
        This function prompts the user to input a tree type and retrieves information about \
that tree type from the forest using the get_type_info method of a Forest_calc object. \
If the tree type exists in the forest, it returns formatted information about the tree type. \
If the tree type is not found in the forest, it returns the string "There is no such type of tree in the forest".

        Parameters:
        forest (Forest_calc): The Forest_calc object representing the forest from which to retrieve tree type information.

        Returns:
        str: formatted information about the tree type, including its type, total quantity, and healthy quantity, \
or a message indicating that the tree type does not exist in the forest.
        '''

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

    @staticmethod
    def output_for_detailed(forest: Forest_calc):
        '''
        This function retrieves detailed disease information for trees in the forest using \
the disease_trees_detailed_percent method of a Forest_calc object. \
It formats the information for each tree type, including the tree type and the disease percentage, \
and returns a string with the formatted details joined by line breaks.

        Parameters:
        forest (Forest_calc): The Forest_calc object representing the forest from which to retrieve detailed disease information.

        Returns:
        str: The formatted details about each tree type in the forest, including the tree type and the corresponding disease percentage. \
The details are joined by line breaks in the returned string.
        '''

        details = forest.disease_trees_detailed_percent()

        return '\n'.join([f"Tree Type: {detail[0]}, disease percentage: {detail[1]:.1f}" for detail in details])
    
    @staticmethod
    def input_for_sort(forest: Forest_calc):
        sort_task = {
            1: lambda tree: tree['type'],
            2: lambda tree: tree['total_quantity'],
            3: lambda tree: tree['healthy_quantity']
        }
        print("1 - by type", "2 - by total quantity", "3 - by healthy quantity", sep='\n')
        print("\nEnter enter the number that is responsible for the criterion by which to sort: ", end='')
        
        while True:
            try:
                func_number = consistent_validation(input(), int_validation)
                if func_number < 1 or func_number > len(sort_task):
                    raise ValueError("Invalid number")
                break
            except ValueError as exc:
                print(exc, ", try again: ", end='', sep='')
                continue
            
        forest.forest.sort(key=sort_task[func_number])