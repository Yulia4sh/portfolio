"""
Title: Huffman Encoding and Decoding

Description:
This script implements the Huffman encoding algorithm for compressing strings and decoding them back to their original form. The script includes the following functionalities:

1. encode_huffman(input_str): Encodes the input string using the Huffman algorithm. It also calculates and prints the average length of encoded characters and verifies McMillan's inequality.
2. decode(encoded_str, code_dict): Decodes a Huffman encoded string using the provided code dictionary.

Requirements:
- Python 3.x
"""

def encode_huffman(input_str):
    """
    Encodes the input string using the Huffman algorithm.

    Args:
    - input_str (str): The string to be encoded.

    Returns:
    - tuple: Encoded string and the dictionary of Huffman codes for characters.
    """
    from collections import Counter
    import heapq

    # Calculate frequencies of characters
    frequency = Counter(input_str)

    # Build a priority queue (min-heap) of nodes
    heap = [[weight, [symbol, ""]] for symbol, weight in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    huffman_dict = sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
    code_dict = {symbol: code for symbol, code in huffman_dict}

    # Encode the input string
    encoded_str = ''.join(code_dict[char] for char in input_str)

    # Calculate average length of encoded character
    average_length = sum(len(code_dict[char]) * (frequency[char] / len(input_str)) for char in frequency)

    # Verify McMillan's inequality
    mcmillans_inequality = sum(1 / (2 ** len(code)) for code in code_dict.values())

    print('The average length of an encoded character:', round(average_length, 1))
    if mcmillans_inequality <= 1:
        print("McMillan's inequality holds and is equal to", round(mcmillans_inequality, 1))
    else:
        print('McMillan’s inequality does not hold')

    return encoded_str, code_dict

def decode(encoded_str, code_dict):
    """
    Decodes a Huffman encoded string using the provided code dictionary.

    Args:
    - encoded_str (str): The Huffman encoded string.
    - code_dict (dict): The dictionary mapping characters to their Huffman codes.

    Returns:
    - str: The decoded string.
    """
    reverse_code_dict = {code: char for char, code in code_dict.items()}
    current_code = ''
    decoded_str = ''

    for bit in encoded_str:
        current_code += bit
        if current_code in reverse_code_dict:
            decoded_str += reverse_code_dict[current_code]
            current_code = ''

    return decoded_str

# Example usage
encoded_str, code_dict = encode_huffman('Three hundred and forty-eight years, six months, and nineteen days ago to-day, the Parisians awoke to the sound of all the bells in the triple circuit of the city, the university, and the town ringing a full peal.')
print('\nDecoded string:', decode(encoded_str, code_dict))
