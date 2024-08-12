import random

# ============================================
# Task 1: Functions for handling relations
# ============================================

# Function to generate a random relation between sets A and B
# of a specified length.
def generation_random_relation(A, B, length):
    """
    Generate a random relation between sets A and B of a specified length.
    """
    result = []
    for _ in range(length):
        result.append((random.choice(A), random.choice(B)))
    return result

# Function to represent a relation as a binary matrix.
def create_matrix(A, B, relation):
    """
    Represent a relation as a binary matrix.
    """
    matrix = [[0]*len(B) for _ in range(len(A))]
    for (a, b) in relation:
        row = A.index(a)
        column = B.index(b)
        matrix[row][column] = 1
    return matrix

# Function to check if the relation is reflexive.
def reflexive(A, B, relation):
    """
    Check if the relation is reflexive.
    """
    for i in A:
        if (i, i) not in relation:
            return False
    for i in B:
        if (i, i) not in relation:
            return False
    return True

# Function to check if the relation is irreflexive.
def ireflexive(A, B, relation):
    """
    Check if the relation is irreflexive.
    """
    for i in A:
        if (i, i) in relation:
            return False
    for i in B:
        if (i, i) in relation:
            return False
    return True

# Function to check if the relation is symmetric.
def symmetric(relation):
    """
    Check if the relation is symmetric.
    """
    for (a, b) in relation:
        if (b, a) not in relation:
            return False
    return True

# Function to check if the relation is antisymmetric.
def antisymmetric(relation):
    """
    Check if the relation is antisymmetric.
    """
    for (a, b) in relation:
        if (b, a) in relation and a != b:
            return False
    return True

# Function to check if the relation is asymmetric.
def asymmetric(relation):
    """
    Check if the relation is asymmetric.
    """
    for (a, b) in relation:
        if (b, a) in relation:
            return False
    return True

# Function to check if the relation is transitive.
def transitive(relation):
    """
    Check if the relation is transitive.
    """
    for (a, b) in relation:
        for (c, d) in relation:
            if b == c and (a, d) not in relation:
                return False
    return True

# ============================================
# Task 2: Functions for cities and roads
# ============================================

# Function to find pairs of cities from sets A and C that are connected
# via set B, and determine the minimum distance in roads to connect them.
def find_city_connections(aRb, bRc):
    """
    Find pairs of cities from sets A and C that are connected via set B.
    """
    aRc = []
    r = []
    count = {}
    for (a, b) in aRb:
        for (c, d) in bRc:
            if b == c and (a, d) not in count:
                count[(a, d)] = 1
            elif b == c:
                count[(a, d)] += 1
            if b == c and (a, d) not in r:
                print(f'From: {a} to {d} - min distance 2 roads')
                aRc.append((a, b, d))
                r.append((a, d))
    for (a, b) in aRb:
        for (c, d) in bRc:
            if b != c:
                for (e, f) in aRc:
                    if c == e and d == f and (a, f) in aRb and (a, d) not in r:
                        if (a, d) not in count:
                            count[(a, d)] = 1
                        else:
                            count[(a, d)] += 1
                        print(f'From: {a} to {d} - min distance 4 roads')
    print('\nPossible number of connection paths:')
    for (a, d) in count:
        print(f'From {a} to {d} - {count[(a, d)]} connection paths')

# ============================================
# Task 3: Functions for family relations
# ============================================

# Function to find and print pairs of full siblings and half-siblings
# from the parent-child relation.
def native_bro(aRb):
    """
    Find and print pairs of full siblings and half-siblings from the parent-child relation.
    """
    dict_parents = {}
    for i in range(len(aRb)):
        for j in range(i + 1, len(aRb)):
            if aRb[i][1] == aRb[j][1]:
                if (aRb[i][0], aRb[j][0]) not in dict_parents:
                    dict_parents[(aRb[i][0], aRb[j][0])] = [aRb[i][1]]
                else:
                    dict_parents[(aRb[i][0], aRb[j][0])].append(aRb[i][1])
    print('\nNative brothers:')
    for pair in dict_parents:
        if len(dict_parents[pair]) >= 2:
            print(pair, dict_parents[pair])

    print('\nHalf-brothers:')
    lst = list(dict_parents.keys())
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i][0] == lst[j][0] or lst[i][0] == lst[j][1]:
                print(dict_parents[lst[i]] + dict_parents[lst[j]])
            elif lst[i][1] == lst[j][0] or lst[i][1] == lst[j][1]:
                print(dict_parents[lst[i]] + dict_parents[lst[j]])

# Example usage

# Task 1
A = [1, 2, 3, 4]
B = [1, 2, 3, 4]
relation = generation_random_relation(A, B, 5)
print("Generated Relation:", relation, '\n')
for row in create_matrix(A, B, relation):
    print(row)
print('\nReflexive:', reflexive(A, B, relation))
print('Irreflexive:', ireflexive(A, B, relation))
print('Symmetric:', symmetric(relation))
print('Antisymmetric:', antisymmetric(relation))
print('Asymmetric:', asymmetric(relation))
print('Transitive:', transitive(relation), '\n')

# Task 2
A = ['city1', 'city2', 'city3']
B = ['city4', 'city5']
C = ['city6', 'city7']
aRb = [('city1', 'city4'), ('city1', 'city5'), ('city2', 'city5'), ('city3', 'city4')]
bRc = [('city4', 'city6'), ('city4', 'city7'), ('city5', 'city7')]
find_city_connections(aRb, bRc)

# Task 3
people = ['Bob', 'Alice', 'Ivan', 'Anna', 'Maria', 'Charles', 'Ruslan', 'Diana', 'Mia', 'Sara', 'Ben', 'Ron']
parents_R_children = [('Bob', 'Alice'), ('Anna', 'Alice'), ('Bob', 'Ruslan'), ('Maria', 'Ruslan'),
                      ('Bob', 'Ivan'), ('Anna', 'Ivan'), ('Charles', 'Mia'), ('Diana', 'Mia'),
                      ('Charles', 'Sara'), ('Diana', 'Sara'), ('Diana', 'Ben'), ('Ron', 'Ben')]
native_bro(parents_R_children)
