"""
Laboratory Work 1

1. Using Object-Oriented Programming (OOP) principles, create a vector-matrix calculator. The calculator should contain the `VMCalculator` class, which will accept arithmetic expressions and include methods for evaluating these expressions and outputting results as objects of the corresponding class (vector, matrix, number). The arithmetic expressions can consist of matrices, vectors, and numbers, along with the operations permissible between them (arithmetic operations, dot and cross products of vectors, matrix-vector multiplication, matrix operations, determinant calculation, etc.). It is advisable to define classes for matrices and vectors, overriding arithmetic operations accordingly. For example, the vector cross product can be implemented via overriding the multiplication operation, and the dot product via another operation like "%". Implement methods to check the validity of arithmetic expressions and the correctness of data for creating matrix or vector objects.

2. Using the results from task 1, create a class that models the motion of a projectile launched at an angle to the horizon, accounting for non-inertial forces and air resistance (assume air resistance is proportional to velocity). The class should include:
   a) A method that takes initial parameters of the projectile (initial velocity: direction and magnitude), geographic parameters of the launch point (longitude, latitude, height), and environmental parameters (gravitational acceleration, air resistance coefficient) and returns the geographic coordinates and time of impact with the Earth's surface (considering the Earth as flat for this scale).
   b) A method that takes geographic parameters of the launch and impact points and environmental parameters to return the initial parameters of the projectile.
   c) A method to graphically display the projectile's trajectory using matplotlib.

3. Using wxPython, develop an application that provides an interface for implementing tasks 1 and 2. Design the application according to your preferences.

Laboratory Work 2

1. Create a class `VMKCalculator` that extends the functionality of the `VMCalculator` class from Laboratory Work 1. This new class should support quaternion operations, including:
   - Multiplication of a quaternion by a scalar, vector, or another quaternion
   - Finding the inverse of a quaternion

2. Model and visualize the motion of a charged particle in perpendicular electric and magnetic fields using matplotlib. Users should input:
   - The direction and magnitude of the electric field (E)
   - The magnetic field induction (B)
   - The charge, direction, and magnitude of the particle's velocity

   Implement two approaches for simulating the particle's rotation around the magnetic field vector:
   a) Rodrigues' rotation formula
   b) Quaternion formalism

3. Extend the functionality of your application from Laboratory Work 1 to include an interface for tasks 1 and 2. This should enable users to interact with both quaternion calculations and particle motion simulations through a unified application interface, incorporating user input and visualization capabilities.
"""

import wx
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve
import math


class Check:

    def __init__(self, mul_obj):
        self.mul_obj = mul_obj

    def check(self):

        if type(self.mul_obj) == Vector:
            return 'vector'

        elif type(self.mul_obj) == Matrix:
            return 'matrix'

        elif type(self.mul_obj) == Scalar:
            return 'scalar'

        elif type(self.mul_obj) == Quaternion:
            return 'quaternion'


class Scalar:

    def __init__(self, scalar):
        self.scalar = scalar

    def __mul__(self, mul_obj):
        for_return = []

        if Check(mul_obj).check() == 'vector':
            for i in mul_obj:
                for_return.append(self.scalar * i)
            return Vector(for_return)

        elif Check(mul_obj).check() == 'matrix':
            for i in mul_obj:
                row = []
                for j in i:
                    row.append(self.scalar * j)
                for_return.append(row)
            return Matrix(for_return)

        elif Check(mul_obj).check() == 'scalar':
            return Scalar(self.scalar * mul_obj.scalar)

        elif Check(mul_obj).check() == 'quaternion':
            return Quaternion(self.scalar * mul_obj.scalar, [self.scalar * i for i in mul_obj.vector[:]])

    def __truediv__(self, div_obj):
        for_return = []

        if Check(div_obj).check() == 'vector':
            for i in div_obj:
                for_return.append(self.scalar * (1 / i))
            return Vector(for_return)

        elif Check(div_obj).check() == 'matrix':
            for i in div_obj:
                row = []
                for j in i:
                    row.append(self.scalar * (1 / j))
                for_return.append(row)
            return Matrix(for_return)

        elif Check(div_obj).check() == 'scalar':
            return Scalar(self.scalar * (1 / div_obj.scalar))

        elif Check(div_obj).check() == 'quaternion':
            return SyntaxError('Not today')

    def __add__(self, add_obj):

        if Check(add_obj).check() == 'vector':
            return SyntaxError('Vector and scalar, really?')

        elif Check(add_obj).check() == 'matrix':
            for_return = []
            for i in range(len(add_obj)):
                row = []
                for j in range(len(add_obj[i])):
                    if i == j:
                        row.append(self.scalar + add_obj[i][j])
                    else:
                        row.append(add_obj[i][j])
                for_return.append(row)
            return Matrix(for_return)

        elif Check(add_obj).check() == 'scalar':
            return Scalar(self.scalar + add_obj.scalar)

        elif Check(add_obj).check() == 'quaternion':
            return Quaternion(self.scalar + add_obj.scalar, add_obj.vector[:])

    def __sub__(self, sub_obj):

        if Check(sub_obj).check() == 'vector':
            return SyntaxError('Vector and scalar, really?')

        elif Check(sub_obj).check() == 'matrix':
            for_return = []
            for i in range(len(sub_obj)):
                row = []
                for j in range(len(sub_obj[i])):
                    if i == j:
                        row.append(self.scalar - sub_obj[i][j])
                    else:
                        row.append(sub_obj[i][j])
                for_return.append(row)
            return Matrix(for_return)

        elif Check(sub_obj).check() == 'scalar':
            return Scalar(self.scalar - sub_obj.scalar)

        elif Check(sub_obj).check() == 'quaternion':
            return Quaternion(self.scalar - sub_obj.scalar, [-i for i in sub_obj.vector[:]])

    def __mod__(self, mod_obj):
        if type(mod_obj) == int:
            return self.scalar % mod_obj
        return SyntaxError('Vector product, really?')

    def __pow__(self, pow_obj):

        if Check(pow_obj).check() == 'vector':
            return SyntaxError('Vector pow, really?')

        elif Check(pow_obj).check() == 'matrix':
            if self.scalar == np.e:
                return SyntaxError('I can but I don\'t want to')
            return SyntaxError('Matrix pow, really?')

        elif Check(pow_obj).check() == 'scalar':
            return Scalar(self.scalar ** pow_obj.scalar)

        elif Check(pow_obj).check() == 'quaternion':
            return SyntaxError('I think it is possible')

    def __str__(self):
        return str(self.scalar)

    def __getitem__(self):
        return self.scalar


class Vector:

    def __init__(self, lst: list):
        self.lst = lst
        self.vector = lst

    def __mul__(self, mul_obj):

        if Check(mul_obj).check() == 'vector':
            for_return = 0
            if len(mul_obj) == len(self.lst):
                for i in range(len(mul_obj)):
                    for_return += self.lst[i] * mul_obj[i]
                return Scalar(for_return)
            else:
                return SyntaxError('Not today')

        elif Check(mul_obj).check() == 'matrix':
            if len(mul_obj) == len(self.lst):
                lst_for_mul = [self.lst[:]]
                return Matrix(lst_for_mul) * mul_obj
            return SyntaxError('Not today')

        elif Check(mul_obj).check() == 'scalar':
            for_return = []
            for i in self.vector:
                for_return.append(mul_obj.scalar * i)
            return Vector(for_return)

        elif Check(mul_obj).check() == 'quaternion' and len(self.lst) == len(mul_obj.vector):
            return Quaternion((Scalar(-1) * (Vector(self.lst)*Vector(mul_obj.vector))).scalar,
                              (Vector(self.lst) % Vector(mul_obj.vector)).lst)

    def __truediv__(self, div_obj):
        if Check(div_obj).check() == 'vector':
            return SyntaxError('Not today')

        elif Check(div_obj).check() == 'matrix':
            return SyntaxError('Not today')

        elif Check(div_obj).check() == 'scalar':
            for_return = []
            for i in self.lst:
                for_return.append(i / div_obj.scalar)
            return Vector(for_return)

        elif Check(div_obj).check() == 'quaternion' and len(self.lst) == len(div_obj.vector):
            div = div_obj.inv_q()  # return lst
            return Quaternion((Scalar(-1) * (Vector(self.lst)*Vector(div))).scalar,
                              (Vector(self.lst) % Vector(div)).lst)

    def __add__(self, add_obj):

        if Check(add_obj).check() == 'vector':
            if len(add_obj) == len(self.lst):
                for_return = []
                for i in range(len(add_obj)):
                    for_return.append(add_obj.lst[i] + self.lst[i])
                return Vector(for_return)
            return SyntaxError('Not today')

        elif Check(add_obj).check() == 'matrix':
            return SyntaxError('Not today')

        elif Check(add_obj).check() == 'scalar':
            return SyntaxError('Not today')

        elif Check(add_obj).check() == 'quaternion' and len(self.lst) == len(add_obj.vector):
            return Quaternion(add_obj.scalar, (Vector(self.lst) + Vector(add_obj.vector)).vector)

    def __sub__(self, sub_obj):

        if Check(sub_obj).check() == 'vector':
            if len(sub_obj) == len(self.lst):
                for_return = []
                for i in range(len(sub_obj)):
                    for_return.append(self.lst[i] - sub_obj[i])
                return Vector(for_return)
            return SyntaxError('Not today')

        elif Check(sub_obj).check() == 'matrix':
            return SyntaxError('Not today')

        elif Check(sub_obj).check() == 'scalar':
            return SyntaxError('Not today')

        elif Check(sub_obj).check() == 'quaternion' and len(self.lst) == len(sub_obj.vector):
            return Quaternion(-sub_obj.scalar, (Vector(self.lst) - Vector(sub_obj.vector)).vector)

    def __mod__(self, mod_obj):
        if Check(mod_obj).check() == 'vector' and len(self.vector) == 3 and len(mod_obj.vector) == 3:
            return Vector((np.cross(self.np_arr(), mod_obj.np_arr())).tolist())
        elif Check(mod_obj).check() == 'quaternion':
            return SyntaxError('Not today')
        else:
            return SyntaxError('Not today')

    def __pow__(self, pow_obj):

        if Check(pow_obj).check() == 'vector':
            return SyntaxError('Not today')

        elif Check(pow_obj).check() == 'matrix':
            return SyntaxError('Not today')

        elif Check(pow_obj).check() == 'scalar':
            total = 0
            if pow_obj.__getitem__() == 1:
                return self.lst
            if pow_obj.__getitem__() == 0:
                return SyntaxError('I wonder what will happen')
            if pow_obj % 2 == 0:
                for_range1 = Vector(self.lst[:])
                for_range2 = Vector(self.lst[:])
                for i in range(pow_obj.__getitem__()-1):
                    total = for_range1 * for_range2
                    for_range1 = total
                return Scalar(total)
            elif Check(pow_obj).check() == 'quaternion':
                return SyntaxError('Not today')
            else:
                for_range1 = Vector(self.lst[:])
                for_range2 = Vector(self.lst[:])
                for i in range(pow_obj.__getitem__()-1):
                    total = for_range1 * for_range2
                    for_range1 = total
                return Vector(total)

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index < len(self.lst):
            x = self.lst[self.current_index]
            self.current_index += 1
            return x
        raise StopIteration

    def __str__(self):
        return str(self.lst)

    def __getitem__(self, index):
        return self.lst[index]

    def __len__(self):
        return len(self.lst)

    def np_arr(self):
        return np.array(self.lst)


class Matrix:

    def __init__(self, lst):
        self.lst = lst
        self.vector = lst

    def __mul__(self, mul_obj):

        if Check(mul_obj).check() == 'vector':
            if len(mul_obj) == len(self.lst):
                mul_obj_for_mul = mul_obj.to_matrix()
                return self.lst * mul_obj_for_mul
            return SyntaxError('Not today')

        elif Check(mul_obj).check() == 'matrix':
            if len(mul_obj) == len(self.lst) and len(mul_obj[0]) == len(self.lst[0]):
                return Matrix(np.matmul(self.np_arr(), mul_obj.np_arr()).tolist())
            return SyntaxError('Not today')

        elif Check(mul_obj).check() == 'scalar':
            for_return = []
            for i in self.lst:
                row = []
                for j in i:
                    row.append(mul_obj.scalar * j)
                for_return.append(row)
            return Matrix(for_return)

        elif Check(mul_obj).check() == 'quaternion' and len(self.lst) == 4:
            return Matrix(np.matmul(self.lst, mul_obj.matrix_form()).tolist())

    def __truediv__(self, div_obj):
        if Check(div_obj).check() == 'vector':
            return SyntaxError('Not today')

        elif Check(div_obj).check() == 'matrix':
            if (len(div_obj) == len(self.lst) and len(div_obj[0]) == len(self.lst[0])) \
                    and np.linalg.det(div_obj.np_arr()) != 0:
                return Matrix(np.matmul(self.lst.np_arr(), np.linalg.inv(div_obj.np_arr())).tolist())
            return SyntaxError('Not today')

        elif Check(div_obj).check() == 'scalar':
            for_return = []
            for i in self.lst:
                row = []
                for j in i:
                    row.append(div_obj.scalar * (1/j))
                for_return.append(row)
            return Matrix(for_return)

        elif Check(div_obj).check() == 'quaternion' and len(self.lst) == 4:
            return Matrix(np.matmul(self.lst, np.linalg.inv(div_obj.matrix_form())).tolist())

    def __add__(self, add_obj):

        if Check(add_obj).check() == 'vector':
            return SyntaxError('Not today')

        elif Check(add_obj).check() == 'matrix':
            if len(add_obj) == len(self.lst) and len(add_obj[0]) == len(self.lst[0]):
                return Matrix((self.lst.np_arr() + add_obj.np_arr()).tolist())
            return SyntaxError('Not today')

        elif Check(add_obj).check() == 'scalar':
            for_return = []
            for i in range(len(self.lst)):
                row = []
                for j in range(len(self.lst[i])):
                    if i == j:
                        row.append(add_obj.scalar + self.lst[i][j])
                    else:
                        row.append(self.lst[i][j])
                for_return.append(row)
            return Matrix(for_return)

        elif Check(add_obj).check() == 'quaternion' and len(self.lst) == 4:
            return Matrix((self.lst.np_arr() + np.array(add_obj.matrix_form())).tolist())

    def __sub__(self, sub_obj):

        if Check(sub_obj).check() == 'vector':
            return SyntaxError('Not today')

        elif Check(sub_obj).check() == 'matrix':
            if len(sub_obj) == len(self.lst) and len(sub_obj[0]) == len(self.lst[0]):
                return Matrix((self.lst.np_arr() - sub_obj.np_arr()).tolist())
            return SyntaxError('Not today')

        elif Check(sub_obj).check() == 'scalar':
            for_return = []
            for i in range(len(self.lst)):
                row = []
                for j in range(len(self.lst[i])):
                    if i == j:
                        row.append(self.lst[i][j] - sub_obj.scalar)
                    else:
                        row.append(self.lst[i][j])
                for_return.append(row)
            return Matrix(for_return)

        elif Check(sub_obj).check() == 'quaternion' and len(self.lst) == 4:
            return Matrix((self.lst.np_arr() - np.array(sub_obj.matrix_form())).tolist())

    def __mod__(self, mod_obj):
        return SyntaxError('Not today')

    def __pow__(self, pow_obj):

        if Check(pow_obj).check() == 'vector':
            return SyntaxError('Not today')

        elif Check(pow_obj).check() == 'matrix':
            return SyntaxError('Not today')

        elif Check(pow_obj).check() == 'scalar':
            total = 0
            if pow_obj.__getitem__() == 1:
                return self.lst
            if pow_obj.__getitem__() == 0:
                return SyntaxError('I wonder what will happen')
            for_range1 = Matrix(self.lst[:])
            for_range2 = Matrix(self.lst[:])
            for i in range(pow_obj.__getitem__()-1):
                total = for_range1 * for_range2
                for_range1 = total
            return Matrix(total)

        if Check(pow_obj).check() == 'quaternion':
            return SyntaxError('Not today')

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index < len(self.lst):
            x = self.lst[self.current_index]
            self.current_index += 1
            return x
        raise StopIteration

    def __str__(self):
        strs = ''
        for i in self.lst:
            strs += str(i) + '\n'
        return strs

    def __getitem__(self, index):
        return self.lst[index]

    def __len__(self):
        return len(self.lst)

    def np_arr(self):
        return np.array(self.lst)


class Quaternion:

    def __init__(self, scalar: int, vector: list):
        self.scalar = int(scalar)
        self.vector = list(vector)

    @property
    def scalar(self) -> int:
        return self.scalar

    @property
    def vector(self) -> list:
        return self.vector

    def __mul__(self, mul_obj):
        if Check(mul_obj).check() == 'scalar':
            return Quaternion(mul_obj.scalar * self.scalar, [mul_obj.scalar * i for i in self.vector[:]])

        elif Check(mul_obj).check() == 'vector' and len(self.vector) == len(mul_obj.vector):
            return Quaternion((Scalar(-1) * (Vector(self.vector) * mul_obj.vector)).scalar, (Vector(self.vector) %
                                                                                             mul_obj.vector).lst)

        elif Check(mul_obj).check() == 'matrix' and len(mul_obj.lst) == 4:
            return Matrix(np.matmul(self.matrix_form(), mul_obj).tolist())

        elif Check(mul_obj).check() == 'quaternion':
            return Quaternion(Scalar(self.scalar) * Scalar(mul_obj.scalar) - Vector(self.vector) *
                              Vector(mul_obj.vector),
                              Scalar(self.scalar) * Vector(mul_obj.vector) + Scalar(mul_obj.scalar) *
                              Vector(self.vector) + Vector(self.vector) % Vector(mul_obj.vector))

    def __truediv__(self, div_obj):
        if Check(div_obj).check() == 'scalar':
            return Quaternion(div_obj.scalar / self.scalar, [div_obj.scalar / i for i in self.vector[:]])

        elif Check(div_obj).check() == 'vector' and len(self.vector) == len(div_obj.vector):
            div = Quaternion(0, div_obj.vector).inv_q()
            return Quaternion((Scalar(-1) * (Vector(self.vector) * div)).scalar,
                              (Vector(self.vector) % Vector(div.vector)).lst)

        elif Check(div_obj).check() == 'matrix' and len(div_obj.lst) == 4:
            return Matrix(np.matmul((self.matrix_form()).np_arr(), np.linalg.inv(div_obj.np_arr())).tolist())

        elif Check(div_obj).check() == 'quaternion':
            div = div_obj.inv_q()
            return Quaternion(
                Scalar(self.scalar) * Scalar(div.scalar) - Vector(self.vector) * Vector(div.vector),
                Scalar(self.scalar) * Vector(div.vector) + Scalar(div.scalar) * Vector(self.vector)
                + Vector(self.vector) % Vector(div.vector))

    def __add__(self, add_obj):
        if Check(add_obj).check() == 'scalar':
            return Quaternion(self.scalar + add_obj.scalar, self.vector[:])

        elif Check(add_obj).check() == 'vector' and len(self.vector) == len(add_obj.vector):
            return Quaternion(self.scalar, (Vector(self.vector) + add_obj.vector).vector)

        elif Check(add_obj).check() == 'matrix' and len(add_obj.lst) == 4:
            return self.matrix_form() + add_obj

        elif Check(add_obj).check() == 'quaternion':
            return Quaternion(self.scalar + add_obj.scalar, [self.vector[0] + add_obj.vector[0], self.vector[1]
                                                             + add_obj.vector[1], self.vector[2] + add_obj.vector[2]])

    def __sub__(self, sub_obj):
        if Check(sub_obj).check() == 'scalar':
            return Quaternion(self.scalar - sub_obj.scalar, self.vector[:])

        elif Check(sub_obj).check() == 'vector' and len(self.vector) == len(sub_obj.vector):
            return Quaternion(self.scalar, (Vector(self.vector) - sub_obj.vector).vector)

        elif Check(sub_obj).check() == 'matrix' and len(sub_obj.lst) == 4:
            return self.matrix_form() - sub_obj

        elif Check(sub_obj).check() == 'quaternion':
            return Quaternion(self.scalar - sub_obj.scalar, [self.vector[0] - sub_obj.vector[0], self.vector[1]
                                                             - sub_obj.vector[1], self.vector[2] - sub_obj.vector[2]])

    def __mod__(self, mod_obj):
        return SyntaxError('Not today')

    def __pow__(self, pow_obj):
        if Check(pow_obj).check() == 'scalar':
            n = pow_obj.scalar
            for_iter = Quaternion(self.scalar, self.vector)
            for i in range(n):
                for_iter *= Quaternion(self.scalar, self.vector)
            return for_iter

        elif Check(pow_obj).check() == 'vector':
            return SyntaxError('Not today')

        elif Check(pow_obj).check() == 'matrix':
            return SyntaxError('Not today')

        elif Check(pow_obj).check() == 'quaternion':
            return SyntaxError('Not today')

    def inv_q(self):
        norm_square = self.scalar**2 + self.vector[0]**2 + self.vector[1]**2 + self.vector[2]**2
        return Quaternion(self.scalar/norm_square, [-i/norm_square for i in self.vector[:]])

    def matrix_form(self):
        a, b, c, d = self.scalar, self.vector[0], self.vector[1], self.vector[2]
        return Matrix([[a, -b, -c, -d], [b, a, -d, c], [c, d, a, -b], [d, -c, b, a]])

    @scalar.setter
    def scalar(self, value):
        self.scalar = value

    @vector.setter
    def vector(self, value):
        self.vector = value


class Validation:

    def __init__(self, expression):
        self.expression = self.try_correct(expression)

    @staticmethod
    def try_correct(expression):
        if eval(expression) != SyntaxError and eval(expression) is not None:
            return eval(expression)
        else:
            return 'The expression failed validation'


class VMCalculator:

    def __call__(self, expression):
        find_bags = Validation(expression)
        self.expression = find_bags.expression

    def __str__(self):
        return self.expression


class VMKCalculator(VMCalculator):
    pass


class BodyMovement:

    def __init__(self, g, air_resistance):
        self.g = g
        self.k = air_resistance

    def equations(self, t, y):
        x, y, z, vx, vy, vz = y
        speed = np.sqrt(vx ** 2 + vy ** 2 + vz ** 2)
        ax = -self.k * speed * vx
        ay = -self.k * speed * vy
        az = -self.g - self.k * speed * vz
        return [vx, vy, vz, ax, ay, az]

    def simulate(self, v0, angles, lat, lon, height):
        angle_xy, angle_xz = np.radians(angles)
        vx0 = v0 * np.cos(angle_xy) * np.cos(angle_xz)
        vy0 = v0 * np.sin(angle_xy) * np.cos(angle_xz)
        vz0 = v0 * np.sin(angle_xz)
        initial_conditions = [0, 0, height, vx0, vy0, vz0]

        def event(t, y):
            return y[2]

        event.terminal = True
        event.direction = -1
        solution = solve_ivp(self.equations, [0, 10000], initial_conditions, events=event, dense_output=True)
        x = solution.y[0]
        y = solution.y[1]
        z = solution.y[2]
        t = solution.t
        final_position = (x[-1], y[-1], z[-1])
        final_time = t[-1]
        return final_position, final_time

    def initial_velocity(self, unknowns, *args):
        r_vector_start, r_vector_end, g_vector, w_vector, k_m = args
        v_x, v_y, v_z = unknowns
        v_vector_0 = np.array([v_x, v_y, v_z], dtype=np.float64)
        v_vector = np.copy(v_vector_0).astype(np.float64)
        r_vector = np.copy(r_vector_start).astype(np.float64)
        t = 0.1
        while r_vector[2] >= 0:
            t += 0.1
            acceleration = g_vector + k_m * v_vector + 2 * np.cross(w_vector, v_vector) + np.cross(w_vector,
                                                                                                   np.cross(w_vector,
                                                                                                            r_vector_start))
            v_vector += acceleration * t
            r_vector += v_vector_0 * t + 0.5 * acceleration * t ** 2
            r_vector_start = np.copy(r_vector)
            v_vector_0 = np.copy(v_vector)
        return r_vector - r_vector_end

    @staticmethod
    def geographic_to_cartesian(lat, lon, height):
        R = 6371.0
        phi = math.radians(lat)
        lam = math.radians(lon)
        x = (R + height) * math.cos(phi) * math.cos(lam)
        y = (R + height) * math.cos(phi) * math.sin(lam)
        z = (R + height) * math.sin(phi)
        return x, y, z

    def find_initial_conditions(self, lat1, lon1, height1, lat2, lon2, height2, g_vector, w_vector, k_m):
        r_vector_start = self.geographic_to_cartesian(lat1, lon1, height1)
        r_vector_end = self.geographic_to_cartesian(lat2, lon2, height2)
        def objective(params):
            v0, angle_xy, angle_xz = params
            final_position, _ = self.simulate(v0, (angle_xy, angle_xz), lat1, lon1, height1)
            return ((final_position[0] - (lat2 - lat1)) ** 2 +
                    (final_position[1] - (lon2 - lon1)) ** 2 +
                    (final_position[2] - (height2 - height1)) ** 2)
        initial_guess = [0, 0, 0]
        result = fsolve(self.initial_velocity, initial_guess, args=(r_vector_start, r_vector_end, g_vector, w_vector, k_m))
        return result

    def plot_trajectory(self, v0, angles, lat, lon, height):
        final_position, time = self.simulate(v0, angles, lat, lon, height)
        solution = solve_ivp(self.equations, [0, time],
                             [0, 0, height, v0 * np.cos(np.radians(angles[0])) * np.cos(np.radians(angles[1])),
                              v0 * np.sin(np.radians(angles[0])) * np.cos(np.radians(angles[1])),
                              v0 * np.sin(np.radians(angles[1]))],
                             dense_output=True)
        t = np.linspace(0, time, 500)
        sol = solution.sol(t)
        x = sol[0]
        y = sol[1]
        z = sol[2]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(x, y, z)
        ax.set_title("Trajectory of the projectile")
        ax.set_xlabel("X distance (m)")
        ax.set_ylabel("Y distance (m)")
        ax.set_zlabel("Z distance (m)")
        plt.show()


g = 10
air_resistance = 9
pm = BodyMovement(g, air_resistance)
v0 = 1000
angles = (45, 13)
lat = 0
lon = 0
height = 0
try:
    v0 = pm.find_initial_conditions(0, 0, 0, 37, 37, 0, [0, 0, -10], [0, 1, 0], air_resistance)
    print(f"Оптимальна початкова швидкість: {v0}")
    final_position, final_time = pm.simulate(v0, angles, lat, lon, height)
    print(f"Фінальна позиція: {final_position}, Час: {final_time}")
    pm.plot_trajectory(v0, angles, lat, lon, height)
except ValueError as e:
    print(e)


class ParticleMovement:

    def __init__(self, q, direction_e, magnitude_e, direction_b, magnitude_b, direction_v, magnitude_v):
        self.q = q
        if np.linalg.norm(np.array(direction_e)) != 0:
            self.E = np.array(direction_e) / np.linalg.norm(np.array(direction_e))
        else:
            self.E = np.array(direction_e)
        self.magnitude_e = magnitude_e
        if np.linalg.norm(np.array(direction_b)) != 0:
            self.B = np.array(direction_b / np.linalg.norm(np.array(direction_b)))
        else:
            self.B = np.array(direction_b)
        self.magnitude_b = np.array(magnitude_b)
        self.v = np.array(direction_v) / np.linalg.norm(np.array(direction_v))
        self.magnitude_v = magnitude_v

    @staticmethod
    def quaternion_multiply(q1, q2):
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        return np.array([
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
        ])

    def rotate_vector_by_quaternion(self, v, q):
        q_v = np.hstack(([0], v))
        q_conj = np.hstack(([q[0]], -q[1:]))
        q_v_rot = self.quaternion_multiply(self.quaternion_multiply(q, q_v), q_conj)
        return q_v_rot[1:]

    def movement(self):
        dt = 0.01
        all_coord = np.zeros((1000, 3))
        all_coord[0] = np.array([0, 0, 0])
        for i in range(1, 1000):
            f = self.q * (self.E + np.cross(self.v, self.B))
            theta = np.linalg.norm(f) / self.magnitude_v * dt
            # a = f / self.q
            # self.v += a * dt
            # cos_theta = np.cos(theta)
            # sin_theta = np.sin(theta)
            # v_rot = self.v * cos_theta + np.cross(self.B, self.v) * sin_theta + self.B * np.dot(self.B, self.v) * (1 - cos_theta)
            # self.v = v_rot

            omega = self.q * self.magnitude_b * self.B / np.linalg.norm(self.v)
            q = np.hstack((np.cos(theta / 2), omega / np.linalg.norm(omega) * np.sin(theta / 2)))
            self.v = self.rotate_vector_by_quaternion(self.v, q)

            all_coord[i] = all_coord[i - 1] + self.v * dt
        Visualization3D(all_coord).visualization()


class Visualization3D:
    def __init__(self, trajectory):
        self.trajectory = trajectory

    def visualization(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(self.trajectory[:, 0], self.trajectory[:, 1], self.trajectory[:, 2])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()


particle = ParticleMovement(q=10,
                            direction_e=[0, 0, 0], magnitude_e=0,
                            direction_b=[0, 0, 1], magnitude_b=1,
                            direction_v=[1, 1, 1], magnitude_v=1)
# particle.movement()


# інтерфейс в wx
class ParticleMovementFrame(wx.Panel):

    def __init__(self, parent):
        super(ParticleMovementFrame, self).__init__(parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.text_ctrl_q = wx.TextCtrl(self, value='10', style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_direction_e = wx.TextCtrl(self, value='0 0 0', style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_direction_b = wx.TextCtrl(self, value='0 0 1', style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_magnitude_b = wx.TextCtrl(self, value='1', style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_direction_v = wx.TextCtrl(self, value='1 1 1', style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_magnitude_v = wx.TextCtrl(self, value='1', style=wx.TE_PROCESS_ENTER)
        self.btn_run_simulation = wx.Button(self, label='Run Simulation')
        self.btn_run_simulation.Bind(wx.EVT_BUTTON, self.on_run_simulation)
        vbox.Add(wx.StaticText(self, label='Charge (q):'), 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.text_ctrl_q, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(wx.StaticText(self, label='Direction of E (x y z):'), 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.text_ctrl_direction_e, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(wx.StaticText(self, label='Direction of B (x y z):'), 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.text_ctrl_direction_b, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(wx.StaticText(self, label='Magnitude of B:'), 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.text_ctrl_magnitude_b, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(wx.StaticText(self, label='Direction of V (x y z):'), 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.text_ctrl_direction_v, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(wx.StaticText(self, label='Magnitude of V:'), 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.text_ctrl_magnitude_v, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.btn_run_simulation, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vbox)

    def on_run_simulation(self, event):
        q = float(self.text_ctrl_q.GetValue())
        direction_e = list(map(float, self.text_ctrl_direction_e.GetValue().split()))
        direction_b = list(map(float, self.text_ctrl_direction_b.GetValue().split()))
        magnitude_b = float(self.text_ctrl_magnitude_b.GetValue())
        direction_v = list(map(float, self.text_ctrl_direction_v.GetValue().split()))
        magnitude_v = float(self.text_ctrl_magnitude_v.GetValue())
        particle = ParticleMovement(q=q,
                                    direction_e=direction_e, magnitude_e=0,
                                    direction_b=direction_b, magnitude_b=magnitude_b,
                                    direction_v=direction_v, magnitude_v=magnitude_v)
        particle.movement()


class BodyMovementFrame(wx.Panel):

    def __init__(self, parent):
        super(BodyMovementFrame, self).__init__(parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.text_ctrl_g = wx.TextCtrl(self, value='10', style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_air_resistance = wx.TextCtrl(self, value='0.1', style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_v0 = wx.TextCtrl(self, value='500', style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_angles = wx.TextCtrl(self, value='45 45', style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_lat = wx.TextCtrl(self, value='0', style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_lon = wx.TextCtrl(self, value='0', style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_height = wx.TextCtrl(self, value='0', style=wx.TE_PROCESS_ENTER)
        self.btn_run_simulation = wx.Button(self, label='Run Simulation')
        self.btn_run_simulation.Bind(wx.EVT_BUTTON, self.on_run_simulation)
        vbox.Add(wx.StaticText(self, label='Gravity (g):'), 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.text_ctrl_g, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(wx.StaticText(self, label='Air Resistance:'), 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.text_ctrl_air_resistance, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(wx.StaticText(self, label='Initial Velocity (v0):'), 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.text_ctrl_v0, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(wx.StaticText(self, label='Angles (angle_xy angle_xz):'), 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.text_ctrl_angles, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(wx.StaticText(self, label='Latitude (lat):'), 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.text_ctrl_lat, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(wx.StaticText(self, label='Longitude (lon):'), 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.text_ctrl_lon, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(wx.StaticText(self, label='Height:'), 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.text_ctrl_height, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.btn_run_simulation, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vbox)

    def on_run_simulation(self, event):
        g = float(self.text_ctrl_g.GetValue())
        air_resistance = float(self.text_ctrl_air_resistance.GetValue())
        v0 = float(self.text_ctrl_v0.GetValue())
        angles = tuple(map(float, self.text_ctrl_angles.GetValue().split()))
        lat = float(self.text_ctrl_lat.GetValue())
        lon = float(self.text_ctrl_lon.GetValue())
        height = float(self.text_ctrl_height.GetValue())
        body_movement = BodyMovement(g, air_resistance)
        try:
            final_position, final_time = body_movement.simulate(v0, angles, lat, lon, height)
            print(f"Final Position: {final_position}, Time: {final_time}")
            body_movement.plot_trajectory(v0, angles, lat, lon, height)
        except ValueError as e:
            print(e)


class MyFrame(wx.Frame):

    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(800, 600))
        notebook = wx.Notebook(self)
        particle_tab = ParticleMovementFrame(notebook)
        body_tab = BodyMovementFrame(notebook)
        notebook.AddPage(particle_tab, "Particle Movement")
        notebook.AddPage(body_tab, "Body Movement")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)


app = wx.App(False)
frame = MyFrame(None, 'Physics Simulation App')
frame.Show(True)
app.MainLoop()
