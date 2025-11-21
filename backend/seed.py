"""
Seed script to create initial admin user and sample problem
"""
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from auth import get_password_hash
import models

def seed_database():
    # Initialize database
    init_db()
    
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin:
            # Create admin user
            admin = models.User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                role="admin"
            )
            db.add(admin)
            print("✓ Created admin user (username: admin, password: admin123)")
        else:
            print("✓ Admin user already exists")

        # Check if student test user exists
        student = db.query(models.User).filter(models.User.username == "student").first()
        if not student:
            # Create test student user
            student = models.User(
                username="student",
                password_hash=get_password_hash("student123"),
                role="student"
            )
            db.add(student)
            print("✓ Created student user (username: student, password: student123)")
        else:
            print("✓ Student user already exists")
        
        # Check if sample problem exists
        sample_problem = db.query(models.Problem).filter(models.Problem.title == "Sum of Two Numbers").first()
        if not sample_problem:
            # Create sample problem
            problem = models.Problem(
                title="Sum of Two Numbers",
                description="""# Sum of Two Numbers

Write a C program that reads two integers from standard input and prints their sum.

## Input Format
Two integers separated by a space on a single line.

## Output Format
A single integer representing the sum.

## Example
**Input:**
```
5 3
```

**Output:**
```
8
```

## Constraints
- -1000 ≤ each integer ≤ 1000
""",
                difficulty="easy",
                constraints="-1000 ≤ each integer ≤ 1000"
            )
            db.add(problem)
            db.flush()
            
            # Add visible test cases
            visible_test_cases = [
                models.TestCase(
                    problem_id=problem.id,
                    input="5 3",
                    expected_output="8",
                    is_hidden=False,
                    display_order=1
                ),
                models.TestCase(
                    problem_id=problem.id,
                    input="10 20",
                    expected_output="30",
                    is_hidden=False,
                    display_order=2
                ),
                models.TestCase(
                    problem_id=problem.id,
                    input="-5 5",
                    expected_output="0",
                    is_hidden=False,
                    display_order=3
                ),
            ]
            
            # Add hidden test cases
            hidden_test_cases = [
                models.TestCase(
                    problem_id=problem.id,
                    input="0 0",
                    expected_output="0",
                    is_hidden=True,
                    display_order=4
                ),
                models.TestCase(
                    problem_id=problem.id,
                    input="100 200",
                    expected_output="300",
                    is_hidden=True,
                    display_order=5
                ),
                models.TestCase(
                    problem_id=problem.id,
                    input="-100 -200",
                    expected_output="-300",
                    is_hidden=True,
                    display_order=6
                ),
                models.TestCase(
                    problem_id=problem.id,
                    input="1000 -1000",
                    expected_output="0",
                    is_hidden=True,
                    display_order=7
                ),
                models.TestCase(
                    problem_id=problem.id,
                    input="999 1",
                    expected_output="1000",
                    is_hidden=True,
                    display_order=8
                ),
                models.TestCase(
                    problem_id=problem.id,
                    input="-999 -1",
                    expected_output="-1000",
                    is_hidden=True,
                    display_order=9
                ),
                models.TestCase(
                    problem_id=problem.id,
                    input="42 58",
                    expected_output="100",
                    is_hidden=True,
                    display_order=10
                ),
                models.TestCase(
                    problem_id=problem.id,
                    input="-50 25",
                    expected_output="-25",
                    is_hidden=True,
                    display_order=11
                ),
                models.TestCase(
                    problem_id=problem.id,
                    input="123 456",
                    expected_output="579",
                    is_hidden=True,
                    display_order=12
                ),
                models.TestCase(
                    problem_id=problem.id,
                    input="-123 -456",
                    expected_output="-579",
                    is_hidden=True,
                    display_order=13
                ),
            ]
            
            for tc in visible_test_cases + hidden_test_cases:
                db.add(tc)
            
            print(f"✓ Created sample problem: {problem.title}")
            print(f"  - 3 visible test cases")
            print(f"  - 10 hidden test cases")
        else:
            print("✓ Sample problem already exists")
        
        db.commit()
        print("\n✅ Database seeded successfully!")
        print("\n📝 Login credentials:")
        print("   Admin  - Username: admin,   Password: admin123")
        print("   Student - Username: student, Password: student123")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

