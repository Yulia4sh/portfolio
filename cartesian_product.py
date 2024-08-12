"""
This function generates the Cartesian product of the set {0, 1} with itself n times, 
creating all possible binary strings of length n. Unlike the typical methods that use 
libraries like itertools or recursive backtracking for more generalized Cartesian products, 
this implementation leverages a specific pattern: it alternates between adding '1' and '0' 
to the beginning of the existing strings in a recursive manner. This approach capitalizes on 
the observation that each step can build upon the previous step's results by simply appending 
the new digits in a controlled pattern.
"""


def cartesian_product(n):
    # Base case: if n is 0, return a list with an empty string
    if n == 0:
        return ['']
    
    # Recursive call to generate strings of length n-1
    state = cartesian_product(n-1)
    
    # Initialize an empty list to store the results
    s = []
    
    # For each string obtained in the previous step,
    # prepend '1' and '0' in an alternating pattern and add them to the list
    for i in state:
        s.append('1' + i)
        s.append('0' + i)
    
    # Return the list with all possible binary strings of length n
    return s

# Example function call: generate all possible binary strings of length 3
print(cartesian_product(3))
