# State Typing in React + TypeScript

## Overview

Properly typed state prevents invalid state transitions and makes state management predictable. This guide covers `useState`, `useReducer`, derived state patterns, and state machines.

---

## 1. useState Typing

```typescript
import React, { useState } from 'react';

// Basic useState — type inferred from initial value
const Counter = () => {
  const [count, setCount] = useState(0); // number
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
};

// Explicit type annotation
const [name, setName] = useState<string>('');

// Union type with explicit annotation
type SortDirection = 'asc' | 'desc' | null;
const [sortDir, setSortDir] = useState<SortDirection>(null);

// Complex object state
interface UserState {
  name: string;
  email: string;
  isLoggedIn: boolean;
  preferences: {
    theme: 'light' | 'dark';
    language: string;
    notifications: boolean;
  };
}

const [user, setUser] = useState<UserState>({
  name: '',
  email: '',
  isLoggedIn: false,
  preferences: {
    theme: 'light',
    language: 'en',
    notifications: true,
  },
});

// Partial update with spread
const updateUser = (updates: Partial<UserState>) => {
  setUser((prev) => ({ ...prev, ...updates }));
};

// Nested update
const updateTheme = (theme: 'light' | 'dark') => {
  setUser((prev) => ({
    ...prev,
    preferences: { ...prev.preferences, theme },
  }));
};
```

---

## 2. useState with Union Types

```typescript
// State that transitions between distinct types
type FetchState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

function DataLoader<T>() {
  const [state, setState] = useState<FetchState<T>>({ status: 'idle' });

  const fetchData = async (url: string) => {
    setState({ status: 'loading' });
    try {
      const response = await fetch(url);
      const data = await response.json();
      setState({ status: 'success', data });
    } catch (error) {
      setState({ status: 'error', error: error as Error });
    }
  };

  // Exhaustive checking
  switch (state.status) {
    case 'idle':
      return <div>Ready to load</div>;
    case 'loading':
      return <div>Loading...</div>;
    case 'success':
      return <div>Data: {JSON.stringify(state.data)}</div>;
    case 'error':
      return <div>Error: {state.error.message}</div>;
  }
}

// Toggle state
const [isOpen, setIsOpen] = useState(false);

// Indexed state
const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());

const toggleId = (id: string) => {
  setSelectedIds((prev) => {
    const next = new Set(prev);
    if (next.has(id)) {
      next.delete(id);
    } else {
      next.add(id);
    }
    return next;
  });
};

// Array state
interface Todo {
  id: string;
  text: string;
  completed: boolean;
}

const [todos, setTodos] = useState<Todo[]>([]);

const addTodo = (text: string) => {
  setTodos((prev) => [
    ...prev,
    { id: crypto.randomUUID(), text, completed: false },
  ]);
};

const toggleTodo = (id: string) => {
  setTodos((prev) =>
    prev.map((todo) =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    )
  );
};

const removeTodo = (id: string) => {
  setTodos((prev) => prev.filter((todo) => todo.id !== id));
};
```

---

## 3. useReducer Typing

```typescript
import React, { useReducer } from 'react';

// --- Typed Action Pattern 1: Discriminated Union ---

interface TodoState {
  todos: Todo[];
  filter: 'all' | 'active' | 'completed';
  loading: boolean;
  error: string | null;
}

type TodoAction =
  | { type: 'ADD_TODO'; payload: { text: string } }
  | { type: 'TOGGLE_TODO'; payload: { id: string } }
  | { type: 'REMOVE_TODO'; payload: { id: string } }
  | { type: 'SET_FILTER'; payload: { filter: TodoState['filter'] } }
  | { type: 'LOAD_START' }
  | { type: 'LOAD_SUCCESS'; payload: { todos: Todo[] } }
  | { type: 'LOAD_ERROR'; payload: { error: string } }
  | { type: 'CLEAR_COMPLETED' };

function todoReducer(state: TodoState, action: TodoAction): TodoState {
  switch (action.type) {
    case 'ADD_TODO':
      return {
        ...state,
        todos: [
          ...state.todos,
          { id: crypto.randomUUID(), text: action.payload.text, completed: false },
        ],
      };

    case 'TOGGLE_TODO':
      return {
        ...state,
        todos: state.todos.map((todo) =>
          todo.id === action.payload.id
            ? { ...todo, completed: !todo.completed }
            : todo
        ),
      };

    case 'REMOVE_TODO':
      return {
        ...state,
        todos: state.todos.filter((todo) => todo.id !== action.payload.id),
      };

    case 'SET_FILTER':
      return { ...state, filter: action.payload.filter };

    case 'LOAD_START':
      return { ...state, loading: true, error: null };

    case 'LOAD_SUCCESS':
      return { ...state, loading: false, todos: action.payload.todos };

    case 'LOAD_ERROR':
      return { ...state, loading: false, error: action.payload.error };

    case 'CLEAR_COMPLETED':
      return {
        ...state,
        todos: state.todos.filter((todo) => !todo.completed),
      };

    default:
      // Exhaustiveness check — compile error if action is not handled
      const _exhaustive: never = action;
      return state;
  }
}

// Initial state
const initialState: TodoState = {
  todos: [],
  filter: 'all',
  loading: false,
  error: null,
};

// Component usage
function TodoApp() {
  const [state, dispatch] = useReducer(todoReducer, initialState);

  const filteredTodos = state.todos.filter((todo) => {
    if (state.filter === 'active') return !todo.completed;
    if (state.filter === 'completed') return todo.completed;
    return true;
  });

  return (
    <div>
      <input
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            dispatch({ type: 'ADD_TODO', payload: { text: e.currentTarget.value } });
            e.currentTarget.value = '';
          }
        }}
      />
      <div>
        {(['all', 'active', 'completed'] as const).map((f) => (
          <button
            key={f}
            onClick={() => dispatch({ type: 'SET_FILTER', payload: { filter: f } })}
            style={{ fontWeight: state.filter === f ? 'bold' : 'normal' }}
          >
            {f}
          </button>
        ))}
      </div>
      {filteredTodos.map((todo) => (
        <div key={todo.id}>
          <span
            onClick={() => dispatch({ type: 'TOGGLE_TODO', payload: { id: todo.id } })}
            style={{ textDecoration: todo.completed ? 'line-through' : 'none' }}
          >
            {todo.text}
          </span>
          <button
            onClick={() => dispatch({ type: 'REMOVE_TODO', payload: { id: todo.id } })}
          >
            ×
          </button>
        </div>
      ))}
    </div>
  );
}
```

---

## 4. useReducer with Creator Functions (Action Creators)

```typescript
// Define action creators alongside the reducer
interface CounterState {
  count: number;
  step: number;
}

type CounterAction =
  | { type: 'INCREMENT' }
  | { type: 'DECREMENT' }
  | { type: 'SET_STEP'; step: number }
  | { type: 'RESET' };

function counterReducer(state: CounterState, action: CounterAction): CounterState {
  switch (action.type) {
    case 'INCREMENT':
      return { ...state, count: state.count + state.step };
    case 'DECREMENT':
      return { ...state, count: state.count - state.step };
    case 'SET_STEP':
      return { ...state, step: action.step };
    case 'RESET':
      return { count: 0, step: 1 };
  }
}

// Action creator functions — strongly typed
const actions = {
  increment: (): CounterAction => ({ type: 'INCREMENT' }),
  decrement: (): CounterAction => ({ type: 'DECREMENT' }),
  setStep: (step: number): CounterAction => ({ type: 'SET_STEP', step }),
  reset: (): CounterAction => ({ type: 'RESET' }),
} as const;

// Usage
function Counter() {
  const [state, dispatch] = useReducer(counterReducer, { count: 0, step: 1 });

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch(actions.decrement())}>-</button>
      <button onClick={() => dispatch(actions.increment())}>+</button>
      <button onClick={() => dispatch(actions.setStep(5))}>Set Step 5</button>
      <button onClick={() => dispatch(actions.reset())}>Reset</button>
    </div>
  );
}
```

---

## 5. State vs Props

```typescript
// Props are immutable — passed from parent
// State is mutable — managed internally

interface TodoItemProps {
  id: string;
  text: string;
  completed: boolean;
  onToggle: (id: string) => void;  // Callback as prop
  onDelete: (id: string) => void;  // Callback as prop
}

// State: internal, changeable
// Props: external, immutable (from component's perspective)
function TodoItem({ id, text, completed, onToggle, onDelete }: TodoItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(text);

  return (
    <li>
      {isEditing ? (
        <input
          value={editText}
          onChange={(e) => setEditText(e.target.value)}
          onBlur={() => {
            setIsEditing(false);
            // Props are passed up via callbacks
          }}
        />
      ) : (
        <>
          <span
            onClick={() => onToggle(id)}
            style={{ textDecoration: completed ? 'line-through' : 'none' }}
          >
            {text}
          </span>
          <button onClick={() => setIsEditing(true)}>Edit</button>
          <button onClick={() => onDelete(id)}>Delete</button>
        </>
      )}
    </li>
  );
}
```

---

## 6. Derived State

```typescript
import React, { useState, useMemo } from 'react';

// BAD: Redundant state that can be derived
// const [filteredTodos, setFilteredTodos] = useState<Todo[]>([]);
// const [count, setCount] = useState(0);

// GOOD: Derive state from existing state
interface TodoListState {
  todos: Todo[];
  filter: 'all' | 'active' | 'completed';
  searchQuery: string;
}

function TodoList() {
  const [state, setState] = useState<TodoListState>({
    todos: [],
    filter: 'all',
    searchQuery: '',
  });

  // Derived state — computed from existing state
  const filteredTodos = useMemo(() => {
    return state.todos
      .filter((todo) => {
        if (state.filter === 'active') return !todo.completed;
        if (state.filter === 'completed') return todo.completed;
        return true;
      })
      .filter((todo) =>
        todo.text.toLowerCase().includes(state.searchQuery.toLowerCase())
      );
  }, [state.todos, state.filter, state.searchQuery]);

  const stats = useMemo(() => ({
    total: state.todos.length,
    active: state.todos.filter((t) => !t.completed).length,
    completed: state.todos.filter((t) => t.completed).length,
  }), [state.todos]);

  return (
    <div>
      <p>Total: {stats.total} | Active: {stats.active} | Completed: {stats.completed}</p>
      <input
        value={state.searchQuery}
        onChange={(e) =>
          setState((prev) => ({ ...prev, searchQuery: e.target.value }))
        }
      />
      {filteredTodos.map((todo) => (
        <div key={todo.id}>{todo.text}</div>
      ))}
    </div>
  );
}
```

---

## 7. State Machine Pattern

```typescript
import React, { useReducer } from 'react';

// Finite state machine for a form
type FormState =
  | { step: 'idle' }
  | { step: 'personal'; personalData: PersonalData }
  | { step: 'address'; personalData: PersonalData; addressData: AddressData }
  | { step: 'review'; personalData: PersonalData; addressData: AddressData }
  | { step: 'submitting'; personalData: PersonalData; addressData: AddressData }
  | { step: 'success' }
  | { step: 'error'; error: Error; previousStep: Exclude<FormState, { step: 'error' }>['step'] };

type FormAction =
  | { type: 'START'; data: PersonalData }
  | { type: 'NEXT_PERSONAL'; data: AddressData }
  | { type: 'NEXT_ADDRESS' }
  | { type: 'SUBMIT' }
  | { type: 'SUBMIT_SUCCESS' }
  | { type: 'SUBMIT_ERROR'; error: Error }
  | { type: 'GO_BACK' }
  | { type: 'RESET' };

function formReducer(state: FormState, action: FormAction): FormState {
  switch (state.step) {
    case 'idle':
      if (action.type === 'START') {
        return { step: 'personal', personalData: action.data };
      }
      break;

    case 'personal':
      if (action.type === 'NEXT_PERSONAL') {
        return {
          step: 'address',
          personalData: state.personalData,
          addressData: action.data,
        };
      }
      break;

    case 'address':
      if (action.type === 'NEXT_ADDRESS') {
        return {
          step: 'review',
          personalData: state.personalData,
          addressData: state.addressData,
        };
      }
      if (action.type === 'GO_BACK') {
        return { step: 'personal', personalData: state.personalData };
      }
      break;

    case 'review':
      if (action.type === 'SUBMIT') {
        return {
          step: 'submitting',
          personalData: state.personalData,
          addressData: state.addressData,
        };
      }
      if (action.type === 'GO_BACK') {
        return {
          step: 'address',
          personalData: state.personalData,
          addressData: state.addressData,
        };
      }
      break;

    case 'submitting':
      if (action.type === 'SUBMIT_SUCCESS') {
        return { step: 'success' };
      }
      if (action.type === 'SUBMIT_ERROR') {
        return { step: 'error', error: action.error, previousStep: 'review' };
      }
      break;

    case 'error':
      if (action.type === 'GO_BACK') {
        return { step: state.previousStep } as FormState;
      }
      if (action.type === 'RESET') {
        return { step: 'idle' };
      }
      break;

    case 'success':
      if (action.type === 'RESET') {
        return { step: 'idle' };
      }
      break;
  }

  return state;
}

// Usage
function MultiStepForm() {
  const [state, dispatch] = useReducer(formReducer, { step: 'idle' });

  switch (state.step) {
    case 'idle':
      return <button onClick={() => dispatch({ type: 'START', data: personalData })}>Start</button>;
    case 'personal':
      return <PersonalStep onNext={(data) => dispatch({ type: 'NEXT_PERSONAL', data })} />;
    case 'address':
      return <AddressStep onNext={() => dispatch({ type: 'NEXT_ADDRESS' })} onBack={() => dispatch({ type: 'GO_BACK' })} />;
    case 'review':
      return <ReviewStep onSubmit={() => dispatch({ type: 'SUBMIT' })} onBack={() => dispatch({ type: 'GO_BACK' })} />;
    case 'submitting':
      return <div>Submitting...</div>;
    case 'success':
      return <div>Success! <button onClick={() => dispatch({ type: 'RESET' })}>Start Over</button></div>;
    case 'error':
      return <div>Error: {state.error.message} <button onClick={() => dispatch({ type: 'GO_BACK' })}>Go Back</button></div>;
  }
}
```

---

## 8. useState with Function Initializers

```typescript
// Lazy initialization — function runs only once
interface ExpensiveState {
  data: Map<string, unknown>;
  config: AppConfig;
}

const [state, setState] = useState<ExpensiveState>(() => {
  // Expensive computation only runs on mount
  const config = loadConfig();
  const data = new Map<string, unknown>();
  return { data, config };
});

// Generic useState helper
function useSafeState<T>(
  initialValue: T | (() => T)
): [T, React.Dispatch<React.SetStateAction<T>>] {
  return useState<T>(initialValue);
}
```

---

## 9. Best Practices

1. **Use `useState` for simple state** — strings, numbers, booleans, small objects.
2. **Use `useReducer` for complex state** — multiple related values, many transitions.
3. **Always use discriminated unions** for action types in `useReducer`.
4. **Include an exhaustive check** (`never` assertion) in reducer switch statements.
5. **Derive state** instead of duplicating it — avoid `useEffect` for state derivation.
6. **Use `useMemo`** for expensive derived computations.
7. **Prefer functional updates** (`setState(prev => ...)`) over direct values.
8. **Use `Partial<T>`** for partial state updates on objects.
9. **Keep state minimal** — only store what you can't compute.
10. **Use state machines** for multi-step flows with strict transitions.

---

## Interview Questions

1. When should you use `useState` vs `useReducer`?
2. How do you type discriminated unions for reducer actions?
3. What is derived state and why shouldn't you store it?
4. Explain the `never` exhaustiveness check in a reducer.
5. How do you type complex nested state updates?
6. What is the state machine pattern in React?
7. How do you handle async operations in `useReducer`?
8. Explain lazy initialization of `useState`.
9. How do you update state objects immutably with TypeScript?
10. What are the common pitfalls when typing state in React?
