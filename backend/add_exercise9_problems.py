"""
Add Exercise 9 problems to the database
These are data structure problems from ESE124 Fall 2025
"""

import sqlite3
import json
from datetime import datetime

def add_problems():
    conn = sqlite3.connect('homework_grader.db')
    cursor = conn.cursor()

    problems = [
        {
            "title": "Reverse K Elements in Queue",
            "description": """Write a C program that reverses the first K elements of a queue (represented as an array).

Input Format:
- First line: N (number of elements in queue)
- Second line: K (number of elements to reverse)
- Third line: N space-separated integers (the queue elements)

Output Format:
- Print the modified queue with first K elements reversed, space-separated

Example:
Input:
9
4
10 20 30 40 50 60 70 80 90

Output:
40 30 20 10 50 60 70 80 90

Constraints:
- 1 ≤ K ≤ N ≤ 100
- Array elements are integers between -1000 and 1000""",
            "difficulty": "Hard",
            "test_cases": [
                # Visible test cases
                {
                    "input": "9\n4\n10 20 30 40 50 60 70 80 90",
                    "expected_output": "40 30 20 10 50 60 70 80 90",
                    "is_hidden": False
                },
                {
                    "input": "5\n3\n1 2 3 4 5",
                    "expected_output": "3 2 1 4 5",
                    "is_hidden": False
                },
                {
                    "input": "6\n6\n10 20 30 40 50 60",
                    "expected_output": "60 50 40 30 20 10",
                    "is_hidden": False
                },
                # Hidden test cases
                {
                    "input": "1\n1\n42",
                    "expected_output": "42",
                    "is_hidden": True
                },
                {
                    "input": "5\n1\n5 4 3 2 1",
                    "expected_output": "5 4 3 2 1",
                    "is_hidden": True
                },
                {
                    "input": "10\n5\n1 2 3 4 5 6 7 8 9 10",
                    "expected_output": "5 4 3 2 1 6 7 8 9 10",
                    "is_hidden": True
                },
                {
                    "input": "7\n4\n-10 -20 -30 -40 50 60 70",
                    "expected_output": "-40 -30 -20 -10 50 60 70",
                    "is_hidden": True
                },
                {
                    "input": "8\n8\n100 200 300 400 500 600 700 800",
                    "expected_output": "800 700 600 500 400 300 200 100",
                    "is_hidden": True
                },
                {
                    "input": "4\n2\n15 25 35 45",
                    "expected_output": "25 15 35 45",
                    "is_hidden": True
                },
                {
                    "input": "10\n7\n9 8 7 6 5 4 3 2 1 0",
                    "expected_output": "3 4 5 6 7 8 9 2 1 0",
                    "is_hidden": True
                }
            ]
        },
        {
            "title": "Hospital Priority Queue",
            "description": """Write a C program that simulates a hospital priority queue. Lower severity number = higher priority.
If two patients have the same severity, the one who arrived earlier has priority.

Input Format:
- First line: N (number of patients)
- Next N lines: patient_id name severity (e.g., "101 Alice 3")
- Next line: D (number of dequeues to perform)

Output Format:
- Print "Initial queue:" followed by all patients in arrival order
- Print "Dequeued:" followed by D patients in priority order (lowest severity first, then by arrival)
- Print "Remaining:" followed by remaining patients in arrival order

Example:
Input:
6
101 Alice 3
102 Bob 1
103 Carol 2
104 Dave 5
105 Erin 1
106 Frank 4
3

Output:
Initial queue:
[101] Alice sev=3
[102] Bob sev=1
[103] Carol sev=2
[104] Dave sev=5
[105] Erin sev=1
[106] Frank sev=4
Dequeued:
[102] Bob sev=1
[105] Erin sev=1
[103] Carol sev=2
Remaining:
[101] Alice sev=3
[106] Frank sev=4
[104] Dave sev=5

Constraints:
- 1 ≤ N ≤ 50
- 0 ≤ D ≤ N
- Patient IDs are positive integers
- Names have no spaces (max 20 characters)
- Severity is 1-10""",
            "difficulty": "Hard",
            "test_cases": [
                # Visible test cases
                {
                    "input": "6\n101 Alice 3\n102 Bob 1\n103 Carol 2\n104 Dave 5\n105 Erin 1\n106 Frank 4\n3",
                    "expected_output": "Initial queue:\n[101] Alice sev=3\n[102] Bob sev=1\n[103] Carol sev=2\n[104] Dave sev=5\n[105] Erin sev=1\n[106] Frank sev=4\nDequeued:\n[102] Bob sev=1\n[105] Erin sev=1\n[103] Carol sev=2\nRemaining:\n[101] Alice sev=3\n[106] Frank sev=4\n[104] Dave sev=5",
                    "is_hidden": False
                },
                {
                    "input": "3\n201 John 2\n202 Jane 1\n203 Jack 3\n2",
                    "expected_output": "Initial queue:\n[201] John sev=2\n[202] Jane sev=1\n[203] Jack sev=3\nDequeued:\n[202] Jane sev=1\n[201] John sev=2\nRemaining:\n[203] Jack sev=3",
                    "is_hidden": False
                },
                {
                    "input": "4\n301 Amy 5\n302 Ben 5\n303 Cara 5\n304 Dan 5\n2",
                    "expected_output": "Initial queue:\n[301] Amy sev=5\n[302] Ben sev=5\n[303] Cara sev=5\n[304] Dan sev=5\nDequeued:\n[301] Amy sev=5\n[302] Ben sev=5\nRemaining:\n[303] Cara sev=5\n[304] Dan sev=5",
                    "is_hidden": False
                },
                # Hidden test cases
                {
                    "input": "2\n401 Tom 1\n402 Tim 2\n1",
                    "expected_output": "Initial queue:\n[401] Tom sev=1\n[402] Tim sev=2\nDequeued:\n[401] Tom sev=1\nRemaining:\n[402] Tim sev=2",
                    "is_hidden": True
                },
                {
                    "input": "5\n501 A 3\n502 B 1\n503 C 2\n504 D 1\n505 E 3\n5",
                    "expected_output": "Initial queue:\n[501] A sev=3\n[502] B sev=1\n[503] C sev=2\n[504] D sev=1\n[505] E sev=3\nDequeued:\n[502] B sev=1\n[504] D sev=1\n[503] C sev=2\n[501] A sev=3\n[505] E sev=3\nRemaining:",
                    "is_hidden": True
                },
                {
                    "input": "1\n601 Solo 7\n0",
                    "expected_output": "Initial queue:\n[601] Solo sev=7\nDequeued:\nRemaining:\n[601] Solo sev=7",
                    "is_hidden": True
                },
                {
                    "input": "4\n701 X 10\n702 Y 1\n703 Z 5\n704 W 1\n3",
                    "expected_output": "Initial queue:\n[701] X sev=10\n[702] Y sev=1\n[703] Z sev=5\n[704] W sev=1\nDequeued:\n[702] Y sev=1\n[704] W sev=1\n[703] Z sev=5\nRemaining:\n[701] X sev=10",
                    "is_hidden": True
                },
                {
                    "input": "3\n801 P1 2\n802 P2 2\n803 P3 2\n1",
                    "expected_output": "Initial queue:\n[801] P1 sev=2\n[802] P2 sev=2\n[803] P3 sev=2\nDequeued:\n[801] P1 sev=2\nRemaining:\n[802] P2 sev=2\n[803] P3 sev=2",
                    "is_hidden": True
                },
                {
                    "input": "5\n901 First 4\n902 Second 3\n903 Third 2\n904 Fourth 1\n905 Fifth 5\n4",
                    "expected_output": "Initial queue:\n[901] First sev=4\n[902] Second sev=3\n[903] Third sev=2\n[904] Fourth sev=1\n[905] Fifth sev=5\nDequeued:\n[904] Fourth sev=1\n[903] Third sev=2\n[902] Second sev=3\n[901] First sev=4\nRemaining:\n[905] Fifth sev=5",
                    "is_hidden": True
                },
                {
                    "input": "6\n111 Alpha 6\n222 Beta 4\n333 Gamma 4\n444 Delta 6\n555 Epsilon 4\n666 Zeta 6\n3",
                    "expected_output": "Initial queue:\n[111] Alpha sev=6\n[222] Beta sev=4\n[333] Gamma sev=4\n[444] Delta sev=6\n[555] Epsilon sev=4\n[666] Zeta sev=6\nDequeued:\n[222] Beta sev=4\n[333] Gamma sev=4\n[555] Epsilon sev=4\nRemaining:\n[111] Alpha sev=6\n[444] Delta sev=6\n[666] Zeta sev=6",
                    "is_hidden": True
                }
            ]
        },
        {
            "title": "Stack Transformation Sequence",
            "description": """Write a C program that transforms a stack s1 into s3 using s2 as auxiliary storage.

Input Format:
- First line: N (number of elements, always 4)
- Second line: N characters representing initial stack s1 (top to bottom)
- Third line: N characters representing desired final stack s3 (top to bottom)

Output Format:
- If transformation is possible, print the sequence of operations, one per line:
  - "s2.push(s1.pop())" - move top of s1 to s2
  - "s3.push(s1.pop())" - move top of s1 to s3
  - "s3.push(s2.pop())" - move top of s2 to s3
  - "s1.push(s2.pop())" - move top of s2 to s1
- If transformation is impossible, print "IMPOSSIBLE"

Example:
Input:
4
ABCD
ABDC

Output:
s2.push(s1.pop())
s2.push(s1.pop())
s3.push(s1.pop())
s3.push(s1.pop())
s3.push(s2.pop())
s3.push(s2.pop())

Constraints:
- N is always 4
- Elements are single uppercase letters A-Z
- s2 must be empty at the end""",
            "difficulty": "Hard",
            "test_cases": [
                # Visible test cases
                {
                    "input": "4\nABCD\nABDC",
                    "expected_output": "s2.push(s1.pop())\ns2.push(s1.pop())\ns3.push(s1.pop())\ns3.push(s1.pop())\ns3.push(s2.pop())\ns3.push(s2.pop())",
                    "is_hidden": False
                },
                {
                    "input": "4\nABCD\nBDAC",
                    "expected_output": "s2.push(s1.pop())\ns3.push(s1.pop())\ns2.push(s1.pop())\ns3.push(s2.pop())\ns3.push(s1.pop())\ns3.push(s2.pop())",
                    "is_hidden": False
                },
                {
                    "input": "4\nABCD\nDCBA",
                    "expected_output": "s3.push(s1.pop())\ns3.push(s1.pop())\ns3.push(s1.pop())\ns3.push(s1.pop())",
                    "is_hidden": False
                },
                # Hidden test cases
                {
                    "input": "4\nABCD\nABCD",
                    "expected_output": "s2.push(s1.pop())\ns2.push(s1.pop())\ns2.push(s1.pop())\ns2.push(s1.pop())\ns3.push(s2.pop())\ns3.push(s2.pop())\ns3.push(s2.pop())\ns3.push(s2.pop())",
                    "is_hidden": True
                },
                {
                    "input": "4\nXYZW\nWZYX",
                    "expected_output": "s3.push(s1.pop())\ns3.push(s1.pop())\ns3.push(s1.pop())\ns3.push(s1.pop())",
                    "is_hidden": True
                },
                {
                    "input": "4\nPQRS\nPQSR",
                    "expected_output": "s2.push(s1.pop())\ns2.push(s1.pop())\ns3.push(s1.pop())\ns3.push(s1.pop())\ns3.push(s2.pop())\ns3.push(s2.pop())",
                    "is_hidden": True
                },
                {
                    "input": "4\nMNOP\nPONM",
                    "expected_output": "s3.push(s1.pop())\ns3.push(s1.pop())\ns3.push(s1.pop())\ns3.push(s1.pop())",
                    "is_hidden": True
                },
                {
                    "input": "4\nEFGH\nEGFH",
                    "expected_output": "s2.push(s1.pop())\ns3.push(s1.pop())\ns3.push(s1.pop())\ns3.push(s2.pop())\ns2.push(s1.pop())\ns3.push(s2.pop())",
                    "is_hidden": True
                },
                {
                    "input": "4\nIJKL\nKJIL",
                    "expected_output": "s2.push(s1.pop())\ns2.push(s1.pop())\ns2.push(s1.pop())\ns3.push(s2.pop())\ns3.push(s2.pop())\ns3.push(s2.pop())\ns3.push(s1.pop())",
                    "is_hidden": True
                },
                {
                    "input": "4\nSTUV\nVUTS",
                    "expected_output": "s3.push(s1.pop())\ns3.push(s1.pop())\ns3.push(s1.pop())\ns3.push(s1.pop())",
                    "is_hidden": True
                }
            ]
        }
    ]

    for problem in problems:
        # Insert problem
        cursor.execute("""
            INSERT INTO problems (title, description, difficulty, constraints, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            problem["title"],
            problem["description"],
            problem["difficulty"],
            problem.get("constraints", ""),
            datetime.utcnow()
        ))

        problem_id = cursor.lastrowid
        print(f"Added problem: {problem['title']} (ID: {problem_id})")

        # Insert test cases
        for test_case in problem["test_cases"]:
            cursor.execute("""
                INSERT INTO test_cases (problem_id, input, expected_output, is_hidden)
                VALUES (?, ?, ?, ?)
            """, (
                problem_id,
                test_case["input"],
                test_case["expected_output"],
                test_case["is_hidden"]
            ))

        visible_count = sum(1 for tc in problem["test_cases"] if not tc["is_hidden"])
        hidden_count = sum(1 for tc in problem["test_cases"] if tc["is_hidden"])
        print(f"  Added {visible_count} visible and {hidden_count} hidden test cases")

    conn.commit()
    conn.close()
    print("\nAll Exercise 9 problems added successfully!")

if __name__ == "__main__":
    add_problems()
