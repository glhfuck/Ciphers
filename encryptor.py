import argparse
import collections
import pickle
from dataclasses import dataclass

parser = argparse.ArgumentParser()

#parser.add_argument("mode", choices=['encode', 'decode', 'train', 'hack'])
parser.add_argument("--cipher", choices=['caesar', 'vigenere'])
parser.add_argument("--key")
parser.add_argument("--input-file", dest = "inF")
parser.add_argument("--output-file", dest = "outF")
parser.add_argument("--text-file", dest = "txtF")
parser.add_argument("--model-file", dest = "mdlF")


args = parser.parse_args()

print(args)

alphabets = ("abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def alphabet_pos(char):
    for i in range(len(alphabets)):
        if (char in alphabets[i]):
            pos = alphabets[i].index(char)
            return pos
    return -0.5

def chr_shift(char, key):
    for i in range(len(alphabets)):
        if (char in alphabets[i]):
            char = alphabets[i][(alphabets[i].index(char) + key) % len(alphabets[i])]
    return char


@dataclass
class caesar():
    key: int
    src: str
    dir: str

    def encode(self):
        if (self.src == None):
            text = list(input())
        else:
            inputFile = open(self.src)
            text = list(inputFile.read())
        encodedText = [chr_shift(char, int(self.key)) for char in text]
        if (self.dir == None):
            print("".join(encodedText))
        else:
            outputFile = open(self.dir, "w")
            outputFile.write("".join(encodedText))
        inputFile.close()
        outputFile.close()

    def decode(self):
        if (self.src == None):
            text = list(input())
        else:
            inputFile = open(self.src)
            text = list(inputFile.read())
        encodedText = [chr_shift(char, -int(self.key)) for char in text]
        if (self.dir == None):
            print("".join(encodedText))
        else:
            outputFile = open(self.dir, "w")
            outputFile.write("".join(encodedText))
        inputFile.close()
        outputFile.close()


@dataclass
class vigenere():
    key: str
    src: str
    dir: str

    def encode(self):
        if (self.src == None):
            text = list(input())
        else:
            inputFile = open(self.src)
            text = list(inputFile.read())
        shift_size = list(map(alphabet_pos, list(self.key)))
        encodedText = []
        unknownCharsCounter = 0
        for i in range(len(text)):
            if (alphabet_pos(text[i]) == -0.5):
                unknownCharsCounter += 1
            encodedText.append(chr_shift(text[i], shift_size[(i - unknownCharsCounter) % len(shift_size)]))
        if (self.dir == None):
            print("".join(encodedText))
        else:
            outputFile = open(self.dir, "w")
            outputFile.write("".join(encodedText))

    def decode(self):
        if (self.src == None):
            text = list(input())
        else:
            inputFile = open(self.src)
            text = list(inputFile.read())
        shift_size = list(map(alphabet_pos, list(self.key)))
        shift_size = [-x for x in shift_size]
        encodedText = []
        unknownCharsCounter = 0
        for i in range(len(text)):
            if (alphabet_pos(text[i]) == -0.5):
                unknownCharsCounter += 1
            encodedText.append(chr_shift(text[i], shift_size[(i - unknownCharsCounter) % len(shift_size)]))
        if (self.dir == None):
            print("".join(encodedText))
        else:
            outputFile = open(self.dir, "w")
            outputFile.write("".join(encodedText))

@dataclass
class train():
    src: str
    mdl: str

    def make_mdl(self):
        if (self.src == None):
            text = list(input())
        else:
            inputFile = open(self.src)
            text = list(inputFile.read())
        for char in text:
            if (not char.isalpha()):
               text.remove(char)

        charCounter = collections.Counter()
        for char in text:
            charCounter[char] += 1;
        charSum = sum(charCounter.values())
        for key in charCounter.keys():
            charCounter[key] /= charSum
        pickle.dump(charCounter, open(self.mdl, "wb"))
        inputFile.close()

@dataclass
class hack():
    src: str
    dir: str
    mdl: str

    def decoder(self):
        if (self.src == None):
            text = list(input())
        else:
            inputFile = open(self.src)
            text = list(inputFile.read())
        results = []
        for i in range(len(alphabets[0])):
            encodedText = [chr_shift(char, i) for char in text]
            for char in encodedText:
                if (not char.isalpha()):
                    encodedText.remove(char)
            charCounter = collections.Counter()
            for char in encodedText:
                charCounter[char] += 1;
            charSum = sum(charCounter.values())
            for key in charCounter.keys():
                charCounter[key] /= charSum
            modelCounter = pickle.load(open(self.mdl, "rb"))
            deltaCounter = modelCounter - charCounter
            for key in deltaCounter.keys():
                deltaCounter[key] = abs(deltaCounter[key])
            results.append(sum(deltaCounter.values()))
        Shift_size = results.index(min(results))
        trueText = [chr_shift(char, Shift_size) for char in text]
        if (self.dir == None):
            print("".join(trueText))
        else:
            outputFile = open(self.dir, "w")
            outputFile.write("".join(trueText))
        inputFile.close()
        outputFile.close()




CaesarShifrator = caesar(5, 'inF.txt', 'outF.txt')
Training = train("text.txt", "mdl.txt")
Haker = hack("outF.txt", 'hackout.txt', 'mdl.txt')

CaesarShifrator.encode()
Training.make_mdl()
Haker.decoder()