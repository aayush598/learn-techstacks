# Variables, Constants, and Type Inference

This module explains how TypeScript types variables and constants, when it infers a type from a value, and when inference widens or preserves literals. You will learn to choose between annotations, `const`, `as const`, and `satisfies` so that types stay precise without becoming noisy.

## Table of contents

| # | Topic |
| --- | --- |
| 01 | [Type Annotations for Variables](./01-type-annotations-for-variables.md) |
| 02 | [Inferred Variable Types](./02-inferred-variable-types.md) |
| 03 | [Explicit Variable Types](./03-explicit-variable-types.md) |
| 04 | [Literal Inference](./04-literal-inference.md) |
| 05 | [Literal Widening](./05-literal-widening.md) |
| 06 | [`const` Inference](./06-const-inference.md) |
| 07 | [`let` Inference](./07-let-inference.md) |
| 08 | [Contextual Typing](./08-contextual-typing.md) |
| 09 | [Best Common Type](./09-best-common-type.md) |
| 10 | [Type Inference in Arrays](./10-type-inference-in-arrays.md) |
| 11 | [Type Inference in Objects](./11-type-inference-in-objects.md) |
| 12 | [Type Inference in Functions](./12-type-inference-in-functions.md) |
| 13 | [Type Inference in Callbacks](./13-type-inference-in-callbacks.md) |
| 14 | [Type Inference in Generic Contexts](./14-type-inference-in-generic-contexts.md) |
| 15 | [`as const`](./15-as-const.md) |
| 16 | [Const Contexts](./16-const-contexts.md) |
| 17 | [The `satisfies` Operator](./17-the-satisfies-operator.md) |
| 18 | [Type Inference with `satisfies`](./18-type-inference-with-satisfies.md) |
| 19 | [Preventing Unwanted Type Widening](./19-preventing-unwanted-type-widening.md) |
| 20 | [Avoiding Unnecessary Annotations](./20-avoiding-unnecessary-annotations.md) | |

## Key outcomes

- Annotate variables deliberately and recognize when inference is sufficient.
- Explain how `const` and `let` differ in literal inference and widening.
- Use contextual typing, best common type, and generic inference correctly.
- Preserve literal types with `as const`, const contexts, and `satisfies`.
- Prevent unwanted widening and remove annotations that add no information.
