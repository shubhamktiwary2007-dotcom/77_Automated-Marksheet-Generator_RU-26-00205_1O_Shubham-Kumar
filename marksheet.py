
import pandas as pd
import os

FILE_NAME = "marks.csv"
SUBJECTS = ["Maths", "Physics", "Programming"]


# Function to read and validate CSV file
def load_marksheet(filename=FILE_NAME):

    if not os.path.exists(filename):
        print(f"Error: {filename} file not found.")
        return None

    try:
        df = pd.read_csv(filename)
    except Exception as error:
        print(f"Error reading {filename}: {error}")
        return None

    required_columns = ["RollNo", "Name"] + SUBJECTS

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        print("Error: Missing columns: " + ", ".join(missing_columns))
        return None

    valid_students = []

    for _, row in df.iterrows():

        roll_no = row["RollNo"]
        name = str(row["Name"]).strip()

        try:
            roll_no = int(roll_no)
            marks = [float(row[sub]) for sub in SUBJECTS]
        except (ValueError, TypeError, OverflowError):
            print(
                f"Warning: Row for roll no {row['RollNo']} skipped "
                "- roll number and marks must be numeric."
            )
            continue

        # Validate marks
        if not name or any(mark < 0 or mark > 100 for mark in marks):
            print(
                f"Warning: Row for roll no {roll_no} skipped "
                "- marks must be between 0 and 100."
            )
            continue

        # Display whole-number marks without .0
        marks = [
            int(mark) if mark.is_integer() else mark
            for mark in marks
        ]

        student = {
            "RollNo": roll_no,
            "Name": name,
            "Maths": marks[0],
            "Physics": marks[1],
            "Programming": marks[2]
        }

        valid_students.append(student)

    return valid_students


# Function to calculate grade
def get_grade(percentage):

    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    elif percentage >= 40:
        return "E"
    else:
        return "F"


# Function to print the marksheet
def print_marksheet(student):

    maths = student["Maths"]
    physics = student["Physics"]
    programming = student["Programming"]

    total = maths + physics + programming
    percentage = (total / 300) * 100
    grade = get_grade(percentage)

    # Check for failed subjects
    failed_subjects = [
        subject for subject in SUBJECTS
        if student[subject] < 40
    ]

    print("\n" + "=" * 42)
    print("          STUDENT MARKSHEET")
    print("=" * 42)

    print(
        f"Roll No: {student['RollNo']} | "
        f"Name: {student['Name']}"
    )

    print(
        f"Maths: {maths} | Physics: {physics} | "
        f"Programming: {programming}"
    )

    print(f"Total: {total}/300 | Percentage: {percentage:.2f}%")
    print(f"Grade: {grade}", end=" | ")

    if failed_subjects:
        failed = ", ".join(failed_subjects)
        print(f"Result: FAIL ({failed} below 40)")
    else:
        print("Result: PASS")

    print("=" * 42)


# Main function
def main():

    print("\nAUTOMATED MARKSHEET GENERATOR")
    print("1. Single marksheet")
    print("2. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":

        students = load_marksheet()

        if students is None:
            return

        try:
            roll_no = int(input("Enter roll no: ").strip())
        except ValueError:
            print("Invalid input: Enter a numeric roll number.")
            return

        # Find student using roll number
        student = next(
            (
                item for item in students
                if item["RollNo"] == roll_no
            ),
            None
        )

        if student is None:
            print(f"Roll number {roll_no} not found.")
        else:
            print_marksheet(student)

    elif choice == "2":
        print("Program closed.")

    else:
        print("Invalid menu choice. Please enter 1 or 2.")


# Program execution starts here
if __name__ == "__main__":
    main()
