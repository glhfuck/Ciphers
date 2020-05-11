# Ciphers

> My first serious project made specifically for the code review

### This python script can encode and decode Caesar, Vigenere and Vernams ciphers, and hack Caesars cipher

## Usage

### `python encryptor.py [encode|decode|train|hack] [OPTIONS]`

- ##### Encode mode OPTIONS:
###### `--cipher [caesar|vigenere|vernam]`**[required]**
###### `--key KEY` int for Caesar, str for Vigenere and Vernam **[required]**
###### `--input-file FILENAME`
###### `--output-file FILENAME`
---
- ##### Decode mode OPTIONS:
###### `--cipher [caesar|vigenere|vernam]`**[required]**
###### `--key KEY` int for Caesar, str for Vigenere and Vernam **[required]**
###### `--input-file FILENAME`
###### `--output-file FILENAME`
---
- ##### Train mode OPTIONS:
###### `--text-file FILENAME` text to learn how often letters meet **[required]**
###### `--model-file FILENAME` 
---
- ##### Hack mode OPTIONS:
###### `--model-file FILENAME` the file that was created in training mode **[required]**
###### `--input-file FILENAME`
###### `--output-file FILENAME`
---
#### Maintained alphabet: 
abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZабвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ !"#$%&'()*+,-./:;<=>?@[\\]^_\`{|}~
