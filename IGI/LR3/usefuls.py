def when_executed(func):
    '''This function is a decorator that wraps another function and displays the timestamp when the wrapped function is called. \
It adds a timestamp print statement before and after executing the wrapped function.

Parameters:
func (function): The function to be wrapped and decorated.

Returns:
inner (function): The wrapped function.'''
    
    from datetime import datetime, timezone
    
    def inner(*args, **kwargs):
        called_at = datetime.now(timezone.utc)
        res = func(*args, **kwargs)
        print(f'{func.__name__} called at {called_at}')
        return res
    
    return inner


@when_executed
def do_reexcecution(func) -> None:
    '''This function repeatedly executes the specified function until the character 'y' is entered. \
It displays the documentation of the function, executes it, and prompts the user to terminate the program by entering 'y'.

Parameters:
func (function): The function to be repeatedly executed until termination.'''

    print(func.__doc__, '\n')
    while True:
        func()
        print("Do you want to terminate the program? (print \'y\' if yes): ")
        if input() == 'y':
            break
        print()