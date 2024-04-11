def float_validation(value: str) -> float:
    '''This function checks whether a given value can be converted to a float. It attempts to convert the value to a float and raises a ValueError if the conversion fails.

Parameters:
value (str): The value to be checked for conversion to float.

Returns:
result (float): The result of the function, which is the converted float value of the input.'''

    result = 0
    try:
        result = float(value)
    except ValueError:
        raise ValueError("Enter float value")

    return result


def absolute_less_than_one_validation(value: float) -> float:
    '''This function checks whether a given value is between -1 and 1 (excluding -1 and 1). It raises a ValueError if the value is not within the specified range.

Parameters:
value (float): The value to be checked.

Returns:
value (float): The result of the function, which is the input value if it satisfies the range condition.'''

    if abs(value) >= 1.0:
        raise ValueError("Enter a value between -1 and 1, excluded")

    return value


def positive_validation(value: float) -> float:
    '''This function checks whether a given value is positive. It raises a ValueError if the value is not positive (zero or negative).

Parameters:
value (float): The value to be checked.

Returns:
value (float): The result of the function, which is the input value if it is positive.'''

    if value <= 0:
        raise ValueError("Enter a positive value, excluded")

    return value


def consistent_validation(value: str, *funcs):
    '''This function sequentially applies the specified validation functions to a given value. \
It iterates over the validation functions and applies each one to the value in the order they are provided. \
The result of each validation function is passed as the argument to the next validation function. The final result is returned.

Parameters:
value (str): The value to be validated.
*funcs: Variable-length argument list of validation functions. These functions should take a value as an argument and perform the necessary validation. \
Each function should raise a ValueError if the validation fails.

Returns:
result: The result of the function, which is the final result after applying all the validation functions to the value.'''

    result = value
    for func in funcs:
        result = func(result)

    return result


def int_validation(value: str) -> int:
    '''This function checks whether a given value can be converted to an integer. It attempts to convert the value to an integer and raises a ValueError if the conversion fails.

Parameters:
value (str): The value to be checked for conversion to an integer.

Returns:
result (int): The result of the function, which is the converted integer value of the input.'''

    result = 0
    try:
        result = int(value)
    except ValueError:
        raise ValueError("Enter integer value")

    return result
