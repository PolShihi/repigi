'''For a given string, the number of spaces symbols is displayed
lr: 3, name: Working with Python
version: 1.0.1
FIO: Lyamtsev H. K.
date of development: 19.03.2024'''

import usefuls


SPACE_SYMBOLS = " ,\t"


def execute():
    '''For a given string, the number of spaces symbols is displayed'''
    entered_string = input("Enter the string: ")
    result = sum(entered_string.count(sym) for sym in SPACE_SYMBOLS)
    print('-' * 50, "Results:",
          f"the number of space symbols = {result}", '-' * 50, sep='\n')


if __name__ == "__main__":
    usefuls.do_reexcecution(execute)
