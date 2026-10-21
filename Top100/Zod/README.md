# Zod Interview Questions and Answers

## Q1: What is Zod?
**A:** Zod is a TypeScript-first schema declaration and validation library. It allows defining schemas for data structures and validating runtime data against those schemas. It automatically infers TypeScript types from schemas, eliminating the need for duplicate type definitions.

## Q2: How is Zod different from Yup or Joi?
**A:** Zod is TypeScript-first with automatic type inference, meaning you define the schema once and get types for free. Yup and Joi are JavaScript-first with limited TypeScript integration. Zod also has a smaller bundle size and a more functional, composable API.

## Q3: How do you install Zod?
**A:** Install via npm: `npm install zod`. No additional dependencies. TypeScript types are included. Basic usage: `import { z } from 'zod'; const schema = z.string(); schema.parse('hello')`.

## Q4: How do you define a string schema in Zod?
**A:** `z.string()` creates a string schema. Chain methods for constraints: `z.string().min(1, 'Required').max(100).email().url().startsWith('prefix').includes('sub').regex(/pattern/)`.

## Q5: How do you define a number schema?
**A:** `z.number()` creates a number schema. Constraints: `.min(0)`, `.max(100)`, `.int()` (integer only), `.positive()`, `.negative()`, `.nonnegative()`, `.finite()` (no Infinity). Use `z.number({ required_error: 'Required', invalid_type_error: 'Must be number' })`.

## Q6: How do you define a boolean schema?
**A:** `z.boolean()` validates boolean values. Default error message: "Expected boolean, received ...". Use `z.boolean().default(false)` for optional booleans with defaults.

## Q7: How do you define an object schema?
**A:** `z.object({ name: z.string(), age: z.number() })` creates an object schema. It validates that the input is an object with the specified shape. Extra keys are stripped by default during parsing.

## Q8: How do you define an array schema?
**A:** `z.array(z.string())` creates an array of strings. Constraints: `.min(1)`, `.max(10)`, `.length(5)`. `.nonempty()` requires at least one element. `.element` accesses the inner schema.

## Q9: How do you define an enum schema in Zod?
**A:** `z.enum(['A', 'B', 'C'])` creates an enum schema that validates against one of the string values. The inferred type is the union of literal types: `'A' | 'B' | 'C'`. `z.nativeEnum(ColorEnum)` works with TypeScript enums.

## Q10: How do you define a union schema?
**A:** `z.union([z.string(), z.number()])` validates if the value matches any of the schemas. The inferred type is `string | number`. For discriminated unions, use `z.discriminatedUnion('type', [...])` for better error messages.

## Q11: How do you define an optional field?
**A:** `z.string().optional()` accepts either a string or undefined. The inferred type is `string | undefined`. Use `.nullable()` for `null`, `.nullish()` for both `null` and `undefined`.

## Q12: How do you define a default value?
**A:** `z.string().default('default')` uses 'default' when the value is undefined. If the field is present but null, it stays null (use `.nullish().default()` for both).

## Q13: How do you parse data with Zod?
**A:** `schema.parse(data)` validates and returns the data if valid, throws `ZodError` if invalid. `schema.safeParse(data)` returns `{ success: true, data }` or `{ success: false, error: ZodError }` without throwing.

## Q14: What is the difference between `parse` and `safeParse`?
**A:** `parse` throws a `ZodError` on validation failure, making it suitable for try-catch. `safeParse` returns a discriminated union result object, making it suitable for functional error handling without try-catch.

## Q15: How do you transform data with Zod?
**A:** Use `.transform(val => transformedVal)`. Pipe operator chains transformations: `z.string().transform(s => s.length).pipe(z.number().min(1))`. Transforms run after validation and can change the output type.

## Q16: What is the `pipe` method in Zod?
**A:** `z.string().pipe(z.number())` applies the first schema for input validation, then pipes the result to the second schema for further validation/transformation. The output type is the second schema's type. Useful for parsing strings to numbers: `z.string().pipe(z.coerce.number())`.

## Q17: How does Zod infer TypeScript types?
**A:** `z.infer<typeof schema>` extracts the TypeScript type from a Zod schema. Example: `const UserSchema = z.object({ name: z.string() }); type User = z.infer<typeof UserSchema>; // { name: string }`. No manual type duplication needed.

## Q18: What is the `z.input` and `z.output` types?
**A:** `z.input<typeof schema>` is the type accepted by `.parse()` (before transformations). `z.output<typeof schema>` is the type returned by `.parse()` (after transformations). For schemas without transform, input and output are the same.

## Q19: How do you handle nested objects in Zod?
**A:** Nest `z.object()` inside another: `z.object({ user: z.object({ name: z.string(), address: z.object({ street: z.string() }) }) })`. Error paths include the full path: `user.address.street`.

## Q20: How do you validate discriminated unions?
**A:** Use `z.discriminatedUnion('type', [z.object({ type: z.literal('a'), a: z.string() }), z.object({ type: z.literal('b'), b: z.number() })])`. Provides better error messages than regular unions by using the discriminator key for branch selection.

## Q21: What is `z.literal()`?
**A:** `z.literal('exact')` validates that the value exactly matches the literal. Works with strings, numbers, booleans. Used in unions and discriminated unions to create tagged types. Inferred type is the literal type `'exact'`.

## Q22: What is `z.any()` and `z.unknown()`?
**A:** `z.any()` accepts any value without validation. `z.unknown()` accepts any value but requires explicit type narrowing before use (safer). Prefer `z.unknown()` over `z.any()` for type safety.

## Q23: What is `z.never()`?
**A:** `z.never()` is a schema that never matches any value. Useful for making certain code paths unreachable or for ensuring exhaustive type checking in conditional schemas.

## Q24: What is `z.void()`?
**A:** `z.void()` accepts undefined (or absent values). Useful for function return type validation and optional fields where the value should always be undefined.

## Q25: What is `z.null()`?
**A:** `z.null()` validates that the value is exactly `null`. Combine with `.nullable()` on other schemas: `z.string().nullable()` accepts `string | null`.

## Q26: What is `z.undefined()`?
**A:** `z.undefined()` validates that the value is exactly `undefined`. Combine with `.optional()` on other schemas for the same effect: `z.string().optional()`.

## Q27: How do you use Zod with TypeScript generics?
**A:** Zod schemas can be generic: `function createSchema<T extends z.ZodTypeAny>(schema: T) { return z.object({ data: schema }) }`. Use `z.infer` to extract the inferred type from generic schemas.

## Q28: How do you create custom error messages in Zod?
**A:** Pass error messages as the first argument to validation methods: `z.string().min(1, 'Name is required').email('Invalid email format')`. For type errors, use `z.string({ required_error: 'Required', invalid_type_error: 'Must be text' })`.

## Q29: How do you customize Zod error messages globally?
**A:** Use `z.setErrorMap(zodErrorMap)` to set a custom error map for all validation errors. The error map function receives the issue and context, returning a custom error message. Can also set per-schema with `z.string({ errorMap: myMap })`.

## Q30: How do you refine a schema with custom validation?
**A:** `.refine((val) => val.length > 5, 'Must be longer than 5')`. The first argument is a validation function, the second is the error message or a function returning a message. `superRefine` provides more control for complex validation.

## Q31: What is `superRefine` in Zod?
**A:** `.superRefine((val, ctx) => { if (val.length < 5) ctx.addIssue({ code: z.ZodIssueCode.custom, message: 'Too short' }) })`. Unlike `refine`, `superRefine` allows adding multiple issues, accessing path context, and conditional issue adding. More powerful than `refine`.

## Q32: How do you do cross-field validation with Zod?
**A:** Use `.refine()` on the parent object: `z.object({ password: z.string(), confirm: z.string() }).refine(data => data.password === data.confirm, { message: 'Passwords do not match', path: ['confirm'] })`. The `path` option points the error to the correct field.

## Q33: What is `path` in Zod error context?
**A:** The `path` property in error issues indicates which field caused the error. For nested objects: `['user', 'address', 'street']`. Used in `superRefine` and `refine` to point errors to specific fields within the parent object.

## Q34: How do you make all object properties optional?
**A:** `.partial()` makes all properties optional: `z.object({ a: z.string(), b: z.number() }).partial()` infers as `{ a?: string; b?: number }`. `.required()` is the inverse, making all properties required.

## Q35: How do you pick/omit fields from a schema?
**A:** `.pick({ a: true, b: true })` selects specific fields. `.omit({ c: true })` excludes specific fields. Both return a new schema with only the specified fields. Useful for creating DTO variants like CreateUserSchema vs UpdateUserSchema.

## Q36: What does `.deepPartial()` do?
**A:** Makes all properties optional recursively through the entire object hierarchy: `z.object({ a: z.object({ b: z.string() }) }).deepPartial()` makes both `a` and `b` optional. Useful for partial update schemas.

## Q37: How do you merge two schemas?
**A:** `schema1.merge(schema2)` combines two object schemas. If both have the same key, schema2's version wins. `z.intersection(schema1, schema2)` creates a TypeScript intersection of both schemas.

## Q38: What is `z.intersection()`?
**A:** Creates a schema that validates against both schemas: `z.intersection(A, B)` validates if the value matches both A and B. Inferred type is `A & B`. Less common than `.merge()` for objects.

## Q39: How do you create a recursive schema (like a tree)?
**A:** Use `z.late(() => schema)` for self-referencing schemas: `const CategorySchema: z.ZodType<Category> = z.late(() => z.object({ id: z.string(), children: z.array(CategorySchema) }))`. The `late` wrapper defers evaluation.

## Q40: How do you handle promises in Zod?
**A:** `z.promise(z.string())` validates that the value is a Promise that resolves to a string. `parse` on a promise schema does not await the promise; use the async methods for that.

## Q41: What are async methods in Zod?
**A:** `parseAsync`, `safeParseAsync`, `refine` (async variant), `superRefine` (async variant). These handle async validation functions, like checking a database for uniqueness. Return Promises.

## Q42: How do you do async validation with Zod?
**A:** Use `schema.refine(async (val) => { const exists = await db.check(val); return !exists; }, 'Already exists')`. Then call `schema.parseAsync(data)` which returns a Promise. The form waits for all async refinements.

## Q43: How do you handle Zod errors?
**A:** `ZodError` has `.issues` (array of issue objects) and `.format()` (nested error format). Each issue has: `code`, `message`, `path`, `received`, `expected`. `.flatten()` returns a flat `{ fieldErrors: { field: [messages] }, formErrors: [] }` format.

## Q44: What is `ZodError.issues`?
**A:** An array of `ZodIssue` objects. Each issue has: `code` (invalid_type, too_small, custom, etc.), `message` (human-readable), `path` (field path array), `received` (what was received), `expected` (what was expected). Iterate for custom error handling.

## Q45: What is `ZodError.format()`?
**A:** Returns a nested object of errors matching the schema shape: `{ name: { _errors: ['Required'] }, address: { street: { _errors: ['Too short'] } } }`. Useful for mapping errors to form fields in libraries like React Hook Form.

## Q46: What is `ZodError.flatten()`?
**A:** Returns a flat structure: `{ fieldErrors: { name: ['Required'], 'address.street': ['Too short'] }, formErrors: [] }`. The keys are dot-path strings. Simpler to work with when you don't need nested structure.

## Q47: How do you use Zod with React Hook Form?
**A:** Use `@hookform/resolvers/zod`. Define a Zod schema. Pass to useForm: `useForm({ resolver: zodResolver(schema) })`. The resolver validates form data against the schema and maps Zod errors to form field errors with proper paths.

## Q48: How do you use Zod with tRPC?
**A:** Zod schemas define input validation for tRPC procedures: `procedure.input(z.object({ name: z.string() })).query(({ input }) => ...)`. tRPC uses Zod schemas to validate inputs and infer TypeScript types automatically.

## Q49: How do you use Zod with Next.js server actions?
**A:** Define a Zod schema for the action input. Call `schema.parse(formData)` at the start of the server action. On `ZodError`, return error messages to the client. Type-safe form handling with server-side validation.

## Q50: How do you use Zod with Express.js?
**A:** Create middleware that validates request body/query/params against a Zod schema. Wrap in try-catch. On `ZodError`, return 400 with formatted errors. Many libraries (zod-express, express-zod-api) provide integration.

## Q51: How do you use Zod with Fastify?
**A:** Fastify natively supports JSON Schema for validation. Use `typebox` or build Zod-to-JSON-Schema converters (`zod-to-json-schema` library) to convert Zod schemas to Fastify-compatible JSON schemas.

## Q52: What is the `z.coerce` namespace?
**A:** `z.coerce.string()`, `z.coerce.number()`, `z.coerce.boolean()`, `z.coerce.date()` coerce the input value to the target type before validation. Example: `z.coerce.number().parse('123')` returns `123` (number). Useful for parsing form data and query strings.

## Q53: What is `z.date()`?
**A:** Validates that the value is a JavaScript Date object. Use `z.coerce.date()` to accept ISO strings and parse them to Date. Constraints: `.min(new Date('2020-01-01'))`, `.max(new Date())`.

## Q54: What is `z.bigint()`?
**A:** Validates BigInt values: `z.bigint()` accepts integer values of type `bigint`. Use `z.coerce.bigint()` to convert strings/numbers to BigInt.

## Q55: What is `z.symbol()`?
**A:** Validates Symbol values. Less commonly used in data validation. `z.symbol()` accepts any symbol. `z.symbol('name')` validates against a specific symbol by description.

## Q56: What is `z.map()` and `z.set()`?
**A:** `z.map(z.string(), z.number())` validates a Map with string keys and number values. `z.set(z.string())` validates a Set of strings. Both validate the collection type and all elements.

## Q57: How do you check if a value matches a schema?
**A:** `schema.safeParse(data).success` returns a boolean. `schema.guard(data)` is a type guard: `if (schema.guard(data)) { data // typed }`. `schema.check(data)` returns boolean (throws on invalid in strict mode).

## Q58: What is `schema.guard()`?
**A:** A type guard function: `if (UserSchema.guard(data)) { data.name // typed as string }`. Returns a boolean and narrows the TypeScript type. Works as `data is z.infer<typeof schema>`.

## Q59: What is `schema.check()`?
**A:** `schema.check(data)` returns `true` if valid, `false` if invalid. Does NOT return error details. Use `safeParse` when you need error information. `check` is for simple boolean checks.

## Q60: How do you create a schema from an existing TypeScript type?
**A:** Use `z.custom<T>()` to create a schema from a TypeScript type without runtime validation: `const schema = z.custom<{ name: string }>()`. Or use `z.object()` matching the type structure for both runtime validation and type inference.

## Q61: What is `z.ZodType`?
**A:** The base class for all Zod schemas. `z.ZodType<Output, Def, Input>` is the generic type for custom schema implementations. Extend it to create custom schema types with custom validation and inference.

## Q62: How do you create a custom Zod schema?
**A:** Use `z.custom<T>((val, ctx) => { if (typeof val !== 'custom') { ctx.addIssue({ code: z.ZodIssueCode.custom, message: 'Must be custom' }); return false; } return true; })`. Or extend `z.ZodType` for reusable custom schemas.

## Q63: How do you use Zod for environment variable validation?
**A:** Define a schema for env vars: `const EnvSchema = z.object({ DATABASE_URL: z.string().url(), PORT: z.coerce.number().default(3000) })`. Call `EnvSchema.parse(process.env)` at app startup. The app fails fast with clear error messages if env vars are misconfigured.

## Q64: How do you use Zod for API response validation?
**A:** Define a schema for the expected API response shape. Parse the fetch response: `const data = ApiResponseSchema.parse(await response.json())`. Catches API contract violations early with clear error messages.

## Q65: How do you use Zod for configuration validation?
**A:** Define a schema for your config object. Parse config at startup: `const config = ConfigSchema.parse(yamlConfig)`. Ensures all required fields are present and correctly typed, failing fast on misconfiguration.

## Q66: What is the Zod `safeParse` return type?
**A:** `{ success: true; data: OutputType } | { success: false; error: ZodError }`. The discriminated union allows type-safe handling: `const result = schema.safeParse(data); if (result.success) { result.data } else { result.error }`.

## Q67: How do you deeply clone a schema?
**A:** `schema.deepPartial()` creates a deep partial clone. `.pick()`, `.omit()`, `.partial()`, `.required()` all return new schema instances. Use `.readonly()` to create a clone with readonly properties.

## Q68: What does `.readonly()` do in Zod?
**A:** Makes all properties in an object schema readonly: `z.object({ name: z.string() }).readonly()` infers as `{ readonly name: string }`. Helps prevent mutation of parsed data.

## Q69: What is `z.preprocess()`?
**A:** Runs a transformation before validation: `z.preprocess((val) => Number(val), z.number())`. Useful for preprocessing inputs like form data (which are strings) before validation. Runs before type checking.

## Q70: How does `z.preprocess` differ from `.transform()`?
**A:** `preprocess` runs before validation, modifying the input. `transform` runs after validation, modifying the output. Preprocess for type coercion (string to number), transform for data enrichment (adding computed fields).

## Q71: How do you create optional chained schemas?
**A:** Chain `.optional()`, `.nullable()`, `.nullish()` at the end: `z.string().email().optional().nullable()`. The order matters - refinement methods should come before optional/nullable wrappers.

## Q72: What is `schema.schema`?
**A:** The internal schema representation. Not typically accessed directly. Used internally by Zod for serialization and introspection. `z.string().schema` returns `{ type: 'string', checks: [...] }`.

## Q73: How do you serialize/deserialize Zod schemas?
**A:** Use `zod-to-json-schema` to convert to JSON Schema for storage or transmission. Use `zod-to-ts` to generate TypeScript types. Schemas can also be serialized as code strings and evaluated.

## Q74: What is the `ZodFirstPartyTypeTypes`?
**A:** An internal Zod type representing the union of all first-party Zod types. Not commonly used in application code. Useful for library developers building on top of Zod.

## Q75: How do you handle discriminators in complex unions?
**A:** Use `z.discriminatedUnion('type', variants)` for tagged unions. Each variant must have a `type` field with a literal value. Zod uses the discriminator to determine which schema to validate against, providing better performance and error messages.

## Q76: How do you validate UUIDs in Zod?
**A:** `z.string().uuid()` validates UUID format (v1 through v5). Also available: `.cuid()`, `.cuid2()`, `.ulid()` for other identifier formats. These are string refinements.

## Q77: How do you validate IP addresses in Zod?
**A:** `z.string().ip()` validates IPv4 and IPv6 addresses. Options: `.ip({ version: 'v4' })` for IPv4 only, `.ip({ version: 'v6' })` for IPv6 only. Also: `z.string().url()` for URLs, `z.string().email()` for emails.

## Q78: How do you validate dates with Zod?
**A:** `z.date()` validates Date objects. Use `.min(new Date('2020-01-01'))`, `.max(new Date())` for range. For string date validation: `z.string().datetime()` (ISO 8601), `z.string().date()` (date-only), `z.string().time()` (time-only).

## Q79: What is `z.string().datetime()`?
**A:** Validates ISO 8601 datetime strings: `2024-01-01T00:00:00.000Z`. Options: `.datetime({ offset: true })` allows timezone offsets. `.datetime({ precision: 3 })` requires millisecond precision.

## Q80: What is `z.string().cuid()`?
**A:** Validates CUID (Collision-resistant Unique IDentifier) format: strings starting with 'c' followed by alphanumeric characters. `.cuid2()` validates the newer CUID2 format. Both are common in web applications.

## Q81: What is `z.string().startsWith()` and `z.string().endsWith()`?
**A:** `z.string().startsWith('prefix')` validates that a string starts with a given prefix. `z.string().endsWith('suffix')` validates the suffix. Useful for validating specific formatted strings like file extensions or identifiers.

## Q82: What is `z.string().includes()`?
**A:** `z.string().includes('sub')` validates that a string contains a substring. Options: `z.string().includes('sub', { position: 5 })` checks if the substring starts at a specific position. Useful for format validation.

## Q83: How do you validate string length in Zod?
**A:** `.min(1)` minimum length, `.max(255)` maximum length, `.length(10)` exact length. Error messages: `z.string().min(1, 'String is required')`. Length refers to string character count.

## Q84: How do you validate number range in Zod?
**A:** `.min(0)` minimum value, `.max(100)` maximum value. `.int()` requires integer. `.positive()` requires > 0. `.negative()` requires < 0. `.nonnegative()` requires >= 0. `.nonpositive()` requires <= 0.

## Q85: How do you validate array length in Zod?
**A:** `.min(1)` minimum elements, `.max(10)` maximum elements, `.length(5)` exact count. `.nonempty()` is shorthand for `.min(1)`. Error messages include the constraint and actual count.

## Q86: How do you validate multiple schemas (AND logic)?
**A:** `z.intersection(A, B)` requires matching both A and B. `.and(B)` is a shorthand: `z.string().min(1).and(z.string().email())`. The inferred type is the intersection of both schemas' outputs.

## Q87: How do you validate one of multiple schemas (OR logic)?
**A:** `z.union([A, B, C])` validates if the value matches any of the schemas. Zod tries each schema in order and returns the first successful match. Advanced: `z.discriminatedUnion` for tagged unions.

## Q88: What is Schema branding in Zod?
**A:** `.brand('BrandName')` creates a branded type: `const UserId = z.string().brand('UserId')`. The inferred type is `string & Brand<'UserId'>`. Prevents mixing different branded types (e.g., passing a PostId where UserId is expected).

## Q89: Why use branded types in Zod?
**A:** Branded types provide nominal typing at the type level without runtime overhead. They prevent accidentally passing the wrong ID type, e.g., `function getUser(id: UserId)` won't accept a plain string or PostId.

## Q90: How do you create a branded email type?
**A:** `const Email = z.string().email().brand('Email')`. `type Email = z.infer<typeof Email>` is `string & z.Brand<'Email'>`. Functions can require `Email` instead of plain `string`.

## Q91: How do you use Zod for form validation with React Hook Form?
**A:** Define schema, use `zodResolver`: `const schema = z.object({ email: z.string().email() }); useForm({ resolver: zodResolver(schema) })`. The resolver maps Zod errors to form field errors. Supports nested objects and arrays.

## Q92: How do you use Zod for API input validation in tRPC?
**A:** Pass Zod schemas to tRPC's `.input()`: `procedure.input(z.object({ id: z.string().uuid() })).query(({ input }) => { ... })`. tRPC validates inputs against the schema and infers TypeScript types automatically.

## Q93: How do you use Zod for environment variable validation in production?
**A:** `const Env = z.object({ NODE_ENV: z.enum(['development', 'production', 'test']), DATABASE_URL: z.string().url(), PORT: z.coerce.number().default(3000) }).parse(process.env)`. Call at app entry point. Export typed Env for use throughout the app.

## Q94: How do you use Zod for parsing query strings?
**A:** Define a schema for query params: `z.object({ page: z.coerce.number().default(1), limit: z.coerce.number().max(100).default(20) }).parse(req.query)`. Uses `z.coerce` since query strings are string values.

## Q95: How do you use Zod for safe JSON parsing?
**A:** Parse unknown JSON: `const data = JSON.parse(jsonString); const validated = schema.parse(data)`. Or use a function: `function parseJSON<T extends z.ZodTypeAny>(schema: T, json: string): z.infer<T> { return schema.parse(JSON.parse(json)) }`.

## Q96: How do you test Zod schemas?
**A:** Write unit tests: `expect(() => schema.parse({ name: 'A' })).not.toThrow()`; `expect(() => schema.parse({})).toThrow()`. Test specific constraints, edge cases, and error messages. Use `safeParse` for assertion-based testing.

## Q97: How do you debug Zod schemas?
**A:** Log the schema: `console.log(schema)`. Use `safeParse` to see error details. Use `.describe('field description')` to add metadata. Use `schema.parse(data, { error: { issues: true } })` for verbose error output.

## Q98: What is the Zod ecosystem?
**A:** Key libraries: `zod-to-json-schema` (convert to JSON Schema), `zod-to-ts` (generate TypeScript types), `@hookform/resolvers/zod` (React Hook Form), `zod-validation-error` (better error messages), `nestjs-zod` (NestJS integration), `ts-to-zod` (generate schemas from TS types).

## Q99: How do you handle Zod errors in a user-friendly way?
**A:** Custom error formatting: map Zod issues to user-facing messages. Use `zod-validation-error` for readable messages. Group errors by field path. Show field-specific and form-level errors separately. Use localization for internationalized messages.

## Q100: What are the best practices for using Zod?
**A:** (1) Define schemas in a central `schemas/` directory, (2) Use `z.infer` for types instead of manual interfaces, (3) Always validate external data (API requests, env vars, config), (4) Use `safeParse` over `parse` for graceful error handling, (5) Brand IDs for type safety, (6) Use discriminated unions for complex objects, (7) Use `z.preprocess` for type coercion, (8) Test critical schemas, (9) Keep schemas DRY with `.pick()`/`.omit()`/`.partial()`, (10) Use async refinement for database-backed validation.
