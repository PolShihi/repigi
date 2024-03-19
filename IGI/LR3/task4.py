'''Display amount of words with length less than 7, word with minimal lenght and starts with \'a\' and sorted words by len of INITIAL_STRING
lr: 3, name: Working with Python
version: 1.0.1
FIO: Lyamtsev H. K.
date of development: 19.03.2024'''

import usefuls


INITIAL_STRING = "So she was considering in her own mind, as well as she could, for the hot day made her feel \
very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble \
of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by \
her"


def get_words(string: str) -> list:
    '''This function takes a string as input and returns a list of words extracted from the string. Each word is separated by a space character (' '). \
The function also removes any trailing commas (',') from the words.

Parameters:
string (str): The input string from which words are extracted.

Returns:
words (list): The result of the function, which is a list of words extracted from the input string.'''

    words = string.split(' ')
    words = [word.strip(',') for word in words]
    return words


def count_str_max_len(strings: list, max_len: int) -> int:
    '''This function counts the number of words in a given list of strings that have a length less than or equal to the specified maximum length.

Parameters:
strings (list): The list of strings to be processed.
max_len (int): The maximum length allowed for a word to be counted.

Returns:
count (int): The result of the function, which is the count of words in the list that satisfy the length condition.'''

    return len([string for string in strings if len(string) <= max_len])


def find_min_string_startsym(strings: str, symbol: str) -> str:
    '''This function finds the word with the minimum length among a given list of strings that starts with a specified symbol.

Parameters:
strings (list): The list of strings to be searched.
symbol (str): The symbol that the word should start with.

Returns:
min_string (str): The result of the function, which is the word with the minimum length among the strings that start with the specified symbol.'''

    strings_with_startsym = [
        string for string in strings if string.startswith(symbol)]
    return min(strings_with_startsym, key=len)


def execute():
    '''display amount of words with length less than 7, word with minimal lenght and starts with \'a\' and sorted words by len of INITIAL_STRING'''
    print("Initial string:", INITIAL_STRING)
    words = get_words(INITIAL_STRING)
    num_words_less_7 = count_str_max_len(words, 7 - 1)
    word_min_a = find_min_string_startsym(words, 'a')
    words.sort(key=len, reverse=True)
    print('-' * 50, "Results:", f"amount of words with length less than 7 = {num_words_less_7}",
          f"word with minimal lenght and starts with \'a\' = {word_min_a}", f"sorted words by len = {'[' + ', '.join(words) + ']'}", '-' * 50, sep='\n')


if __name__ == "__main__":
    usefuls.do_reexcecution(execute)
