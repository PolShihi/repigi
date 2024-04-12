from zip_serializer import *
from information_finder import *
from validation_functions import *

class TaskOutput:
    def __init__(self, information_finder: InformationFinder, zip_serializer: ZipSerializer):
        '''
        Initializes a TaskOutput object with an InformationFinder instance and a ZipSerializer instance.

        Parameters:
        information_finder (InformationFinder): An instance of the InformationFinder class.
        zip_serializer (ZipSerializer): An instance of the ZipSerializer class.
        '''

        self.information_finder = information_finder
        self.zip_serializer = zip_serializer

    def get_text(self):
        '''
        Retrieves the text from the InformationFinder instance.

        Returns:
        str: The text stored in the InformationFinder instance.
        '''

        return self.information_finder.text

    def get_results(self):
        '''
        Generates a list of various information about the text.
        Information: number of sentences in the text, number of narrative, interrogative, motivating sentences, \
average sentence length in characters, average word length in characters, \
number of Emoticons, list of dates, \
list of words whose third letter from the end is a consonant, and penultimate is vowel, \
number of words starting with a vowel, list of words containing two identical letters in a row and their serial numbers, \
list of words in alphabetical order.

        Returns:
        str: A string containing the generated information.
        '''

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
        '''
        Loads the text from a file named 'input.txt' into the InformationFinder instance.

        Returns:
        str: A message indicating the success or failure of the operation.
        '''

        path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "input.txt")

        if not os.path.exists(path):
            return "File doesn't exist"

        with open(path, "r") as file:
            self.information_finder.text = file.read()

        return "Text was loaded"

    def upload_results(self):
        '''
        Uploads the results to a file named 'output.txt'.

        Returns:
        str: A message indicating the success or failure of the operation, along with the results.
        '''

        path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "output.txt")
        results = self.get_results()
        with open(path, "w") as file:
            file.write(self.get_results())

        return f"Results were uploaded, results:\n\n{results}"

    def archive_file(self):
        '''
        Archives the file using the ZipSerializer instance.

        Returns:
        str: A message indicating the success of archiving the file.
        '''

        self.zip_serializer.archive_file()

        return "File was archived"

    def get_information_about_archive_file(self):
        '''
        Retrieves information about the archived file from the ZipSerializer instance.

        Returns:
        str: A string containing information about the archived file.
        '''

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