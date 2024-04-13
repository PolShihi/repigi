'''Allows you to specify a matrix of size n by m and generate it randomly, \
it is possible to find the sum of the elements below the main diagonal and \
the standard deviation of the elements of the main diagonal
lr: 4
version: 1.0.0
FIO: Lyamtsev H. K.
date of development: 13.04.2024'''


from task_output_5 import *


TASKS ={
    1 : (TaskOutput.show_matrix, ()),
    2 : (TaskOutput.input_for_sizes, ('number of lines', )),
    3 : (TaskOutput.input_for_sizes, ('number of columns', )),
    4 : (TaskOutput.input_for_random, ('min', )),
    5 : (TaskOutput.input_for_random, ('max', )),
    6 : (TaskOutput.print_results, (MatrixCalculation.generate_matrix, "Generated matrix:\n")),
    7 : (TaskOutput.print_results, (MatrixCalculation.sum_below_diagonal, "Sum of elements below diagonal: ")),
    8 : (TaskOutput.print_results, (MatrixCalculation.diagonal_std_deviation, "Diagonal standart deviation (NumPy): ")),
    9 : (TaskOutput.print_results, (MatrixCalculation.diagonal_std_deviation_formula, "Diagonal standart deviation (formula): ")),
}


def execute(task_obj : TaskOutput):
    print('-' * 50, "1 - show matrix",
          f"2 - change number of lines (now {task_obj.matrix_calc.n})",
          f"3 - change number of columns (now {task_obj.matrix_calc.m})",
          f"4 - change the minimum value at random (now {task_obj.matrix_calc.rand_min})",
          f"5 - change the maximum value at random (now {task_obj.matrix_calc.rand_max})",
          "6 - generate a matrix randomly", 
          "7 - find the sum of the elements under the main diagonal",
          "8 - find the standard deviation for the elements of the main diagonal (NumPy)",
          "9 - find the standard deviation for the elements of the main diagonal (formula)", sep='\n')

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

    TASKS[func_number][0](task_obj, *TASKS[func_number][1])
    
    print('\n')


if __name__ == "__main__":
    print(__doc__)
    task_obj = TaskOutput()
    while True:
        execute(task_obj)