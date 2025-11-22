export  interface FileNode {
  kind: string,
  name: string,
  source_code: string,
  language_id: number,
  id: string
}

export interface FolderNode{
  kind: string,
  id: string,
  children: string[],
  name: string,
}

export type Data = {
  language_id: number,
  additional_files: DataNode[],
  compile_id: string,
  run_id: string,
}

export type DataNode = FileNode|FolderNode

/*
id = Column(Integer, primary_key=True, index=True)
problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, index=True)
input = Column(Text, nullable=False)
expected_output = Column(Text, nullable=False)
is_hidden = Column(Boolean, default=False, index=True)
display_order = Column(Integer, default=0)

problem = relationship("Problem", back_populates="test_cases")*/

// Base test case fields
export interface TestCaseBase {
  input: string;
  expected_output: string;
  is_hidden: boolean;
  display_order: number;
}

// Full test case with all fields (from backend)
export interface TestCaseResponse extends TestCaseBase {
  id: number;
  problem_id: number;
}

// Public test case (visible to students)
export interface TestCasePublic {
  id: number;
  input: string;
  expected_output: string;
  display_order: number;
}

// Alias for backward compatibility
export type TestCase = TestCaseResponse;

export enum Status {
  COMPLETED = "completed",
  COMPILATION_ERROR = "compilation_error",
  ERROR = "error"
}

export interface SubmissionResponse {
  id: number;
  user_id: number;
  problem_id: number;
  code: string;
  score: number; // percentage 0-100 (float)
  status: string; // "completed" | "compilation_error" | "error"
  results?: any; // Can be dict/list (JSON) or string
  created_at: string; // ISO datetime string from backend
} 
export enum Difficulty {
  EASY = "easy",
  MEDIUM = "medium",
  HARD = "hard"
}

export interface ProblemBase {
  title: string;
  description: string;
  difficulty: string;
  constraints?: string;
}

export interface ProblemResponse extends ProblemBase {
  id: number;
  created_at: string; // ISO datetime string
  test_cases: TestCaseResponse[];
}

export interface ProblemPublic extends ProblemBase {
  id: number;
  created_at: string; // ISO datetime string
  visible_test_cases: TestCasePublic[];
}

// Additional Files for multi-file submissions
export interface AdditionalFile {
  filename: string;
  content: string; // Base64 encoded file content
}

// Submission Create (request payload)
export interface SubmissionCreate {
  problem_id: number;
  code: string;
  additional_files?: AdditionalFile[];
}

// User Test Case (custom test cases created by students)
export interface UserTestCaseCreate {
  problem_id: number;
  input: string;
  expected_output: string;
}

export interface UserTestCaseResponse {
  id: number;
  user_id: number;
  problem_id: number;
  input: string;
  expected_output: string;
}

// Auth types
export interface UserCreate {
  username: string;
  password: string;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface UserResponse {
  id: number;
  username: string;
  role: string;
  created_at: string; // ISO datetime string
}