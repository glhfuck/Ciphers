import argparse


def parse() -> argparse.Namespace:
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

    return args