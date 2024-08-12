#!/usr/bin/env python
# coding: utf-8

# In[2]:


import math
import cmath
from time import perf_counter
import doctest

class LinearEquation:
    #ax+b=0
    def __init__(self, equation):
        self.__equation = equation
    def solve(self):
        equation = self.__equation
        if equation[0] == 'x' or (equation[0] == '-' and equation[1] == 'x'):
            a = 1 if equation[0] == 'x' else -1
        elif 'x' in equation and (equation[0] != 'x' or equation[0] != '-'):
            a = int(equation[0:equation.index('x')])
        else:
            raise TypeError
        if equation[(equation.index('x')+1):equation.index('=')] == '':
            b = 0
        else:
            b = int(equation[(equation.index('x')+1):equation.index('=')])
        if a != 0 and b != 0:
            return [-b/a], 'LinearEquation'
        else:
            return ['inf'], 'LinearEquation'
        
class QuadraticEquation(LinearEquation):
    #ax^2+bx+c=0
    def __init__(self, equation):
        self.__equation = equation
    def solve(self, equation=''):
        if equation == '':
            equation = self.__equation
        if 'x^2' not in equation:
            return super().solve()
        elif (equation[0] == 'x' or (equation[0] == '-' and equation[1] == 'x')) and equation[equation.index('x')+2] == '2':
            a = 1 if equation[0] == 'x' else -1
        elif 'x^2' in equation and (equation[0] != 'x' or equation[0] != '-'):
            a = int(equation[0:equation.index('x')])
        fake_equation = equation[equation.index('x')+3:]
        if fake_equation[0] == 'x' or (equation[0] == '-' and equation[1] == 'x'):
            b = 1 if equation[0] == 'x' else -1
        elif 'x' in equation and (equation[0] != 'x' or equation[0] != '-'):
            b = int(equation[0:equation.index('x')])
        elif x not in fake_equation:
            b = 0
        if fake_equation[(fake_equation.index('x')+1):fake_equation.index('=')] == '':
            c = 0
        else:
            c = int(fake_equation[(fake_equation.index('x')+1):fake_equation.index('=')])
        return [(-b+cmath.sqrt(b**2-(4*a*c)))/(2*a), (-b-cmath.sqrt(b**2-(4*a*c)))/(2*a)], 'QuadraticEquation'

class QubicEquation:
    #ax^3+bx^2+cx+d=0
    def __init__(self, equation):
        self.__equation = equation
    def solve(self):
        equation = self.__equation
        if 'x^3' not in equation:
            return super().solve()
        a, b, c, d = 0, 0, 0, 0
        if equation[0] == 'x' or equation[0] == '-':
            a = 1 if equation[0] == 'x' else -1
        elif 'x^3' in equation:
            a = int(equation[:equation.index('x^3')])
        equation_without_x_3 = equation[equation.index('x^3') + 3:]
        if 'x^2' in equation_without_x_3:
            if equation_without_x_3[0] == 'x' or (equation_without_x_3[0] == '-' and equation_without_x_3[1] == 'x'):
                b = 1 if equation_without_x_3[0] == 'x' else -1
            elif 'x^2' in equation_without_x_3 or (equation_without_x_3[0] == '-' and equation_without_x_3[1] != 'x'):
                b = int(equation_without_x_3[:equation_without_x_3.index('x^2')])
        equation_without_x_2 = equation_without_x_3[equation_without_x_3.index('x^2') + 3:] if 'x^2' in equation_without_x_3 else equation_without_x_3
        if 'x' in equation_without_x_2:
            if equation_without_x_2[0] == 'x' or equation_without_x_2[0] == '-':
                c = 1 if equation_without_x_2[0] == 'x' else -1
            elif 'x' in equation_without_x_2:
                c = int(equation_without_x_2[:equation_without_x_2.index('x')])
        if 'x' in equation_without_x_2:
            if equation_without_x_2[(equation_without_x_2.index('x') + 1):equation_without_x_2.index('=')] != '':
                d = int(equation_without_x_2[(equation_without_x_2.index('x')+1):equation_without_x_2.index('=')])
        p = (3 * a * c - b**2) / (3 * a**2)
        q = (2 * b**3 - 9 * a * b * c + 27 * a**2 * d) / (27 * a ** 3)
        discriminant = q**2 + 4 * p**3 / 27 
        if discriminant > 0:
            u = (-q + math.sqrt(discriminant)) / 2
            v = (-q - math.sqrt(discriminant)) / 2
            root1 = u**(1/3) + v**(1/3) - b / (3 * a)
            roots = [root1]
        elif discriminant == 0:
            if q >= 0:
                root1 = -2 * (q**(1/3)) - b / (3 * a)
            else:
                root1 = 2 * ((-q)**(1/3)) - b / (3 * a)
            root2 = q**(1/3) - b / (3 * a)
            roots = [root1, root2]
        else:
            r = math.sqrt(-p ** 3 / 27)
            theta = math.acos(-q / (2 * r))
            root1 = 2 * (r**(1/3)) * math.cos(theta / 3) - b / (3 * a)
            root2 = 2 * (r**(1/3)) * math.cos((theta + 2 * math.pi) / 3) - b / (3 * a)
            root3 = 2 * (r**(1/3)) * math.cos((theta + 4 * math.pi) / 3) - b / (3 * a)
        return [root1, root2, root3], 'QubicEquation'
        

class BiQuadraticEquation(QuadraticEquation):
    #ax^4+bx^2+c=0
    def __init__(self, equation):
        self.__equation = equation
    def solve(self):
        equation = self.__equation
        if 'x^4' not in equation:
            return super().solve()
        if 'x^3' in equation or 'x+' in equation or 'x-' in equation:
            raise ValueError ("I can't help at all")
        a, b, c = 0, 0, 0
        if 'x^4' in equation and equation[0] == 'x' or equation[0] == '-':
            a = 1 if equation[0] == 'x' else -1
        elif 'x^4' in equation:
            a = int(equation[0:equation.index('x')])
        equation_without_x_4 = equation[equation.index('x') + 3:]
        if 'x^2' in equation_without_x_4:
            if equation_without_x_4[0] == 'x' or (equation_without_x_4[0] == '-' and equation_without_x_4[1] != 'x'):
                b = 1 if equation_without_x_4[0] == 'x' else -1
            elif 'x^2' in equation_without_x_4:
                b = int(equation_without_x_4[0:equation_without_x_4.index('x')])
        if equation_without_x_4[(equation_without_x_4.index('x') + 3):equation_without_x_4.index('=')] != '':
            c = int(equation_without_x_4[(equation_without_x_4.index('x') + 3):equation_without_x_4.index('=')])
        d = cmath.sqrt(b**2 - 4*a*c)
        root1 = (-b + d) / (2*a)
        root2 = (-b - d) / (2*a)
        root3 = cmath.sqrt(root1)
        root4 = -cmath.sqrt(root1)
        root5 = cmath.sqrt(root2)
        root6 = -cmath.sqrt(root2)
        return [root3, root4, root5, root6], 'BiQuadraticEquation'

class Equation(BiQuadraticEquation, QubicEquation):
    """
    a class that accepts an equation of the form ax^4+bx^2+c=0 or other linear, quadratic, cubic, and biquadratic equations,
    and returns a dictionary with the roots, type, and time for which it calculated.
    
    >>> e1 = Equation('x^3-6x^2+11x-6=0')
    >>> e1.solve(True)
    {'roots': [3.0, 0.9999999999999998, 1.9999999999999998], 'type': 'QubicEquation'}
    
    >>> e2 = Equation('2x^4+2x^2+2=0')
    >>> e2.solve(True)
    {'roots': [(0.5+0.8660254037844386j), (-0.5-0.8660254037844386j), (0.5-0.8660254037844386j), (-0.5+0.8660254037844386j)], 'type': 'BiQuadraticEquation'}
    
    >>> e3 = Equation('2x^2+2x+2=0')
    >>> e3.solve(True)
    {'roots': [(-0.5+0.8660254037844386j), (-0.5-0.8660254037844386j)], 'type': 'QuadraticEquation'}
    
    >>> e4 = Equation('2x+2=0')
    >>> e4.solve(True)
    {'roots': [-1.0], 'type': 'LinearEquation'}
    """
    def __init__(self, equation):
        self.__equation = equation
        BiQuadraticEquation.__init__(self, equation)
        QubicEquation.__init__(self, equation)
        QuadraticEquation.__init__(self, equation)
        LinearEquation.__init__(self, equation)
    def solve(self, if_doctest=False):
        for  i, el in enumerate(self.__equation):
            if el == '^' and self.__equation[i+1] not in ('2', '3', '4'):
                raise ValueError ("I can't help at all")
            if el == 'x' and self.__equation[i+1] != '^' and self.__equation[i+1] not in ('+', '-', '='):
                raise ValueError ("I can't help at all")
        time_1 = perf_counter()
        if 'x^3' in self.__equation:
            for_x_3 = QubicEquation(self.__equation)
            solve_list, type_eq = for_x_3.solve()
        else:
            solve_list, type_eq = super().solve()
        time_2 = perf_counter()
        time_result = time_2 - time_1
        dict_result = {'roots': solve_list, 'type': type_eq, 'time': time_result}
        if if_doctest:
            dict_result = {'roots': solve_list, 'type': type_eq}
        return dict_result
    
    

        

e1 = Equation('x^3-6x^2+11x-6=0')
print(e1.solve())
doctest.testmod()

