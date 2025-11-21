from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from datetime import datetime

# Auth Schemas
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Problem Schemas
class TestCaseBase(BaseModel):
    input: str
    expected_output: str
    is_hidden: bool = False
    display_order: Optional[int] = 0

class TestCaseCreate(TestCaseBase):
    pass

class TestCaseResponse(TestCaseBase):
    id: int
    problem_id: int
    
    class Config:
        from_attributes = True

class TestCasePublic(BaseModel):
    id: int
    input: str
    expected_output: str
    display_order: Optional[int] = 0

    class Config:
        from_attributes = True

class ProblemBase(BaseModel):
    title: str
    description: str
    difficulty: str
    constraints: Optional[str] = None

class ProblemCreate(ProblemBase):
    pass

class ProblemUpdate(ProblemBase):
    pass

class ProblemResponse(ProblemBase):
    id: int
    created_at: datetime
    test_cases: List[TestCaseResponse] = []
    
    class Config:
        from_attributes = True

class ProblemPublic(ProblemBase):
    id: int
    created_at: datetime
    visible_test_cases: List[TestCasePublic] = []
    
    class Config:
        from_attributes = True

# Submission Schemas
class AdditionalFile(BaseModel):
    filename: str
    content: str  # Base64 encoded file content

class SubmissionCreate(BaseModel):
    problem_id: int
    code: str
    additional_files: Optional[List[AdditionalFile]] = None  # For multi-file programs (ADT, headers, etc.)

class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    problem_id: int
    code: str
    score: float
    status: str
    results: Optional[Any] = None  # Can be dict/list (JSON) or string (for backward compatibility)
    created_at: datetime

    class Config:
        from_attributes = True

# User Test Case Schemas
class UserTestCaseCreate(BaseModel):
    problem_id: int
    input: str
    expected_output: str

class UserTestCaseResponse(BaseModel):
    id: int
    user_id: int
    problem_id: int
    input: str
    expected_output: str
    
    class Config:
        from_attributes = True

