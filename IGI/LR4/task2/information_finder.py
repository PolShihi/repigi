import re


class InformationFinderBasicMixin:
    def count_sentences(self):
        '''
        Count the number of sentences in the text.

        Returns:
        int: The number of sentences in the text.
        '''

        sentences = re.split(r'[.!?]+', self.text)

        return len(sentences)

    def count_sentence_types(self):
        '''
        Count the number of sentences of each type (narration, interrogative, imperative) in the text.

        Returns:
        tuple: A tuple containing the counts of narration, interrogative, and imperative sentences respectively.
        '''

        narration_count = len(re.findall(r'[.]', self.text))
        interrogative_count = len(re.findall(r'[?]', self.text))
        imperative_count = len(re.findall(r'[!]', self.text))

        return narration_count, interrogative_count, imperative_count

    def get_average_sentence_length(self):
        '''
        Calculate the average length of sentences in the text.

        Returns:
        float: The average length of sentences in the text.
        '''

        sentences = re.split(r'[.!?]+', self.text)
        total_length = sum(char for char in self.text if char.isalpha())
        average_length = total_length / len(sentences)

        return average_length

    def get_average_word_length(self):
        '''
        Calculate the average length of words in the text.

        Returns:
        float: The average length of words in the text.
        '''

        words = re.findall(r'\b\w+\b', self.text)
        total_length = sum(len(word) for word in words)
        average_length = total_length / len(words)

        return average_length

    def count_smileys(self):
        '''
        Count the number of smileys (like :), ;--[, :--[[) in the text.

        Returns:
        int: The number of smileys in the text.
        '''

        smileys = re.findall(r'[;:]-*([\[]+|[\]]+|[\(]+|[\)]+)', self.text)

        return len(smileys)


class InformationFinder(InformationFinderBasicMixin):
    def __init__(self, text=''):
        '''
        Initialize the InformationFinder object with the given text.

        Parameters:
        str: The text to be analyzed.
        '''

        self.text = text

    def get_dates(self):
        '''
        Extract all dates in the format DD.MM.YYYY from the text.

        Returns:
        list: A list of dates found in the text.
        '''

        dates = re.findall(r'\b(\d{1,2}\.\d{1,2}\.\d{1,4})\b', self.text)

        return dates

    def get_words_consonant_vowel(self):
        '''
        Extract words that contain a consonant on third from end position,  followed by a vowel and another letter.

        Returns:
        list: A list of extracted words.
        '''

        words = re.findall(
            r'\b\w*[^aeiou][aeiou]\w{1}\b', self.text, re.IGNORECASE)

        return words

    def count_words_starting_with_vowel(self):
        '''
        Count the number of words in the text that start with a vowel.

        Returns:
        int: The number of words starting with a vowel.
        '''

        words = re.findall(r'\b[aeiou]\w*\b', self.text, re.IGNORECASE)

        return len(words)

    def find_words_with_repeated_letters(self):
        '''
        Find words in the text that contain repeated letters and theirs position.

        Returns:
        list: A list of tuples containing the words and their positions in the text.
        '''

        words_with_repeat = [word[0] for word in re.findall(
            r'\b(\w*(\w)\2\w*)\b', self.text, re.IGNORECASE)]
        words_all = re.findall(r'\b\w+\b', self.text)
        words_res = []
        for word in words_with_repeat:
            index = words_all.index(word)
            words_all.pop(index)
            words_res.append((word, index + 1 + len(words_res)))

        return words_res

    def sort_words_alphabetically(self):
        '''
        Sort the words in the text alphabetically.

        Returns:
        list: The sorted words.
        '''

        words = re.findall(r'\b\w+\b', self.text)
        sorted_words = sorted(words, key=str.lower)

        return sorted_words