from abc import abstractmethod


class Cipher:
    @abstractmethod
    def encode(self) -> None:
        pass

    @abstractmethod
    def decode(self) -> None:
        pass