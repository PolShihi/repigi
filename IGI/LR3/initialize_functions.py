import random
from validation_functions import *


def initialize_with_input(length: int, hint: str, *func_valid) -> list:
    '''This function initializes a list of numbers based on user input. It prompts the user to enter values for a specified number of times and performs validation on the entered values.

Parameters:
length (int): The number of elements to be entered in the list.
hint (str): A hint or message to display as a prompt for the user during input.
*func_valid: Variable-length argument list of validation functions. These functions are called to validate the user's input. Each validation function should take the entered value as an argument and raise a ValueError if the validation fails.

Returns:
seq (list): The result of the function, which is a list of entered values. Each element in the list represents a valid user input after passing the specified validation functions.'''

    seq = []
    for _ in range(length):
        print(hint, end='')
        while True:
            try:
                entered_num = consistent_validation(input(), *func_valid)
            except ValueError as exc:
                print(exc, ", try again: ", end='', sep='')
                continue
            break
        seq.append(entered_num)
    return seq


def initialize_with_generator_rand():
    '''This function is a generator that continuously yields random integers within the range of -100 to 100.

Yielded Values:
Random integers: The generator yields random integers within the specified range (-100 to 100) indefinitely.'''

    while True:
        yield random.randint(-100, 100)
        

def initialize_with_generator_input(length: int, hint: str, *func_valid):
    '''This function is a generator that prompts the user to enter a value and validates it using the specified validation functions. It repeatedly prompts the user until a valid value is entered. \
The entered value is yielded as the output.

Parameters:
length (int): The number of elements to be yielded.
hint (str): The prompt or hint to be displayed to the user when requesting input.
*func_valid: Variable-length argument list of validation functions. These functions should take a value as an argument and perform the necessary validation. Each function should raise a ValueError if the validation fails.

Yielded Value:
entered_num: The value entered by the user, which has passed all the specified validation functions.'''

    for _ in range(length):
        print(hint, end='')
        while True:
            try:
                entered_num = consistent_validation(input(), *func_valid)
            except ValueError as exc:
                print(exc, ", try again: ", end='', sep='')
                continue
            break
        yield entered_num
    return