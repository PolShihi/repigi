import task1, task2, task3, task4, task5
from validation_functions import *
import usefuls

TASKS = {
    1 : task1,
    2 : task2,
    3 : task3,
    4 : task4,
    5 : task5,
}


def main():
    '''For given task number executes the task'''
    
    print(f"Enter the number of the task you want to execute (1 to {len(TASKS)}): ", end='')
    while True:
        try:
            task_number = consistent_validation(input(), int_validation)
        except ValueError as exc:
            print(exc, ", try again: ", end='', sep='')
            continue
        if task_number < 1 or task_number > len(TASKS):
            print("Inavalid number, try again: ", end='')
            continue
        break
    print('\\/' * 25)
    print(TASKS[task_number].__doc__, '\n\n')
    TASKS[task_number].execute()
    print('/\\' * 25)
    

if __name__ == "__main__":
    usefuls.do_reexcecution(main)