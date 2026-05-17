# React Hook Form Interview Questions and Answers

## Q1: What is React Hook Form?
**A:** React Hook Form (RHF) is a library for managing form state and validation in React applications. It uses uncontrolled components and native HTML input validation, minimizing re-renders and improving performance. It leverages React hooks for form state management.

## Q2: How does React Hook Form differ from Formik?
**A:** RHF uses uncontrolled components (ref-based) with the native DOM to collect form data, reducing re-renders. Formik uses controlled components with React state, causing more re-renders. RHF also has a smaller bundle size and simpler API for basic forms.

## Q3: How do you install React Hook Form?
**A:** Install via npm: `npm install react-hook-form`. No additional dependencies are required. For validation integration, install `@hookform/resolvers` along with your preferred validation library (zod, yup, joi).

## Q4: What is the `useForm` hook?
**A:** `useForm` is the primary hook that initializes form state and methods. It returns an object with: `register`, `handleSubmit`, `watch`, `getValues`, `setValue`, `formState` (errors, isDirty, isValid, etc.), `reset`, `trigger`, and more.

## Q5: How do you register an input field?
**A:** Use the `register` function returned by `useForm`: `<input {...register('fieldName')} />`. This registers the input with the form, attaching refs and event handlers. The field name becomes the key in the form data object.

## Q6: How do you handle form submission?
**A:** Use `handleSubmit` from `useForm`. It takes two callbacks: `handleSubmit(onSubmit, onError)`. The first receives valid form data, the second receives errors (optional). Example: `<form onSubmit={handleSubmit(onSubmit)}>`.

## Q7: How do you display validation errors?
**A:** Access errors from `formState.errors`: `const { register, handleSubmit, formState: { errors } } = useForm()`. Display: `{errors.fieldName && <p>{errors.fieldName.message}</p>}`. Each error object has `type` and `message` properties.

## Q8: How do you add validation rules to a field?
**A:** Pass validation rules as the second argument to `register`: `{...register('email', { required: 'Email is required', pattern: { value: /^\S+@\S+$/i, message: 'Invalid email' } })}`. Rules include required, minLength, maxLength, pattern, validate (custom), etc.

## Q9: What is the `Controller` component?
**A:** `Controller` wraps controlled components (like React-Select, Material-UI TextField, Ant Design inputs) that don't expose a ref. It uses render props to integrate with RHF: `<Controller name="field" control={control} render={({ field }) => <TextField {...field} />} />`.

## Q10: What is the `useController` hook?
**A:** An alternative to `Controller` for controlled components. `const { field, fieldState } = useController({ name: 'field', control, rules })`. Returns `field` (with onChange, onBlur, value, ref) and `fieldState` (with error, isTouched, isDirty).

## Q11: What is the `control` object in React Hook Form?
**A:** `control` is an object returned by `useForm()` that contains methods for registering fields into the form. It's passed to `Controller` and `useController` to connect controlled components. It can be passed via React context for deep component trees.

## Q12: How do you set a field value programmatically?
**A:** Use `setValue('fieldName', value, config)`. The config object can include `shouldValidate` (trigger validation), `shouldDirty` (mark as dirty), `shouldTouch` (mark as touched). Example: `setValue('email', 'test@test.com', { shouldValidate: true })`.

## Q13: How do you get current form values?
**A:** Two methods: `watch('fieldName')` returns the value of a specific field (causes re-renders on change); `getValues('fieldName')` returns the current value without re-rendering. Use `getValues()` for reading values imperatively.

## Q14: What is the difference between `watch` and `getValues`?
**A:** `watch` subscribes to value changes and triggers re-renders when the watched value changes. `getValues` reads the current value without subscribing or re-rendering. Use `watch` for reactive UI, `getValues` for imperative reads (like onSubmit).

## Q15: How do you reset a form?
**A:** Use the `reset` method. `reset()` resets to initial values. `reset({ fieldName: 'value' })` resets with new values. `reset(undefined, { keepValues: true })` preserves current values. Resets errors, dirty state, and touched state by default.

## Q16: How do you clear errors in React Hook Form?
**A:** Use `clearErrors('fieldName')` to clear a specific field error, or `clearErrors()` to clear all errors. Errors are also cleared when the field value changes and passes validation.

## Q17: How do you set focus on a field?
**A:** Use `setFocus('fieldName')` to programmatically focus a field. It's useful after form submission failure to focus the first field with an error. Works with registered fields that have a ref.

## Q18: What is `formState` in React Hook Form?
**A:** `formState` is a collection of form state properties including: `errors` (validation errors), `isDirty` (any field modified), `dirtyFields` (which fields modified), `touchedFields` (which fields blurred), `isValid` (no validation errors), `isSubmitting`, `isSubmitted`, `submitCount`.

## Q19: What is the difference between `isDirty` and `dirtyFields`?
**A:** `isDirty` is a boolean indicating whether any field has been modified from its default value. `dirtyFields` is an object listing which specific fields have been modified (e.g., `{ name: true, email: true }`).

## Q20: How do you handle form submission with async validation?
**A:** Use the `validate` function in register rules that returns a Promise: `{...register('username', { validate: async (value) => { const taken = await checkUsername(value); return taken ? 'Username taken' : true } })}`. The form waits for all async validations before submitting.

## Q21: How do you integrate Zod with React Hook Form?
**A:** Use `@hookform/resolvers/zod`. Define a Zod schema, then pass it to `useForm`: `const { register, handleSubmit } = useForm({ resolver: zodResolver(schema) })`. The resolver validates form data against the schema and maps errors to form fields.

## Q22: How do you integrate Yup with React Hook Form?
**A:** Use `@hookform/resolvers/yup`. Define a Yup schema: `const schema = yup.object({ email: yup.string().email().required() })`. Pass to useForm: `useForm({ resolver: yupResolver(schema) })`. Yup errors are automatically mapped to form fields.

## Q23: How do you integrate Joi with React Hook Form?
**A:** Use `@hookform/resolvers/joi`. Define a Joi schema, pass to useForm: `useForm({ resolver: joiResolver(schema) })`. Works similarly to other resolvers, mapping validation errors to the correct form fields.

## Q24: What are resolvers in React Hook Form?
**A:** Resolvers are adapters that connect external validation libraries (Zod, Yup, Joi, etc.) to React Hook Form. They convert validation errors from the library's format to RHF's error format. Provided by the `@hookform/resolvers` package.

## Q25: How do you create a custom resolver?
**A:** A resolver is a function that takes `values` and `context` and returns `{ values, errors }`. The errors object should match RHF's field path format. Example: `const customResolver = (values) => { const errors = {}; if (!values.name) errors.name = { type: 'required', message: 'Required' }; return { values, errors } }`.

## Q26: How do you handle nested form objects?
**A:** Use dot notation in field names: `register('address.street')`, `register('address.city')`. The form data becomes `{ address: { street: '...', city: '...' } }`. Arrays use bracket notation: `register('items[0].name')`.

## Q27: How do you handle dynamic form fields (arrays)?
**A:** Use `useFieldArray` hook: `const { fields, append, prepend, remove, swap, move, insert } = useFieldArray({ name: 'items', control })`. Each field has an `id` for the key prop. `append({ name: '' })` adds a new field. `remove(index)` deletes.

## Q28: What is `useFieldArray`?
**A:** A hook for managing form arrays. Returns `fields` (array of field objects with `id`), and methods: `append`, `prepend`, `insert`, `swap`, `move`, `remove`, `replace`, `update`. Each field must have a unique `id` (not the index) for React keys.

## Q29: How do you validate array fields with `useFieldArray`?
**A:** Validation works the same as regular fields. Register each array item: `{...register(`items.${index}.name`, { required: true })}`. For Zod, define an array in the schema: `z.object({ items: z.array(z.object({ name: z.string().min(1) })) })`.

## Q30: How do you set default values for useFieldArray?
**A:** Pass `defaultValues` in `useForm`: `useForm({ defaultValues: { items: [{ name: '' }] } })`. Or use `append` initially: `useEffect(() => { append({ name: '' }) }, [])`. The `fields` array is populated from `defaultValues`.

## Q31: What is the `mode` option in useForm?
**A:** `mode` controls when validation triggers: `onSubmit` (default, validate on submit), `onChange` (validate on every change), `onBlur` (validate on blur), `onTouched` (validate on first blur, then onChange), `all` (validate on both change and blur).

## Q32: What is the `reValidateMode` option?
**A:** Controls when re-validation occurs after submission errors: `onChange` (default, re-validate on change), `onBlur` (re-validate on blur), `onSubmit` (re-validate only on next submit).

## Q33: How do you conditionally show/hide fields?
**A:** Watch the controlling field value: `const showEmail = watch('subscribe')`. Conditionally render: `{showEmail && <input {...register('email')} />}`. RHF handles registration/unregistration automatically when components mount/unmount.

## Q34: How do you handle cross-field validation?
**A:** Use the `validate` function with access to all form values: `{...register('confirmPassword', { validate: (val) => val === watch('password') || 'Passwords do not match' })}`. Or use a resolver with schema-level validations like Zod's `refine`.

## Q35: How does React Hook Form handle performance?
**A:** RHF uses uncontrolled components with native HTML inputs, meaning re-renders are isolated to components using `watch` or `useWatch`. The form state is stored outside React's component tree using refs, minimizing unnecessary re-renders.

## Q36: What is `useWatch`?
**A:** A hook that watches specified fields without causing the entire form to re-render: `const values = useWatch({ name: 'fieldName', control })`. Unlike `watch`, it only re-renders the component that calls it, making it better for performance in large forms.

## Q37: What is the difference between `watch` and `useWatch`?
**A:** `watch` is called from `useForm` and re-renders the component where `useForm` is called. `useWatch` is a standalone hook that subscribes to field changes and only re-renders its own component. Use `useWatch` for isolated value observation.

## Q38: How do you handle form-wide submission with validation?
**A:** Use `handleSubmit(onValid, onInvalid)`. The `onInvalid` callback receives form errors. Useful for scrolling to the first error or showing a summary. The `onValid` callback only fires when all validations pass.

## Q39: How do you disable form submission while submitting?
**A:** Check `formState.isSubmitting`: `<button disabled={isSubmitting}>Submit</button>`. The `isSubmitting` flag is true during async onSubmit execution and resets when it completes.

## Q40: How do you handle file uploads with React Hook Form?
**A:** Register a file input: `<input type="file" {...register('file')} />`. The value is a FileList. For validation, use `validate`: `{...register('file', { validate: (files) => files.length > 0 || 'File required' })}`. Use `Controller` for custom file upload components.

## Q41: How do you integrate React Hook Form with Material-UI?
**A:** Use `Controller` to wrap MUI components: `<Controller name="email" control={control} render={({ field }) => <TextField {...field} error={!!errors.email} helperText={errors.email?.message} />} />`. MUI components are controlled, so Controller is required.

## Q42: How do you integrate React Hook Form with Ant Design?
**A:** Use `Controller` with Ant Design components: `<Controller name="select" control={control} render={({ field }) => <Select {...field} options={options} />} />`. Ant Design's Form.Item' `validateStatus` and `help` can show RHF errors.

## Q43: How do you integrate React Hook Form with Chakra UI?
**A:** Chakra UI inputs accept refs, so `register` works directly: `<Input {...register('name', { required: true })} />`. For errors: `<FormErrorMessage>{errors.name?.message}</FormErrorMessage>`. Use Controller for non-ref components like Switch.

## Q44: How do you integrate React Hook Form with Shadcn UI?
**A:** Shadcn UI components (built on Radix) work well with `Controller`. Use `<Controller name="email" control={control} render={({ field }) => <Input {...field} />} />`. For form fields like Select, wrap with Controller.

## Q45: How do you handle async default values?
**A:** Use `useEffect` to set values after async fetch: `useEffect(() => { fetchUser().then(data => reset(data)) }, [])`. Or pass `values` option to `useForm`: `useForm({ values: asyncData })` which auto-populates when asyncData changes.

## Q46: What is the `values` option in useForm?
**A:** An option to pass external form values: `useForm({ values: userData })`. When `userData` changes, the form is updated. Useful when form data comes from an API or parent component. Avoids manual `reset()` calls.

## Q47: What is the `errors` option in useForm?
**A:** Used to set external errors, typically from server-side validation: `useForm({ errors: serverErrors })`. When serverErrors change, they're merged into `formState.errors`. Useful for showing server validation errors on the client.

## Q48: How do you handle server-side validation errors?
**A:** After form submission fails on the server, map errors back: `setError('email', { type: 'server', message: 'Email already exists' })`. The `setError` method sets errors on specific fields that appear in the form state.

## Q49: What is `setError` used for?
**A:** `setError('fieldName', { type: 'manual', message: 'Error message' })` manually sets an error on a field. Useful for server-side validation, cross-field validation in onSubmit, or business logic errors.

## Q50: How do you trigger validation manually?
**A:** Use `trigger('fieldName')` to validate a specific field, or `trigger()` to validate all fields. Returns a Promise<boolean> indicating if validation passed. Useful for validating on custom events like button clicks.

## Q51: How do you handle form state persistence?
**A:** Save form values to localStorage/watch: `const values = watch(); useEffect(() => { localStorage.setItem('form', JSON.stringify(values)) }, [values])`. On mount, read from localStorage and call `reset(storedValues)`. Use `shouldUnregister: false` to preserve state on unmount.

## Q52: What is `shouldUnregister`?
**A:** An option in `useForm({ shouldUnregister: false })`. When false, field values persist when inputs unmount (conditional rendering). When true (default in v7), unmounting removes the field value. Set to false for multi-step forms or conditional fields.

## Q53: How do you handle multi-step forms (wizard pattern)?
**A:** Keep `useForm` at the parent level. Use conditional rendering for steps: `{step === 1 && <Step1 />}`. Set `shouldUnregister: false` to preserve values across steps. Validate each step using `trigger()` before advancing.

## Q54: How do you validate a multi-step form step-by-step?
**A:** Before advancing to the next step, call `trigger(fieldsOfCurrentStep)` to validate only that step's fields. If validation passes, advance. On final step, call `handleSubmit(onSubmit)`. This gives per-step validation feedback.

## Q55: How do you handle form dirty checking?
**A:** `formState.isDirty` indicates if any field has been modified from default values. `formState.dirtyFields` lists specific dirty fields. Use for "unsaved changes" prompts: `useEffect(() => { if (isDirty) window.onbeforeunload = () => true }, [isDirty])`.

## Q56: How do you get touched field state?
**A:** `formState.touchedFields` is an object like `{ email: true }` indicating which fields have been blurred. Use to conditionally show errors only after a field has been interacted with: `{touchedFields.email && errors.email && <Error/>}`.

## Q57: What is the `shouldFocusError` option?
**A:** When true (default), after form submission with errors, the first field with an error is auto-focused. Set `shouldFocusError: false` in `useForm` to disable this behavior.

## Q58: How do you handle form submit count?
**A:** `formState.submitCount` is a number incremented on each submit attempt. Useful for tracking: `{submitCount > 1 && <p>Tried {submitCount} times</p>}`. Resets with `reset()`.

## Q59: How do you debounce form input?
**A:** Use `useWatch` with a debounce: `const name = useWatch({ name: 'name' }); useEffect(() => { const timeout = setTimeout(() => validateName(name), 300); return () => clearTimeout(timeout) }, [name])`. Or use `useForm({ delayError: 300 })` for error display delay.

## Q60: How do you create a custom input component that works with React Hook Form?
**A:** The component should accept and forward `field` props: `const CustomInput = ({ field, error }) => (<><input {...field} /><Error/></>)`. Use in form: `<Controller name="field" control={control} render={({ field }) => <CustomInput field={field} />} />`.

## Q61: How do you use React Hook Form with TypeScript?
**A:** Use generics: `useForm<{ email: string; password: string }>()`. This types the form values, errors, watch return, etc. Define types/interfaces for form data. Use `FieldValues` from RHF for generic form types.

## Q62: What is `FieldValues`?
**A:** A generic type representing form data: `type FormData = { email: string; password: string }`. Pass to `useForm<FormData>()`. RHF provides `FieldErrors<FormData>` for typed errors and `UseFormRegister<FormData>` for typed register.

## Q63: What is `FieldErrors`?
**A:** A TypeScript type from RHF that represents the errors object structure for a typed form: `FieldErrors<FormData>`. It maps each field to an error object with `message`, `type`, and optional nested errors.

## Q64: How do you type the `register` function with custom props?
**A:** Use `UseFormRegisterReturn`: `const { ref, ...rest } = register('name')`. For custom components, accept `RegisterReturn` props: `interface InputProps extends UseFormRegisterReturn<string> { label: string }`.

## Q65: How do you use `useFormContext`?
**A:** `useFormContext()` provides all useForm methods to nested components without prop drilling. Requires wrapping the form with `<FormProvider {...methods}>`. Components call `const { register } = useFormContext()`.

## Q66: What is `FormProvider`?
**A:** A context provider that passes `useForm` methods down the component tree. Wrap the form with `<FormProvider {...methods}>`. Child components call `useFormContext()` to access register, errors, watch, etc.

## Q67: How do you create a reusable form section?
**A:** Create a component that uses `useFormContext()` to access form methods. Example: `const AddressFields = () => { const { register, errors } = useFormContext(); return (<><input {...register('address.street')} /><Error/></>) }`. Use inside `<FormProvider>`.

## Q68: How do you deeply compare defaultValues?
**A:** Pass `resetOptions` to control reset behavior: `useForm({ defaultValues, resetOptions: { keepDirtyValues: true } })`. By default, RHF does a deep comparison of defaultValues to determine if the form should reset.

## Q69: What is the `resetField` method?
**A:** Resets a single field to its default value: `resetField('fieldName')`. Options: `{ keepError: true, keepDirty: true, keepTouched: true }`. Useful for resetting individual fields without affecting the rest of the form.

## Q70: How do you handle form arrays with nested objects?
**A:** Use dot/bracket notation: `register('users.0.address.street')`. `useFieldArray` returns fields with `id`. Access nested fields: `{...register(`users.${index}.address.street`, { required: true })}`.

## Q71: What is the `useFieldArray` `replace` method?
**A:** `replace(newItems)` completely replaces the field array with new items. Useful after an API call returns updated data. Unlike `remove` + `append`, it's a single operation that preserves field identity where possible.

## Q72: How do you handle field array validation with custom rules?
**A:** Register fields with validation: `{...register(`items.${index}.quantity`, { required: 'Required', min: { value: 1, message: 'Min 1' }, valueAsNumber: true })}`. For schema validation, define the array schema with proper constraints.

## Q73: What is `valueAsNumber` in register?
**A:** An option to automatically convert string input to a number: `{...register('age', { valueAsNumber: true })}`. Other options: `valueAsDate` (convert to Date), `setValueAs` (custom transformation function).

## Q74: What is `valueAsDate` in register?
**A:** Converts the input string to a JavaScript Date object: `{...register('birthday', { valueAsDate: true })}`. The value stored in form state becomes a Date object instead of a string.

## Q75: What is `setValueAs` in register?
**A:** A custom transformation function: `{...register('tags', { setValueAs: (val) => val.split(',').map(s => s.trim()) })}`. Transforms the raw input value before storing it in form state.

## Q76: How do you disable a field in React Hook Form?
**A:** Add the `disabled` attribute: `<input {...register('field')} disabled />`. Disabled fields are not included in form values. To include them, use `readOnly` instead, or configure `shouldUseNativeValidation: false`.

## Q77: How do you handle read-only fields?
**A:** Use the `readOnly` attribute on the input: `<input {...register('readOnlyField')} readOnly />`. Read-only fields are included in form values and validation, but the user cannot modify them.

## Q78: What is `shouldUseNativeValidation`?
**A:** An option in `useForm({ shouldUseNativeValidation: true })`. Uses the browser's native validation constraint API (ValidityState) for error messages. This means the browser's built-in tooltips/popups handle error display.

## Q79: How do you use the native validation API with React Hook Form?
**A:** Set `useForm({ shouldUseNativeValidation: true })`. Add HTML5 validation attributes in `register`: `{...register('email', { required: 'Required' })}`. The browser shows native validation bubbles for errors.

## Q80: How do you handle form focus management?
**A:** Use `setFocus('fieldName')` to programmatically focus a field. Use `shouldFocusError: true` (default) to auto-focus the first field with an error after submission. For custom focus sequences, use `useEffect` with `setFocus`.

## Q81: How do you handle form keyboard shortcuts?
**A:** Use `watch` and `useEffect` to listen for specific key combinations. Or use `handleSubmit` with `onKeyDown` handlers on specific fields. Submitting via Enter on an input triggers the form's onSubmit.

## Q82: How do you handle form autofill?
**A:** Browsers autofill works with registered fields. Use proper `name` attributes matching common autofill tokens: `name="email"`, `name="tel"`, `name="address-line1"`, etc. Set `autoComplete` attribute: `<input autoComplete="email" {...register('email')} />`.

## Q83: How do you prevent XSS in form values?
**A:** React Hook Form stores raw input values. Sanitize before rendering or sending to the server: `const sanitized = DOMPurify.sanitize(value)`. RHF doesn't sanitize by default; implement sanitization in the onSubmit handler or transformer.

## Q84: How do you test React Hook Form components?
**A:** Use React Testing Library. Render the form component. Use `fireEvent.change` and `fireEvent.submit`. For controlled components, test via Controller. Use `waitFor` for async validation. RHF provides testing utilities but is testable with standard tools.

## Q85: How do you test form submission with React Hook Form?
**A:** Render the form with a mock onSubmit. `fireEvent.change(input, { target: { value: 'test' } })`. `fireEvent.click(submitButton)`. Assert `onSubmit` was called with correct data. For validation, check that errors are displayed.

## Q86: How do you test field validation with React Hook Form?
**A:** Render the form, submit without filling required fields. Assert error messages appear. For pattern validation, fill with invalid format and assert error. For async validation, use `waitFor` to wait for validation to complete.

## Q87: How do you handle form change detection between different form instances?
**A:** Each `useForm` instance is independent. Use `reset` with `keepDirtyValues` when switching between forms. Compare `getValues()` snapshots to detect changes. Use `formState.isDirty` per instance.

## Q88: What is the `shouldUseNativeValidation` option?
**A:** When true, RHF uses the browser's native validation constraint API (ValidityState) instead of managing validation internally. This leverages the browser's built-in validation UI (tooltips, styling) but limits customization.

## Q89: How do you handle form state with URL query parameters?
**A:** Watch all fields: `const values = watch()`. Sync to URL: `useEffect(() => { updateQueryParams(values) }, [values])`. On mount, read URL params and `reset(queryParams)`. Use `shouldUnregister: false` to preserve state.

## Q90: How do you handle form auto-save?
**A:** Watch form values: `const values = watch()`. Debounce the save: `useEffect(() => { const timeout = setTimeout(() => save(values), 2000); return () => clearTimeout(timeout) }, [values])`. Show "Saving..." / "Saved" indicator based on save state.

## Q91: How do you implement a "dirty form" confirmation dialog?
**A:** Use `formState.isDirty` with `BeforeUnloadEvent`: `useEffect(() => { if (isDirty) { window.onbeforeunload = () => '' }; return () => { window.onbeforeunload = null } }, [isDirty])`. For in-app navigation, use a router's blocking mechanism.

## Q92: How do you handle form keyboard navigation?
**A:** Register inputs and let the browser handle Tab/Shift+Tab naturally. Use `ref` forwarding for custom inputs. For custom sequences, use `setFocus` and keyboard event handlers on the form element.

## Q93: How do you implement a custom form input with controlled state?
**A:** Use `Controller`: `<Controller name="custom" control={control} render={({ field: { value, onChange } }) => <CustomInput value={value} onChange={onChange} />} />`. The custom input manages its internal state and calls onChange when the value changes.

## Q94: How do you handle form data transformation on submit?
**A:** Transform in the onSubmit handler: `const onSubmit = (data) => { const transformed = { ...data, amount: Number(data.amount) }; api.submit(transformed) }`. For automatic transformation, use `setValueAs` in register or a resolver.

## Q95: How do you handle conditional required fields?
**A:** Use dynamic validation based on another field: `const required = watch('hasPhone'); register('phone', { required: required ? 'Phone required' : false })`. When `hasPhone` changes, the phone field's required rule updates.

## Q96: How do you handle form arrays with useFieldArray and TypeScript?
**A:** Define typed array items: `interface Item { name: string; quantity: number }`. Use `useFieldArray<{ items: Item[] }>({ name: 'items' })`. Each `field` in `fields` is typed as `Item & { id: string }`.

## Q97: How do you use `useFieldArray` with nested arrays?
**A:** RHF supports nested arrays: `useFieldArray({ name: 'groups' })` where each group has an inner array. Use nested `useFieldArray`: `const { fields: itemFields } = useFieldArray({ name: `groups.${groupIndex}.items`, control })`.

## Q98: What is the `append` method options in useFieldArray?
**A:** `append(obj, options)`. Options include: `{ shouldFocus: true }` (auto-focus the new field). Can pass empty object `append({})` to add a default-value item. Multiple items: `append([obj1, obj2])`.

## Q99: How do you handle form performance with large forms (50+ fields)?
**A:** Use `useWatch` instead of `watch` for isolated subscriptions. Avoid re-rendering the entire form by splitting into sub-components with `useFormContext`. Use `shouldUnregister: false` to prevent re-registration overhead. Use field arrays sparingly.

## Q100: What are the main advantages of React Hook Form?
**A:** Key advantages: (1) Performance - uncontrolled inputs minimize re-renders, (2) Bundle size - small (~10KB gzipped), (3) Simplicity - minimal boilerplate, (4) Native HTML validation support, (5) Excellent TypeScript support, (6) Integrations with validation libraries (Zod, Yup), (7) Support for complex forms (nested, arrays, dynamic), (8) Active community and maintenance.
