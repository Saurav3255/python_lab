
"""
Program: Functional Data Filtering & Matrix Transformation Suite
Author: Saurav 241492

Description:
Implements matrix filtering, sorting, and transformation using
lambda expressions and functional tools like map(), filter(), and sorted().

Input: 2D lists and tuples containing numerical data.
Output: Filtered, sorted, and transformed data sequences.
"""

from typing import List, Tuple


# Function to remove negative values from a matrix
def filter_matrix(matrix: List[List[int]]) -> List[List[int]]:
    return list(map(
        lambda row: list(filter(lambda x: x >= 0, row)),
        matrix
    ))


# Function to sort each row in ascending order
def sort_matrix(matrix: List[List[int]]) -> List[List[int]]:
    return list(map(lambda row: sorted(row), matrix))


# Function to calculate the square of each element
def transform_matrix(matrix: List[List[int]]) -> List[List[int]]:
    return list(map(
        lambda row: list(map(lambda x: x ** 2, row)),
        matrix
    ))


# Function to sort tuples by their second element
def sort_tuples(data: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    return sorted(data, key=lambda item: item[1])


# Main program
if __name__ == "__main__":
    matrix = [
        [3, -1, 5],
        [-2, 4, 1],
        [7, -3, 2]
    ]

    tuples = [(1, 30), (2, 10), (3, 20)]

    print("Original Matrix:", matrix)

    print("Filtered Matrix:", filter_matrix(matrix))

    print("Sorted Matrix:", sort_matrix(matrix))

    print("Squared Matrix:", transform_matrix(matrix))

    print("Original Tuples:", tuples)

    print("Tuples Sorted by Second Element:", sort_tuples(tuples))