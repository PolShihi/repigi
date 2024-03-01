def float_validation(value):
    '''
    checks whether the value can be converted to float
    '''
    
    result = 0
    try:
        result = float(value)
    except ValueError:
        raise ValueError("Enter float value")
    
    return result

def absolute_less_than_one_validation(value):
    '''
    checks that the value is between -1 and 1
    '''

    if abs(value) >= 1.0:
        raise ValueError("Enter a value between -1 and 1, excluded")
    
    return value

def positive_validation(value):
    '''
    checks that the value is positive
    '''
    
    if value <= 0:
        raise ValueError("Enter a value between -1 and 1, excluded")
    
    return value

def consistent_validation(value, *funcs):
    '''
    sequentially applies the specified validation functions (funcs) to the value
    '''
    
    result = value
    for func in funcs:
        result = func(result)
        
    return result