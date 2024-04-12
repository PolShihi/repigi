'''Allows you to plot graphs of the function ln(1-x) and its approximations using the Taylor series. \
It is also possible to save the resulting image. \
You can obtain additional statistical quantities from the Taylor series values at points.
lr: 4
version: 1.0.0
FIO: Lyamtsev H. K.
date of development: 12.04.2024'''


from task_output_3 import *


TASKS = {
    1: TaskOutput.input_for_epsilon,
    2: TaskOutput.input_for_step,
    3: TaskOutput.show_plots,
    4: TaskOutput.save_plot,
    5: TaskOutput.show_statistics
}


def execute():
    print('-' * 50, f"1 - change epsilon (now {FunctionCalculation.EPS})",
          f"2 - change step (now {FunctionCalculation.STEP}, range of x values from -1 to 1 not inclusive)",
          "3 - show plots of function ln(1-x) and series that approximates this function",
          "4 - upload plot to file (series_and_function.png)", "5 - show statistics about series values in points", sep='\n')

    print('\n', f"Enter the number of action (1 to {len(TASKS)}): ",
          end='', sep='')

    while True:
        try:
            func_number = consistent_validation(input(), int_validation)
            if func_number < 1 or func_number > len(TASKS):
                raise ValueError("Invalid number")
            break
        except ValueError as exc:
            print(exc, ", try again: ", end='', sep='')
            continue

    print('=' * 50, '\n')

    res = TASKS[func_number]()
    print(res, '\n') if res is not None else None


if __name__ == "__main__":
    while True:
        print(__doc__)
        execute()
