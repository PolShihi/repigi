from zip_serializer import *
from information_finder import *
from validation_functions import *


class TaskOutput:
    def __init__(self, information_finder: InformationFinder, zip_serializer: ZipSerializer):
        self.information_finder = information_finder
        self.zip_serializer = zip_serializer

    def get_text(self):
        return self.information_finder.text

    def get_results(self):
        answer_list = []
        answer_list.append(
            f"Number of sentences in the text: {self.information_finder.count_sentences()}")
        answer_list.append("Number of narrative, interrogative, motivating sentences respectively: " +
                           f"{self.information_finder.count_sentence_types()}")

        try:
            ave_sentence_length = self.information_finder.get_average_sentence_length()
            ave_sentence_length_str = str(ave_sentence_length)
        except ZeroDivisionError:
            ave_sentence_length_str = "no sentences"
        answer_list.append(
            f"Average sentence length in characters: {ave_sentence_length_str}")

        try:
            ave_word_length = self.information_finder.get_average_word_length()
            ave_word_length_str = str(ave_word_length)
        except ZeroDivisionError:
            ave_word_length_str = "no words"
        answer_list.append(
            f"Average word length in characters: {ave_word_length_str}")

        answer_list.append(
            f"Number of Emoticons: {self.information_finder.count_smileys()}")
        answer_list.append(
            f"List of dates: {', '.join(self.information_finder.get_dates())}")
        answer_list.append(f"List of words whose third letter from the end is a consonant, " +
                           "and penultimate is vowel: " + ', '.join(self.information_finder.get_words_consonant_vowel()))
        answer_list.append(
            f"Number of words starting with a vowel: {self.information_finder.count_words_starting_with_vowel()}")
        answer_list.append(f"List of words containing two identical letters in a row and their serial numbers: " +
                           ', '.join(f"{el[0]} ({el[1]})" for el in self.information_finder.find_words_with_repeated_letters()))
        answer_list.append(
            f"List of words in alphabetical order: {', '.join(self.information_finder.sort_words_alphabetically())}")

        return '\n'.join(answer_list)

    def load_text(self):
        path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "input.txt")

        if not os.path.exists(path):
            return "File doesn't exist"

        with open(path, "r") as file:
            self.information_finder.text = file.read()

        return "Text was loaded"

    def upload_results(self):
        path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "output.txt")
        results = self.get_results()
        with open(path, "w") as file:
            file.write(self.get_results())

        return f"Results were uploaded, results:\n\n{results}"

    def archive_file(self):
        self.zip_serializer.archive_file()

        return "File was archived"

    def get_information_about_archive_file(self):
        try:
            file_info = self.zip_serializer.get_file_info_in_archive()
        except FileNotFoundError:
            return "There is no such archive file"

        if file_info is None:
            return "There is no such file in archive "

        answer_list = []
        answer_list.append(f"Filename: {file_info['filename']}")
        answer_list.append(
            f"Initial file size (bytes): {file_info['file_size']}")
        answer_list.append(
            f"Compress file size (bytes): {file_info['compress_size']}")
        y, m, d, h, min, s = file_info['date_time']
        answer_list.append(
            f"Date and time of last change: {d}.{m}.{y} {h}:{min}:{s}")

        return '\n'.join(answer_list)


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
    serializer = ZipSerializer("output.txt", "output.zip")
    information_finder = InformationFinder('')
    task_obj = TaskOutput(information_finder, serializer)
    while True:
        execute(task_obj)
