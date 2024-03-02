'''For given entered integers until the difference of 10000 and their sum is negative, the difference will be displayed
lr: 3, name: Working with Python
version: 1.0
FIO: Lyamtsev H. K.
date of development: 02.03.2024'''

import usefuls
from validation_functions import *


def execute():
    '''Enter integers until the difference of 10000 and their sum is negative, the difference will be displayed'''
    initial_value = 10000
    while initial_value >= 0:
        print('Enter a value (integer): ', end='')
        while True:
            try:
                entered_num = consistent_validation(input(), int_validation)
            except ValueError as exc:
                print(exc, ", try again: ", end='', sep='')
                continue
            break
        initial_value -= entered_num
    print("-" * 50, "Results:",
          f"final value = {initial_value}", "-" * 50, sep='\n')


if __name__ == "__main__":
    usefuls.do_reexcecution(execute)
