from typing import List

import fakeredis

FILE_PATH = 'limited_dictionary.txt'


def load_words_from_file(redis_client: fakeredis.FakeRedis):
    file = open(FILE_PATH)

    for word in file.readlines():
        redis_client.set(word.rstrip("\n").upper(), "")


def load_dictionary(redis_client: fakeredis.FakeRedis):
    print("Loading Dictionary...")
    load_words_from_file(redis_client)
    print("Dictionary Loaded!")


def is_valid_word(word: str, redis_client: fakeredis.FakeRedis) -> bool:
    return redis_client.exists(word)


def break_string_until_end_index(end_index: int, dp: List[str]):
    valid_words_until_end_index = ""

    for start_index in range(end_index - 1, -1, -1):
        word = input_string[start_index:end_index]

        if is_valid_word(word, redis_client):
            if start_index == 0:
                valid_words_until_end_index = word
            elif dp[start_index]:
                valid_words_until_end_index = dp[start_index] + ' ' + word

    return valid_words_until_end_index


def break_string_to_valid_words(string: str):
    input_size = len(string)

    dp = [""] * (input_size + 1)

    for end_index in range(1, input_size + 1):
        dp[end_index] = break_string_until_end_index(end_index, dp.copy())

    return dp[input_size]


if __name__ == '__main__':
    redis_client = fakeredis.FakeRedis()

    load_dictionary(redis_client)

    input_string = input("\nEnter Input:\n").strip()

    answer = break_string_to_valid_words(input_string)

    print(answer) if answer else print("The String is Invalid!")
