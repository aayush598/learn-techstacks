# Event Handling in React + TypeScript

## Overview

React wraps native DOM events in SyntheticEvents. TypeScript provides specific types for every event, ensuring you only access properties that exist on the event.

---

## 1. React Event Types

```typescript
import React from 'react';

// All React event types are in React namespace
type ChangeEvent = React.ChangeEvent<HTMLInputElement>;
type ClickEvent = React.MouseEvent<HTMLButtonElement>;
type FormEvent = React.FormEvent<HTMLFormElement>;
type KeyboardEvent = React.KeyboardEvent<HTMLInputElement>;
type FocusEvent = React.FocusEvent<HTMLInputElement>;
type BlurEvent = React.FocusEvent<HTMLInputElement>;
type SubmitEvent = React.FormEvent<HTMLFormElement>;
type ScrollEvent = React.UIEvent<HTMLDivElement>;
type WheelEvent = React.WheelEvent<HTMLDivElement>;
type TouchEvent = React.TouchEvent<HTMLDivElement>;
type DragEvent = React.DragEvent<HTMLDivElement>;
type ClipboardEvent = React.ClipboardEvent<HTMLInputElement>;
type AnimationEvent = React.AnimationEvent<HTMLDivElement>;
type TransitionEvent = React.TransitionEvent<HTMLDivElement>;
```

---

## 2. SyntheticEvent

```typescript
import React from 'react';

// Base SyntheticEvent
function handleClick(event: React.SyntheticEvent) {
  event.preventDefault();    // Prevent default browser behavior
  event.stopPropagation();   // Stop event bubbling

  // event.target — the element that triggered the event
  // event.currentTarget — the element the handler is attached to

  const target = event.target as HTMLButtonElement;
  console.log(target.textContent);
}

// SyntheticEvent properties
function inspectEvent(event: React.SyntheticEvent) {
  console.log('Event type:', event.type);
  console.log('Target:', event.target);
  console.log('Current target:', event.currentTarget);
  console.log('Time stamp:', event.timeStamp);
  console.log('Default prevented:', event.defaultPrevented);
  console.log('Event phase:', event.eventPhase);
  console.log('Is trusted:', event.isTrusted);

  // Native event access
  const nativeEvent = event.nativeEvent;
  console.log('Native event:', nativeEvent);
}
```

---

## 3. MouseEvent

```typescript
import React from 'react';

// Basic click handler
function handleClick(event: React.MouseEvent<HTMLButtonElement>) {
  event.preventDefault();
  console.log('Button clicked at:', event.clientX, event.clientY);
  console.log('Button text:', event.currentTarget.textContent);
}

// MouseEvent with position data
interface PositionData {
  x: number;
  y: number;
  pageX: number;
  pageY: number;
}

function getClickPosition(event: React.MouseEvent<HTMLElement>): PositionData {
  return {
    x: event.clientX,
    y: event.clientY,
    pageX: event.pageX,
    pageY: event.pageY,
  };
}

// Right-click handler
function handleContextMenu(event: React.MouseEvent<HTMLDivElement>) {
  event.preventDefault();
  console.log('Right clicked at:', event.clientX, event.clientY);
}

// Mouse enter/leave for hover effects
function HoverCard() {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      onMouseEnter={(e: React.MouseEvent<HTMLDivElement>) => setIsHovered(true)}
      onMouseLeave={(e: React.MouseEvent<HTMLDivElement>) => setIsHovered(false)}
      style={{ background: isHovered ? 'lightblue' : 'white' }}
    >
      Hover me
    </div>
  );
}

// Draggable element
function DraggableItem() {
  const handleDragStart = (event: React.DragEvent<HTMLDivElement>) => {
    event.dataTransfer.setData('text/plain', 'item-id');
    event.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    const itemId = event.dataTransfer.getData('text/plain');
    console.log('Dropped:', itemId);
  };

  return (
    <div
      draggable
      onDragStart={handleDragStart}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      Drag me
    </div>
  );
}
```

---

## 4. KeyboardEvent

```typescript
import React from 'react';

// Basic key handlers
function SearchInput() {
  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      console.log('Search:', event.currentTarget.value);
    }
    if (event.key === 'Escape') {
      event.currentTarget.blur();
    }
  };

  return <input onKeyDown={handleKeyDown} placeholder="Press Enter to search" />;
}

// Shortcut handler with key combinations
function useKeyboardShortcut() {
  const handleKeyDown = (event: React.KeyboardEvent) => {
    const { key, ctrlKey, metaKey, shiftKey, altKey } = event;
    const modifier = ctrlKey || metaKey;

    if (modifier && key === 's') {
      event.preventDefault();
      saveDocument();
    }
    if (modifier && key === 'z' && shiftKey) {
      event.preventDefault();
      redo();
    }
    if (modifier && key === 'z') {
      event.preventDefault();
      undo();
    }
    if (modifier && key === 'k') {
      event.preventDefault();
      openCommandPalette();
    }
  };

  return handleKeyDown;
}

// Arrow key navigation
function ArrowNavigation({ items }: { items: string[] }) {
  const [activeIndex, setActiveIndex] = useState(0);

  const handleKeyDown = (event: React.KeyboardEvent<HTMLUListElement>) => {
    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault();
        setActiveIndex((prev) => Math.min(prev + 1, items.length - 1));
        break;
      case 'ArrowUp':
        event.preventDefault();
        setActiveIndex((prev) => Math.max(prev - 1, 0));
        break;
      case 'Home':
        event.preventDefault();
        setActiveIndex(0);
        break;
      case 'End':
        event.preventDefault();
        setActiveIndex(items.length - 1);
        break;
      case 'Enter':
      case ' ':
        event.preventDefault();
        console.log('Selected:', items[activeIndex]);
        break;
    }
  };

  return (
    <ul onKeyDown={handleKeyDown} tabIndex={0} role="listbox">
      {items.map((item, index) => (
        <li
          key={item}
          role="option"
          aria-selected={index === activeIndex}
          style={{ background: index === activeIndex ? 'lightblue' : 'white' }}
        >
          {item}
        </li>
      ))}
    </ul>
  );
}

// Input with specific key constraints
function NumericInput() {
  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    const allowedKeys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-'];
    const controlKeys = ['Backspace', 'Delete', 'Tab', 'Enter', 'ArrowLeft', 'ArrowRight'];

    if (
      !allowedKeys.includes(event.key) &&
      !controlKeys.includes(event.key) &&
      !(event.ctrlKey || event.metaKey)
    ) {
      event.preventDefault();
    }
  };

  return <input onKeyDown={handleKeyDown} type="text" inputMode="numeric" />;
}
```

---

## 5. ChangeEvent

```typescript
import React from 'react';

// Input change
function TextInput() {
  const [value, setValue] = useState('');

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValue(event.target.value);
  };

  return <input type="text" value={value} onChange={handleChange} />;
}

// Select change
function RoleSelect() {
  const [role, setRole] = useState('user');

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setRole(event.target.value);
  };

  return (
    <select value={role} onChange={handleChange}>
      <option value="admin">Admin</option>
      <option value="user">User</option>
      <option value="guest">Guest</option>
    </select>
  );
}

// Textarea change
function CommentInput() {
  const [comment, setComment] = useState('');

  const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setComment(event.target.value);
  };

  return (
    <textarea
      value={comment}
      onChange={handleChange}
      maxLength={500}
      rows={5}
    />
  );
}

// Checkbox change
function TermsCheckbox() {
  const [accepted, setAccepted] = useState(false);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAccepted(event.target.checked);
  };

  return (
    <label>
      <input type="checkbox" checked={accepted} onChange={handleChange} />
      I accept the terms
    </label>
  );
}

// File input change
function FileUpload() {
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      console.log('Selected file:', files[0].name);
    }
  };

  return <input type="file" onChange={handleChange} accept="image/*" />;
}

// Radio group change
type Color = 'red' | 'blue' | 'green';

function ColorPicker() {
  const [color, setColor] = useState<Color>('blue');

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setColor(event.target.value as Color);
  };

  return (
    <div>
      {(['red', 'blue', 'green'] as const).map((c) => (
        <label key={c}>
          <input
            type="radio"
            name="color"
            value={c}
            checked={color === c}
            onChange={handleChange}
          />
          {c}
        </label>
      ))}
    </div>
  );
}
```

---

## 6. FormEvent

```typescript
import React from 'react';

// Form submission
interface FormData {
  email: string;
  password: string;
}

function LoginForm() {
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const form = event.currentTarget;
    const formData = new FormData(form);

    const data: FormData = {
      email: formData.get('email') as string,
      password: formData.get('password') as string,
    };

    console.log('Login:', data);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" required />
      <input name="password" type="password" required />
      <button type="submit">Login</button>
    </form>
  );
}

// Form with controlled inputs and validation
interface ContactFormData {
  name: string;
  email: string;
  message: string;
}

function ContactForm() {
  const [formData, setFormData] = useState<ContactFormData>({
    name: '',
    email: '',
    message: '',
  });
  const [errors, setErrors] = useState<Partial<Record<keyof ContactFormData, string>>>({});

  const handleChange = (field: keyof ContactFormData) =>
    (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
      setFormData((prev) => ({ ...prev, [field]: event.target.value }));
      // Clear error on change
      if (errors[field]) {
        setErrors((prev) => ({ ...prev, [field]: undefined }));
      }
    };

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof ContactFormData, string>> = {};
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.email.includes('@')) newErrors.email = 'Invalid email';
    if (formData.message.length < 10) newErrors.message = 'Message too short';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (validate()) {
      console.log('Submitting:', formData);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          value={formData.name}
          onChange={handleChange('name')}
          placeholder="Name"
        />
        {errors.name && <span className="error">{errors.name}</span>}
      </div>
      <div>
        <input
          value={formData.email}
          onChange={handleChange('email')}
          placeholder="Email"
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>
      <div>
        <textarea
          value={formData.message}
          onChange={handleChange('message')}
          placeholder="Message"
        />
        {errors.message && <span className="error">{errors.message}</span>}
      </div>
      <button type="submit">Send</button>
    </form>
  );
}
```

---

## 7. Typed Event Handler Props

```typescript
import React from 'react';

// Reusable typed event handler props
interface ClickableProps {
  onClick?: (event: React.MouseEvent<HTMLElement>) => void;
  onDoubleClick?: (event: React.MouseEvent<HTMLElement>) => void;
  onContextMenu?: (event: React.MouseEvent<HTMLElement>) => void;
}

interface FocusableProps {
  onFocus?: (event: React.FocusEvent<HTMLElement>) => void;
  onBlur?: (event: React.FocusEvent<HTMLElement>) => void;
}

interface SubmittableProps {
  onSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
}

// Combining handler props
interface InputFieldProps extends ClickableProps, FocusableProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

// Generic handler wrapper
function withStopPropagation<P extends React.MouseEvent>(
  handler: (event: P) => void
): (event: P) => void {
  return (event: P) => {
    event.stopPropagation();
    handler(event);
  };
}

// Prevent default wrapper
function withPreventDefault<P extends React.SyntheticEvent>(
  handler: (event: P) => void
): (event: P) => void {
  return (event: P) => {
    event.preventDefault();
    handler(event);
  };
}

// Event handler type utilities
type EventHandler<T extends React.SyntheticEvent> = (event: T) => void;
type ButtonClickHandler = EventHandler<React.MouseEvent<HTMLButtonElement>>;
type InputChangeHandler = EventHandler<React.ChangeEvent<HTMLInputElement>>;
type FormSubmitHandler = EventHandler<React.FormEvent<HTMLFormElement>>;
```

---

## 8. Event Propagation Types

```typescript
import React from 'react';

// Capturing events — use Capture suffix
function CaptureExample() {
  return (
    <div
      onClickCapture={(event: React.MouseEvent<HTMLDivElement>) => {
        console.log('Capture phase: parent');
      }}
    >
      <button
        onClick={(event: React.MouseEvent<HTMLButtonElement>) => {
          console.log('Bubble phase: button');
          // event.stopPropagation();  // Stop bubbling
        }}
      >
        Click me
      </button>
    </div>
  );
}

// Event delegation pattern
interface EventDelegationProps {
  items: { id: string; label: string }[];
  onItemSelect: (id: string) => void;
}

function EventDelegation({ items, onItemSelect }: EventDelegationProps) {
  const handleClick = (event: React.MouseEvent<HTMLUListElement>) => {
    const target = event.target as HTMLElement;
    const itemId = target.closest('[data-item-id]')?.getAttribute('data-item-id');
    if (itemId) {
      onItemSelect(itemId);
    }
  };

  return (
    <ul onClick={handleClick}>
      {items.map((item) => (
        <li key={item.id} data-item-id={item.id}>
          {item.label}
        </li>
      ))}
    </ul>
  );
}

// Preventing double submission
function PreventDoubleSubmit() {
  const isSubmitting = useRef(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (isSubmitting.current) return;
    isSubmitting.current = true;
    try {
      await submitForm();
    } finally {
      isSubmitting.current = false;
    }
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

---

## 9. Best Practices

1. **Always type event parameters** — never use `any` for events.
2. **Use specific event types** — `React.MouseEvent<HTMLButtonElement>` not just `React.MouseEvent`.
3. **Use `event.currentTarget`** for the element the handler is attached to.
4. **Use `event.target`** carefully — it can be a child element.
5. **Always call `event.preventDefault()`** for form submissions.
6. **Use `event.stopPropagation()`** to prevent unwanted bubbling.
7. **Prefer controlled components** for most input scenarios.
8. **Type event handler props** with the specific element type.

---

## Interview Questions

1. What is the difference between `event.target` and `event.currentTarget`?
2. How do you type a click handler for a specific HTML element?
3. What is `SyntheticEvent` and why does React use it?
4. How do you handle keyboard events with modifier keys?
5. Explain event capturing vs bubbling in React.
6. How do you type a form submission handler?
7. What are the common event types in React TypeScript?
8. How do you prevent event propagation in TypeScript React?
9. How do you type an onChange handler for a select element?
10. What is event delegation and how do you implement it with types?
