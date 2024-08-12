"""
Use NumPy methods to create and manipulate arrays of random integers, sort by a specific column, identify and handle
zero rows and columns, adjust rows by subtracting their means, print rows with unique elements, and modify the array by
inserting zeros. Generate a matrix of random points, compute their polar coordinates, and apply a coordinate rotation.
Work with a 3D array by changing the sign of certain elements and calculating Shannon entropy. Create boundary arrays
with ones on the edges and zeros inside, compute distances from points to lines, and process arrays to find distances
between points. Identify rows in one array that contain elements from each row of another array, and convert integers
to their binary matrix representation. Visualize a system of point charges by displaying their magnitudes with color,
plotting scalar potential surfaces and level lines, and showing the gradient of the potential in both 3D and 2D. Animate
the motion of a charged body in the field from the previous step using Newton's laws and iterative methods to determine
the trajectory.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. All tasks in this exercise should be completed using only NumPy methods

# a) Create an array of size N x M filled with random integers
N = 3
M = 3
matrix = np.random.randint(0, 3, size=(N, M))

# i) Sort the array by the k-th column
k = 1
sorted_matrix = matrix[matrix[:, k].argsort()]
print(matrix)
print(sorted_matrix)

# ii) Determine if there are any zero columns or rows
zero_columns = np.any(np.all(matrix == 0, axis=0))
zero_rows = np.any(np.all(matrix == 0, axis=1))

# iii) Subtract the mean of each row from every element in that row
mean_subtracted_matrix = matrix - np.mean(matrix, axis=1, keepdims=True)

# iv) Print rows where all elements are unique
unique_rows = []
for row in matrix:
    if len(np.unique(row)) == len(row):
        unique_rows.append(row)
unique_rows = np.array(unique_rows)

# v) Insert two zeros after each element in each row of the original matrix
array_with_zeros = np.zeros((matrix.shape[0], matrix.shape[1] * 3), dtype=matrix.dtype)
array_with_zeros[:, ::3] = matrix[:, ::1]

# b) Create a matrix of shape (10,2) with random numbers representing point coordinates
matrix = np.random.randint(-100, 100, size=(10, 2))

# i) Find the matrix with the polar coordinates of these points
r = np.sqrt(matrix[:, 0]**2 + matrix[:, 1]**2)
theta = np.arctan2(matrix[:, 1], matrix[:, 0])
polar_coordinates = np.column_stack((r, theta))

# ii) Find the matrix with the coordinates of these points in a different coordinate system
# rotated relative to the original by an angle alpha counterclockwise.
alpha = np.pi / 2
rotation_matrix = np.array([[np.cos(alpha), -np.sin(alpha)], [np.sin(alpha), np.cos(alpha)]])
rotated_matrix = np.dot(matrix, rotation_matrix)

# c) Create a 3D array of shape (5,3,2) containing 30 elements (random numbers from 0 to 9).
matrix = np.random.randint(0, 10, size=(5, 3, 2))

# i) Change the sign of all elements in the array that are in the range from 3 to 7 (in place)
matrix[(matrix >= 3) & (matrix <= 7)] *= -1

# ii) Calculate the Shannon entropy for this array using the formula $S = \sum\limits_i p_i\ln(p_i)$,
# where $p_i$ is the frequency of the i-th symbol
hist, _ = np.histogram(matrix, bins=range(11))
prob = hist / hist.sum()
entropy = -np.sum(prob[np.nonzero(prob)] * np.log(prob[np.nonzero(prob)]))

# d) Create 2D and 3D arrays (with at least 100 elements) with 1s on the boundary and 0s inside
matrix_2d = np.ones((101, 101))
matrix_2d[1:-1, 1:-1] = 0
matrix_3d = np.ones((5, 101, 101))
matrix_3d[1:-1, 1:-1, 1:-1] = 0

# e) Given a set of N pairs of points (P0, P1) that define lines on a plane and a set of M points P.
# Compute the distance of each point (P[j]) to each line (P0[i], P1[i])
N = np.random.randint(1, 10)
M = np.random.randint(1, 10)
# print(f'N: {N}, M:: {M}')
P0 = np.random.randint(0, 10, size=(N, 2))
P1 = np.random.randint(0, 10, size=(N, 2))
P = np.random.randint(0, 10, size=(M, 2))
for j in range(N):
    numerator = np.abs((P1[j][1] - P0[j][1]) * P[:, 0] - (P1[j][0] - P0[j][0]) * P[:, 1] + P1[j][0] * P0[j][1]
                       - P1[j][1] * P0[j][0])
    denominator = np.linalg.norm(P1[j] - P0[j])
    if denominator == 0:
        distance = 'nan'
    else:
        distance = numerator / denominator
    # for i in range(M):
    #     print(f'distance from ({P0[j]}, {P1[j]}) to {P[i]}: {distance[i]}')

# f) Given a one-dimensional array Z (with at least 10 elements). Construct a two-dimensional array where the first row equals
# (Z[0], Z[1], Z[2]), and each subsequent row is shifted by 1 (the last row should be (Z[-3], Z[-2], Z[-1]))
Z = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
n = len(Z) - 2
result_1 = np.lib.stride_tricks.as_strided(Z, shape=(n, 3), strides=(Z.itemsize, Z.itemsize))

# g) For two arrays X and Y, build a Cauchy matrix $C (C_{ij} = 1 / (x_i — y_j))$
N = np.random.randint(1, 10)
M = np.random.randint(1, 10)
X = np.random.randint(0, 10, N)
Y = np.random.randint(0, 10, M)
C = 1 / (X[:, np.newaxis] - Y)

# j) Create a matrix of shape (5,3) with random numbers representing point coordinates. Find distances between all
# points (the result should be a 5x5 matrix where the element with index (i, j) is the distance between the i-th and j-th points).
points = np.random.rand(5, 3)
diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
distances = np.sqrt(np.sum(diff ** 2, axis=-1))

# k) Given two arrays A and B of shapes (8,3) and (2,2). Find rows in A that contain elements from each row of B regardless
# of the order of elements in B
A = np.random.randint(0, 10, size=(8, 3))
B = np.random.randint(0, 10, size=(2, 2))
contains_elements = np.logical_or.reduce(np.isin(A, B[0]), axis=1) & np.logical_or.reduce(np.isin(A, B[1]), axis=1)
selected_rows_A = A[contains_elements]
# print("Array A:")
# print(A)
# print("\nArray B:")
# print(B)
# print("\nResult:")
# print(selected_rows_A)

# l) Convert a vector of positive integers to its matrix binary representation.
numbers = np.array([0, 1, 8])
max_bits = int(np.ceil(np.log2(np.max(numbers)) + 1))
binary_repr = np.array([list(np.binary_repr(num, width=max_bits)) for num in numbers], dtype=int)

# 2. User provides a list of coordinates (x, y, z) and charge values (q) of point charges
# a) Visualize the charges, choosing colors to represent the magnitude of the charge
positions = np.array([[-8, -8, 0], [8, 8, 0]])
q = np.array([1, 5])
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
colors = np.sign(q) * np.log(np.abs(q) + 1)
norm = plt.Normalize(colors.min(), colors.max())
cmap = plt.get_cmap('coolwarm')
sc = ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], c=cmap(norm(colors)), s=100)
plt.colorbar(sc)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.title('Point Charge Visualization')
plt.show()

# a) Visualize the level surfaces of the scalar potential of this charge system;
def scalar_potential(coordinates, charges, point):
    k = 8.9875517923e9
    potential = 0
    for i in range(len(coordinates)):
        r_vector = coordinates[i] - point
        r = np.linalg.norm(r_vector)
        potential += k * charges[i] / r
    return potential

x = np.linspace(-30, 30, 20)
y = np.linspace(-30, 30, 20)
z = np.linspace(-30, 30, 20)
X, Y, Z = np.meshgrid(x, y, z)
potential_values = np.zeros_like(X)
for i in range(len(x)):
    for j in range(len(y)):
        for k in range(len(z)):
            point = np.array([X[i, j, k], Y[i, j, k], Z[i, j, k]])
            potential_values[i, j, k] = scalar_potential(positions, q, point)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
contour = ax.contour3D(X, Y, Z, potential_values, 50, cmap='viridis')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.title('Scalar Potential Level Surfaces')
plt.colorbar(contour)
plt.show()

# b) Animate the motion of point charges in a box with random velocity
def update(num, positions, velocities, scatter):
    positions += velocities
    scatter._offsets3d = (positions[:, 0], positions[:, 1], positions[:, 2])
    return scatter,

positions = np.array([[-8, -8, 0], [8, 8, 0]])
velocities = np.random.uniform(-1, 1, size=(2, 3))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], s=100)
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)
ani = FuncAnimation(fig, update, frames=100, fargs=(positions, velocities, scatter))
plt.show()
