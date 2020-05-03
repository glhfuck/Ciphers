import argparse
import collections
import pickle
import string
from dataclasses import dataclass

parser = argparse.ArgumentParser()

parser.add_argument("mode", choices=['encode', 'decode', 'train', 'hack'])
parser.add_argument("--cipher", choices=['caesar', 'vigenere'])
parser.add_argument("--key")
parser.add_argument("--input-file", dest="inF")
parser.add_argument("--output-file", dest="outF")
parser.add_argument("--text-file", dest="txtF")
parser.add_argument("--model-file", dest="mdlF")

args = parser.parse_args()

alphabets = (string.ascii_lowercase, string.ascii_uppercase)

def alphabet_pos(char):
    for i in range(len(alphabets)):
        if char in alphabets[i]:
            pos = alphabets[i].index(char)
            return pos
    return None

def char_shift(char, key):
    for i in range(len(alphabets)):
        if char in alphabets[i]:
            char = alphabets[i][(alphabets[i].index(char) + key) % len(alphabets[i])]
    return char


@dataclass
class IOManager:
    src: str
    dir: str

    def read(self):
        if self.src == None:
            text = list(input())
        else:
            with open(self.src) as input_file:
                text = list(input_file.read())
        return text

    def write(self, encoded_text):
        if self.dir == None:
            print("".join(encoded_text))
        else:
            with open(self.dir, "w") as output_file:
                output_file.write("".join(encoded_text))


@dataclass
class Caesar:
    key: int
    src: str
    dir: str

    def encode(self):
        iomanager = IOManager(self.src, self.dir)
        text = iomanager.read()
        encoded_text = [char_shift(char, int(self.key)) for char in text]
        iomanager.write(encoded_text)

    def decode(self):
        self.key *= -1
        Caesar.encode(self)
        self.key *= -1


@dataclass
class Vigenere:
    key: str
    src: str
    dir: str

    def encode(self):
        iomanager = IOManager(self.src, self.dir)
        text = iomanager.read()
        shift_size = list(map(alphabet_pos, list(self.key)))
        encoded_text = []
        unknown_chars_counter = 0
        for i in range(len(text)):
            if alphabet_pos(text[i]) == None:
                unknown_chars_counter += 1
            encoded_text.append(char_shift(text[i], shift_size[(i - unknown_chars_counter) % len(shift_size)]))
        iomanager.write(encoded_text)

    def decode(self):
        self.key = Vigenere.make_complement_key(self.key)
        Vigenere.encode(self)
        self.key = Vigenere.make_complement_key(self.key)

    @staticmethod
    def make_complement_key(key):
        complement_key = []
        for char in key:
            try:
                complement_key.append(char_shift(char, -2 * alphabet_pos(char)))
            except TypeError:
                pass
        return "".join(complement_key)


@dataclass
class Trainer:
    src: str
    mdl: str

    def make_model(self):
        iomanager = IOManager(self.src, None)
        text = iomanager.read()
        char_counter = collections.Counter()
        for char in text:
            if char.isalpha():
                char_counter[char] += 1;
        char_sum = max(1, sum(char_counter.values()))
        for key in char_counter:
            char_counter[key] /= char_sum
        with open(self.mdl, "wb") as model_file:
            pickle.dump(char_counter, model_file)

@dataclass
class Hacker:
    src: str
    dir: str
    mdl: str

    def decode(self):
        iomanager = IOManager(self.src, self.dir)
        text = iomanager.read()
        model_counter = pickle.load(open(self.mdl, "rb"))
        results = []
        for i in range(len(alphabets[0])):
            encoded_text = [char_shift(char, i) for char in text]
            char_counter = collections.Counter()
            for char in encoded_text:
                if char.isalpha():
                    char_counter[char] += 1;
            char_sum = max(1, sum(char_counter.values()))
            for key in char_counter:
                char_counter[key] /= char_sum
            delta_counter = model_counter - char_counter
            for key in delta_counter:
                delta_counter[key] = abs(delta_counter[key])
            results.append(sum(delta_counter.values()))

        shift_size = results.index(min(results))
        true_text = [char_shift(char, shift_size) for char in text]
        iomanager.write(true_text)


if args.cipher == "caesar":
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
elif args.mode == "train":
    Training = Trainer(args.inF, args.mdlF)
    Training.make_model()
elif args.mode == "hack":
    Hack = Hacker(args.inF, args.outF, args.mdlF)
    Hack.decode()
