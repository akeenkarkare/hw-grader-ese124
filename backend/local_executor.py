"""
Local C code executor - compiles once and runs multiple test cases
This is MUCH faster than Judge0 for multiple test cases (compiles once vs 13 times)
Supports multiple source files, headers, and stack overflow detection
"""
import subprocess
import tempfile
import os
from typing import List, Dict, Optional
import asyncio
import base64
import signal

class LocalExecutor:
    def __init__(self, timeout: float = 2.0):
        self.timeout = timeout

    def _compare_outputs(self, actual: str, expected: str) -> bool:
        """Compare outputs with whitespace tolerance"""
        actual_lines = [line.rstrip() for line in actual.splitlines()]
        expected_lines = [line.rstrip() for line in expected.splitlines()]

        # Remove trailing empty lines
        while actual_lines and not actual_lines[-1]:
            actual_lines.pop()
        while expected_lines and not expected_lines[-1]:
            expected_lines.pop()

        return actual_lines == expected_lines

    async def execute_code(self, source_code: str, test_cases: List[Dict[str, str]], additional_files: Optional[List[Dict[str, str]]] = None) -> List[Dict]:
        """Compile once and run against all test cases - supports multiple files"""
        results = []

        # Create temporary directory for compilation
        with tempfile.TemporaryDirectory() as tmpdir:
            source_file = os.path.join(tmpdir, "solution.c")
            binary_file = os.path.join(tmpdir, "solution")

            # Write main source code to file
            with open(source_file, 'w') as f:
                f.write(source_code)

            # Write additional files if provided (headers, other .c files, etc.)
            source_files = [source_file]
            if additional_files:
                for file_data in additional_files:
                    filename = file_data['filename']
                    content = file_data['content']

                    # Decode base64 if it's encoded
                    try:
                        content = base64.b64decode(content).decode()
                    except:
                        pass  # Already plain text

                    file_path = os.path.join(tmpdir, filename)

                    # Create subdirectories if needed
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)

                    with open(file_path, 'w') as f:
                        f.write(content)

                    # Add .c files to compilation list
                    if filename.endswith('.c'):
                        source_files.append(file_path)

            # Compile the code ONCE with all source files
            compile_cmd = ["gcc", "-o", binary_file] + source_files + ["-lm", "-Wall"]
            try:
                compile_result = subprocess.run(
                    compile_cmd,
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if compile_result.returncode != 0:
                    # Compilation failed - return error for all test cases
                    for tc in test_cases:
                        results.append({
                            "input": tc["input"],
                            "expected_output": tc["expected_output"],
                            "actual_output": "",
                            "passed": False,
                            "status": "Compilation Error",
                            "compile_output": compile_result.stderr,
                            "stderr": None,
                            "time": None,
                            "memory": None
                        })
                    return results

            except subprocess.TimeoutExpired:
                for tc in test_cases:
                    results.append({
                        "input": tc["input"],
                        "expected_output": tc["expected_output"],
                        "actual_output": "",
                        "passed": False,
                        "status": "Compilation Error",
                        "compile_output": "Compilation timeout",
                        "stderr": None,
                        "time": None,
                        "memory": None
                    })
                return results

            # Compilation succeeded - run against all test cases
            tasks = []
            for tc in test_cases:
                tasks.append(self._run_test_case(binary_file, tc))

            # Run all test cases in parallel
            results = await asyncio.gather(*tasks)
            return list(results)

    async def _run_test_case(self, binary_file: str, test_case: Dict[str, str]) -> Dict:
        """Run compiled binary against a single test case"""
        try:
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._execute_binary,
                binary_file,
                test_case["input"]
            )

            stdout, stderr, returncode, execution_time = result

            # Check for runtime error with detailed error type detection
            if returncode != 0 or stderr:
                # Detect stack overflow (segmentation fault often caused by stack overflow)
                error_status = "Runtime Error"
                if returncode == -signal.SIGSEGV or "segmentation fault" in stderr.lower():
                    error_status = "Stack Overflow / Segmentation Fault"
                elif returncode == -signal.SIGABRT or "abort" in stderr.lower():
                    error_status = "Runtime Error (Aborted)"
                elif returncode != 0:
                    error_status = f"Runtime Error (Exit Code {returncode})"
                else:
                    error_status = "Runtime Error (stderr)"

                return {
                    "input": test_case["input"],
                    "expected_output": test_case["expected_output"],
                    "actual_output": stdout,
                    "passed": False,
                    "status": error_status,
                    "compile_output": None,
                    "stderr": stderr,
                    "time": f"{execution_time:.3f}",
                    "memory": None
                }

            # Compare outputs
            passed = self._compare_outputs(stdout, test_case["expected_output"])

            return {
                "input": test_case["input"],
                "expected_output": test_case["expected_output"],
                "actual_output": stdout,
                "passed": passed,
                "status": "Accepted" if passed else "Wrong Answer",
                "compile_output": None,
                "stderr": None,
                "time": f"{execution_time:.3f}",
                "memory": None
            }

        except subprocess.TimeoutExpired:
            return {
                "input": test_case["input"],
                "expected_output": test_case["expected_output"],
                "actual_output": "",
                "passed": False,
                "status": "Time Limit Exceeded",
                "compile_output": None,
                "stderr": "Program exceeded time limit",
                "time": None,
                "memory": None
            }
        except Exception as e:
            return {
                "input": test_case["input"],
                "expected_output": test_case["expected_output"],
                "actual_output": "",
                "passed": False,
                "status": "Error",
                "compile_output": None,
                "stderr": str(e),
                "time": None,
                "memory": None
            }

    def _execute_binary(self, binary_file: str, stdin_data: str):
        """Execute binary with input (runs in thread pool)"""
        import time
        start_time = time.time()

        result = subprocess.run(
            [binary_file],
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=self.timeout
        )

        execution_time = time.time() - start_time

        return result.stdout, result.stderr, result.returncode, execution_time
