
"""
Program: Custom Flexible Student Grade & Statistics Calculator
Author: Saurav 241492

Description:
Calculates student performance statistics using *args and **kwargs.
Computes minimum, maximum, average, and letter grade distribution,
and returns structured results using tuple unpacking.

Input: Variable assessment grades and student details.
Output: Minimum, maximum, average, and grade distribution.
"""

# Function to calculate statistics
def calculate_statistics(*grades, **student_info):
    if not grades:
        return None, None, 0.0, {}

    minimum = min(grades)
    maximum = max(grades)
    average = sum(grades) / len(grades)

    # Calculate letter grade distribution
    distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

    for grade in grades:
        if grade >= 90:
            distribution["A"] += 1
        elif grade >= 80:
            distribution["B"] += 1
        elif grade >= 70:
            distribution["C"] += 1
        elif grade >= 60:
            distribution["D"] += 1
        else:
            distribution["F"] += 1

    print("\nStudent Details:", student_info)

    return minimum, maximum, average, distribution


# Main program
if __name__ == "__main__":
    # Assessment grades and keyword arguments
    result = calculate_statistics(
        95, 82, 76, 88, 59, 91,
        name="Rahul",
        course="CSE"
    )

    # Tuple unpacking
    minimum, maximum, average, distribution = result

    print("Minimum Grade:", minimum)
    print("Maximum Grade:", maximum)
    print("Average Grade:", round(average, 2))
    print("Grade Distribution:", distribution)