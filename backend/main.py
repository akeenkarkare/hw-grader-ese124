from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json
import logging
import os
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import models
import schemas
from database import get_db, init_db
from auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_admin
)
from judge0_client import judge0_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Homework Grader API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Health check
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Homework Grader API"}

# ==================== Auth Routes ====================

@app.post("/api/auth/register", response_model=schemas.UserResponse)
@limiter.limit("5/minute")
def register(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Registration attempt for username: {user.username}")

    # Validate username and password
    if len(user.username) < 3 or len(user.username) > 50:
        raise HTTPException(status_code=400, detail="Username must be between 3 and 50 characters")
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    # Check if username already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        logger.warning(f"Registration failed: Username {user.username} already exists")
        raise HTTPException(status_code=400, detail="Username already registered")

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        password_hash=hashed_password,
        role="student"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User registered successfully: {user.username}")
    return db_user

@app.post("/api/auth/login", response_model=schemas.Token)
@limiter.limit("10/minute")
def login(request: Request, user: schemas.UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Login attempt for username: {user.username}")
    db_user = authenticate_user(db, user.username, user.password)
    if not db_user:
        logger.warning(f"Login failed for username: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(
        data={"sub": db_user.username, "role": db_user.role}
    )
    logger.info(f"Login successful for username: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# ==================== Admin Routes ====================

@app.post("/api/admin/problems", response_model=schemas.ProblemResponse)
def create_problem(
    problem: schemas.ProblemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)
):
    db_problem = models.Problem(**problem.dict())
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem

@app.get("/api/admin/problems", response_model=List[schemas.ProblemResponse])
def get_all_problems_admin(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)
):
    problems = db.query(models.Problem).all()
    return problems

@app.get("/api/admin/problems/{problem_id}", response_model=schemas.ProblemResponse)
def get_problem_admin(
    problem_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)
):
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@app.put("/api/admin/problems/{problem_id}", response_model=schemas.ProblemResponse)
def update_problem(
    problem_id: int,
    problem_update: schemas.ProblemUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)
):
    logger.info(f"Admin {current_user.username} updating problem {problem_id}")
    db_problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Explicitly update only allowed fields
    update_data = problem_update.dict(exclude_unset=True)
    allowed_fields = {'title', 'description', 'difficulty', 'constraints'}
    for key, value in update_data.items():
        if key in allowed_fields:
            setattr(db_problem, key, value)

    db.commit()
    db.refresh(db_problem)
    logger.info(f"Problem {problem_id} updated successfully")
    return db_problem

@app.delete("/api/admin/problems/{problem_id}")
def delete_problem(
    problem_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)
):
    db_problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    db.delete(db_problem)
    db.commit()
    return {"message": "Problem deleted successfully"}

@app.post("/api/admin/problems/{problem_id}/testcases", response_model=schemas.TestCaseResponse)
def create_test_case(
    problem_id: int,
    test_case: schemas.TestCaseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)
):
    # Verify problem exists
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    db_test_case = models.TestCase(**test_case.dict(), problem_id=problem_id)
    db.add(db_test_case)
    db.commit()
    db.refresh(db_test_case)
    return db_test_case

@app.delete("/api/admin/testcases/{testcase_id}")
def delete_test_case(
    testcase_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)
):
    test_case = db.query(models.TestCase).filter(models.TestCase.id == testcase_id).first()
    if not test_case:
        raise HTTPException(status_code=404, detail="Test case not found")
    
    db.delete(test_case)
    db.commit()
    return {"message": "Test case deleted successfully"}

@app.get("/api/admin/submissions", response_model=List[schemas.SubmissionResponse])
def get_all_submissions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)
):
    submissions = db.query(models.Submission).order_by(models.Submission.created_at.desc()).all()
    return submissions

# ==================== Student Routes ====================

@app.get("/api/problems", response_model=List[schemas.ProblemPublic])
def get_problems(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    problems = db.query(models.Problem).all()
    result = []
    for problem in problems:
        visible_test_cases = [
            tc for tc in problem.test_cases
            if not tc.is_hidden
        ]
        visible_test_cases.sort(key=lambda x: x.display_order if x.display_order is not None else 0)
        
        problem_dict = {
            "id": problem.id,
            "title": problem.title,
            "description": problem.description,
            "difficulty": problem.difficulty,
            "constraints": problem.constraints,
            "created_at": problem.created_at,
            "visible_test_cases": visible_test_cases[:3]  # Only show first 3
        }
        result.append(schemas.ProblemPublic(**problem_dict))
    
    return result

@app.get("/api/problems/{problem_id}", response_model=schemas.ProblemPublic)
def get_problem(
    problem_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    visible_test_cases = [
        tc for tc in problem.test_cases
        if not tc.is_hidden
    ]
    # Sort by display_order, treating None as 0
    visible_test_cases.sort(key=lambda x: x.display_order if x.display_order is not None else 0)
    
    problem_dict = {
        "id": problem.id,
        "title": problem.title,
        "description": problem.description,
        "difficulty": problem.difficulty,
        "constraints": problem.constraints,
        "created_at": problem.created_at,
        "visible_test_cases": visible_test_cases[:3]
    }
    
    return schemas.ProblemPublic(**problem_dict)

@app.post("/api/submit", response_model=schemas.SubmissionResponse)
@limiter.limit("10/minute")
async def submit_code(
    request: Request,
    submission: schemas.SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    logger.info(f"User {current_user.username} submitting code for problem {submission.problem_id}")

    # Validate code length (max 50KB)
    if len(submission.code) > 50000:
        raise HTTPException(status_code=400, detail="Code exceeds maximum length of 50KB")

    # Verify problem exists
    problem = db.query(models.Problem).filter(models.Problem.id == submission.problem_id).first()
    if not problem:
        logger.warning(f"Submission failed: Problem {submission.problem_id} not found")
        raise HTTPException(status_code=404, detail="Problem not found")

    # Get only hidden test cases for grading
    hidden_test_cases = [
        {"input": tc.input, "expected_output": tc.expected_output}
        for tc in problem.test_cases
        if tc.is_hidden
    ]

    if not hidden_test_cases:
        logger.error(f"No hidden test cases for problem {submission.problem_id}")
        raise HTTPException(status_code=400, detail="No hidden test cases found for this problem")

    # Execute code against hidden test cases
    try:
        # Convert additional_files from Pydantic models to dicts if present
        additional_files_dict = None
        if submission.additional_files:
            additional_files_dict = [
                {"filename": f.filename, "content": f.content}
                for f in submission.additional_files
            ]

        results = await judge0_client.execute_code(submission.code, hidden_test_cases, additional_files_dict)

        # Check for compilation errors
        compilation_error = next((r for r in results if r.get("compile_output")), None)
        if compilation_error and compilation_error.get("compile_output"):
            # Create submission with compilation error
            db_submission = models.Submission(
                user_id=current_user.id,
                problem_id=submission.problem_id,
                code=submission.code,
                score=0,
                status="compilation_error",
                results=results
            )
            db.add(db_submission)
            db.commit()
            db.refresh(db_submission)
            logger.info(f"Submission {db_submission.id} completed with compilation error")
            return db_submission

        # Calculate score
        passed_count = sum(1 for r in results if r.get("passed", False))
        total_count = len(results)
        score = (passed_count / total_count * 100) if total_count > 0 else 0

        # Create submission record
        db_submission = models.Submission(
            user_id=current_user.id,
            problem_id=submission.problem_id,
            code=submission.code,
            score=score,
            status="completed",
            results=results
        )
        db.add(db_submission)
        db.commit()
        db.refresh(db_submission)

        logger.info(f"Submission {db_submission.id} completed with score {score:.1f}%")
        return db_submission

    except Exception as e:
        logger.error(f"Execution error for user {current_user.username}: {str(e)}")
        # Create error submission record
        db_submission = models.Submission(
            user_id=current_user.id,
            problem_id=submission.problem_id,
            code=submission.code,
            score=0,
            status="error",
            results={"error": str(e)}
        )
        db.add(db_submission)
        db.commit()
        db.refresh(db_submission)

        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")

@app.get("/api/submissions/{submission_id}", response_model=schemas.SubmissionResponse)
def get_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    submission = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Students can only see their own submissions
    if current_user.role != "admin" and submission.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return submission

@app.get("/api/problems/{problem_id}/submissions", response_model=List[schemas.SubmissionResponse])
def get_problem_submissions(
    problem_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    submissions = db.query(models.Submission).filter(
        models.Submission.problem_id == problem_id,
        models.Submission.user_id == current_user.id
    ).order_by(models.Submission.created_at.desc()).all()
    
    return submissions

# ==================== User Test Cases Routes ====================

@app.post("/api/user-testcases", response_model=schemas.UserTestCaseResponse)
def create_user_test_case(
    test_case: schemas.UserTestCaseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_test_case = models.UserTestCase(
        **test_case.dict(),
        user_id=current_user.id
    )
    db.add(db_test_case)
    db.commit()
    db.refresh(db_test_case)
    return db_test_case

@app.get("/api/problems/{problem_id}/user-testcases", response_model=List[schemas.UserTestCaseResponse])
def get_user_test_cases(
    problem_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    test_cases = db.query(models.UserTestCase).filter(
        models.UserTestCase.problem_id == problem_id,
        models.UserTestCase.user_id == current_user.id
    ).all()
    return test_cases

@app.delete("/api/user-testcases/{testcase_id}")
def delete_user_test_case(
    testcase_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    test_case = db.query(models.UserTestCase).filter(
        models.UserTestCase.id == testcase_id,
        models.UserTestCase.user_id == current_user.id
    ).first()
    
    if not test_case:
        raise HTTPException(status_code=404, detail="Test case not found")
    
    db.delete(test_case)
    db.commit()
    return {"message": "Test case deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

