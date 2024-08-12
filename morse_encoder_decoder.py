"""
    Task:
    Implement Morse code encoding and decoding functions, and a function to play Morse code messages as sound signals. The Morse code system uses dots (short signals) and dashes (long signals) to represent letters and numbers. The provided code will handle the following functionalities:

    a) Encoding a given text string into Morse code.
    b) Decoding a Morse code string back into readable text.
    c) Playing the Morse code as sound signals using the `beep` module.

    To install the required module for playing sounds, use:
    pip install beep

    Note: The `beep` module is used to play sounds on Linux. For Windows, you can use the `winsound` module as shown in the example.
    """

import os
import time

try:
    # Morse code dictionary
    morse = {
        ('A', 'a'): [1, 3], ('B', 'b'): [3, 1, 1, 1], ('C', 'c'): [3, 1, 3, 1], ('D', 'd'): [3, 1, 1],
        ('E', 'e'): [1], ('F', 'f'): [1, 1, 3, 1], ('G', 'g'): [3, 3, 1], ('H', 'h'): [1, 1, 1, 1],
        ('I', 'i'): [1, 1], ('J', 'j'): [1, 3, 3, 3], ('K', 'k'): [3, 1, 3], ('L', 'l'): [1, 3, 1, 1],
        ('M', 'm'): [3, 3], ('N', 'n'): [3, 1], ('O', 'o'): [3, 3, 3], ('P', 'p'): [1, 3, 3, 1],
        ('Q', 'q'): [3, 3, 1, 3], ('R', 'r'): [1, 3, 1], ('S', 's'): [1, 1, 1], ('T', 't'): [3],
        ('U', 'u'): [1, 1, 3], ('V', 'v'): [1, 1, 1, 3], ('W', 'w'): [1, 3, 3], ('X', 'x'): [3, 1, 1, 3],
        ('Y', 'y'): [3, 1, 3, 3], ('Z', 'z'): [3, 3, 1, 1], ('1', '1'): [1, 3, 3, 3, 3],
        ('2', '2'): [1, 1, 3, 3, 3], ('3', '3'): [1, 1, 1, 3, 3], ('4', '4'): [1, 1, 1, 1, 3],
        ('5', '5'): [1, 1, 1, 1, 1], ('6', '6'): [3, 1, 1, 1, 1], ('7', '7'): [3, 3, 1, 1, 1],
        ('8', '8'): [3, 3, 3, 1, 1], ('9', '9'): [3, 3, 3, 3, 1], ('0', '0'): [3, 3, 3, 3, 3],
        ('.', '.'): [1, 1, 1, 1, 1, 1], (',', ','): [1, 3, 1, 3, 1, 3], ('/', '/'): [3, 1, 1, 3, 1],
        ('?', '?'): [1, 1, 3, 3, 1, 1], ('!', '!'): [3, 3, 1, 1, 3, 3], (':', ':'): [3, 3, 3, 1, 1, 1],
        (';', ';'): [3, 1, 3, 1, 3, 1], ("'", "'"): [1, 3, 3, 3, 3, 1], ('-', '-'): [3, 1, 1, 1, 1, 3],
        ('"', '"'): [1, 3, 1, 1, 3, 1], (' ', ' '): ['@']
    }

    # Reverse Morse dictionary for decoding
    def reversed_dict(dict):
        result = {}
        for key, value in dict.items():
            result[tuple(value)] = key
        return result

    # Function to encode a text string into Morse code
    def encoding(s):
        coded = []
        for i in s:
            if i.upper() in morse:
                value = morse[i.upper()]
                for j in value:
                    coded.append(j)
                coded.append(';')  # Separator between characters
            elif i == ' ':
                coded.append('@')  # Space between words
        return coded

    # Function to decode Morse code back into text
    def decoding(lst):
        decoded = ''
        local_result = []
        for i in lst:
            if i == ';':
                decoded += reversed_morze[tuple(local_result)]
                local_result = []
            elif i == '@':
                decoded += ' '
                local_result = []
            else:
                local_result.append(i)
        return decoded

    # Function to play Morse code as sound signals
    def play_morse(coded):
        try:
            import beep
            for i in coded:
                if i == '@':
                    time.sleep(1.2)  # Space between words
                elif i == ';':
                    time.sleep(0.7)  # Space between characters
                else:
                    beep.beep(frequency=2000, length=450 * i)  # Frequency and duration
        except ImportError:
            print("The 'beep' module is not installed. Please install it using 'pip install beep'.")
        except Exception as e:
            print(f"An error occurred: {e}")

    reversed_morze = reversed_dict(morse)
    coded = encoding('Hello world!')
    print('Coded message:', coded)
    print('Decoded message:', decoding(coded))
    play_morse(coded)

except Exception as e:
    print('NOT FOR ONLINE COMPILER:', e)
