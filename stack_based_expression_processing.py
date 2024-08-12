# Task 1: Write a function that uses a stack to check if parentheses in an arithmetic expression are correctly matched and properly nested.
# Task 2: Write a function that converts an infix expression to postfix notation using a stack and then calculates its value.

def append_it(x, y):
    # Adds an element to the stack
    x.append(y)
    return x

def pop_it(x):
    # Removes the top element from the stack
    x.pop()
    return x

def steck(s):
    # Function to check if the parentheses in the string are correctly matched and nested
    d = []
    for i in s:
        if i == '(':
            d = append_it(d, '(')
        if i == ')':
            if len(d) == 0:
                return 0  # If a closing parenthesis is found without a matching opening parenthesis, it's incorrect
            else:
                d = pop_it(d)
    if len(d) == 0:  # If the stack is empty, parentheses are correctly matched and nested
        return 1
    else:
        return 0

s = ')( )('
if steck(s) == 0:
    print('no good')
else:
    print('very good')

def transformation(x):
    # Function to convert an infix expression to postfix notation
    d = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 4}  # Dictionary for operator precedence
    x = list(x)
    stack = []
    result = []
    for i in x:
        if i not in {'+', '-', '*', '/', '(', ')', '^'}:
            result.append(i)  # Append operands to result
        elif i == '(':
            stack.append(i)  # Push opening parenthesis onto the stack
        elif i == ')':
            while stack and stack[-1] != '(':  # Pop operators until an opening parenthesis is found
                result.append(stack.pop())
            stack.pop()  # Remove the opening parenthesis
        else:  # If the current symbol is an operator
            while stack and stack[-1] != '(' and d[stack[-1]] >= d[i]:
                result.append(stack.pop())  # Pop operators with higher or equal precedence
            stack.append(i)  # Push the current operator onto the stack
    while stack:
        result.append(stack.pop())  # Pop remaining operators from the stack
    return result

s = '(1+2)*(2+3)'
result = transformation(s)
print('Postfix notation of an arithmetic expression: ', s, ' = ', ''.join(result))

def calculation(x):
    # Function to calculate the value of a postfix expression
    stack = []
    for i in x:
        if i == '+':
            stack.append(stack.pop() + stack.pop())  # Add the last two values
        elif i == '-':
            stack.append(stack.pop(-2) - stack.pop())  # Subtract the last two values
        elif i == '*':
            stack.append(stack.pop() * stack.pop())  # Multiply the last two values
        elif i == '/':
            divisor = stack.pop()
            stack.append(stack.pop() / divisor)  # Divide the last two values
        elif i == '^':
            exponent = stack.pop()
            stack.append(stack.pop() ** exponent)  # Raise the second last value to the power of the last value
        else:
            stack.append(int(i))  # Push numbers onto the stack
    return stack.pop()

print('Calculated value: ', calculation(result))
