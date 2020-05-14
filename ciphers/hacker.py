import pickle
import collections
from ciphers.globals import ALPHABETS, char_shift
from dataclasses import dataclass
from typing import Tuple, Counter
from ciphers.iomanager import IOManager

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
        lengths = map(len, ALPHABETS)
        return max(lengths)
