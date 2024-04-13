'''Allows you to view forest information downloaded from a file: \
total number of trees, number of healthy trees, relative number of diseased trees, detailed information about a specific type of tree
lr: 4
version: 1.1.1
FIO: Lyamtsev H. K.
date of development: 13.04.2024'''


from task_output_1 import *


TASKS = {
    1: Forest_calc.show_forest_info,
    2: TaskOutput.input_for_add,
    3: Forest_calc.upload_function(Forest_serializer_csv("forest.csv")),
    4: Forest_calc.load_function(Forest_serializer_csv("forest.csv")),
    5: Forest_calc.upload_function(Forest_serializer_pickle("forest.pickle")),
    6: Forest_calc.load_function(Forest_serializer_pickle("forest.pickle")),
    7: Forest_calc.total_trees_num,
    8: Forest_calc.healthy_trees_num,
    9: Forest_calc.disease_trees_percent,
    10: TaskOutput.output_for_detailed,
    11: TaskOutput.input_for_type,
    12: Forest_calc.clear_forest,
    13: TaskOutput.input_for_sort,
}


def execute(forest):
    print('-' * 50, "1 - show forest info", 
          "2 - add tree", 
          "3 - upload to CSV file", 
          "4 - load from CSV file", 
          "5 - upload to pickle file",
          "6 - load from pickle file", 
          "7 - total number of trees in the forest", 
          "8 - total number of healthy trees in the forest",
          "9 - percentage of diseased trees in the forest", 
          "10 - percentage of diseased trees for each tree type in the forest",
          "11 - information about a specific tree type in the forest",
          "12 - clear forest", 
          "13 - sort forest", sep='\n')
    
    print('\n' , f"Enter the number of action (1 to {len(TASKS)}): ", end='', sep='')
    
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
    
    res = TASKS[func_number](forest)
    if res is not None:
        print(res, '\n')


if __name__ == "__main__":
    print(__doc__)
    forest = Forest_calc()
    while True:
        execute(forest)
