"""
Debug test for multi-file Judge0 submission
"""
import asyncio
import httpx
import base64
import zipfile
import io

JUDGE0_URL = "http://209.182.234.33:2358"

STACK_H = """
#ifndef STACK_H
#define STACK_H

#define MAX_SIZE 100

typedef struct {
    int data[MAX_SIZE];
    int top;
} Stack;

void init_stack(Stack* s);
int push(Stack* s, int value);
int pop(Stack* s, int* value);
int is_empty(Stack* s);

#endif
"""

STACK_C = """
#include "stack.h"

void init_stack(Stack* s) {
    s->top = -1;
}

int push(Stack* s, int value) {
    if (s->top >= MAX_SIZE - 1) {
        return 0;
    }
    s->data[++s->top] = value;
    return 1;
}

int pop(Stack* s, int* value) {
    if (is_empty(s)) {
        return 0;
    }
    *value = s->data[s->top--];
    return 1;
}

int is_empty(Stack* s) {
    return s->top == -1;
}
"""

MAIN_C = """
#include <stdio.h>
#include "stack.h"

int main() {
    Stack s;
    init_stack(&s);

    int n;
    scanf("%d", &n);

    for (int i = 0; i < n; i++) {
        int val;
        scanf("%d", &val);
        push(&s, val);
    }

    int val;
    while (pop(&s, &val)) {
        printf("%d\\n", val);
    }

    return 0;
}
"""

def create_zip(files):
    """Create a zip file from list of files"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in files:
            zip_file.writestr(filename, content)

    zip_buffer.seek(0)
    return base64.b64encode(zip_buffer.read()).decode()

async def test_judge0_multifile():
    """Test Judge0 with additional_files"""
    print("Creating zip with additional files...")

    # Create zip with header and implementation
    additional_files_zip = create_zip([
        ("stack.h", STACK_H),
        ("stack.c", STACK_C)
    ])

    print(f"Zip size: {len(additional_files_zip)} bytes (base64)")

    # Encode main source
    source_b64 = base64.b64encode(MAIN_C.encode()).decode()
    stdin_b64 = base64.b64encode("3\\n10\\n20\\n30".encode()).decode()

    payload = {
        "language_id": 50,  # C (GCC 9.2.0)
        "source_code": source_b64,
        "stdin": stdin_b64,
        "additional_files": additional_files_zip
    }

    print("\\nSubmitting to Judge0...")
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Submit
        response = await client.post(
            f"{JUDGE0_URL}/submissions",
            json=payload,
            params={"base64_encoded": "true"}
        )

        if response.status_code != 201:
            print(f"Submission failed: {response.status_code}")
            print(response.text)
            return

        token = response.json()["token"]
        print(f"Token: {token}")

        # Poll for result
        for i in range(50):
            await asyncio.sleep(0.5)
            result_response = await client.get(
                f"{JUDGE0_URL}/submissions/{token}",
                params={"base64_encoded": "true"}
            )

            result = result_response.json()
            status_id = result.get("status", {}).get("id")

            if status_id and status_id > 2:
                # Done
                print(f"\\nStatus: {result['status']['description']}")

                if result.get("compile_output"):
                    compile_out = base64.b64decode(result["compile_output"]).decode()
                    print(f"\\nCompile output:\\n{compile_out}")

                if result.get("stdout"):
                    stdout = base64.b64decode(result["stdout"]).decode()
                    print(f"\\nStdout:\\n{stdout}")

                if result.get("stderr"):
                    stderr = base64.b64decode(result["stderr"]).decode()
                    print(f"\\nStderr:\\n{stderr}")

                return

            print(f"Polling... status_id={status_id}")

        print("Timeout waiting for result")

if __name__ == "__main__":
    asyncio.run(test_judge0_multifile())
