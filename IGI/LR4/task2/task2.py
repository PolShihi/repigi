'''Allows you to view different information about the text in file and archive it. \
Information: number of sentences in the text, number of narrative, interrogative, motivating sentences, \
average sentence length in characters, average word length in characters, \
number of Emoticons, list of dates, \
list of words whose third letter from the end is a consonant, and penultimate is vowel, \
number of words starting with a vowel, list of words containing two identical letters in a row and their serial numbers, \
list of words in alphabetical order.
lr: 4
version: 1.1.0
FIO: Lyamtsev H. K.
date of development: 12.04.2024'''


from task_output_2 import *


TASKS = {
    1: TaskOutput.get_text,
    2: TaskOutput.load_text,
    3: TaskOutput.upload_results,
    4: TaskOutput.archive_file,
    5: TaskOutput.get_information_about_archive_file,
}


def execute(task_obj):
    print('-' * 50, "1 - show text", "2 - load text from txt file (input.txt)", "3 - upload results to txt file (output.txt)",
          "4 - archive file (output.zip)", "5 - show information about file in archive", sep='\n')

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

    res = TASKS[func_number](task_obj)
    print(res, '\n')


if __name__ == "__main__":
    print(__doc__)
    serializer = ZipSerializer("output.txt", "output.zip")
    information_finder = InformationFinder('')
    task_obj = TaskOutput(information_finder, serializer)
    while True:
        execute(task_obj)
