'''For a given sequence of float numbers, prints the sequence, the index of the minimum negative element of the sequence and \
the sum of the elements of the sequence, located between the first and second negative elements
lr: 3, name: Working with Python
version: 1.0.1
FIO: Lyamtsev H. K.
date of development: 02.03.2024'''

import usefuls
import initialize_functions
from validation_functions import *


def find_min_neg_index(seq):
    '''finds the index of the minimum negative element of the sequence'''
    try:
        min_value = min([el for el in seq if el < 0])
    except ValueError:
        return -1
    return seq.index(min_value)


def find_sum_between_neg(seq: list):
    '''finds the sum of the elements of the sequence, located between the first and second negative elements'''
    neg_seq = [el for el in seq if el < 0]

    if len(neg_seq) < 2:
        return None

    lindex = seq.index(neg_seq[0])
    rindex = seq[lindex + 1:].index(neg_seq[1]) + lindex + 1
    return sum(seq[lindex + 1: rindex])


def execute():
    '''For a given sequence of float numbers, prints the sequence, the index of the minimum negative element of the sequence and \
the sum of the elements of the sequence, located between the first and second negative elements'''

    length = 0
    print("Enter length (positive integer value): ", end='')
    while True:
        try:
            length = consistent_validation(
                input(), int_validation, positive_validation)
        except ValueError as exc:
            print(exc, ", try again: ", end='', sep='')
            continue
        break

    seq = initialize_functions.initialize_with_input(
        length, "Enter float value: ", float_validation)
    min_neg_index = find_min_neg_index(seq)
    sum_between_neg = find_sum_between_neg(seq)

    res_str_min = f"Index of the minimum negative element of the sequence = {min_neg_index}"
    if min_neg_index == -1:
        res_str_min = "there is no minimum negative element in the sequence"

    res_str_sum = f"sum of sequence elements, located between the first and second negative elements = {sum_between_neg}"
    if sum_between_neg is None:
        res_str_sum = "there are no two negative elements in the sequence"

    print('-' * 50, f"sequence = {'[' + ', '.join(map(str, seq)) + ']'}",
          res_str_min, res_str_sum, '-' * 50, sep='\n')


if __name__ == "__main__":
    usefuls.do_reexcecution(execute)
