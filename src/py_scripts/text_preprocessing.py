import os
from typing import List
import re
import json


def get_sms_message(file_line: str) -> str:
    def is_spam(line: str):
        return line[:4] == 'spam'
    if is_spam(file_line):
        return file_line[5:]
    else:
        return file_line[4:]


def split_file_line(file_line: str) -> List[str]:
    line_data = file_line.split('\t')
    if not len(line_data) == 2:
        print(f'Invalid Split. Line: {file_line}')
        return []
    return line_data


def pre_process_message(message: str) -> str:
    return re.sub('[^A-Za-z0-9\s]', '', message).lower().strip()


def add_file_line_words_to_word_dictionary(file_line: str,
                                           word_dictionary: dict,
                                           word_counter: int) -> int:
    message = get_sms_message(file_line)
    message = pre_process_message(message)
    for word in message.split(' '):
        if word not in word_dictionary:
            word_dictionary[word] = word_counter
            word_counter += 1
    return word_counter


def construct_word_dictionary(data_file_path: str, output_word_dictionary_json_file_path: str):
    if not os.path.isfile(data_file_path):
        print(f'Invalid Path to the Dataset File: {data_file_path}')
        return

    if not os.path.isfile(output_word_dictionary_json_file_path):
        print(f'Invalid Path to the Output Dictionary File: {output_word_dictionary_json_file_path}')
        return

    dictionary_writer = open(output_word_dictionary_json_file_path, 'w')

    word_dictionary = dict()
    word_count = 1
    with open(data_file_path, 'r') as file_reader:
        for file_line in file_reader:
            word_count = add_file_line_words_to_word_dictionary(file_line, word_dictionary, word_count)

    json.dump(word_dictionary, dictionary_writer)


def segeregate_dataset(data_file_path: str, output_parent_directory_path: str):
    if not os.path.isfile(data_file_path):
        print(f'Invalid Path to the Dataset File: {data_file_path}')
        return

    if not os.path.isdir(output_parent_directory_path):
        try:
            os.makedirs(output_parent_directory_path)
        except FileNotFoundError:
            print(f'Invalid Path to the Output Directory: {output_parent_directory_path}')
            return

    spam_subdirectory_path = os.path.join(output_parent_directory_path, 'spam')
    if not os.path.isdir(spam_subdirectory_path):
        os.makedirs(spam_subdirectory_path)
    ham_subdirectory_path = os.path.join(output_parent_directory_path, 'ham')
    if not os.path.isdir(ham_subdirectory_path):
        os.makedirs(ham_subdirectory_path)

    subdirectory_map = {'spam': spam_subdirectory_path, 'ham': ham_subdirectory_path}
    counters = {'spam': 1, 'ham': 1}

    with open(data_file_path, 'r') as file_reader:
        for file_line in file_reader:
            [class_label, message] = split_file_line(file_line)
            message = pre_process_message(message)
            fw = open(os.path.join(subdirectory_map[class_label], str(counters[class_label])), 'w')
            fw.write(message)
            fw.close()
            counters[class_label] += 1


def main():
    #construct_word_dictionary(f'../../data/orig_data/SMSSpamCollection', f'../../data/dictionaries/dict.json')
    segeregate_dataset(f'../../data/orig_data/SMSSpamCollection', f'../../data/txt_dataset')


if __name__ == '__main__':
    main()
