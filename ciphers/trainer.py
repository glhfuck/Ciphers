import pickle
import collections
from dataclasses import dataclass
from ciphers.iomanager import IOManager


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