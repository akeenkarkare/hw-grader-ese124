"""
Add exam-grade C programming problems to the database.
Run this after seed.py to add more challenging problems.
"""
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
import models

def add_exam_problems():
    """Add exam-grade C programming problems with test cases"""
    init_db()
    db = SessionLocal()

    try:
        problems = [
            {
                "title": "Array Sum and Average",
                "difficulty": "Easy",
                "description": """Write a C program that reads an integer `n`, followed by `n` integers, and calculates:
1. The sum of all integers
2. The average of all integers (as a floating-point number)

**Input Format:**
- First line: integer `n` (1 ≤ n ≤ 100)
- Second line: `n` space-separated integers

**Output Format:**
- First line: Sum of all integers
- Second line: Average with 2 decimal places

**Example:**
```
Input:
5
10 20 30 40 50

Output:
150
30.00
```""",
                "constraints": "1 ≤ n ≤ 100, -1000 ≤ each integer ≤ 1000",
                "visible_tests": [
                    {"input": "5\n10 20 30 40 50", "output": "150\n30.00"},
                    {"input": "3\n1 2 3", "output": "6\n2.00"},
                    {"input": "1\n42", "output": "42\n42.00"},
                ],
                "hidden_tests": [
                    {"input": "4\n-5 10 -15 20", "output": "10\n2.50"},
                    {"input": "6\n100 200 300 400 500 600", "output": "2100\n350.00"},
                    {"input": "2\n0 0", "output": "0\n0.00"},
                    {"input": "5\n-10 -20 -30 -40 -50", "output": "-150\n-30.00"},
                    {"input": "7\n15 25 35 45 55 65 75", "output": "315\n45.00"},
                    {"input": "3\n1000 -1000 500", "output": "500\n166.67"},
                    {"input": "4\n7 14 21 28", "output": "70\n17.50"},
                ]
            },
            {
                "title": "Find Maximum in Array",
                "difficulty": "Easy",
                "description": """Write a C program that reads an integer `n`, followed by `n` integers, and finds:
1. The maximum value in the array
2. The index (0-based) where the maximum first appears

**Input Format:**
- First line: integer `n` (1 ≤ n ≤ 100)
- Second line: `n` space-separated integers

**Output Format:**
- First line: Maximum value
- Second line: Index of first occurrence (0-based)

**Example:**
```
Input:
5
3 7 2 9 5

Output:
9
3
```""",
                "constraints": "1 ≤ n ≤ 100, -1000 ≤ each integer ≤ 1000",
                "visible_tests": [
                    {"input": "5\n3 7 2 9 5", "output": "9\n3"},
                    {"input": "3\n10 5 8", "output": "10\n0"},
                    {"input": "1\n42", "output": "42\n0"},
                ],
                "hidden_tests": [
                    {"input": "6\n-5 -2 -10 -1 -8 -3", "output": "-1\n3"},
                    {"input": "4\n100 100 50 100", "output": "100\n0"},
                    {"input": "7\n1 2 3 4 5 6 7", "output": "7\n6"},
                    {"input": "5\n50 40 30 20 10", "output": "50\n0"},
                    {"input": "8\n-100 200 -50 150 200 100 50 25", "output": "200\n1"},
                    {"input": "3\n0 0 0", "output": "0\n0"},
                    {"input": "10\n5 5 5 5 10 5 5 5 5 5", "output": "10\n4"},
                ]
            },
            {
                "title": "Count Vowels and Consonants",
                "difficulty": "Easy",
                "description": """Write a C program that reads a string (up to 100 characters) and counts:
1. The number of vowels (a, e, i, o, u - case insensitive)
2. The number of consonants (all other alphabetic characters)

Non-alphabetic characters (spaces, digits, punctuation) should be ignored.

**Input Format:**
- A single line containing a string (may include spaces)

**Output Format:**
- First line: Number of vowels
- Second line: Number of consonants

**Example:**
```
Input:
Hello World

Output:
3
7
```""",
                "constraints": "String length ≤ 100 characters",
                "visible_tests": [
                    {"input": "Hello World", "output": "3\n7"},
                    {"input": "aeiou", "output": "5\n0"},
                    {"input": "bcdfg", "output": "0\n5"},
                ],
                "hidden_tests": [
                    {"input": "The quick brown fox", "output": "5\n11"},
                    {"input": "AEIOU", "output": "5\n0"},
                    {"input": "Programming 101", "output": "3\n8"},
                    {"input": "123 Test!", "output": "1\n3"},
                    {"input": "a", "output": "1\n0"},
                    {"input": "z", "output": "0\n1"},
                    {"input": "AaBbCcDdEe", "output": "4\n6"},
                    {"input": "!@#$%", "output": "0\n0"},
                    {"input": "I love C programming", "output": "6\n10"},
                    {"input": "xyz XYZ", "output": "0\n6"},
                ]
            },
            {
                "title": "Reverse Array",
                "difficulty": "Medium",
                "description": """Write a C program that reads an integer `n`, followed by `n` integers, and prints them in reverse order.

**Input Format:**
- First line: integer `n` (1 ≤ n ≤ 100)
- Second line: `n` space-separated integers

**Output Format:**
- Print all integers in reverse order, space-separated, on a single line

**Example:**
```
Input:
5
1 2 3 4 5

Output:
5 4 3 2 1
```""",
                "constraints": "1 ≤ n ≤ 100, -1000 ≤ each integer ≤ 1000",
                "visible_tests": [
                    {"input": "5\n1 2 3 4 5", "output": "5 4 3 2 1"},
                    {"input": "3\n10 20 30", "output": "30 20 10"},
                    {"input": "1\n42", "output": "42"},
                ],
                "hidden_tests": [
                    {"input": "6\n-5 -10 15 20 -25 30", "output": "30 -25 20 15 -10 -5"},
                    {"input": "4\n100 200 300 400", "output": "400 300 200 100"},
                    {"input": "2\n7 13", "output": "13 7"},
                    {"input": "7\n1 1 1 1 1 1 1", "output": "1 1 1 1 1 1 1"},
                    {"input": "8\n8 7 6 5 4 3 2 1", "output": "1 2 3 4 5 6 7 8"},
                    {"input": "5\n0 -1 0 -1 0", "output": "0 -1 0 -1 0"},
                    {"input": "10\n10 9 8 7 6 5 4 3 2 1", "output": "1 2 3 4 5 6 7 8 9 10"},
                ]
            },
            {
                "title": "Prime Number Check",
                "difficulty": "Medium",
                "description": """Write a C program that reads an integer `n` and determines whether it is a prime number.

A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.

**Input Format:**
- A single integer `n` (2 ≤ n ≤ 10000)

**Output Format:**
- Print "Prime" if the number is prime
- Print "Not Prime" if the number is not prime

**Example:**
```
Input:
7

Output:
Prime
```""",
                "constraints": "2 ≤ n ≤ 10000",
                "visible_tests": [
                    {"input": "7", "output": "Prime"},
                    {"input": "4", "output": "Not Prime"},
                    {"input": "2", "output": "Prime"},
                ],
                "hidden_tests": [
                    {"input": "13", "output": "Prime"},
                    {"input": "100", "output": "Not Prime"},
                    {"input": "97", "output": "Prime"},
                    {"input": "1000", "output": "Not Prime"},
                    {"input": "101", "output": "Prime"},
                    {"input": "49", "output": "Not Prime"},
                    {"input": "53", "output": "Prime"},
                    {"input": "121", "output": "Not Prime"},
                    {"input": "17", "output": "Prime"},
                    {"input": "9999", "output": "Not Prime"},
                ]
            },
            {
                "title": "Factorial Calculation",
                "difficulty": "Easy",
                "description": """Write a C program that reads an integer `n` and calculates its factorial.

The factorial of n (denoted n!) is the product of all positive integers less than or equal to n.
For example: 5! = 5 × 4 × 3 × 2 × 1 = 120

**Input Format:**
- A single integer `n` (0 ≤ n ≤ 20)

**Output Format:**
- Print the factorial of n as a long integer

**Example:**
```
Input:
5

Output:
120
```

**Note:** Use `long long` or `unsigned long long` to handle large factorials.""",
                "constraints": "0 ≤ n ≤ 20",
                "visible_tests": [
                    {"input": "5", "output": "120"},
                    {"input": "0", "output": "1"},
                    {"input": "1", "output": "1"},
                ],
                "hidden_tests": [
                    {"input": "10", "output": "3628800"},
                    {"input": "3", "output": "6"},
                    {"input": "7", "output": "5040"},
                    {"input": "12", "output": "479001600"},
                    {"input": "15", "output": "1307674368000"},
                    {"input": "4", "output": "24"},
                    {"input": "8", "output": "40320"},
                    {"input": "2", "output": "2"},
                    {"input": "6", "output": "720"},
                    {"input": "20", "output": "2432902008176640000"},
                ]
            },
            {
                "title": "Fibonacci Sequence",
                "difficulty": "Medium",
                "description": """Write a C program that reads an integer `n` and prints the first `n` numbers in the Fibonacci sequence.

The Fibonacci sequence is: 0, 1, 1, 2, 3, 5, 8, 13, 21, ...
where each number is the sum of the two preceding ones.

**Input Format:**
- A single integer `n` (1 ≤ n ≤ 30)

**Output Format:**
- Print the first n Fibonacci numbers, space-separated, on a single line

**Example:**
```
Input:
7

Output:
0 1 1 2 3 5 8
```""",
                "constraints": "1 ≤ n ≤ 30",
                "visible_tests": [
                    {"input": "7", "output": "0 1 1 2 3 5 8"},
                    {"input": "1", "output": "0"},
                    {"input": "2", "output": "0 1"},
                ],
                "hidden_tests": [
                    {"input": "10", "output": "0 1 1 2 3 5 8 13 21 34"},
                    {"input": "5", "output": "0 1 1 2 3"},
                    {"input": "3", "output": "0 1 1"},
                    {"input": "15", "output": "0 1 1 2 3 5 8 13 21 34 55 89 144 233 377"},
                    {"input": "8", "output": "0 1 1 2 3 5 8 13"},
                    {"input": "12", "output": "0 1 1 2 3 5 8 13 21 34 55 89"},
                    {"input": "4", "output": "0 1 1 2"},
                    {"input": "20", "output": "0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181"},
                ]
            },
            {
                "title": "Matrix Addition",
                "difficulty": "Hard",
                "description": """Write a C program that reads two matrices of the same dimensions and prints their sum.

**Input Format:**
- First line: two integers `rows` and `cols` (1 ≤ rows, cols ≤ 10)
- Next `rows` lines: `cols` space-separated integers (first matrix)
- Next `rows` lines: `cols` space-separated integers (second matrix)

**Output Format:**
- Print the resulting matrix (sum of the two matrices)
- Each row on a separate line with space-separated integers

**Example:**
```
Input:
2 3
1 2 3
4 5 6
7 8 9
10 11 12

Output:
8 10 12
14 16 18
```""",
                "constraints": "1 ≤ rows, cols ≤ 10, -100 ≤ each element ≤ 100",
                "visible_tests": [
                    {"input": "2 3\n1 2 3\n4 5 6\n7 8 9\n10 11 12", "output": "8 10 12\n14 16 18"},
                    {"input": "1 1\n5\n3", "output": "8"},
                    {"input": "2 2\n1 2\n3 4\n5 6\n7 8", "output": "6 8\n10 12"},
                ],
                "hidden_tests": [
                    {"input": "3 3\n1 0 0\n0 1 0\n0 0 1\n1 0 0\n0 1 0\n0 0 1", "output": "2 0 0\n0 2 0\n0 0 2"},
                    {"input": "2 4\n1 2 3 4\n5 6 7 8\n9 10 11 12\n13 14 15 16", "output": "10 12 14 16\n18 20 22 24"},
                    {"input": "3 2\n-1 -2\n-3 -4\n-5 -6\n1 2\n3 4\n5 6", "output": "0 0\n0 0\n0 0"},
                    {"input": "1 5\n1 2 3 4 5\n5 4 3 2 1", "output": "6 6 6 6 6"},
                    {"input": "4 1\n10\n20\n30\n40\n5\n5\n5\n5", "output": "15\n25\n35\n45"},
                    {"input": "2 2\n100 -50\n-25 75\n-100 50\n25 -75", "output": "0 0\n0 0"},
                    {"input": "3 3\n1 2 3\n4 5 6\n7 8 9\n9 8 7\n6 5 4\n3 2 1", "output": "10 10 10\n10 10 10\n10 10 10"},
                ]
            },
            {
                "title": "String Palindrome Check",
                "difficulty": "Medium",
                "description": """Write a C program that reads a string and determines if it is a palindrome.

A palindrome is a word, phrase, or sequence that reads the same backward as forward (ignoring spaces and case).

**Input Format:**
- A single line containing a string (up to 100 characters)

**Output Format:**
- Print "Palindrome" if the string is a palindrome
- Print "Not Palindrome" otherwise

**Note:** Consider only alphabetic characters and ignore case.

**Example:**
```
Input:
racecar

Output:
Palindrome
```""",
                "constraints": "String length ≤ 100 characters",
                "visible_tests": [
                    {"input": "racecar", "output": "Palindrome"},
                    {"input": "hello", "output": "Not Palindrome"},
                    {"input": "A", "output": "Palindrome"},
                ],
                "hidden_tests": [
                    {"input": "Racecar", "output": "Palindrome"},
                    {"input": "A man a plan a canal Panama", "output": "Palindrome"},
                    {"input": "Was it a car or a cat I saw", "output": "Palindrome"},
                    {"input": "programming", "output": "Not Palindrome"},
                    {"input": "noon", "output": "Palindrome"},
                    {"input": "level", "output": "Palindrome"},
                    {"input": "world", "output": "Not Palindrome"},
                    {"input": "Madam", "output": "Palindrome"},
                    {"input": "Step on no pets", "output": "Palindrome"},
                    {"input": "abcdefg", "output": "Not Palindrome"},
                ]
            },
            {
                "title": "Bubble Sort",
                "difficulty": "Hard",
                "description": """Write a C program that reads an integer `n`, followed by `n` integers, and sorts them in ascending order using the bubble sort algorithm.

**Bubble Sort Algorithm:**
Repeatedly step through the list, compare adjacent elements and swap them if they are in the wrong order. Repeat until the list is sorted.

**Input Format:**
- First line: integer `n` (1 ≤ n ≤ 100)
- Second line: `n` space-separated integers

**Output Format:**
- Print the sorted integers, space-separated, on a single line

**Example:**
```
Input:
5
64 34 25 12 22

Output:
12 22 25 34 64
```""",
                "constraints": "1 ≤ n ≤ 100, -1000 ≤ each integer ≤ 1000",
                "visible_tests": [
                    {"input": "5\n64 34 25 12 22", "output": "12 22 25 34 64"},
                    {"input": "3\n3 2 1", "output": "1 2 3"},
                    {"input": "1\n42", "output": "42"},
                ],
                "hidden_tests": [
                    {"input": "6\n-5 10 -3 7 2 -8", "output": "-8 -5 -3 2 7 10"},
                    {"input": "4\n1 1 1 1", "output": "1 1 1 1"},
                    {"input": "7\n100 50 75 25 90 10 60", "output": "10 25 50 60 75 90 100"},
                    {"input": "5\n5 4 3 2 1", "output": "1 2 3 4 5"},
                    {"input": "8\n-10 -20 -30 40 30 20 10 0", "output": "-30 -20 -10 0 10 20 30 40"},
                    {"input": "2\n100 -100", "output": "-100 100"},
                    {"input": "10\n9 7 5 3 1 2 4 6 8 10", "output": "1 2 3 4 5 6 7 8 9 10"},
                    {"input": "6\n0 0 0 1 1 1", "output": "0 0 0 1 1 1"},
                ]
            },
        ]

        print("Adding exam-grade problems to database...\n")

        for prob_data in problems:
            # Check if problem already exists
            existing = db.query(models.Problem).filter(
                models.Problem.title == prob_data["title"]
            ).first()

            if existing:
                print(f"⚠ Skipping '{prob_data['title']}' - already exists")
                continue

            # Create problem
            problem = models.Problem(
                title=prob_data["title"],
                description=prob_data["description"],
                difficulty=prob_data["difficulty"],
                constraints=prob_data["constraints"]
            )
            db.add(problem)
            db.flush()  # Get the problem ID

            # Add visible test cases
            for i, test in enumerate(prob_data["visible_tests"]):
                test_case = models.TestCase(
                    problem_id=problem.id,
                    input=test["input"],
                    expected_output=test["output"],
                    is_hidden=False,
                    display_order=i
                )
                db.add(test_case)

            # Add hidden test cases
            for i, test in enumerate(prob_data["hidden_tests"]):
                test_case = models.TestCase(
                    problem_id=problem.id,
                    input=test["input"],
                    expected_output=test["output"],
                    is_hidden=True,
                    display_order=i
                )
                db.add(test_case)

            db.commit()

            visible_count = len(prob_data["visible_tests"])
            hidden_count = len(prob_data["hidden_tests"])
            print(f"✓ Added '{prob_data['title']}' ({prob_data['difficulty']})")
            print(f"  - {visible_count} visible test cases")
            print(f"  - {hidden_count} hidden test cases\n")

        print("=" * 60)
        print("✅ All exam problems added successfully!")
        print("=" * 60)

        # Print summary
        total_problems = db.query(models.Problem).count()
        print(f"\nTotal problems in database: {total_problems}")

        easy = db.query(models.Problem).filter(models.Problem.difficulty == "Easy").count()
        medium = db.query(models.Problem).filter(models.Problem.difficulty == "Medium").count()
        hard = db.query(models.Problem).filter(models.Problem.difficulty == "Hard").count()

        print(f"  - Easy: {easy}")
        print(f"  - Medium: {medium}")
        print(f"  - Hard: {hard}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Adding Exam-Grade C Programming Problems")
    print("=" * 60)
    print()
    add_exam_problems()
