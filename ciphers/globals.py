import string
from typing import Optional


ALPHABETS = (string.ascii_lowercase,
             string.ascii_uppercase,
             string.punctuation + " ",
             "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
             "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")


def alphabet_pos(char: str) -> Optional[int]:
    for alphabet in ALPHABETS:
        if char in alphabet:
            pos = alphabet.index(char)
            return pos
    return None


def char_shift(char: str, key: int) -> str:
    for alphabet in ALPHABETS:
        if char in alphabet:
            char = alphabet[(alphabet.index(char) + key) % len(alphabet)]
    return char