## 29. Zod Advanced (791–805)

791. Explain recursive schemas in Zod.
   Recursive schemas handle self-referential types (trees, linked lists) using `z.lazy(() => schema.refine(...))` or `.nullable()` chaining. Zod requires lazy evaluation to break infinite type instantiation.

792. How do branded schemas work?
   Branded schemas (`z.string().brand('Email')`) create phantom types at runtime by adding a brand property. The brand exists only at the type level, preventing accidental cross-type assignment.

793. Explain schema extension patterns.
   Extend schemas with `.extend({ field: z.number() })` for adding fields, `.pick()`/`.omit()` for subset schemas, `.merge()` for combining, and `.partial()` for making fields optional.

794. What are lazy schemas?
   Lazy schemas (`z.lazy(() => schema)`) defer schema definition until runtime. They are essential for recursive types and circular references where the schema references itself.

795. Explain safeParse vs parse.
   `parse()` throws on validation failure; `safeParse()` returns a discriminated union `{ success: true, data } | { success: false, error }`. Use `safeParse` in production for graceful error handling.

796. How do custom error maps work?
   Custom error maps override Zod's default error messages. Pass a function to `new ZodErrorMap()` that takes the issue and returns a custom message, enabling localization or user-friendly errors.

797. Explain coercion handling.
   Zod's `.coerce()` transforms input types (e.g., string `"123"` to number `123`) before validation. It's useful for form inputs and query parameters where types are always strings.

798. What are schema composition techniques?
   Composition techniques include `.union()` for OR, `.intersection()` for AND, `.and()` for merging, `.nullable()`/`.optional()` for nullability, and `.refine()`/`.superRefine()` for custom cross-field validation.

799. Explain partial and deep partial schemas.
   `.partial()` makes top-level fields optional. Deep partial requires recursion: `type DeepPartial<T> = T extends object ? { [K in keyof T]?: DeepPartial<T[K]> } : T`, implementable with Zod's `.partial()` on nested schemas.

800. How do enums integrate with validation?
   Zod enums (`z.enum(['a', 'b', 'c'])`) validate exact string values. `.nativeEnum(MyEnum)` works with TypeScript `enum` keywords, validating against the enum's values at runtime.

801. Explain schema-driven forms.
   Schema-driven forms derive UI components and validation from Zod schemas. Libraries like `@hookform/resolvers/zod` integrate with React Hook Form, generating type-safe forms with minimal boilerplate.

802. What are validation performance concerns?
   Complex schemas with many refinements, large unions, recursive structures, or heavy string validation can be slow. Mitigate with early returns, simple pre-checks, and schema caching.

803. Explain schema versioning.
   Schema versioning manages API evolution by maintaining multiple schema versions. Transform functions convert between versions, and Zod's `.transform()` pipelines migrate data forward or backward.

804. How do you validate dynamic objects?
   Dynamic objects use `z.record(z.string(), z.any())` for arbitrary keys or `z.object({}).catchall(z.string())` for objects with known + unknown fields. Both validate values while accepting flexible keys.

805. Explain centralized validation architecture.
   Centralized validation defines all schemas in a single layer (e.g., `/schemas`), imported by controllers and clients. This ensures consistent validation, single-source-of-truth types, and easy auditing of rules.
