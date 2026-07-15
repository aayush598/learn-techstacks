# Forms Typing in React + TypeScript

## Overview

Forms are a core part of React applications. Properly typed forms prevent bugs, provide better DX, and integrate well with validation libraries.

---

## 1. Controlled Component Typing

```typescript
import React, { useState } from 'react';

// Basic controlled input
function ControlledInput() {
  const [value, setValue] = useState('');

  return (
    <input
      value={value}
      onChange={(e: React.ChangeEvent<HTMLInputElement>) => setValue(e.target.value)}
    />
  );
}

// Multi-field form with single state object
interface FormState {
  firstName: string;
  lastName: string;
  email: string;
  age: number;
  newsletter: boolean;
}

function MultiFieldForm() {
  const [form, setForm] = useState<FormState>({
    firstName: '',
    lastName: '',
    email: '',
    age: 0,
    newsletter: false,
  });

  const handleChange = <K extends keyof FormState>(
    field: K,
    value: FormState[K]
  ) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  return (
    <form>
      <input
        value={form.firstName}
        onChange={(e) => handleChange('firstName', e.target.value)}
        placeholder="First name"
      />
      <input
        value={form.lastName}
        onChange={(e) => handleChange('lastName', e.target.value)}
        placeholder="Last name"
      />
      <input
        value={form.email}
        onChange={(e) => handleChange('email', e.target.value)}
        type="email"
        placeholder="Email"
      />
      <input
        value={form.age}
        onChange={(e) => handleChange('age', Number(e.target.value))}
        type="number"
        placeholder="Age"
      />
      <label>
        <input
          checked={form.newsletter}
          onChange={(e) => handleChange('newsletter', e.target.checked)}
          type="checkbox"
        />
        Subscribe to newsletter
      </label>
    </form>
  );
}

// Dynamic form fields
interface DynamicFormState {
  [key: string]: string | number | boolean;
}

function DynamicForm({ fields }: { fields: { name: string; type: string; label: string }[] }) {
  const [values, setValues] = useState<Record<string, string>>({});

  const handleChange = (name: string, value: string) => {
    setValues((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <form>
      {fields.map((field) => (
        <div key={field.name}>
          <label htmlFor={field.name}>{field.label}</label>
          <input
            id={field.name}
            name={field.name}
            type={field.type as string}
            value={values[field.name] ?? ''}
            onChange={(e) => handleChange(field.name, e.target.value)}
          />
        </div>
      ))}
    </form>
  );
}
```

---

## 2. Form State Typing

```typescript
// Comprehensive form state type
interface FormFieldState<T> {
  value: T;
  error: string | null;
  touched: boolean;
  dirty: boolean;
}

type FormStateV2<T extends Record<string, any>> = {
  [K in keyof T]: FormFieldState<T[K]>;
};

// Form meta state
interface FormMeta {
  isSubmitting: boolean;
  isValid: boolean;
  submitCount: number;
  submitError: string | null;
}

// Complete form state
interface CompleteFormState<T extends Record<string, any>> {
  fields: FormStateV2<T>;
  meta: FormMeta;
}

// Usage
interface LoginFormFields {
  email: string;
  password: string;
  rememberMe: boolean;
}

function createInitialFormState<T extends Record<string, any>>(
  defaults: T
): FormStateV2<T> {
  const state = {} as FormStateV2<T>;
  for (const key of Object.keys(defaults) as (keyof T)[]) {
    (state as any)[key] = {
      value: defaults[key],
      error: null,
      touched: false,
      dirty: false,
    };
  }
  return state;
}

const initialForm = createInitialFormState<LoginFormFields>({
  email: '',
  password: '',
  rememberMe: false,
});
```

---

## 3. Validation Patterns with Types

```typescript
// Type-safe validation with Zod
import { z } from 'zod';

const RegisterSchema = z.object({
  username: z.string().min(3).max(20).regex(/^[a-zA-Z0-9_]+$/),
  email: z.string().email(),
  password: z.string().min(8).regex(/[A-Z]/).regex(/[0-9]/),
  confirmPassword: z.string(),
  age: z.number().int().min(13).max(120),
  terms: z.literal(true, {
    errorMap: () => ({ message: 'You must accept the terms' }),
  }),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

type RegisterFormData = z.infer<typeof RegisterSchema>;

// Custom validation function with types
type ValidationRule<T> = {
  validate: (value: T) => boolean;
  message: string;
};

type ValidationSchema<T> = {
  [K in keyof T]?: ValidationRule<T[K]>[];
};

function validateForm<T extends Record<string, any>>(
  data: T,
  schema: ValidationSchema<T>
): Partial<Record<keyof T, string[]>> {
  const errors: Partial<Record<keyof T, string[]>> = {};

  for (const field of Object.keys(schema) as (keyof T)[]) {
    const rules = schema[field];
    if (!rules) continue;

    const fieldErrors: string[] = [];
    for (const rule of rules) {
      if (!rule.validate(data[field])) {
        fieldErrors.push(rule.message);
      }
    }

    if (fieldErrors.length > 0) {
      errors[field] = fieldErrors;
    }
  }

  return errors;
}

// Usage
interface UserForm {
  name: string;
  email: string;
  age: number;
}

const userSchema: ValidationSchema<UserForm> = {
  name: [
    { validate: (v) => v.length > 0, message: 'Name is required' },
    { validate: (v) => v.length >= 2, message: 'Name too short' },
  ],
  email: [
    { validate: (v) => v.length > 0, message: 'Email is required' },
    { validate: (v) => v.includes('@'), message: 'Invalid email' },
  ],
  age: [
    { validate: (v) => v >= 13, message: 'Must be 13 or older' },
  ],
};

const errors = validateForm({ name: '', email: 'bad', age: 10 }, userSchema);
```

---

## 4. react-hook-form Typing

```typescript
import { useForm, useFieldArray, Control, FieldErrors } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Schema with Zod
const JobApplicationSchema = z.object({
  fullName: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email'),
  phone: z.string().regex(/^\+?[\d\s-]+$/, 'Invalid phone'),
  experiences: z.array(z.object({
    company: z.string().min(1),
    role: z.string().min(1),
    years: z.number().min(0),
    skills: z.array(z.string()).min(1, 'At least one skill'),
  })).min(1, 'At least one experience required'),
  education: z.array(z.object({
    institution: z.string().min(1),
    degree: z.string().min(1),
    year: z.number().min(1900).max(2030),
  })),
});

type JobApplicationData = z.infer<typeof JobApplicationSchema>;

// Form component
function JobApplicationForm() {
  const {
    register,
    control,
    handleSubmit,
    formState: { errors, isSubmitting, isValid },
  } = useForm<JobApplicationData>({
    resolver: zodResolver(JobApplicationSchema),
    defaultValues: {
      fullName: '',
      email: '',
      phone: '',
      experiences: [{ company: '', role: '', years: 0, skills: [] }],
      education: [],
    },
  });

  const {
    fields: experienceFields,
    append: appendExperience,
    remove: removeExperience,
  } = useFieldArray({
    control,
    name: 'experiences',
  });

  const onSubmit = async (data: JobApplicationData) => {
    console.log('Submitted:', data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <input {...register('fullName')} placeholder="Full name" />
        {errors.fullName && <span>{errors.fullName.message}</span>}
      </div>

      <div>
        <input {...register('email')} placeholder="Email" />
        {errors.email && <span>{errors.email.message}</span>}
      </div>

      <div>
        <input {...register('phone')} placeholder="Phone" />
        {errors.phone && <span>{errors.phone.message}</span>}
      </div>

      <h3>Experiences</h3>
      {experienceFields.map((field, index) => (
        <div key={field.id}>
          <input {...register(`experiences.${index}.company`)} placeholder="Company" />
          {errors.experiences?.[index]?.company && (
            <span>{errors.experiences[index]?.company?.message}</span>
          )}

          <input {...register(`experiences.${index}.role`)} placeholder="Role" />
          <input
            {...register(`experiences.${index}.years`, { valueAsNumber: true })}
            type="number"
            placeholder="Years"
          />

          {errors.experiences?.[index]?.skills && (
            <span>{errors.experiences[index]?.skills?.message}</span>
          )}

          <button type="button" onClick={() => removeExperience(index)}>
            Remove
          </button>
        </div>
      ))}

      <button type="button" onClick={() => appendExperience({ company: '', role: '', years: 0, skills: [] })}>
        Add Experience
      </button>

      <button type="submit" disabled={isSubmitting || !isValid}>
        Submit
      </button>
    </form>
  );
}

// Typed form field component
interface FormFieldProps {
  label: string;
  error?: string;
  children: React.ReactNode;
}

function FormField({ label, error, children }: FormFieldProps) {
  return (
    <div className="form-field">
      <label>{label}</label>
      {children}
      {error && <span className="error">{error}</span>}
    </div>
  );
}
```

---

## 5. Formik with Types

```typescript
import { Formik, Form, Field, ErrorMessage, FieldProps } from 'formik';
import * as Yup from 'yup';

// Validation schema
const ValidationSchema = Yup.object().shape({
  name: Yup.string().required('Name is required'),
  email: Yup.string().email('Invalid email').required('Email is required'),
  message: Yup.string().min(10, 'Too short').max(500, 'Too long').required(),
  priority: Yup.string().oneOf(['low', 'medium', 'high']).required(),
});

// Form values type
interface ContactFormValues {
  name: string;
  email: string;
  message: string;
  priority: 'low' | 'medium' | 'high';
}

// Typed custom field
interface CustomInputProps extends FieldProps<string> {
  label: string;
  placeholder?: string;
}

const CustomInput: React.FC<CustomInputProps> = ({ field, form, label, placeholder }) => (
  <div>
    <label>{label}</label>
    <input {...field} placeholder={placeholder} />
    {form.touched[field.name] && form.errors[field.name] && (
      <span className="error">{form.errors[field.name]}</span>
    )}
  </div>
);

// Form component
function ContactForm() {
  return (
    <Formik<ContactFormValues>
      initialValues={{
        name: '',
        email: '',
        message: '',
        priority: 'medium',
      }}
      validationSchema={ValidationSchema}
      onSubmit={async (values, { setSubmitting }) => {
        await submitContactForm(values);
        setSubmitting(false);
      }}
    >
      {({ isSubmitting, isValid }) => (
        <Form>
          <Field name="name" label="Name" component={CustomInput} />
          <Field name="email" label="Email" component={CustomInput} />

          <div>
            <label>Message</label>
            <Field name="message" as="textarea" rows={5} />
            <ErrorMessage name="message" component="span" className="error" />
          </div>

          <div>
            <label>Priority</label>
            <Field name="priority" as="select">
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </Field>
          </div>

          <button type="submit" disabled={isSubmitting || !isValid}>
            {isSubmitting ? 'Sending...' : 'Send'}
          </button>
        </Form>
      )}
    </Formik>
  );
}
```

---

## 6. Field Arrays

```typescript
import { useFieldArray, useForm, Control } from 'react-hook-form';

// Typed field array
interface InvoiceItem {
  description: string;
  quantity: number;
  unitPrice: number;
  total: number;
}

interface InvoiceForm {
  invoiceNumber: string;
  items: InvoiceItem[];
}

function InvoiceForm() {
  const { control, register, watch, setValue } = useForm<InvoiceForm>({
    defaultValues: {
      invoiceNumber: '',
      items: [{ description: '', quantity: 1, unitPrice: 0, total: 0 }],
    },
  });

  const { fields, append, remove, move } = useFieldArray({
    control,
    name: 'items',
  });

  // Watch for item changes to calculate total
  const watchedItems = watch('items');
  const invoiceTotal = watchedItems.reduce((sum, item) => sum + item.total, 0);

  const updateItemTotal = (index: number) => {
    const item = watchedItems[index];
    if (item) {
      setValue(`items.${index}.total`, item.quantity * item.unitPrice);
    }
  };

  return (
    <form>
      <input {...register('invoiceNumber')} placeholder="Invoice #" />

      {fields.map((field, index) => (
        <div key={field.id} className="invoice-item">
          <input {...register(`items.${index}.description`)} placeholder="Description" />
          <input
            {...register(`items.${index}.quantity`, { valueAsNumber: true })}
            type="number"
            min={1}
            onChange={() => updateItemTotal(index)}
          />
          <input
            {...register(`items.${index}.unitPrice`, { valueAsNumber: true })}
            type="number"
            min={0}
            step={0.01}
            onChange={() => updateItemTotal(index)}
          />
          <span>${watchedItems[index]?.total.toFixed(2)}</span>
          <button type="button" onClick={() => remove(index)}>Remove</button>
          <button type="button" onClick={() => move(index, index - 1)} disabled={index === 0}>↑</button>
        </div>
      ))}

      <button type="button" onClick={() => append({ description: '', quantity: 1, unitPrice: 0, total: 0 })}>
        Add Item
      </button>

      <div>Total: ${invoiceTotal.toFixed(2)}</div>
    </form>
  );
}
```

---

## 7. Error Typing

```typescript
// Comprehensive error types
interface FieldError {
  type: string;
  message: string;
}

interface FormErrors<T> {
  [K in keyof T]?: FieldError | string | FormErrors<T[K]>;
}

// Nested error access
type NestedError<T> = {
  [K in keyof T]?: T[K] extends Array<infer U>
    ? NestedError<U>[]
    : T[K] extends object
    ? NestedError<T[K]>
    : string | undefined;
};

// Error display component
interface ErrorDisplayProps {
  errors: Record<string, any>;
  field: string;
}

function ErrorDisplay({ errors, field }: ErrorDisplayProps) {
  const error = field.split('.').reduce((obj, key) => obj?.[key], errors);
  if (!error) return null;

  const message = typeof error === 'string' ? error : error.message;
  return <span className="error">{message}</span>;
}

// Type-safe error getter
function getFieldError(errors: Record<string, any>, path: string): string | undefined {
  const keys = path.split('.');
  let current: any = errors;

  for (const key of keys) {
    if (current === undefined || current === null) return undefined;
    current = current[key];
  }

  if (typeof current === 'string') return current;
  if (current?.message) return current.message;
  return undefined;
}
```

---

## 8. Best Practices

1. **Use Zod or Yup** for runtime validation with TypeScript inference.
2. **Prefer react-hook-form** for performance — minimal re-renders.
3. **Type form state as a single interface** — one source of truth.
4. **Use `z.infer`** to derive form data types from schemas.
5. **Type error objects** to match form state shape.
6. **Use `useFieldArray`** for dynamic field lists.
7. **Prefer controlled components** for complex validation needs.
8. **Type event handlers** for form inputs specifically.

---

## Interview Questions

1. How do you type a controlled form with multiple fields?
2. What is the difference between react-hook-form and Formik in TypeScript?
3. How do you type field arrays with react-hook-form?
4. Create a type-safe validation function.
5. How do you type nested form errors?
6. What is the benefit of using Zod with react-hook-form?
7. How do you handle dynamic form fields in TypeScript?
8. How do you type a custom form field component?
9. Explain the `FormState` type from react-hook-form.
10. How do you prevent type errors in form submissions?
