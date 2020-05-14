from ciphers.trainer import Trainer
from ciphers.hacker import  Hacker
from ciphers.vigenere import Vigenere
from ciphers.caesar import Caesar
from ciphers.vernam import Vernam
from ciphers.argparser import parse
from ciphers.cipher import Cipher


def main() -> None:
    args = parse()

    if args.mode == "train":
        Training = Trainer(args.txtF, args.mdlF)
        Training.make_model()
        return
    elif args.mode == "hack":
        Hack = Hacker(args.inF, args.outF, args.mdlF)
        Hack.decode()
        return

    cipher = Cipher()

    if args.cipher == "caesar":
        cipher = Caesar(args.key, args.inF, args.outF)
    elif args.cipher == "vigenere":
        cipher = Vigenere(args.key, args.inF, args.outF)
    elif args.cipher == "vernam":
        cipher = Vernam(args.key, args.inF, args.outF)

    getattr(cipher, args.mode)()
