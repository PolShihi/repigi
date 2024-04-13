'''Allows you to draw a square according to the specified radius of the inscribed circle and color, \
it is possible to load the image into a file.
lr: 4
version: 1.0.0
FIO: Lyamtsev H. K.
date of development: 13.04.2024'''


from task_output_4 import *


TASKS = {
    1: TaskOutput.show_parametrs,
    2: TaskOutput.input_for_radius,
    3: TaskOutput.input_for_color,
    4: TaskOutput.input_for_text,
    5: TaskOutput.show_plot,
    6: TaskOutput.save_plot,
}


def execute(task_obj: TaskOutput):
    print('-' * 50, "1 - get square parameters",
          f"2 - change inradius (now {task_obj.graph.square.inradius})",
          f"3 - change color (now {task_obj.graph.square.color.color})",
          f"4 - change text on graph (now {task_obj.graph.text})",
          "5 - show graph of square",
          "6 - save graph of square in file", sep='\n')

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

    TASKS[func_number](task_obj)

    print('\n')


if __name__ == "__main__":
    print(__doc__)
    task_obj = TaskOutput()
    while True:
        execute(task_obj)
