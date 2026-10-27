
"""
Program: Multi-Functional Graphical Desktop Calculator
Author: Saurav 241492

Description:
Creates a desktop calculator using Tkinter with a grid layout.
Supports arithmetic operations, percentages, decimals, and
error handling through a graphical Entry display.

Input: Button clicks or keyboard-entered mathematical expressions.
Output: Calculated result displayed in the calculator window.
"""

import tkinter as tk
import ast
import operator


# Safe arithmetic operations
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def safe_calculate(expression):
    """Evaluate arithmetic expressions without using eval()."""
    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 1000:
                raise ValueError("Exponent is too large.")

            result = OPERATORS[type(node.op)](left, right)

            if isinstance(result, complex) or abs(result) > 1e100:
                raise ValueError("Result is too large.")

            return result

        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](evaluate(node.operand))

        raise ValueError("Invalid expression.")

    if len(expression) > 200:
        raise ValueError("Expression is too long.")

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree)


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Calculator")
        self.root.geometry("340x460")
        self.root.resizable(False, False)

        self.expression = tk.StringVar()

        self.display = tk.Entry(
            root,
            textvariable=self.expression,
            font=("Arial", 22),
            justify="right",
            bd=8,
            relief=tk.GROOVE
        )
        self.display.grid(
            row=0, column=0, columnspan=4,
            padx=10, pady=15, sticky="nsew", ipady=10
        )

        buttons = [
            ("C", 1, 0), ("(", 1, 1), (")", 1, 2), ("/", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("0", 5, 0), (".", 5, 1), ("%", 5, 2), ("=", 5, 3),
        ]

        for text, row, col in buttons:
            button = tk.Button(
                root,
                text=text,
                font=("Arial", 16, "bold"),
                command=lambda value=text: self.click(value)
            )
            button.grid(
                row=row, column=col,
                padx=4, pady=4, sticky="nsew", ipadx=5, ipady=10
            )

        for col in range(4):
            root.grid_columnconfigure(col, weight=1)

        for row in range(1, 6):
            root.grid_rowconfigure(row, weight=1)

        self.display.focus_set()
        self.root.bind("<Return>", lambda event: self.click("="))
        self.root.bind("<Escape>", lambda event: self.click("C"))

    def click(self, value):
        if value == "C":
            self.expression.set("")

        elif value == "=":
            try:
                expression = self.expression.get().strip()

                # Interpret percentage as division by 100.
                expression = expression.replace("%", "/100")

                result = safe_calculate(expression)

                if isinstance(result, float) and result.is_integer():
                    result = int(result)

                self.expression.set(str(result))

            except (ValueError, SyntaxError, ZeroDivisionError, OverflowError):
                self.expression.set("Error")

        else:
            current = self.expression.get()

            if current == "Error":
                current = ""

            self.expression.set(current + value)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
