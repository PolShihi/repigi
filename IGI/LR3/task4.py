'''Display amount of words with length less than 7, word with minimal lenght and starts with \'a\' and sorted words by len of INITIAL_STRING
lr: 3, name: Working with Python
version: 1.0
FIO: Lyamtsev H. K.
date of development: 02.03.2024'''

import usefuls


INITIAL_STRING = "So she was considering in her own mind, as well as she could, for the hot day made her feel \
very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble \
of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by \
her"


def get_words(string):
    '''returns list of words from string'''
    words = string.split(' ')
    words = [word.strip(',') for word in words]
    return words


def count_str_max_len(strings, max_len):
    '''returns amount of words with length less than or equal to max_len'''
    return len([string for string in strings if len(string) <= max_len])


def find_min_string_startsym(strings, symbol):
    '''returns word with minimal lenght and starts with symbol'''
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
