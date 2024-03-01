import math
from validation_functions import *

'''
for given x and eps returns 
the number of terms of the Taylor series that approximates the function ln(1 - x), the sum of this series, the value of the function ln(1-x) itself
lr: 3, name: Working with Python
version: 1.0
FIO: Lyamtsev H. K.
date of development: 01.03.2024
'''

MAX_ITERATIONS = 500


def math_func(x):
    '''returns a function that is approximated by the Taylor series'''

    return math.log(1 - x)


def series_sum(x, n):
    '''returns the sum of the Taylor series which approximates the original function'''

    return sum(-(x ** i / i) for i in range(1, n + 1))


def calculate_iters(x, eps):
    '''returns the number of iterations that are required for a given precision'''

    for n in range(1, MAX_ITERATIONS + 1):
        if abs(series_sum(x, n) - math_func(x)) <= eps:
            return n

    raise ValueError(f"Number of iterations is over {MAX_ITERATIONS}")


def execute():
    '''execute first task'''

    x = 0
    print("Input x (float value between -1 and 1, excluded): ", end='')
    while True:
        try:
            x = consistent_validation(
                input(), float_validation, absolute_less_than_one_validation)
        except ValueError as exc:
            print(exc, ", try again: ", end='', sep='')
            continue

        break

    eps = 0
    print("Input eps: ", end='')
    while True:
        try:
            eps = consistent_validation(
                input(), float_validation, positive_validation)
        except ValueError as exc:
            print(exc, ", try again: ", end='', sep='')
            continue

        break

    n = 0
    try:
        n = calculate_iters(x, eps)
    except ValueError as exc:
        print(exc)
        return

    print("-" * 50, "Results:", f"x = {x}", f"n = {n}", f"F(x) = {series_sum(x, n)}",
          f"Math F(x) = {math_func(x)}", f"eps = {eps}", "-" * 50, sep='\n')


if __name__ == "__main__":
    while True:
        execute()
        print("Do you want to terminate the program? (y if yes): ")
        if input() == 'y':
            break
