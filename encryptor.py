#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import argparse
import collections
import pickle
import string
from typing import Optional, List, Tuple, Counter
from dataclasses import dataclass


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


@dataclass
class IOManager:
    src: Optional[str]
    dir: Optional[str]

    def read(self) -> List[str]:
        if self.src is None:
            text = list(input())
        else:
            with open(self.src, encoding='utf-8') as input_file:
                text = list(input_file.read())
        return text

    def write(self, encoded_text: List[str]) -> None:
        if self.dir is None:
            print("".join(encoded_text))
        else:
            with open(self.dir, "w", encoding='utf-8') as output_file:
                output_file.write("".join(encoded_text))


@dataclass
class Caesar:
    key: int
    src: str
    dir: str

    def encode(self) -> None:
        iomanager = IOManager(self.src, self.dir)
        text = iomanager.read()
        encoded_text = [char_shift(char, int(self.key)) for char in text]
        iomanager.write(encoded_text)

    def decode(self) -> None:
        self.key = -1 * int(self.key)
        self.encode()
        self.key *= -1


class Vigenere:
    def __init__(self, key: str, src: str, dir: str):
        self.key: List[int] = self.make_key_list(key)
        self.src = src
        self.dir = dir

    def encode(self) -> None:
        iomanager = IOManager(self.src, self.dir)
        text = iomanager.read()
        len_key_list = len(self.key)
        encoded_text = []
        key_index = 0
        for char in text:
            if alphabet_pos(char) is None:
                encoded_text.append(char)
                continue
            new_char = char_shift(char, self.key[key_index])
            encoded_text.append(new_char)
            key_index = (key_index + 1) % len_key_list
        iomanager.write(encoded_text)

    def decode(self) -> None:
        self.key = [-x for x in self.key]
        self.encode()
        self.key = [-x for x in self.key]

    @staticmethod
    def make_key_list(key: str) -> List[int]:
        key_list = list(map(alphabet_pos, list(key)))
        if None in key_list:
            raise ValueError("Wrong key")
        return key_list


@dataclass
class Vernam:
    key: str
    src: str
    dir: str

    def encode(self) -> None:
        iomanager = IOManager(self.src, self.dir)
        text = iomanager.read()
        len_key_list = len(self.key)
        encoded_text = []
        key_index = 0
        for char in text:
            new_char = ord(char) ^ ord(self.key[key_index])
            encoded_text.append(chr(new_char))
            key_index = (key_index + 1) % len_key_list
        iomanager.write(encoded_text)

    def decode(self) -> None:
        self.encode()


@dataclass
class Trainer:
    src: str
    mdl: str

    def make_model(self) -> None:
        iomanager = IOManager(self.src, None)
        text = iomanager.read()
        char_counter: Counter = collections.Counter()
        for char in text:
            if char.isalpha():
                char_counter[char] += 1
        char_sum = max(1, sum(char_counter.values()))
        for key in char_counter:
            char_counter[key] /= char_sum
        print(char_counter)
        with open(self.mdl, "wb") as model_file:
            pickle.dump(char_counter, model_file)


@dataclass
class Hacker:
    src: str
    dir: str
    mdl: str

    def decode(self) -> None:
        iomanager = IOManager(self.src, self.dir)
        text = iomanager.read()
        model_counter = pickle.load(open(self.mdl, "rb"))
        results = []
        for i in range(0, -self.longest_alphabet_length(ALPHABETS), -1):
            encoded_text = [char_shift(char, i) for char in text]
            char_counter: Counter = collections.Counter()
            for char in encoded_text:
                if char.isalpha():
                    char_counter[char] += 1
            char_sum = max(1, sum(char_counter.values()))
            for key in char_counter:
                char_counter[key] /= char_sum
            delta_counter = model_counter - char_counter
            for key in delta_counter:
                delta_counter[key] = abs(delta_counter[key])
            results.append(sum(delta_counter.values()))

        shift_size = results.index(min(results))
        true_text = [char_shift(char, -shift_size) for char in text]
        iomanager.write(true_text)

    @staticmethod
    def longest_alphabet_length(alphabets: Tuple[str, ...]) -> int:
        lengths = list(map(len, ALPHABETS))
        return max(lengths)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="mode")

    parser_encode = subparsers.add_parser('encode')
    parser_encode.add_argument("--cipher",
                               choices=['caesar', 'vigenere', 'vernam'])
    parser_encode.add_argument("--key")
    parser_encode.add_argument("--input-file", dest="inF")
    parser_encode.add_argument("--output-file", dest="outF")

    parser_decode = subparsers.add_parser('decode')
    parser_decode.add_argument("--cipher",
                               choices=['caesar', 'vigenere', 'vernam'])
    parser_decode.add_argument("--key")
    parser_decode.add_argument("--input-file", dest="inF")
    parser_decode.add_argument("--output-file", dest="outF")

    parser_train = subparsers.add_parser('train')
    parser_train.add_argument("--text-file", dest="txtF")
    parser_train.add_argument("--model-file", dest="mdlF")

    parser_hack = subparsers.add_parser('hack')
    parser_hack.add_argument("--input-file", dest="inF")
    parser_hack.add_argument("--output-file", dest="outF")
    parser_hack.add_argument("--model-file", dest="mdlF")

    args = parser.parse_args()

    if args.mode == "train":
        Training = Trainer(args.txtF, args.mdlF)
        Training.make_model()

    elif args.mode == "hack":
        Hack = Hacker(args.inF, args.outF, args.mdlF)
        Hack.decode()

    elif args.cipher == "caesar":
        CaesarCipher = Caesar(args.key, args.inF, args.outF)
        if args.mode == "encode":
            CaesarCipher.encode()
        elif args.mode == "decode":
            CaesarCipher.decode()

    elif args.cipher == "vigenere":
        VigenereCipher = Vigenere(args.key, args.inF, args.outF)
        if args.mode == "encode":
            VigenereCipher.encode()
        elif args.mode == "decode":
            VigenereCipher.decode()

    elif args.cipher == "vernam":
        VernamCipher = Vernam(args.key, args.inF, args.outF)
        if args.mode == "encode":
            VernamCipher.encode()
        elif args.mode == "decode":
            VernamCipher.decode()


if __name__ == "__main__":
    main()
