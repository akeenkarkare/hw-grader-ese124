"""
Database migration script to update existing database to new schema.
Run this after updating models.py to migrate existing data.
"""
import sqlite3
import json
import os
from pathlib import Path

DB_PATH = "homework_grader.db"

def migrate_database():
    """Migrate database to new schema"""
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found. No migration needed.")
        print("Run seed.py to create a new database.")
        return

    print(f"Migrating database: {DB_PATH}")

    # Backup database
    backup_path = f"{DB_PATH}.backup"
    import shutil
    shutil.copy2(DB_PATH, backup_path)
    print(f"✓ Created backup: {backup_path}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check if migration is needed by checking if results column is TEXT
        cursor.execute("PRAGMA table_info(submissions)")
        columns = cursor.fetchall()
        results_col = next((col for col in columns if col[1] == 'results'), None)

        if results_col and results_col[2] == 'TEXT':
            print("Migration needed: Converting TEXT results to JSON...")

            # Create new table with JSON column
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS submissions_new (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    problem_id INTEGER NOT NULL,
                    code TEXT NOT NULL,
                    score REAL DEFAULT 0.0,
                    status VARCHAR(50) NOT NULL,
                    results JSON,
                    created_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (problem_id) REFERENCES problems(id) ON DELETE CASCADE
                )
            """)

            # Copy data, converting TEXT to JSON
            cursor.execute("SELECT * FROM submissions")
            submissions = cursor.fetchall()

            for sub in submissions:
                sub_id, user_id, problem_id, code, score, status, results_text, created_at = sub

                # Parse results if it's a JSON string
                if results_text:
                    try:
                        results_json = json.loads(results_text)
                    except:
                        results_json = {"error": results_text}
                else:
                    results_json = None

                cursor.execute("""
                    INSERT INTO submissions_new
                    (id, user_id, problem_id, code, score, status, results, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (sub_id, user_id, problem_id, code, score, status,
                      json.dumps(results_json) if results_json else None, created_at))

            # Drop old table and rename new one
            cursor.execute("DROP TABLE submissions")
            cursor.execute("ALTER TABLE submissions_new RENAME TO submissions")

            print(f"✓ Migrated {len(submissions)} submissions")
        else:
            print("✓ No migration needed - database already up to date")

        # Add indexes if they don't exist
        print("\nAdding indexes...")

        indexes = [
            ("CREATE INDEX IF NOT EXISTS ix_testcase_problem_hidden ON test_cases(problem_id, is_hidden)", "test_cases compound index"),
            ("CREATE INDEX IF NOT EXISTS ix_submission_user_problem ON submissions(user_id, problem_id, created_at)", "submissions compound index"),
            ("CREATE INDEX IF NOT EXISTS ix_usertestcase_user_problem ON user_test_cases(user_id, problem_id)", "user_test_cases compound index"),
            ("CREATE INDEX IF NOT EXISTS ix_problems_created_at ON problems(created_at)", "problems created_at index"),
            ("CREATE INDEX IF NOT EXISTS ix_submissions_created_at ON submissions(created_at)", "submissions created_at index"),
            ("CREATE INDEX IF NOT EXISTS ix_test_cases_problem_id ON test_cases(problem_id)", "test_cases problem_id index"),
            ("CREATE INDEX IF NOT EXISTS ix_submissions_user_id ON submissions(user_id)", "submissions user_id index"),
            ("CREATE INDEX IF NOT EXISTS ix_submissions_problem_id ON submissions(problem_id)", "submissions problem_id index"),
            ("CREATE INDEX IF NOT EXISTS ix_user_test_cases_user_id ON user_test_cases(user_id)", "user_test_cases user_id index"),
            ("CREATE INDEX IF NOT EXISTS ix_user_test_cases_problem_id ON user_test_cases(problem_id)", "user_test_cases problem_id index"),
            ("CREATE INDEX IF NOT EXISTS ix_test_cases_is_hidden ON test_cases(is_hidden)", "test_cases is_hidden index"),
        ]

        for sql, desc in indexes:
            try:
                cursor.execute(sql)
                print(f"  ✓ {desc}")
            except Exception as e:
                print(f"  ⚠ {desc}: {e}")

        conn.commit()
        print("\n✅ Migration completed successfully!")
        print(f"Backup saved at: {backup_path}")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Migration failed: {e}")
        print(f"Database restored from backup: {backup_path}")
        shutil.copy2(backup_path, DB_PATH)
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration Script")
    print("=" * 60)
    print()

    response = input("This will modify your database. Continue? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        migrate_database()
    else:
        print("Migration cancelled.")
