'''For given x and eps returns \
the number of terms of the Taylor series that approximates the function ln(1 - x), the sum of this series, the value of the function ln(1-x) itself
lr: 3, name: Working with Python
version: 1.0.2
FIO: Lyamtsev H. K.
date of development: 19.03.2024'''

import math
import usefuls
from validation_functions import *


MAX_ITERATIONS = 500


def math_func(x: float) -> float:
    '''This function returns a value that is approximated by the Taylor series. It calculates the natural logarithm of (1 - x) using the math.log function.

Parameters:
x (float): The input value for the function. It represents the argument of the natural logarithm.

Returns:
Approximation (float): The result of the function, which is the approximation of the natural logarithm of (1 - x) using the Taylor series.'''

    return math.log(1 - x)


def series_sum(x: float, n: int) -> float:
    '''This function calculates the sum of the Taylor series, which approximates the original function.

Parameters:
x (float): The input value for the function. It represents the argument of the Taylor series.
n (int): The number of terms to consider in the Taylor series summation.

Returns:
Sum (float): The result of the function, which is the sum of the Taylor series. It represents the approximation of the original function using the Taylor series.'''

    return sum(-(x ** i / i) for i in range(1, n + 1))


def calculate_iters(x: float, eps: float) -> int:
    '''This function calculates the number of iterations required to achieve a given precision for approximating a function using the Taylor series.

Parameters:
x (float): The input value for the function. It represents the argument of the Taylor series and the original function.
eps (float): The desired precision for the approximation. It specifies the maximum allowed difference between the approximated value and the actual value of the function.

Returns:
Iterations (int): The result of the function, which is the number of iterations required to achieve the desired precision. It represents the number of terms in the Taylor series summation that need to be considered.

Raises:
ValueError: If the number of iterations exceeds the maximum allowed iterations (MAX_ITERATIONS).'''

    for n in range(1, MAX_ITERATIONS + 1):
        if abs(series_sum(x, n) - math_func(x)) <= eps:
            return n

    raise ValueError(f"Number of iterations is over {MAX_ITERATIONS}")


def execute() -> None:
    '''for given x and eps will display \
the number of terms of the Taylor series that approximates the function ln(1 - x), the sum of this series, the value of the function ln(1-x) itself'''

    x = 0
    print("Enter x (float value between -1 and 1, excluded): ", end='')
    while True:
        try:
            x = consistent_validation(
                input(), float_validation, absolute_less_than_one_validation)
        except ValueError as exc:
            print(exc, ", try again: ", end='', sep='')
            continue

        break

    eps = 0
    print("Enter eps: ", end='')
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
    usefuls.do_reexcecution(execute)
