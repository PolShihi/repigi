def when_executed(func):
    '''wrap function and display when it was called'''
    
    from datetime import datetime, timezone
    
    def inner(*args, **kwargs):
        called_at = datetime.now(timezone.utc)
        res = func(*args, **kwargs)
        print(f'{func.__name__} called at {called_at}')
        return res
    
    return inner


@when_executed
def do_reexcecution(func):
    '''repeatedly executes the function until the character \'y\' is entered'''
    print(func.__doc__, '\n')
    while True:
        func()
        print("Do you want to terminate the program? (print \'y\' if yes): ")
        if input() == 'y':
            break
        print()