import httpx
import asyncio
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional
import base64
import zipfile
import io
from local_executor import LocalExecutor

load_dotenv(override=True)

JUDGE0_MODE = os.getenv("JUDGE0_MODE", "local")  # local, rapidapi, self-hosted, or mock
JUDGE0_RAPIDAPI_URL = os.getenv("JUDGE0_RAPIDAPI_URL", "https://judge0-ce.p.rapidapi.com")
JUDGE0_RAPIDAPI_KEY = os.getenv("JUDGE0_RAPIDAPI_KEY", "")
JUDGE0_SELF_HOSTED_URL = os.getenv("JUDGE0_SELF_HOSTED_URL", "http://localhost:2358")

C_LANGUAGE_ID = 50  # C (GCC 9.2.0)
MULTI_FILE_LANGUAGE_ID = 89  # Multi-file program (requires compile/run scripts)
STACK_SIZE_KB = 8192  # 8MB stack limit for Judge0

class Judge0Client:
    def __init__(self):
        self.mode = JUDGE0_MODE
        self.local_executor = LocalExecutor() if self.mode == "local" else None

        if self.mode == "local":
            print("ℹ️  Using LOCAL execution mode - compiles once, runs all test cases (FAST!)")
        elif self.mode == "rapidapi":
            self.base_url = JUDGE0_RAPIDAPI_URL
            self.headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": JUDGE0_RAPIDAPI_KEY,
                "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
            }
            if not JUDGE0_RAPIDAPI_KEY or JUDGE0_RAPIDAPI_KEY == "your-rapidapi-key-here":
                print("⚠️  WARNING: Judge0 RapidAPI key not configured. Using mock mode.")
                self.mode = "mock"
        elif self.mode == "self-hosted":
            self.base_url = JUDGE0_SELF_HOSTED_URL
            self.headers = {
                "content-type": "application/json"
            }
        elif self.mode == "mock":
            print("ℹ️  Judge0 in MOCK mode - simulating code execution for testing")
        else:
            print("⚠️  Invalid Judge0 mode. Falling back to mock mode.")
            self.mode = "mock"

    def _compare_outputs(self, actual: str, expected: str) -> bool:
        """
        Compare outputs with whitespace tolerance.
        Strips trailing whitespace from each line and compares.
        """
        # Strip trailing whitespace from each line and from the end
        actual_lines = [line.rstrip() for line in actual.splitlines()]
        expected_lines = [line.rstrip() for line in expected.splitlines()]

        # Remove trailing empty lines
        while actual_lines and not actual_lines[-1]:
            actual_lines.pop()
        while expected_lines and not expected_lines[-1]:
            expected_lines.pop()

        return actual_lines == expected_lines

    def _encode_base64(self, text: str) -> str:
        """Encode text to base64"""
        return base64.b64encode(text.encode()).decode()

    def _decode_base64(self, text: Optional[str]) -> str:
        """Decode base64 text, return empty string if None"""
        if not text:
            return ""
        try:
            return base64.b64decode(text).decode()
        except:
            return text

    def _create_multifile_zip(self, source_code: str, files: List[Dict[str, str]]) -> str:
        """
        Create a base64-encoded zip for multi-file programs (language ID 89).
        Includes source code, additional files, and compile/run scripts.
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add main source file
            zip_file.writestr("main.c", source_code)

            # Add additional files
            c_files = ["main.c"]
            for file in files:
                # Decode base64 content if it's encoded
                try:
                    content = base64.b64decode(file['content']).decode()
                except:
                    content = file['content']

                zip_file.writestr(file['filename'], content)

                # Track .c files for compilation
                if file['filename'].endswith('.c'):
                    c_files.append(file['filename'])

            # Create compile script
            compile_script = f"""#!/bin/bash
gcc -o program {' '.join(c_files)} -lm -Wall
"""
            zip_file.writestr("compile", compile_script)

            # Create run script
            run_script = """#!/bin/bash
./program
"""
            zip_file.writestr("run", run_script)

        zip_buffer.seek(0)
        return base64.b64encode(zip_buffer.read()).decode()

    async def create_submission(self, source_code: str, stdin: str) -> str:
        """Create a submission and return token"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {
                "language_id": C_LANGUAGE_ID,
                "source_code": self._encode_base64(source_code),
                "stdin": self._encode_base64(stdin),
                "wait": False
            }

            response = await client.post(
                f"{self.base_url}/submissions",
                json=payload,
                headers=self.headers,
                params={"base64_encoded": "true"}
            )
            response.raise_for_status()
            result = response.json()
            return result["token"]

    async def get_submission(self, token: str) -> Dict:
        """Get submission result by token"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.base_url}/submissions/{token}",
                headers=self.headers,
                params={"base64_encoded": "true"}
            )
            response.raise_for_status()
            result = response.json()

            # Decode base64 fields
            if result.get("stdout"):
                result["stdout"] = self._decode_base64(result["stdout"])
            if result.get("stderr"):
                result["stderr"] = self._decode_base64(result["stderr"])
            if result.get("compile_output"):
                result["compile_output"] = self._decode_base64(result["compile_output"])
            if result.get("message"):
                result["message"] = self._decode_base64(result["message"])

            return result

    async def wait_for_submission(self, token: str, max_wait: int = 50) -> Dict:
        """Wait for submission to complete with fast polling"""
        for _ in range(max_wait):
            result = await self.get_submission(token)
            status_id = result.get("status", {}).get("id")

            # Status IDs: 1-2 = In Queue/Processing, 3+ = Done
            if status_id and status_id > 2:
                return result

            # Fast polling - 0.2 second intervals
            await asyncio.sleep(0.2)

        # Timeout - return result with timeout status
        return {
            "status": {"id": 13, "description": "Time Limit Exceeded"},
            "stdout": None,
            "stderr": "Execution timeout - program took too long to complete",
            "compile_output": None,
            "message": None
        }

    async def _process_result(self, result: Dict, test_case: Dict[str, str]) -> Dict:
        """Process a Judge0 submission result into our format"""
        stdout = result.get("stdout") or ""
        expected = test_case["expected_output"]
        status_id = result.get("status", {}).get("id", 0)
        status_desc = result.get("status", {}).get("description", "Unknown")

        # Check for compilation error (status 6)
        compile_output = result.get("compile_output")
        if compile_output or status_id == 6:
            return {
                "input": test_case["input"],
                "expected_output": expected,
                "actual_output": "",
                "passed": False,
                "status": "Compilation Error",
                "time": result.get("time"),
                "memory": result.get("memory"),
                "compile_output": compile_output,
                "stderr": result.get("stderr"),
                "message": result.get("message")
            }

        # Check for runtime error (status 11, 12, etc) with enhanced detection
        stderr = result.get("stderr")
        if status_id in [11, 12] or (stderr and len(stderr) > 0):
            # Enhance status for stack overflow detection
            enhanced_status = status_desc
            if stderr and ("segmentation fault" in stderr.lower() or "core dumped" in stderr.lower()):
                enhanced_status = "Stack Overflow / Segmentation Fault"
            elif status_id == 11:
                enhanced_status = "Runtime Error (NZEC)"

            return {
                "input": test_case["input"],
                "expected_output": expected,
                "actual_output": stdout,
                "passed": False,
                "status": enhanced_status,
                "time": result.get("time"),
                "memory": result.get("memory"),
                "compile_output": None,
                "stderr": stderr,
                "message": result.get("message")
            }

        # Compare outputs with whitespace tolerance
        passed = self._compare_outputs(stdout, expected)

        return {
            "input": test_case["input"],
            "expected_output": expected,
            "actual_output": stdout,
            "passed": passed,
            "status": "Accepted" if passed else "Wrong Answer",
            "time": result.get("time"),
            "memory": result.get("memory"),
            "compile_output": None,
            "stderr": stderr,
            "message": result.get("message")
        }

    async def _execute_single_test(self, source_code: str, test_case: Dict[str, str]) -> Dict:
        """Execute code against a single test case"""
        try:
            token = await self.create_submission(source_code, test_case["input"])
            return {"token": token, "test_case": test_case}
        except Exception as e:
            return {
                "input": test_case["input"],
                "expected_output": test_case["expected_output"],
                "actual_output": "",
                "passed": False,
                "status": "Error",
                "error": str(e)
            }

    async def execute_code(self, source_code: str, test_cases: List[Dict[str, str]], additional_files: Optional[List[Dict[str, str]]] = None) -> List[Dict]:
        """Execute code against multiple test cases - INDIVIDUAL PARALLEL SUBMISSIONS"""
        # Local execution mode - compile once, run all tests (FASTEST!)
        if self.mode == "local":
            return await self.local_executor.execute_code(source_code, test_cases, additional_files)

        # Mock mode for testing without Judge0
        if self.mode == "mock":
            return self._mock_execute(source_code, test_cases)

        # NEW STRATEGY: Submit all test cases as INDIVIDUAL parallel requests
        # This hits all 32 workers at once instead of batch processing
        async with httpx.AsyncClient(timeout=60.0) as client:
            async def submit_and_poll(test_case):
                """Submit ONE test case and poll until complete"""
                try:
                    # Use multi-file mode (language ID 89) if additional files present
                    if additional_files:
                        payload = {
                            "language_id": MULTI_FILE_LANGUAGE_ID,
                            "stdin": self._encode_base64(test_case["input"]),
                            "additional_files": self._create_multifile_zip(source_code, additional_files)
                        }
                        # Note: source_code is NOT included in payload for language ID 89
                    else:
                        # Standard single-file C submission
                        payload = {
                            "language_id": C_LANGUAGE_ID,
                            "source_code": self._encode_base64(source_code),
                            "stdin": self._encode_base64(test_case["input"]),
                        }

                    response = await client.post(
                        f"{self.base_url}/submissions",
                        json=payload,
                        headers=self.headers,
                        params={"base64_encoded": "true"}
                    )
                    response.raise_for_status()
                    token = response.json()["token"]

                    # Poll aggressively until done
                    for _ in range(500):  # 50 seconds max
                        result = await client.get(
                            f"{self.base_url}/submissions/{token}",
                            headers=self.headers,
                            params={"base64_encoded": "true"}
                        )
                        result.raise_for_status()
                        result_json = result.json()

                        # Decode base64 fields
                        if result_json.get("stdout"):
                            result_json["stdout"] = self._decode_base64(result_json["stdout"])
                        if result_json.get("stderr"):
                            result_json["stderr"] = self._decode_base64(result_json["stderr"])
                        if result_json.get("compile_output"):
                            result_json["compile_output"] = self._decode_base64(result_json["compile_output"])
                        if result_json.get("message"):
                            result_json["message"] = self._decode_base64(result_json["message"])

                        status_id = result_json.get("status", {}).get("id")
                        if status_id and status_id > 2:  # Done
                            return await self._process_result(result_json, test_case)

                        await asyncio.sleep(0.1)  # Poll every 0.1 seconds

                    # Timeout
                    return {
                        "input": test_case["input"],
                        "expected_output": test_case["expected_output"],
                        "actual_output": "",
                        "passed": False,
                        "status": "Time Limit Exceeded",
                        "error": "Polling timeout"
                    }

                except Exception as e:
                    return {
                        "input": test_case["input"],
                        "expected_output": test_case["expected_output"],
                        "actual_output": "",
                        "passed": False,
                        "status": "Error",
                        "error": str(e)
                    }

            # Fire off ALL submissions in parallel - each gets its own worker
            tasks = [submit_and_poll(tc) for tc in test_cases]
            results = await asyncio.gather(*tasks)
            return list(results)

    def _mock_execute(self, source_code: str, test_cases: List[Dict[str, str]]) -> List[Dict]:
        """Mock execution for testing without Judge0 API"""
        results = []

        # Simple heuristic: Check if code looks correct
        code_lower = source_code.lower()
        has_scanf = "scanf" in code_lower
        has_printf = "printf" in code_lower
        has_addition = "+" in code_lower or "a + b" in code_lower or "a+b" in code_lower

        # If code has basic structure, pass some tests
        if has_scanf and has_printf and has_addition:
            # Pass 70% of tests (simulating partially correct solution)
            for i, test_case in enumerate(test_cases):
                passed = i < len(test_cases) * 0.7  # Pass first 70%
                results.append({
                    "input": test_case["input"],
                    "expected_output": test_case["expected_output"],
                    "actual_output": test_case["expected_output"] if passed else "wrong output",
                    "passed": passed,
                    "status": "Accepted" if passed else "Wrong Answer",
                    "time": "0.001",
                    "memory": "256",
                    "compile_output": None,
                    "stderr": None,
                    "message": "⚠️ MOCK MODE - Configure Judge0 for real execution"
                })
        else:
            # Fail all tests for obviously wrong code
            for test_case in test_cases:
                results.append({
                    "input": test_case["input"],
                    "expected_output": test_case["expected_output"],
                    "actual_output": "",
                    "passed": False,
                    "status": "Wrong Answer",
                    "time": "0.001",
                    "memory": "256",
                    "compile_output": None,
                    "stderr": "Code does not match expected pattern",
                    "message": "⚠️ MOCK MODE - Configure Judge0 for real execution"
                })

        return results

# Global client instance
judge0_client = Judge0Client()
