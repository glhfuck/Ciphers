from typing import Optional, List
from dataclasses import dataclass


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