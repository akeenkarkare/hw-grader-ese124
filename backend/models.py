from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, JSON, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String(20), nullable=False, default="student")  # admin or student
    created_at = Column(DateTime, default=datetime.utcnow)

    submissions = relationship("Submission", back_populates="user", cascade="all, delete-orphan")
    user_test_cases = relationship("UserTestCase", back_populates="user", cascade="all, delete-orphan")

class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False)  # easy, medium, hard
    constraints = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    test_cases = relationship("TestCase", back_populates="problem", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="problem", cascade="all, delete-orphan")
    user_test_cases = relationship("UserTestCase", back_populates="problem", cascade="all, delete-orphan")

class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, index=True)
    input = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    is_hidden = Column(Boolean, default=False, index=True)
    display_order = Column(Integer, default=0)

    problem = relationship("Problem", back_populates="test_cases")

    __table_args__ = (
        Index('ix_testcase_problem_hidden', 'problem_id', 'is_hidden'),
    )

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, index=True)
    code = Column(Text, nullable=False)
    score = Column(Float, default=0.0)  # percentage 0-100
    status = Column(String(50), nullable=False)  # completed, compilation_error, error
    results = Column(JSON)  # JSON with detailed results
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")

    __table_args__ = (
        Index('ix_submission_user_problem', 'user_id', 'problem_id', 'created_at'),
    )

class UserTestCase(Base):
    __tablename__ = "user_test_cases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, index=True)
    input = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)

    user = relationship("User", back_populates="user_test_cases")
    problem = relationship("Problem", back_populates="user_test_cases")

    __table_args__ = (
        Index('ix_usertestcase_user_problem', 'user_id', 'problem_id'),
    )

