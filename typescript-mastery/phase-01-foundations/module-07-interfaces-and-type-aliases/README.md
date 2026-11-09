# Interfaces and Type Aliases

Interfaces and type aliases are the two ways to name a type in TypeScript, and choosing the right one shapes how a codebase evolves. This module covers both in depth: object contracts, inheritance and merging, callable and generic shapes, unions, intersections, and the design rules that keep reusable types stable.

## Table of contents

| # | Topic | File |
|---|-------|------|
| 1 | Interface fundamentals | [01-interface-fundamentals.md](./01-interface-fundamentals.md) |
| 2 | Type alias fundamentals | [02-type-alias-fundamentals.md](./02-type-alias-fundamentals.md) |
| 3 | Declaring interfaces | [03-declaring-interfaces.md](./03-declaring-interfaces.md) |
| 4 | Declaring type aliases | [04-declaring-type-aliases.md](./04-declaring-type-aliases.md) |
| 5 | Extending interfaces | [05-extending-interfaces.md](./05-extending-interfaces.md) |
| 6 | Extending multiple interfaces | [06-extending-multiple-interfaces.md](./06-extending-multiple-interfaces.md) |
| 7 | Interface inheritance | [07-interface-inheritance.md](./07-interface-inheritance.md) |
| 8 | Interface composition | [08-interface-composition.md](./08-interface-composition.md) |
| 9 | Interface declaration merging | [09-interface-declaration-merging.md](./09-interface-declaration-merging.md) |
| 10 | Interface augmentation | [10-interface-augmentation.md](./10-interface-augmentation.md) |
| 11 | Interface reopening | [11-interface-reopening.md](./11-interface-reopening.md) |
| 12 | Implementing interfaces | [12-implementing-interfaces.md](./12-implementing-interfaces.md) |
| 13 | Interfaces with optional properties | [13-interfaces-with-optional-properties.md](./13-interfaces-with-optional-properties.md) |
| 14 | Interfaces with readonly properties | [14-interfaces-with-readonly-properties.md](./14-interfaces-with-readonly-properties.md) |
| 15 | Interfaces with index signatures | [15-interfaces-with-index-signatures.md](./15-interfaces-with-index-signatures.md) |
| 16 | Interfaces with call signatures | [16-interfaces-with-call-signatures.md](./16-interfaces-with-call-signatures.md) |
| 17 | Interfaces with construct signatures | [17-interfaces-with-construct-signatures.md](./17-interfaces-with-construct-signatures.md) |
| 18 | Generic interfaces | [18-generic-interfaces.md](./18-generic-interfaces.md) |
| 19 | Recursive interfaces | [19-recursive-interfaces.md](./19-recursive-interfaces.md) |
| 20 | Union type aliases | [20-union-type-aliases.md](./20-union-type-aliases.md) |
| 21 | Intersection type aliases | [21-intersection-type-aliases.md](./21-intersection-type-aliases.md) |
| 22 | Primitive type aliases | [22-primitive-type-aliases.md](./22-primitive-type-aliases.md) |
| 23 | Object type aliases | [23-object-type-aliases.md](./23-object-type-aliases.md) |
| 24 | Function type aliases | [24-function-type-aliases.md](./24-function-type-aliases.md) |
| 25 | Recursive type aliases | [25-recursive-type-aliases.md](./25-recursive-type-aliases.md) |
| 26 | Interface versus type alias | [26-interface-versus-type-alias.md](./26-interface-versus-type-alias.md) |
| 27 | Choosing between interface and type | [27-choosing-between-interface-and-type.md](./27-choosing-between-interface-and-type.md) |
| 28 | Naming conventions | [28-naming-conventions.md](./28-naming-conventions.md) |
| 29 | Public API type design | [29-public-api-type-design.md](./29-public-api-type-design.md) |
| 30 | Best practices for reusable contracts | [30-best-practices-for-reusable-contracts.md](./30-best-practices-for-reusable-contracts.md) |

## Key outcomes

- Declare and use `interface` and `type` with confidence under `strict` mode.
- Extend, merge, reopen, and augment interfaces without breaking consumers.
- Model callable, constructable, generic, and recursive shapes correctly.
- Use unions, intersections, and semantic aliases to express precise contracts.
- Choose between interface and type alias deliberately, not by habit.
- Design public types that are small, stable, readable, and hard to misuse.
