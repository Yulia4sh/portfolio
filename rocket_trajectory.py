#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
Rocket Drawing Simulation

This script uses the Turtle graphics library to simulate a rocket's trajectory
using a combination of rectangular, circular, and triangular shapes. The rocket
is drawn as a combination of these shapes, and its movement is animated to show
the rocket's trajectory based on a given trajectory list. The trajectory is
calculated using basic physics principles, and the rocket's path is visualized
on the screen.

Classes:
- XandYDescriptor: A descriptor to validate and handle x and y coordinates.
- Figure: A base class for shapes with color and position attributes.
- Moveable: An abstract base class for shapes that can be moved, shown, and rotated.
- Rectangular: A class to draw rectangular shapes.
- Circle: A class to draw circular shapes.
- Triangular: A class to draw triangular shapes.
- Rocket: A class that combines rectangular, circular, and triangular shapes to
  represent a rocket and animate its trajectory.

Usage:
- Create a Rocket instance and call the `trajectory_move` method with the desired
  trajectory to see the rocket move and display on the screen.
"""

import turtle as t
from abc import ABCMeta, abstractmethod
import math
import time
import random


class XandYDescriptor:
    """
    Descriptor for validating and handling x and y coordinates.
    Coordinates must be integers or floats between -500 and 500.
    """
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]
    
    def __set__(self, instance, value):
        if isinstance(value, (int, float)) and (-500 <= value < 500):
            instance.__dict__[self.name] = value
        else:
            raise ValueError("Incorrect coordinate format")
    
    def __set_name__(self, owner, name):
        self.name = name


class Figure:
    """
    Base class for figures with color and position attributes.
    """
    x = XandYDescriptor()
    y = XandYDescriptor()
    
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.__color = color
    
    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, color):
        self.__color = color


class Moveable(metaclass=ABCMeta):
    """
    Abstract base class for moveable figures that can be shown, hidden, moved,
    and rotated.
    """
    def _draw(self):
        pass
    
    def show(self):
        self._draw()
    
    def hide(self, x, y):
        """
        Hide the figure at the specified position by drawing it with the background color.
        """
        t.color('navy')
        t.fillcolor("navy")
        t.penup()
        t.setpos(x, y)
        t.pendown()
        self._draw()
        t.color(self.color)
    
    def move(self, dx, dy, x, y):
        """
        Move the figure by dx, dy from the current position.
        """
        t.penup()
        local_x, local_y = x + dx, y + dy
        t.setpos(local_x, local_y)
        t.pendown()
        self.show()
        t.tracer(1)
        time.sleep(0.1)
        t.tracer(0)
        self.hide(local_x, local_y)
    
    def rotate(self, angle):
        """
        Rotate the figure by the specified angle.
        """
        t.setheading(t.heading() + angle)


class Rectangular(Moveable, Figure):
    """
    A class to draw rectangular shapes.
    """
    def __init__(self, x, y, color, a, b):
        super().__init__(x, y, color)
        self.a = min(a, b)
        self.b = max(a, b)
    
    def _draw(self):
        """
        Draw a filled rectangle using the Turtle graphics library.
        """
        t.begin_fill()
        need_x, need_y = t.xcor(), t.ycor()
        t.forward(self.a / 2)
        t.setheading(t.heading() + 90)
        t.forward(self.b)
        t.setheading(t.heading() + 90)
        t.forward(self.a)
        t.setheading(t.heading() + 90)
        t.forward(self.b)
        t.setheading(t.heading() + 90)
        t.forward(self.a / 2)
        t.end_fill()
        t.penup()
        t.setpos(need_x, need_y)
        t.pendown()
        super()._draw()


class Circle(Moveable, Figure):
    """
    A class to draw circular shapes.
    """
    def __init__(self, x, y, color, radius):
        super().__init__(x, y, color)
        self.radius = radius
    
    def _draw(self):
        """
        Draw a filled circle using the Turtle graphics library.
        """
        t.begin_fill()
        t.circle(self.radius, 180)
        need_x, need_y = t.xcor(), t.ycor()
        t.circle(self.radius, 180)
        t.end_fill()
        t.penup()
        t.setpos(need_x, need_y)
        t.pendown()
        super()._draw()


class Triangular(Moveable, Figure):
    """
    A class to draw triangular shapes.
    """
    def __init__(self, x, y, color, c, d, e):
        super().__init__(x, y, color)
        self.c = c
        self.d = d
        self.e = e
    
    def _draw(self):
        """
        Draw a filled triangle using the Turtle graphics library.
        """
        t.begin_fill()
        t.forward(self.c / 2)
        t.setheading(t.heading() + 120)
        t.forward(self.d)
        t.setheading(t.heading() + 120)
        t.forward(self.e)
        t.setheading(t.heading() + 120)
        t.forward(self.c / 2)
        t.end_fill()


class Rocket(Rectangular, Circle, Triangular):
    """
    A class that combines rectangular, circular, and triangular shapes to
    represent a rocket and animate its trajectory.
    """
    def __init__(self, x, y, color: str, L, W):
        if L <= 2 * W:
            raise ValueError('Does not fit into any framework')
        super().__init__(x, y, color, L, W)
        self.L = L
        self.W = W
    
    def trajectory_move(self, trajectory: list):
        """
        Animate the rocket's trajectory based on the given list of trajectory points.
        """
        t.tracer(0)
        t.clear()
        t.hideturtle()
        wn = t.Screen()
        wn.bgcolor("navy")
        for _ in range(100):
            t.penup()
            t.setpos(random.randint(-500, 500), random.randint(-500, 500))
            t.dot(random.randint(1, 10), 'white')
        t.penup()
        t.setpos(80, -357)
        t.dot(700, 'SkyBlue1')
        # Trajectory calculation
        t.color(self.color)
        x_1, y_1, x_2, y_2, max_h = trajectory[0][0], trajectory[0][1], trajectory[1][0], trajectory[1][1], trajectory[2]
        t.setheading(math.degrees(math.atan(y_2 / x_2)))
        self.a, self.b, self.radius = self.W, self.L - self.W - max_h, self.W / 2
        self.c = self.d = self.e = 2 * self.W
        angle = math.atan(max_h / (x_2 / 2)) * (180 / math.pi)
        speed = (2 * 9.81 * max_h) ** 0.5
        angle_for_iter = t.heading() + 90
        x_0, y_0, dT = 0, self.W, 0.000000001
        while True:
            x = speed * abs(math.cos(angle)) * dT
            y = speed * math.sin(angle) * dT - ((9.81 * dT ** 2) / 2) + self.W
            dT += 0.1
            angle_for_rotate = angle_for_iter - math.degrees(math.atan((y - y_0) / (x - x_0)))
            angle_for_iter -= angle_for_rotate
            t.fillcolor("white")
            super().rotate(-angle_for_rotate)
            super().move(x - x_0, y - y_0, x, y)
            x_0, y_0 = x, y
            if y < y_2 and x > x_2:
                break


r1 = Rocket(0, 0, 'black', 50, 20)
r1.trajectory_move([(0, 0), (100, 0), 100])

