"""
Test script for multi-file compilation with ADT (Abstract Data Type)
Tests stack overflow detection and multiple source files
"""
import asyncio
import base64
from judge0_client import judge0_client

# Example ADT: Stack implementation
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
        return 0; // Stack overflow
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

    // Push values
    for (int i = 0; i < n; i++) {
        int val;
        scanf("%d", &val);
        push(&s, val);
    }

    // Pop and print in reverse
    int val;
    while (pop(&s, &val)) {
        printf("%d\\n", val);
    }

    return 0;
}
"""

# Stack overflow test (infinite recursion)
STACK_OVERFLOW_C = """
#include <stdio.h>

void infinite_recursion(int n) {
    int large_array[10000];  // Consume stack space
    large_array[0] = n;
    printf("%d ", n);
    infinite_recursion(n + 1);  // Never returns
}

int main() {
    infinite_recursion(1);
    return 0;
}
"""

async def test_multifile_adt():
    """Test ADT with multiple files (stack.h, stack.c, main.c)"""
    print("\\n=== Testing Multi-File ADT (Stack Implementation) ===")

    additional_files = [
        {"filename": "stack.h", "content": STACK_H},
        {"filename": "stack.c", "content": STACK_C}
    ]

    test_cases = [
        {
            "input": "3\n10\n20\n30",
            "expected_output": "30\n20\n10"
        },
        {
            "input": "5\n1\n2\n3\n4\n5",
            "expected_output": "5\n4\n3\n2\n1"
        }
    ]

    results = await judge0_client.execute_code(MAIN_C, test_cases, additional_files)

    for i, result in enumerate(results):
        print(f"\\nTest Case {i + 1}:")
        print(f"  Status: {result['status']}")
        print(f"  Passed: {result['passed']}")
        print(f"  Input: {repr(result['input'])}")
        print(f"  Expected: {repr(result['expected_output'])}")
        print(f"  Actual: {repr(result['actual_output'])}")
        if result.get('stderr'):
            print(f"  Stderr: {result['stderr']}")

async def test_stack_overflow():
    """Test stack overflow detection"""
    print("\\n=== Testing Stack Overflow Detection ===")

    test_cases = [
        {
            "input": "",
            "expected_output": "Should not reach here"
        }
    ]

    results = await judge0_client.execute_code(STACK_OVERFLOW_C, test_cases)

    result = results[0]
    print(f"\\nStack Overflow Test:")
    print(f"  Status: {result['status']}")
    print(f"  Passed: {result['passed']}")
    if result.get('stderr'):
        print(f"  Error: {result['stderr']}")

    # Check if stack overflow was detected
    if "Stack Overflow" in result['status'] or "Segmentation Fault" in result['status']:
        print("  ✓ Stack overflow correctly detected!")
    else:
        print(f"  ✗ Expected stack overflow detection, got: {result['status']}")

async def test_single_file_simple():
    """Test simple single-file program (baseline)"""
    print("\\n=== Testing Single-File Simple Program (Baseline) ===")

    simple_code = """
#include <stdio.h>

int main() {
    int a, b;
    scanf("%d %d", &a, &b);
    printf("%d\\n", a + b);
    return 0;
}
"""

    test_cases = [
        {"input": "5 3", "expected_output": "8"},
        {"input": "100 200", "expected_output": "300"}
    ]

    results = await judge0_client.execute_code(simple_code, test_cases)

    for i, result in enumerate(results):
        print(f"\\nTest Case {i + 1}:")
        print(f"  Status: {result['status']}")
        print(f"  Passed: {result['passed']}")

async def main():
    print("=" * 60)
    print("Multi-File Compilation & Stack Overflow Detection Test")
    print(f"Judge0 Mode: {judge0_client.mode}")
    print("=" * 60)

    # Run all tests
    await test_single_file_simple()
    await test_multifile_adt()
    await test_stack_overflow()

    print("\\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
