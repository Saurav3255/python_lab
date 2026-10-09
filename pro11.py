"""
Program: Turtle Graphics - Geometric Patterns and Recursive Fractals
Author: Saurav 241492

Description:
Generates colorful geometric patterns and recursive fractals using
the turtle graphics library. Customizes pen colors, background,
drawing speed, and screen settings.

Input: User's choice of pattern and drawing parameters.
Output: Colorful Koch snowflake or geometric spiral.
"""

import turtle
import math


# Configure drawing screen
screen = turtle.Screen()
screen.title("Geometric Patterns and Recursive Fractals")
screen.setup(width=900, height=700)
screen.bgcolor("#101820")
screen.colormode(255)


# Configure turtle pen
pen = turtle.Turtle()
pen.speed(0)
pen.pensize(2)
pen.hideturtle()


# Function to draw Koch curve recursively
def koch_curve(length, depth):
    if depth == 0:
        pen.forward(length)
    else:
        length /= 3
        koch_curve(length, depth - 1)
        pen.left(60)
        koch_curve(length, depth - 1)
        pen.right(120)
        koch_curve(length, depth - 1)
        pen.left(60)
        koch_curve(length, depth - 1)


# Function to draw Koch snowflake
def koch_snowflake(length, depth):
    pen.penup()
    pen.goto(-length / 2, length / 3)
    pen.pendown()

    colors = [(0, 255, 255), (255, 80, 150), (255, 200, 50)]

    for color in colors:
        pen.pencolor(color)
        koch_curve(length, depth)
        pen.right(120)


# Function to draw a colorful spiral
def logarithmic_spiral():
    pen.penup()
    pen.goto(0, 0)
    pen.pendown()

    for i in range(360):
        angle = math.radians(i * 5)
        radius = 0.5 * math.exp(0.008 * i)

        pen.pencolor(
            int(127 + 127 * math.sin(i * 0.05)),
            int(127 + 127 * math.sin(i * 0.05 + 2)),
            int(127 + 127 * math.sin(i * 0.05 + 4))
        )

        pen.goto(radius * math.cos(angle), radius * math.sin(angle))


# Main program
print("===== TURTLE GRAPHICS PROJECT =====")
print("1. Koch Snowflake")
print("2. Colorful Spiral")

choice = input("Enter your choice (1 or 2): ")

if choice == "1":
    depth = int(input("Enter recursion depth (0-4): "))

    if 0 <= depth <= 4:
        koch_snowflake(300, depth)
    else:
        print("Please enter a depth between 0 and 4.")

elif choice == "2":
    logarithmic_spiral()

else:
    print("Invalid choice.")

turtle.done()