"""
Title: Fano Algorithm and Simplified QR Code

Description:
This script implements the Fano algorithm for encoding and decoding strings, and generates a simplified QR code representation. The script includes the following functionalities:

1. fano_algorithm(input_str): Encodes the input string using the Fano algorithm and prints the average length of the encoded characters. It also verifies McMillan's inequality and returns the encoded string and the coding dictionary.
2. decode(coded_str, coded_dict): Decodes the encoded string using the provided coding dictionary.
3. draw_qr_code(coded_str): Graphically represents the encoded string as a simplified QR code using the turtle graphics library.

Requirements:
- Turtle graphics library for drawing.
"""

import turtle as t

def fano_algorithm(input_str):
    """
    Encodes the input string using the Fano algorithm.

    Args:
    - input_str (str): The string to be encoded.

    Returns:
    - tuple: Encoded string and the dictionary of Fano codes for characters.
    """
    set_str = set(input_str)
    probabilities = {}

    # Calculate probabilities of each character
    for i in set_str:
        probabilities[i] = input_str.count(i) / len(input_str)

    # Sort characters by probability
    sort_value = sorted(probabilities.values(), reverse=True)
    sort_letters = []
    for i in sort_value:
        for j in set_str:
            if probabilities[j] == i and j not in sort_letters:
                sort_letters.append(j)

    result = [''] * len(sort_letters)

    def tree(result, sort_value):
        """
        Helper function to build Fano codes.

        Args:
        - result (list): List of character codes.
        - sort_value (list): Sorted list of probabilities.

        Returns:
        - list: List of Fano codes for each character.
        """
        if len(result) == 1:
            return result
        elif len(result) == 2:
            if sort_value[0] > sort_value[1] or sort_value[0] == sort_value[1]:
                result[0] += '0'
                result[1] += '1'
            else:
                result[0] += '1'
                result[1] += '0'
            return result
        else:
            r = []
            for i in range(len(result)):
                local_result = abs(sum(sort_value[:(i+1)]) - sum(sort_value[(i+1):]))
                next_result = abs(sum(sort_value[:(i+2)]) - sum(sort_value[(i+2):]))
                if local_result == next_result or local_result < next_result:
                    r.append(i)
            mid = r[0] + 1
            if sum(sort_value[:mid]) > sum(sort_value[:mid]) or sum(sort_value[:mid]) == sum(sort_value[:mid]):
                for j in range(mid):
                    result[j] += '0'
                for j in range(mid, len(result)):
                    result[j] += '1'
            else:
                for j in range(mid):
                    result[j] += '1'
                for j in range(mid, len(result)):
                    result[j] += '0'
            return tree(result[:mid], sort_value[:mid]) + tree(result[mid:], sort_value[mid:])

    tree_value = tree(result, sort_value)
    coded_dict = {letter: code for letter, code in zip(sort_letters, tree_value)}
    result = ''.join(coded_dict[i] for i in input_str)

    # Calculate average length of encoded character
    average_length = sum(i * len(tree_value[j]) for j, i in enumerate(sort_value))
    mcmillans_inequality = sum(1 / 2 ** len(i) for i in tree_value)

    print('The average length of an encoded character:', round(average_length, 1))
    if mcmillans_inequality <= 1:
        print("McMillan's inequality holds and is equal to", round(mcmillans_inequality, 1))
    else:
        print('McMillan’s inequality does not hold')

    return result, coded_dict

def decode(coded_str, coded_dict):
    """
    Decodes the Fano encoded string using the coding dictionary.

    Args:
    - coded_str (str): The Fano encoded string.
    - coded_dict (dict): The dictionary mapping characters to their Fano codes.

    Returns:
    - str: The decoded string.
    """
    local_search = ''
    result = ''
    for i in coded_str:
        local_search += i
        if local_search in coded_dict.values():
            for j in coded_dict.keys():
                if coded_dict[j] == local_search:
                    result += j
                    local_search = ''
    return result

def draw_qr_code(coded_str):
    """
    Draws a simplified QR code using turtle graphics.

    Args:
    - coded_str (str): The encoded string to be represented as a QR code.
    """
    t.hideturtle()

    def black_square(x, y):
        """
        Draws a black square at the specified coordinates.

        Args:
        - x (int): The x-coordinate of the square.
        - y (int): The y-coordinate of the square.
        """
        t.penup()
        t.setpos(x, y)
        t.pendown()
        for _ in range(4):
            t.forward(1)
            t.right(90)
        t.penup()

    def big_square(x, y, r):
        """
        Draws a square of size r x r starting at coordinates (x, y).

        Args:
        - x (int): The x-coordinate of the top-left corner.
        - y (int): The y-coordinate of the top-left corner.
        - r (int): The size of the square.
        """
        t.tracer(0)
        copy_x = x
        for _ in range(r):
            x += 2
            black_square(x, y)
        for _ in range(r-2):
            y -= 2
            black_square(copy_x+2, y)
            black_square(copy_x+(r*2), y)
        y -= 2
        x = copy_x
        for _ in range(r):
            x += 2
            black_square(x, y)

    # Draw position markers
    x, y = -50, 50
    for i in range(3):
        x += 2
        y -= 2
        t.color('white')
        big_square(x, y, 9)
        x += 2
        y -= 2
        t.color('black')
        big_square(x, y, 7)
        x += 2
        y -= 2
        t.color('white')
        big_square(x, y, 5)
        x += 2
        y -= 2
        t.color('black')
        big_square(x, y, 3)
        x += 2
        y -= 2
        big_square(x, y, 1)
        x, y = -14, 50
        if i == 1:
            x, y = -50, 14

    def draw_information():
        """
        Draws the information portion of the QR code based on the encoded string.
        """
        copy_coded_str = list(coded_str)
        y = 48
        for _ in range(8):
            x = -30
            y -= 2
            for _ in range(9):
                try:
                    element = copy_coded_str.pop(0)
                except IndexError:
                    break
                if element == '0':
                    x += 2
                    t.color('black')
                    black_square(x, y)
                else:
                    x += 2
                    t.color('white')
                    black_square(x, y)
        for _ in range(9):
            x = -46
            y -= 2
            for _ in range(25):
                try:
                    element = copy_coded_str.pop(0)
                except IndexError:
                    break
                if element == '0':
                    x += 2
                    t.color('black')
                    black_square(x, y)
                else:
                    x += 2
                    t.color('white')
                    black_square(x, y)
        for _ in range(8):
            x = -30
            y -= 2
            for _ in range(17):
                try:
                    element = copy_coded_str.pop(0)
                except IndexError:
                    break
                if element == '0':
                    x += 2
                    t.color('black')
                    black_square(x, y)
                else:
                    x += 2
                    t.color('white')
                    black_square(x, y)

    draw_information()

# Example usage
coded_str, coded_dict = fano_algorithm('Three hundred and forty-eight years, six months, and nineteen days ago to-day, the Parisians awoke to the sound of all the bells in the triple circuit of the city, the university, and the town ringing a full peal.')
print('\nDecoded string:', decode(coded_str, coded_dict))
draw_qr_code(coded_str)
