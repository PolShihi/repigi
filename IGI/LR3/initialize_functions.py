import random
from validation_functions import *


def initialize_with_input(length, hint, *func_valid):
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


def initialize_with_generator():
    while True:
        yield random.randint(-100, 100)
