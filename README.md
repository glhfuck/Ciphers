# Ciphers

### This python script can encode and decode Caesar, Vigenere and Vernams ciphers, and hack Caesars cipher

## Usage

#### 
```sh
python encryptor.py [encode|decode|train|hack] OPTIONS
```


- ##### Encode mode OPTIONS:
```sh
--cipher [caesar|vigenere|vernam] --key KEY [--input-file IN_FILENAME] [--output-file OUT_FILENAME]
```
###### `KEY` int for Caesar, str for Vigenere and Vernam
###### `IN_FILENAME = inF` by default 
###### `OUT_FILENAME = outF` by default 


- ##### Decode mode OPTIONS:
```sh
--cipher [caesar|vigenere|vernam] --key KEY [--input-file IN_FILENAME] [--output-file OUT_FILENAME]
```
###### `KEY` int for Caesar, str for Vigenere and Vernam
###### `IN_FILENAME = inF` by default 
###### `OUT_FILENAME = outF` by default 


- ##### Train mode OPTIONS:
```sh
[--text-file TEXT_FILENAME] [--model-file MODEL_FILENAME]
```
###### `TEXT_FILENAME` file name with text for training, `txtF` by default
###### `MODEL_FILENAME` the name of the file to be generated, `mdlF` by default


- ##### Hack mode OPTIONS:
```sh
[--model-file MODEL_FILENAME] [--input-file IN_FILENAME] [--output-file OUT_FILENAME]
```
###### `MODEL_FILENAME` the file that was generated in training mode, `mdlF` by default
###### `IN_FILENAME = inF` by default 
###### `OUT_FILENAME = outF` by default 
---
#### Maintained alphabet: 
abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZабвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ !"#$%&'()*+,-./:;<=>?@[\\]^_\`{|}~
