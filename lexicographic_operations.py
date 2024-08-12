# 1. Write a function that takes an arbitrary permutation of a set in the form of a string,
#    along with a natural number n, and returns the next n lexicographically ordered permutations as a list of strings.
# 2. Write a function that takes an arbitrary combination of a set in the form of a string,
#    the number of elements in the set from which the combinations are constructed,
#    along with a natural number n, and returns the next n lexicographically ordered combinations as a list of strings.
# 3. Write a function that takes a set in the form of a list and prints all partitions of this set,
#    where each partition is a list of lists.
# 4*. Implement tasks 1 and 2, but the functions should return the previous lexicographically ordered permutations or combinations instead of the next ones.
# 5*. Implement task 3 using a recursive approach.

def permutations(s, n):
    result = []
    j = len(s) - 1
    result.append(s)
    for i in range(n):
        local_result = ''
        while True:
            if j == -1:
                break
            # If the previous character is smaller, swap it with the current one to get the next permutation
            elif s[j - 1] < s[j]:
                try:
                    local_result += s[:j - 1] + s[j] + s[j - 1] + s[j + 1:]
                except IndexError:
                    local_result += s[:j - 1] + s[j] + s[j - 1]
                s = local_result
                j = len(s) - 1
                result.append(local_result)
            else:
                local_result += s
                j -= 1
                s = local_result
            break
    return result

print('lexicographically ordered permutations:')
print(permutations('123', 5), '\n')


def combination(s, n, m):
    result = []
    i = len(s)
    index = len(s) - 1
    result.append(s)
    for j in range(m):
        while True:
            local_result = ''
            if index == -1:
                break
            # If the current digit is not the largest possible, increase it to get the next combination
            elif int(s[index]) != (n - len(s) + i):
                local_result += s[:index] + str(int(s[index]) + 1)
                # Adjust the remaining digits if needed
                if index != len(s) - 1:
                    for k in range(index, len(s) - 1):
                        local_result += str(int(local_result[k]) + 1)
                i = len(s)
                index = len(s) - 1
                result.append(local_result)
                s = local_result
                break
            else:
                index -= 1
                i -= 1
    return result

print('lexicographically ordered combinations:')
print(combination('1356', 6, 20), '\n')


def breakdown(set_for_breakdown):
    stack = []
    stack_2 = []
    for i in set_for_breakdown:
        if len(stack) == 0:
            stack.append([[i]])
        else:
            for _ in range(len(stack)):
                el = stack.pop()
                local_result = []
                for j in range(len(el)):
                    local_result.append(el[j])
                local_result.append([i])
                stack_2.append(local_result)
                for j in range(len(el)):
                    local_result = []
                    for k in range(len(el)):
                        if j == k:
                            if type(el[k]) is list:
                                not_local_result = []
                                for m in el[k]:
                                    not_local_result.append(m)
                                not_local_result.append(i)
                                local_result.append(not_local_result)
                            else:
                                local_result.append([el[k], i])
                        else:
                            local_result.append(el[k])
                    stack_2.append(local_result)
            stack = stack_2.copy()
            stack_2 = []
    return stack

print('all partitions of the set [1, 2, 3]:')
result = breakdown([1, 2, 3])
for i in result:
    print(i)


def permutations_star(s, n):
    result = []
    j = len(s) - 1
    result.append(s)
    for i in range(n):
        local_result = ''
        while True:
            if j == -1:
                break
            # If the previous character is larger, swap it with the current one to get the previous permutation
            elif s[j - 1] > s[j]:
                try:
                    local_result += s[:j - 1] + s[j] + s[j - 1] + s[j + 1:]
                except IndexError:
                    local_result += s[:j - 1] + s[j] + s[j - 1]
                s = local_result
                j = len(s) - 1
                result.append(local_result)
            else:
                local_result += s
                j -= 1
                s = local_result
            break
    return result

print('\n* lexicographically ordered preliminary permutations:')
print(permutations_star('321', 5), '\n')


def combination_star(s, n, m):
    result = []
    i = 1
    index = 0
    result.append(s)
    for j in range(m):
        while True:
            local_result = ''
            if index == len(s):
                break
            # If the current digit is not the smallest possible, decrease it to get the previous combination
            elif int(s[index]) != (n - i + 1):
                local_result += s[:index] + str(int(s[index]) + 1)
                # Adjust the remaining digits if needed
                if index != len(s) - 1:
                    for k in range(index, len(s) - 1):
                        local_result += str(int(local_result[k]) - 1)
                i = 1
                index = 0
                result.append(local_result)
                s = local_result
                break
            else:
                index += 1
                i += 1
    return result

print('* lexicographically ordered preliminary combinations:')
print(combination_star('3456', 6, 20), '\n')


def breakdown_star(set_for_breakdown, index=0, result=[]):
    # Recursive function to generate all partitions of the set
    if index == len(set_for_breakdown):
        print(result)
        return
    for i in result:
        i.append(set_for_breakdown[index])
        breakdown_star(set_for_breakdown, index + 1, result)
        i.pop()
    result.append([set_for_breakdown[index]])
    breakdown_star(set_for_breakdown, index + 1, result)
    result.pop()

print('* all partitions of the set [1, 2, 3]:')
breakdown_star([1, 2, 3])
