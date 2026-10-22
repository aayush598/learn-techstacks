# API Error → Form Field Mapping

> Part XIV · Chapter 37 · Sections 37.7–37.8 · _Estimated reading time: 18 min_
> **Prerequisite:** [Forms, API Response Errors, Validation Mapping](../01-concepts/04-forms-api-validation-mapping.md), [Full-Stack Contracts](../../38-full-stack-error-contracts/README.md)

## In one sentence

**Map `application/problem+json` validation errors to specific form fields and a cross-field summary, preserve user input, use error codes for logic, and keep messages localizable.**

## Real-world use case

**Acme SaaS** org creation: API returns `422` with `invalid_params` (`slug` taken, `domain` invalid). UI must show per-field errors without clearing the form; domain rule may go to summary if it's cross-cutting.

## Key data / numbers

| Status | Action |
| ------ | ------ |
| **422** | Parse `invalid_params` → map to fields/summaries |
| **400** | Often malformed → summary fallback |
| **409** | Conflict → field if resource-specific else summary |
| **401/403/429** | Flow-level, not field errors (route to auth/retry) |

## Types

```ts
export type ApiErrorDetails = {
  invalid_params?: Array<{
    field?: string;      // e.g., "email", "address.city", "form"
    code?: string;       // stable machine code e.g., "EMAIL_TAKEN"
    message?: string;    // server hint (may be overridden by i18n)
    value?: unknown;
  }>;
  [k: string]: unknown;
};

export type ApiError = {
  status: number;
  title?: string;
  detail?: string;
  error_id?: string;
  details?: ApiErrorDetails;
};
```

## Mapping function

```ts
import { FieldValues, UseFormSetError } from 'react-hook-form';

export type FieldErrorSetter<T extends FieldValues> = UseFormSetError<T>;

export function mapApiValidationErrors<T extends FieldValues>(
  err: ApiError,
  setError: FieldErrorSetter<T>,
  setFormError: (msg: string | null) => void,
  t?: (code: string, fallback?: string) => string
) {
  setFormError(null);
  if (err.status !== 422) throw err; // let caller handle other cases
  const params = err.details?.invalid_params;
  if (!Array.isArray(params) || params.length === 0) {
    setFormError(err.detail || err.title || 'Validation failed. Please check your input.');
    return;
  }
  let hasFieldError = false;
  for (const p of params) {
    const code = p.code || 'INVALID';
    const msg = t ? t(`errors.codes.${code}`, p.message || mapDefault(code)) : (p.message || mapDefault(code));
    if (p.field && p.field !== 'form') {
      // support nested paths react-hook-form understands
      setError(p.field as any, { type: code, message: msg });
      hasFieldError = true;
    } else {
      setFormError(msg);
    }
  }
  if (!hasFieldError && !err.details?.invalid_params?.some(p => p.field && p.field !== 'form')) {
    // already set form error if any
  }
}

function mapDefault(code: string) {
  switch (code) {
    case 'EMAIL_TAKEN': return 'This email is already in use.';
    case 'SLUG_TAKEN': return 'This slug is already taken.';
    case 'SLUG_INVALID': return 'Slug contains invalid characters.';
    case 'REQUIRED': return 'This field is required.';
    default: return 'Invalid value.';
  }
}
```

## Form usage (react-hook-form)

```tsx
import { useForm } from 'react-hook-form';
import { mapApiValidationErrors } from './mapApiValidationErrors';

type OrgForm = { name: string; slug: string; email: string };

export function CreateOrgForm() {
  const { register, handleSubmit, setError, formState: { errors } } = useForm<OrgForm>();
  const [formError, setFormError] = useState<string|null>(null);

  const onSubmit = async (values: OrgForm) => {
    setFormError(null);
    try {
      await api.post('/orgs', values);
      navigate('/orgs/created');
    } catch (e: any) {
      if (e.status === 422) {
        mapApiValidationErrors(e, setError, setFormError);
        return; // expected, do not throw
      }
      if (e.status === 401) return triggerAuthExpiry(e);
      throw e; // unexpected
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label>Org name</label>
        <input {...register('name')} />
        {errors.name && <span role="alert">{errors.name.message}</span>}
      </div>
      <div>
        <label>Slug</label>
        <input {...register('slug')} />
        {errors.slug && <span role="alert">{errors.slug.message}</span>}
      </div>
      <div>
        <label>Admin email</label>
        <input {...register('email')} />
        {errors.email && <span role="alert">{errors.email.message}</span>}
      </div>
      {formError && <div role="alert">{formError}</div>}
      <button type="submit">Create</button>
    </form>
  );
}
```

## Handling nested paths

For nested objects (`address.city`), react-hook-form accepts dot paths with `setError`. Ensure the API uses consistent paths matching form shape.

## Real-world use case recap

**Checkout:** address validation fails on `address.zip` — map to that field; card validation may be cross-field → summary. User fixes only the zip without re-entering card details.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Show all in summary | Simple | User doesn't know which field | Bad for large forms |
| Map per field | Great UX | Needs schema alignment | **Recommended default** |
| Ignore server and only client | Fast | Misses business rules | Insufficient |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Preserve all form values on 422 | Reset form on validation errors |
| Use codes for logic; allow i18n override | Hardcode server messages everywhere |
| Put cross-field in summary banner | Attach cross-field to arbitrary field |
| Throw for 401/500/network to proper handlers | Treat auth/network as field errors |

## Common mistakes

- **Clearing form.** Loses work.
- **Wrong paths.** Nested fields don't map.
- **Mixing expected/unexpected.** 500 becomes "field error".
- **Leaking internals.** Showing SQL/constraint names.

## Checklist

- [ ] 422 parsed safely with guards.
- [ ] Field vs summary split implemented.
- [ ] Nested paths supported.
- [ ] Codes used for mapping + i18n ready.
- [ ] Non-validation errors routed correctly.

## Related

- [Forms, API Validation Mapping (Concept)](../01-concepts/04-forms-api-validation-mapping.md)
- [Full-Stack — Mapping API→UI and Validation→Fields](../../38-full-stack-error-contracts/01-concepts/02-mapping-api-to-ui-and-validation-to-fields.md)
- [Shared Error Code Enum (Practical)](./03-shared-error-code-enum-frontend-backend.md)
