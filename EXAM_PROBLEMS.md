# Exam-Grade C Programming Problems

This document lists all the exam-grade C programming problems added to the database.

## Problem List

### Easy Problems (4)

1. **Array Sum and Average**
   - Topics: Arrays, loops, basic math, floating-point output
   - Test cases: 3 visible, 7 hidden
   - Skills tested: Array traversal, accumulation, average calculation
   - Expected output format: Integer sum, then float with 2 decimals

2. **Find Maximum in Array**
   - Topics: Arrays, loops, comparison operations
   - Test cases: 3 visible, 7 hidden
   - Skills tested: Finding maximum value and its position
   - Edge cases: Negative numbers, duplicates, single element

3. **Count Vowels and Consonants**
   - Topics: Strings, character classification, conditionals
   - Test cases: 3 visible, 10 hidden
   - Skills tested: String traversal, case handling, character checking
   - Edge cases: Mixed case, spaces, punctuation, numbers

4. **Factorial Calculation**
   - Topics: Loops, arithmetic, large numbers
   - Test cases: 3 visible, 10 hidden
   - Skills tested: Iterative calculation, handling edge case (0!)
   - Important: Use `long long` or `unsigned long long` for results

### Medium Problems (4)

5. **Reverse Array**
   - Topics: Arrays, in-place manipulation or auxiliary array
   - Test cases: 3 visible, 7 hidden
   - Skills tested: Array reversal, indexing
   - Edge cases: Single element, negative numbers, duplicates

6. **Prime Number Check**
   - Topics: Number theory, loops, optimization
   - Test cases: 3 visible, 10 hidden
   - Skills tested: Divisibility testing, efficient checking (up to √n)
   - Range: 2 to 10,000

7. **Fibonacci Sequence**
   - Topics: Sequences, loops, iterative algorithms
   - Test cases: 3 visible, 8 hidden
   - Skills tested: Generating sequences, handling first two terms
   - Range: Up to 30 terms

8. **String Palindrome Check**
   - Topics: Strings, two-pointer technique, character manipulation
   - Test cases: 3 visible, 10 hidden
   - Skills tested: String comparison, case-insensitive checking, filtering
   - Important: Ignore spaces and non-alphabetic characters

### Hard Problems (2)

9. **Matrix Addition**
   - Topics: 2D arrays, nested loops, matrix operations
   - Test cases: 3 visible, 7 hidden
   - Skills tested: 2D array input/output, element-wise addition
   - Matrix size: Up to 10×10

10. **Bubble Sort**
    - Topics: Sorting algorithms, nested loops, swapping
    - Test cases: 3 visible, 8 hidden
    - Skills tested: Implementation of classic sorting algorithm
    - Edge cases: Already sorted, reverse sorted, duplicates

## Solution Tips

### Array Sum and Average
```c
#include <stdio.h>
int main() {
    int n, sum = 0;
    scanf("%d", &n);
    int arr[n];
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
        sum += arr[i];
    }
    printf("%d\n", sum);
    printf("%.2f\n", (double)sum / n);  // Cast to double for proper division
    return 0;
}
```

### Find Maximum in Array
- Remember to track both the max value AND its index
- Initialize max with first element, not with 0 (could be all negative)

### Count Vowels and Consonants
- Use `tolower()` or `toupper()` for case-insensitive checking
- Check `isalpha()` to filter out non-letters
- Create a helper function or use switch statement for vowels

### Reverse Array
- Two approaches: swap in-place OR create new array
- In-place: swap elements from both ends moving toward center
- Be careful with output format (space-separated)

### Prime Number Check
- Optimization: only check divisors up to √n
- Special case: 2 is the only even prime
- No need to check even divisors after 2

### Factorial Calculation
```c
unsigned long long factorial = 1;
for (int i = 1; i <= n; i++) {
    factorial *= i;
}
```

### Fibonacci Sequence
- Start with F(0) = 0, F(1) = 1
- Use three variables: prev, current, next
- Print first two terms explicitly if needed

### String Palindrome Check
- Extract only alphabetic characters
- Convert to same case
- Compare forward and backward

### Matrix Addition
```c
int matrix1[rows][cols], matrix2[rows][cols], result[rows][cols];
// Read both matrices
// Add element by element: result[i][j] = matrix1[i][j] + matrix2[i][j]
```

### Bubble Sort
```c
for (int i = 0; i < n - 1; i++) {
    for (int j = 0; j < n - i - 1; j++) {
        if (arr[j] > arr[j + 1]) {
            // Swap arr[j] and arr[j + 1]
            int temp = arr[j];
            arr[j] = arr[j + 1];
            arr[j + 1] = temp;
        }
    }
}
```

## Common Pitfalls

1. **Floating-point output**: Use `%.2f` for 2 decimal places
2. **Integer division**: Cast to double when dividing integers
3. **Array indexing**: Remember arrays are 0-indexed
4. **Input format**: Pay attention to single line vs multiple lines
5. **Output format**: Watch for spaces between numbers vs newlines
6. **Large numbers**: Use `long long` for factorials
7. **String handling**: Remember null terminator, use `fgets()` for strings with spaces
8. **Off-by-one errors**: Check loop bounds carefully

## Testing Strategy

1. **Visible tests**: Given as examples, test basic functionality
2. **Hidden tests**: Cover edge cases:
   - Minimum/maximum input sizes
   - Negative numbers
   - Zero values
   - Duplicate values
   - Already sorted/reverse sorted
   - Special characters (for strings)

## Grading

- Each problem has 3 visible + 7-10 hidden test cases
- Score = (Passed Hidden Tests / Total Hidden Tests) × 100
- Visible tests are for your reference only
- Compilation errors result in 0% score
- Partial credit awarded for partially correct solutions

## Common Input/Output Patterns

### Reading an array:
```c
int n;
scanf("%d", &n);
int arr[n];
for (int i = 0; i < n; i++) {
    scanf("%d", &arr[i]);
}
```

### Reading a string with spaces:
```c
char str[101];
fgets(str, sizeof(str), stdin);
// Remove newline if present
str[strcspn(str, "\n")] = 0;
```

### Printing array on one line:
```c
for (int i = 0; i < n; i++) {
    printf("%d", arr[i]);
    if (i < n - 1) printf(" ");  // Space between elements, not after last
}
printf("\n");
```

## Running the Problem Adder

To add these problems to your database:

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
python add_exam_problems.py
```

The script:
- Checks for duplicates (won't add if problem title exists)
- Creates problems with proper difficulty levels
- Adds visible and hidden test cases
- Maintains LeetCode-style grading (only hidden tests count)

## Problem Difficulty Guidelines

**Easy (4 problems)**
- Single concept focus
- Straightforward logic
- Basic loops and conditionals
- Standard input/output

**Medium (4 problems)**
- Multiple concept integration
- Requires algorithm knowledge
- More complex logic flow
- Edge case handling important

**Hard (2 problems)**
- Advanced data structures (2D arrays)
- Classic algorithms (sorting)
- Nested loops and complex logic
- Performance considerations

## Additional Practice

After solving these problems, students should be able to:
- Manipulate arrays and strings effectively
- Implement basic algorithms from scratch
- Handle various input/output formats
- Write efficient, bug-free code
- Debug compilation and runtime errors
- Understand time complexity basics

## Resources for Students

Recommended topics to study:
1. C syntax and basic I/O
2. Arrays (1D and 2D)
3. Loops (for, while)
4. Conditionals (if-else, switch)
5. String handling (`string.h` functions)
6. Basic algorithms (searching, sorting)
7. Number theory (primes, factorials)
8. Debugging techniques
