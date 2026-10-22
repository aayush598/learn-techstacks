# API Error → Form Field Mapping (End-to-End)

> Part XIV · Chapter 38 · Sections 38.3–38.4 · _Estimated reading time: 18 min_
> **Prerequisite:** [Chapter 37 — API Error to Form Field Mapping](../../37-frontend-error-handling/03-practical-examples/02-api-error-to-form-field-mapping.md), [Shared Enum](./01-shared-error-code-enum-typescript.md)

## In one sentence

**End-to-end mapping:** backend emits Problem Details with `invalid_params` and shared codes; frontend mapper converts to field errors and summary with i18n, preserving inputs and using safe fallbacks.

## Backend (emit)

```ts
import { ErrorCode, ProblemDetails } from '@acme/errors';

function validationProblem(invalid: Array<{field?:string; code: ErrorCode; message?:string}>): ProblemDetails {
  return {
    type: 'https://api.acme.com/errors/validation-failed',
    title: 'Validation failed',
    status: 422,
    detail: 'One or more fields are invalid',
    error_id: `err_${nanoid()}`,
    code: ErrorCode.VALIDATION_FAILED,
    invalid_params: invalid,
  };
}

// POST /orgs
if (!isSlugValid(slug)) {
  return res.status(422).json(validationProblem([
    { field: 'slug', code: ErrorCode.SLUG_INVALID, message: 'Slug format invalid.' }
  ]));
}
if (await slugTaken(slug)) {
  return res.status(422).json(validationProblem([
    { field: 'slug', code: ErrorCode.SLUG_TAKEN }
  ]));
}
```

## Frontend mapper (full)

```ts
import { ErrorCode, isErrorCode, ProblemDetails } from '@acme/errors';
import { FieldValues, UseFormSetError } from 'react-hook-form';

export function applyProblemToForm<T extends FieldValues>(
  p: ProblemDetails,
  setError: UseFormSetError<T>,
  setFormError: (m: string | null) => void,
  t: (k: string, d?: string) => string
) {
  setFormError(null);
  if (p.status !== 422) throw p as any;
  const params = p.invalid_params || [];
  if (params.length === 0) {
    setFormError(t('errors.validation.generic', p.detail || 'Validation failed.'));
    return;
  }
  let hasField = false;
  for (const ip of params) {
    const code = isErrorCode(ip.code) ? ip.code : ErrorCode.VALIDATION_FAILED;
    const key = `errors.codes.${code}`;
    const msg = t(key, ip.message || t('errors.validation.generic'));
    if (ip.field && ip.field !== 'form') {
      setError(ip.field as any, { type: code, message: msg });
      hasField = true;
    } else {
      setFormError(msg);
    }
  }
  if (!hasField && params.every(x => !x.field || x.field === 'form')) {
    // form error already set
  }
}
```

## Form component

```tsx
export function CreateOrgForm() {
  const { register, handleSubmit, setError, formState:{errors} } = useForm();
  const [formError, setFormError] = useState<string|null>(null);
  const { t } = useTranslation();

  const onSubmit = async (v:any) => {
    setFormError(null);
    try {
      await api.post('/orgs', v);
      navigate('/orgs/created');
    } catch (e:any) {
      const p = e.problem as ProblemDetails | undefined;
      if (e.status === 422 && p) {
        applyProblemToForm(p, setError, setFormError, t);
        return;
      }
      if (e.status === 401) return triggerAuthExpiry(e);
      throw e;
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('slug')} aria-invalid={!!errors.slug} />
      {errors.slug && <span role="alert">{errors.slug.message}</span>}
      {formError && <div role="alert">{formError}</div>}
      <button type="submit">Create</button>
    </form>
  );
}
```

## Testing notes

- Test field mapping, nested paths, cross-field, unknown codes
- Test form preservation on 422
- Test auth/network routed correctly

## Real-world use case

**Acme SaaS:** org creation and **Checkout** billing address both use same mapper; consistent UX.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Tight coupling to react-hook-form | Easy | Less reusable | Fine if standard |
| Adapter pattern | Reusable | Extra layer | **Recommended for shared lib** |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Preserve values on 422 | Clear form |
| Localize by code | Render server detail verbatim |
| Handle unknown codes safely | Throw on unknown |

## Checklist

- [ ] Backend emits correct envelope + codes
- [ ] Frontend maps deterministically
- [ ] i18n integrated
- [ ] Form tests cover mapping
- [ ] Non-validation errors handled

## Related

- [API Error → Form Field Mapping (Ch37)](../../37-frontend-error-handling/03-practical-examples/02-api-error-to-form-field-mapping.md)
- [Shared Error Code Enum](./01-shared-error-code-enum-typescript.md)
- [Mapping Concepts](../01-concepts/02-mapping-api-to-ui-and-validation-to-fields.md)
