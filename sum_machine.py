"""
Task:
Create a finite automaton that takes two binary numbers as input and returns their sum. The automaton should handle binary addition and carry-over correctly. The provided implementation should be able to handle binary numbers of different lengths.

The function `sum_machine` performs the following steps:
1. Defines the finite automaton's state transition and output functions.
2. Reverses the input binary numbers to facilitate addition from the least significant bit.
3. Iterates through each bit of the input numbers, calculates the sum and carry, and updates the state accordingly.
4. Handles the case where the binary numbers have different lengths by padding with zeros.
5. Appends the result of each bit addition to the final result string.
6. Reverses the result string to return the final sum in the correct order.

Function Signature:
    def sum_machine(n_1: str, n_2: str) -> str:
        pass
"""

def sum_machine(n_1, n_2):
    # Finite automaton transition function
    f = {
        ('S0', '00'): 'S0', ('S0', '01'): 'S0', ('S0', '10'): 'S0', ('S0', '11'): 'S1',
        ('S1', '00'): 'S0', ('S1', '01'): 'S1', ('S1', '10'): 'S1', ('S1', '11'): 'S1'
    }

    # Finite automaton output function
    g = {
        ('S0', '00'): 0, ('S0', '01'): 1, ('S0', '10'): 1, ('S0', '11'): 0,
        ('S1', '00'): 1, ('S1', '01'): 0, ('S1', '10'): 0, ('S1', '11'): 1
    }

    # Initial state
    stan = 'S0'

    # Reverse the input binary numbers for addition from the least significant bit
    n_1 = n_1[::-1]
    n_2 = n_2[::-1]

    result = ''

    # Perform binary addition
    for i in range(max(len(n_1), len(n_2))):
        try:
            # Calculate value and update state
            value = g[(stan, n_1[i] + n_2[i])]
            stan = f[(stan, n_1[i] + n_2[i])]
        except IndexError:
            # Handle cases where input numbers have different lengths
            if len(n_1) < len(n_2):
                value = g[(stan, '0' + n_2[i])]
                stan = f[(stan, '0' + n_2[i])]
            if len(n_1) > len(n_2):
                value = g[(stan, n_1[i] + '0')]
                stan = f[(stan, n_1[i] + '0')]

        # Append the result of the current bit addition
        result += str(value)

    # Handle the final carry if necessary
    while stan == 'S1' and value == 0:
        try:
            value = g[(stan, n_1[i] + n_2[i])]
            stan = f[(stan, n_1[i] + n_2[i])]
        except IndexError:
            if len(n_1) < len(n_2):
                value = g[(stan, '0' + n_2[i])]
                stan = f[(stan, '0' + n_2[i])]
            if len(n_1) > len(n_2):
                value = g[(stan, n_1[i] + '0')]
                stan = f[(stan, n_1[i] + '0')]
            if i >= len(n_1) or i >= len(n_2):
                value = g[(stan, '0' + '0')]
                stan = f[(stan, '0' + '0')]
        i += 1
        result += str(value)

    # Return the final result in the correct order
    return result[::-1]

# Example usage
print('Sum of numbers in binary system:', sum_machine(input('Enter first binary number: '), input('Enter second binary number: ')))
