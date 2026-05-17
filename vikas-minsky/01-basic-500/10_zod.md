## 10. Zod (291–305)

291. What is Zod?
     Z**Answer:** Zod is a TypeScript-first schema declaration and validation library. It uses a declarative API to define data schemas, infers TypeScript types from them, and provides runtime validation with detailed error messages.

292. Why use schema validation?
     S**Answer:** Schema validation ensures data conforms to expected shapes at runtime, catching malformed data from API responses, form submissions, or user input. It prevents type mismatches, security vulnerabilities (injection), and provides clear error messages during debugging.

293. Explain Zod object schemas.
     `**Answer:** `z.object({ name: z.string(), age: z.number() })` defines an object schema where each field has its own type constraint. Objects can be nested, optional with `.optional()`, or partial with `.partial()` for partial updates.

294. How does type inference work in Zod?
     `**Answer:** `z.infer<typeof schema>` extracts the TypeScript type from a Zod schema, automatically generating types that match the validation rules. The inferred type is always aligned with the schema — changing the schema updates the type automatically.

295. Explain parsing vs validation.
     P**Answer:** Parsing (`.parse()`) validates and returns typed data or throws a `ZodError`. Validation (`.safeParse()`) returns an object with `{ success, data, error }` without throwing, allowing graceful error handling.

296. What are refinements?
     R**Answer:** Refinements (`.refine()`) add custom validation logic beyond basic type checks. They take a function returning boolean and an optional error message. Used for cross-field validation like password confirmation or business rule validation.

297. Explain transformations in Zod.
     T**Answer:** Transformations (`.transform()`) modify parsed data after validation, like trimming strings, converting dates, or mapping values. They run after validation succeeds and can change the output type, which is reflected in `z.infer`.

298. How do unions work in Zod?
     `**Answer:** `z.union([z.string(), z.number()])` accepts values matching any of the provided schemas. Zod tries each schema in order and returns the first successful parse, enabling polymorphism and flexible input types.

299. Explain discriminated unions.
     `**Answer:** `z.discriminatedUnion('type', [ ... ])` optimizes union validation by first checking the discriminant field to determine which schema to apply. This provides better performance and error messages compared to regular unions.

300. What are preprocessors?
     P**Answer:** Preprocessors (`.preprocess()`) run before validation, transforming raw input before schema checking. Useful for coercing strings to numbers (`z.preprocess(val => Number(val), z.number())`), trimming whitespace, or normalizing data.

301. Explain async validation.
     Z**Answer:** Zod supports async validation with `.parseAsync()`, `.refine().async()`, and `.superRefine().async()`. Used for database lookups or API calls during validation, like checking if a username is taken or an email exists.

302. How does Zod integrate with forms?
     Z**Answer:** Zod integrates with React Hook Form via `@hookform/resolvers/zod`, enabling schema-based form validation. The schema defines form rules and error messages, and the resolver maps Zod errors to form field errors automatically.

303. Explain Zod with tRPC.
     Z**Answer:** Zod schemas define input validation for tRPC procedures. tRPC automatically infers TypeScript types from Zod schemas, validates incoming requests, and provides type-safe procedure definitions without manual type annotations.

304. What are common validation pitfalls?
     C**Answer:** Common pitfalls include: not handling `null` vs `undefined`, forgetting to `.transform()` after `.refine()` (refine doesn't change type), complex nested schemas with unclear errors, and relying solely on client-side validation without server-side checks.

305. How do you reuse schemas?
     S**Answer:** Schemas are reused through composition: base schemas with `.extend()` for specialization, `z.infer` for type extraction, exporting shared schemas from modules, and combining small schemas into larger ones for consistent validation across the stack.
