"""
Title: Hamming Coding with Error Detection and Correction

Description:
This script implements Hamming encoding and error detection and correction for binary strings. It includes the following functionalities:

1. hamming_coding(input_str): Encodes the input binary string using the Hamming (7,4) algorithm and returns the encoded string.
2. error_generator(encoded_string): Simulates random errors in the encoded string and returns the string with errors.
3. error_correction(string_with_errors): Detects and corrects errors in the "corrupted" string and prints the positions of any detected errors.

Requirements:
- Python 3.x
"""

import random

# Hamming (7,4) generator matrix
generative_matrix = [
    [0, 0, 1],  # Column 1
    [0, 1, 0],  # Column 2
    [0, 1, 1],  # Column 3
    [1, 0, 0],  # Column 4
    [1, 0, 1],  # Column 5
    [1, 1, 0],  # Column 6
    [1, 1, 1]   # Column 7
]

def hamming_coding(input_str):
    """
    Encodes a binary string using the Hamming (7,4) code.

    Args:
    - input_str (str): The binary string to be encoded (should be a multiple of 4 bits).

    Returns:
    - str: The Hamming encoded binary string.
    """
    x_indices = [2 ** i for i in range(3)]  # Positions of parity bits
    result_with_x = []

    # Insert parity bits placeholders
    i, j, k = 0, 0, 0
    while j < len(input_str):
        if i == (x_indices[k] - 1):
            result_with_x.append('x' + str(k + 1))
            k += 1
        else:
            result_with_x.append(input_str[j])
            j += 1
        i += 1

    # Compute parity bits
    i = 0
    count_for_matrix = 0
    while i < len(result_with_x):
        local_x_1 = ''
        local_x_2 = ''
        local_x_3 = ''
        for _ in range(7):
            try:
                local_x_1 += result_with_x[i] + '*' + str(generative_matrix[count_for_matrix][0]) + '+'
                local_x_2 += result_with_x[i] + '*' + str(generative_matrix[count_for_matrix][1]) + '+'
                local_x_3 += result_with_x[i] + '*' + str(generative_matrix[count_for_matrix][2]) + '+'
                i += 1
                count_for_matrix += 1
            except IndexError:
                pass

        count_for_matrix = 0

        def find_x(str_x):
            local_result = ''
            for i in range(len(str_x)):
                if str_x[i] == '*' and str_x[i + 1] == '1' and str_x[i - 1] != '0':
                    if str_x[i - 2] == 'x':
                        local_result += str_x[i - 2] + str_x[i - 1] + '+'
                    else:
                        local_result += str_x[i - 1] + '+'
            res = 0
            x = 0
            for i in range(len(local_result)):
                if local_result[i].isdigit() and local_result[i - 1] != 'x':
                    res += int(local_result[i])
                if local_result[i] == 'x':
                    x = local_result[i + 1]
            res %= 2
            return ('0', x) if res == 0 else ('1', x)

        if 'x' in local_x_1:
            x_1, x = find_x(local_x_1)
            for j in range(len(result_with_x)):
                if result_with_x[j] == 'x' + str(x):
                    result_with_x[j] = x_1
        if 'x' in local_x_2:
            x_2, x = find_x(local_x_2)
            for j in range(len(result_with_x)):
                if result_with_x[j] == 'x' + str(x):
                    result_with_x[j] = x_2
        if 'x' in local_x_3:
            x_3, x = find_x(local_x_3)
            for j in range(len(result_with_x)):
                if result_with_x[j] == 'x' + str(x):
                    result_with_x[j] = x_3

    return ''.join(result_with_x)

def error_generator(encoded_string):
    """
    Simulates random errors in the encoded string.

    Args:
    - encoded_string (str): The encoded binary string.

    Returns:
    - str: The encoded string with simulated errors.
    """
    choice = [True, False, True]
    string = list(encoded_string)

    for i in range(0, len(string), 7):
        if random.choice(choice):
            try:
                index_error = random.randint(i, i + 6)
                string[index_error] = str((int(string[index_error]) + 1) % 2)
                print('Error is introduced at position:', index_error + 1)
            except IndexError:
                pass

    return ''.join(string)

def error_correction(string_with_errors):
    """
    Detects and corrects errors in the corrupted Hamming code string.

    Args:
    - string_with_errors (str): The encoded string with errors.

    Returns:
    - str: The corrected string.
    """
    corrected_str = ''
    i = 0
    add_to_count = -7
    k = 0

    while i < len(string_with_errors):
        add_to_count += 7
        j = 0
        x_1 = x_2 = x_3 = 0

        for _ in range(7):
            try:
                x_1 += int(string_with_errors[i]) * generative_matrix[j][0]
                x_2 += int(string_with_errors[i]) * generative_matrix[j][1]
                x_3 += int(string_with_errors[i]) * generative_matrix[j][2]
                i += 1
                j += 1
            except IndexError:
                pass

        count = 0
        x_1 %= 2
        x_2 %= 2
        x_3 %= 2

        if x_1 == 1:
            count += 2 ** (k + 2)
        if x_2 == 1:
            count += 2 ** (k + 1)
        if x_3 == 1:
            count += 2 ** k

        k += 3

    if count == 0:
        print('No error found.')
        return string_with_errors
    else:
        print('Error found at position:', count)
        corrected_str = ''.join(
            str((int(string_with_errors[i]) + 1) % 2) if i == count - 1 else string_with_errors[i]
            for i in range(len(string_with_errors))
        )
        return corrected_str

# Example usage
binary_string = '1001'
encoded_string = hamming_coding(binary_string)
string_with_errors = error_generator(encoded_string)
corrected_string = error_correction(string_with_errors)

print('Encoded string:  ', encoded_string)
print('String with errors:', string_with_errors)
print('Corrected string:', corrected_string)
