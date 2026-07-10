# Expression Evaluation

> Expression evaluation is where stacks shine brightest. Converting between infix, postfix, and prefix, and evaluating expressions — all use the stack's LIFO nature to handle operator precedence naturally.

## Infix, Postfix, Prefix — The Basics

```
Infix:     (A + B) * C - D     → human-readable, needs parentheses
Postfix:   A B + C * D -       → computer-friendly, no parentheses needed
Prefix:    - * + A B C D       → also no parentheses (less common)
```

**Why postfix?** Because it can be evaluated left to right with a single stack — no need to look ahead for precedence.

---

## Infix to Postfix Conversion

**Algorithm:** Use a stack for operators. Output operands directly. Apply precedence rules.

```java
public static String infixToPostfix(String expression) {
    StringBuilder result = new StringBuilder();
    Deque<Character> stack = new ArrayDeque<>();

    for (int i = 0; i < expression.length(); i++) {
        char c = expression.charAt(i);

        // If operand, add to result
        if (Character.isLetterOrDigit(c)) {
            result.append(c);
        }
        // If '(', push to stack
        else if (c == '(') {
            stack.push(c);
        }
        // If ')', pop until '('
        else if (c == ')') {
            while (!stack.isEmpty() && stack.peek() != '(') {
                result.append(stack.pop());
            }
            stack.pop();  // discard '('
        }
        // If operator
        else {
            while (!stack.isEmpty() && precedence(stack.peek()) >= precedence(c)) {
                result.append(stack.pop());
            }
            stack.push(c);
        }
    }

    // Pop remaining operators
    while (!stack.isEmpty()) {
        result.append(stack.pop());
    }

    return result.toString();
}

private static int precedence(char op) {
    switch (op) {
        case '+': case '-': return 1;
        case '*': case '/': return 2;
        case '^':           return 3;
        default:            return 0;
    }
}
```

### Walkthrough

```
Expression: A + B * C - D

Step | Char | Stack      | Output
-----|------|------------|--------
  1  |  A   |            | A
  2  |  +   | +          | A
  3  |  B   | +          | A B
  4  |  *   | + *        | A B       (* has higher prec than +, push)
  5  |  C   | + *        | A B C
  6  |  -   | -          | A B C * + (- same prec as +, pop + first, then push -)
  7  |  D   | -          | A B C * + D
  8  | EOS  |            | A B C * + D -

Result: A B C * + D -  →  (A + (B * C)) - D  ✓
```

**Key rule:** An operator pops all operators from the stack that have **greater or equal** precedence. This ensures higher-precedence operators are applied first in the postfix output.

---

## Evaluate Postfix

```java
public static int evaluatePostfix(String expression) {
    Deque<Integer> stack = new ArrayDeque<>();

    for (int i = 0; i < expression.length(); i++) {
        char c = expression.charAt(i);

        if (Character.isDigit(c)) {
            stack.push(c - '0');  // convert char to int
        } else {
            int b = stack.pop();  // second operand (top)
            int a = stack.pop();  // first operand

            switch (c) {
                case '+': stack.push(a + b); break;
                case '-': stack.push(a - b); break;
                case '*': stack.push(a * b); break;
                case '/': stack.push(a / b); break;
            }
        }
    }

    return stack.pop();
}

// Example: "231*+9-"
// 
// 2 → stack=[2]
// 3 → stack=[2,3]
// 1 → stack=[2,3,1]
// * → pop 1,3 → push 3*1=3 → stack=[2,3]
// + → pop 3,2 → push 2+3=5 → stack=[5]
// 9 → stack=[5,9]
// - → pop 9,5 → push 5-9=-4 → stack=[-4]
//
// Result: -4
```

**Critical:** Notice the operand order. `b` is popped first (top), `a` is popped second. For non-commutative operations (-, /), the order matters: `a - b`, not `b - a`.

---

## Basic Calculator I (LeetCode 224)

Handle `+`, `-`, `(`, `)` with spaces. No multiplication/division.

```java
public int calculate(String s) {
    Deque<Integer> stack = new ArrayDeque<>();
    int result = 0;
    int number = 0;
    int sign = 1;  // 1 for positive, -1 for negative

    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);

        if (Character.isDigit(c)) {
            number = number * 10 + (c - '0');
        }
        else if (c == '+') {
            result += sign * number;
            number = 0;
            sign = 1;
        }
        else if (c == '-') {
            result += sign * number;
            number = 0;
            sign = -1;
        }
        else if (c == '(') {
            stack.push(result);   // save current result
            stack.push(sign);     // save current sign
            result = 0;           // reset for sub-expression
            sign = 1;
        }
        else if (c == ')') {
            result += sign * number;
            number = 0;
            result *= stack.pop();  // restore sign
            result += stack.pop();  // restore previous result
        }
    }

    return result + sign * number;
}

// Example: "(1+(4+5+2)-3)+(6+8)"
//
// '(' → push result=0, push sign=1, reset: result=0, sign=1
// '1' → number=1
// '+' → result=0+1=1, number=0, sign=1
// '(' → push result=1, push sign=1, reset: result=0, sign=1
// '4' → number=4
// '+' → result=4, number=0
// '5' → number=5
// '+' → result=9, number=0
// '2' → number=2
// ')' → result=9+2=11, *=1, +=1 → result=12
// '-' → number=0, sign=-1
// '3' → number=3
// ')' → result=12+(-1)*3=9, *=1, +=0 → result=9... 
// Actually let me re-trace more carefully...
```

### The stack trick for parentheses

```
When we see '(':
    Push the CURRENT result and sign onto the stack
    Reset result and sign for the new sub-expression

When we see ')':
    Complete the sub-expression: result += sign * number
    Multiply by saved sign (to handle cases like -(3+4))
    Add to saved result (to chain with previous computation)
```

---

## Basic Calculator II (LeetCode 227)

Handle `+`, `-`, `*`, `/` without parentheses.

**Key insight:** `*` and `/` must be done immediately (higher precedence). Use a stack to defer `+` and `-`.

```java
public int calculate(String s) {
    Deque<Integer> stack = new ArrayDeque<>();
    int number = 0;
    char operator = '+';  // default operator for first number

    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);

        if (Character.isDigit(c)) {
            number = number * 10 + (c - '0');
        }

        // Process when we hit an operator or reach the end
        if ((!Character.isDigit(c) && c != ' ') || i == s.length() - 1) {
            switch (operator) {
                case '+': stack.push(number); break;
                case '-': stack.push(-number); break;
                case '*': stack.push(stack.pop() * number); break;  // immediate
                case '/': stack.push(stack.pop() / number); break;  // immediate
            }
            operator = c;
            number = 0;
        }
    }

    // Sum everything in the stack
    int result = 0;
    while (!stack.isEmpty()) {
        result += stack.pop();
    }

    return result;
}

// Example: "3+2*2"
//
// '3' → number=3
// '+' → stack.push(3), operator='+', number=0
// '2' → number=2
// '*' → stack.push(2), operator='*', number=0
//       Wait — we push with '+', not '*'
//       Correction: at '+', we push +2 (operator was '+')
//       Then operator becomes '*', number=0
// '2' → number=2
// EOS → operator='*', push 2*2=4
//
// Stack: [3, 4]
// Result: 3 + 4 = 7 ✓
```

### The deferred operator trick

```java
// The operator variable holds the PREVIOUS operator, not the current one.
// This means when we see a new operator, we process the number with the previous one.
//
// "3 + 2 * 2"
//  ↑ first operator is '+' (default)
//
// Process: 3 with '+' → push +3
// Process: 2 with '+' → push +2    ← operator was '+' when we hit '*'
// Process: 2 with '*' → push 2*2=4 ← operator was '*' when we hit EOS
//
// Stack: [3, 2, 4] → wait, that's wrong. Let me retrace.
//
// Actually: when we hit '+', operator is '+' (default), so push +3
// When we hit '*', operator is '+', so push +2
// At end, operator is '*', so push 2*2=4
// Stack: [3, 2, 4] → sum = 9? No!
//
// Hmm, the issue is: at '*', we should be pushing the PREVIOUS number, not 2.
// Let me re-read the code...
//
// At '+': operator was '+' (default), push number=3 → stack=[3]
//         operator becomes '+', number=0
// At '*': operator was '+', push number=2 → stack=[3,2]
//         operator becomes '*', number=0
// At EOS: operator was '*', push stack.pop()*2 = 2*2=4 → stack=[3,4]
// Sum: 3+4=7 ✓
//
// The trick: operator is ALWAYS one behind. We process with the previous operator.
```

---

## Complexity Summary

| Problem | Time | Space | Key Idea |
|---------|------|-------|----------|
| Infix to Postfix | O(n) | O(n) | Operator stack + precedence |
| Evaluate Postfix | O(n) | O(n) | Operand stack |
| Calculator I | O(n) | O(n) | Stack for saved results at '(' |
| Calculator II | O(n) | O(n) | Stack for deferred + and - |

---

## Key Takeaways

1. **Infix → Postfix:** Stack holds operators, use precedence to decide when to pop
2. **Postfix evaluation:** Stack holds operands, apply operator to top two
3. **Calculator I:** Push result and sign before '(' to save context
4. **Calculator II:** Process `*` and `/` immediately, defer `+` and `-` with a stack
5. **Operand order matters** for `-` and `/` — second popped is the second operand
6. **Default operator trick** (Calculator II) simplifies the first number handling

Expression evaluation comes up in interviews as "implement a calculator." Know these patterns and you can handle any variant.
