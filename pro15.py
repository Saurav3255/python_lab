
"""
Program: Abstract Shape Math Engine with Operator Overloading
Author: Saurav 241492

Description:
Uses the abc module to define an abstract geometric framework.
Implements Vector and Circle classes with operator overloading
for mathematical operations and comparisons.

Input: Vector coordinates and circle radii.
Output: Vector calculations, comparisons, and circle areas.
"""

from abc import ABC, abstractmethod
import math


# Abstract base class
class Shape(ABC):

    @abstractmethod
    def area(self):
        """Calculate the area of the shape."""
        pass

    @abstractmethod
    def __str__(self):
        """Return a readable description of the shape."""
        pass


# Vector class
class Vector(Shape):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def area(self):
        # A vector is not a 2D region, so this is not applicable.
        return 0

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.magnitude() < other.magnitude()

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __str__(self):
        return f"Vector({self.x}, {self.y})"


# Circle class
class Circle(Shape):
    def __init__(self, radius):
        if radius < 0:
            raise ValueError("Radius cannot be negative.")
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def __add__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        # Combine areas and return an equivalent circle.
        combined_radius = math.sqrt(
            self.radius ** 2 + other.radius ** 2
        )
        return Circle(combined_radius)

    def __eq__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return math.isclose(self.radius, other.radius)

    def __lt__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.area() < other.area()

    def __str__(self):
        return (
            f"Circle(radius={self.radius:.2f}, "
            f"area={self.area():.2f})"
        )


# Demonstration
if __name__ == "__main__":
    print("===== VECTOR OPERATIONS =====")

    v1 = Vector(3, 4)
    v2 = Vector(1, 2)
    v3 = Vector(3, 4)

    print("Vector 1:", v1)
    print("Vector 2:", v2)
    print("Addition:", v1 + v2)
    print("Magnitude of Vector 1:", v1.magnitude())
    print("Are vectors equal?", v1 == v3)
    print("Is Vector 2 smaller than Vector 1?", v2 < v1)

    print("\n===== CIRCLE OPERATIONS =====")

    c1 = Circle(3)
    c2 = Circle(4)
    c3 = c1 + c2

    print("Circle 1:", c1)
    print("Circle 2:", c2)
    print("Combined-area circle:", c3)
    print("Are circles equal?", c1 == c2)
    print("Is Circle 1 smaller than Circle 2?", c1 < c2)
