# State Management Patterns in TypeScript

## Table of Contents

- [Typed Redux](#typed-redux)
- [Zustand with Types](#zustand-with-types)
- [Typed Context](#typed-context)
- [State Machine with Types](#state-machine-with-types)
- [useReducer Typing](#usereducer-typing)
- [Atom-Based State](#atom-based-state)
- [Immutable Update Patterns](#immutable-update-patterns)
- [Typed Selectors](#typed-selectors)
- [Interview Questions](#interview-questions)

---

## Typed Redux

```typescript
// Redux Toolkit with TypeScript
import { createSlice, PayloadAction, configureStore } from "@reduxjs/toolkit";

// Define state type
interface CounterState {
  value: number;
  loading: boolean;
  error: string | null;
}

// Initial state with type
const initialState: CounterState = {
  value: 0,
  loading: false,
  error: null,
};

// Create typed slice
const counterSlice = createSlice({
  name: "counter",
  initialState,
  reducers: {
    increment(state) {
      state.value += 1;
    },
    decrement(state) {
      state.value -= 1;
    },
    incrementByAmount(state, action: PayloadAction<number>) {
      state.value += action.payload;
    },
    setLoading(state, action: PayloadAction<boolean>) {
      state.loading = action.payload;
    },
    setError(state, action: PayloadAction<string | null>) {
      state.error = action.payload;
    },
    reset() {
      return initialState;
    },
  },
});

export const { increment, decrement, incrementByAmount, setLoading, setError, reset } =
  counterSlice.actions;

// Typed async thunk
import { createAsyncThunk } from "@reduxjs/toolkit";

const fetchUser = createAsyncThunk<User, string, { rejectValue: ApiError }>(
  "users/fetchUser",
  async (userId, { rejectWithValue }) => {
    try {
      const response = await fetch(`/api/users/${userId}`);
      if (!response.ok) {
        return rejectWithValue({
          status: response.status,
          message: response.statusText,
        });
      }
      return response.json();
    } catch (error) {
      return rejectWithValue({
        status: 0,
        message: error instanceof Error ? error.message : "Network error",
      });
    }
  }
);

// Typed store
const store = configureStore({
  reducer: {
    counter: counterSlice.reducer,
  },
});

// Typed hooks
type RootState = ReturnType<typeof store.getState>;
type AppDispatch = typeof store.dispatch;

// Typed selectors
const selectCounter = (state: RootState) => state.counter;
const selectCounterValue = (state: RootState) => state.counter.value;

// Typed custom hooks
import { useDispatch, useSelector } from "react-redux";

const useAppDispatch = useDispatch.withTypes<AppDispatch>();
const useAppSelector = useSelector.withTypes<RootState>();
```

---

## Zustand with Types

```typescript
import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";

// Define store type
interface TodoState {
  todos: Todo[];
  filter: "all" | "active" | "completed";
  addTodo: (text: string) => void;
  toggleTodo: (id: string) => void;
  removeTodo: (id: string) => void;
  setFilter: (filter: TodoState["filter"]) => void;
  clearCompleted: () => void;
}

interface Todo {
  id: string;
  text: string;
  completed: boolean;
  createdAt: Date;
}

// Create typed store
const useTodoStore = create<TodoState>()(
  devtools(
    persist(
      (set) => ({
        todos: [],
        filter: "all",

        addTodo: (text) =>
          set(
            (state) => ({
              todos: [
                ...state.todos,
                {
                  id: crypto.randomUUID(),
                  text,
                  completed: false,
                  createdAt: new Date(),
                },
              ],
            }),
            false,
            "addTodo"
          ),

        toggleTodo: (id) =>
          set(
            (state) => ({
              todos: state.todos.map((todo) =>
                todo.id === id ? { ...todo, completed: !todo.completed } : todo
              ),
            }),
            false,
            "toggleTodo"
          ),

        removeTodo: (id) =>
          set(
            (state) => ({
              todos: state.todos.filter((todo) => todo.id !== id),
            }),
            false,
            "removeTodo"
          ),

        setFilter: (filter) => set({ filter }, false, "setFilter"),

        clearCompleted: () =>
          set(
            (state) => ({
              todos: state.todos.filter((todo) => !todo.completed),
            }),
            false,
            "clearCompleted"
          ),
      }),
      { name: "todo-storage" }
    ),
    { name: "TodoStore" }
  )
);

// Usage
function TodoApp() {
  const todos = useTodoStore((state) => state.todos);
  const filter = useTodoStore((state) => state.filter);
  const addTodo = useTodoStore((state) => state.addTodo);
  const toggleTodo = useTodoStore((state) => state.toggleTodo);

  const filteredTodos = todos.filter((todo) => {
    if (filter === "active") return !todo.completed;
    if (filter === "completed") return todo.completed;
    return true;
  });

  return (
    <div>
      {filteredTodos.map((todo) => (
        <div key={todo.id} onClick={() => toggleTodo(todo.id)}>
          {todo.text}
        </div>
      ))}
    </div>
  );
}
```

---

## Typed Context

```typescript
import React, { createContext, useContext, useReducer } from "react";

// State and action types
interface AppState {
  user: User | null;
  theme: "light" | "dark";
  notifications: Notification[];
  loading: boolean;
}

type AppAction =
  | { type: "SET_USER"; payload: User }
  | { type: "CLEAR_USER" }
  | { type: "SET_THEME"; payload: "light" | "dark" }
  | { type: "ADD_NOTIFICATION"; payload: Notification }
  | { type: "REMOVE_NOTIFICATION"; payload: string }
  | { type: "SET_LOADING"; payload: boolean };

// Reducer
function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case "SET_USER":
      return { ...state, user: action.payload };
    case "CLEAR_USER":
      return { ...state, user: null };
    case "SET_THEME":
      return { ...state, theme: action.payload };
    case "ADD_NOTIFICATION":
      return {
        ...state,
        notifications: [...state.notifications, action.payload],
      };
    case "REMOVE_NOTIFICATION":
      return {
        ...state,
        notifications: state.notifications.filter(
          (n) => n.id !== action.payload
        ),
      };
    case "SET_LOADING":
      return { ...state, loading: action.payload };
    default:
      return state;
  }
}

// Context with types
interface AppContextType {
  state: AppState;
  dispatch: React.Dispatch<AppAction>;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

// Provider
function AppProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, {
    user: null,
    theme: "light",
    notifications: [],
    loading: false,
  });

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}

// Typed hook
function useApp(): AppContextType {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useApp must be used within AppProvider");
  }
  return context;
}

// Usage
function UserProfile() {
  const { state, dispatch } = useApp();

  return (
    <div>
      <h1>{state.user?.name ?? "Not logged in"}</h1>
      <button onClick={() => dispatch({ type: "SET_THEME", payload: "dark" })}>
        Toggle Theme
      </button>
    </div>
  );
}
```

---

## State Machine with Types

```typescript
// Type-safe state machine
type StateConfig = {
  [state: string]: {
    [event: string]: string;
  };
};

type StateOf<T extends StateConfig> = keyof T & string;
type EventOf<T extends StateConfig> = {
  [S in keyof T]: keyof T[S];
}[keyof T] & string;

class StateMachine<T extends StateConfig> {
  private state: StateOf<T>;
  private transitions: T;
  private listeners: Array<(state: StateOf<T>) => void> = [];

  constructor(transitions: T, initial: StateOf<T>) {
    this.transitions = transitions;
    this.state = initial;
  }

  getState(): StateOf<T> {
    return this.state;
  }

  send(event: EventOf<T>): StateOf<T> {
    const transition = this.transitions[this.state]?.[event];
    if (!transition) {
      throw new Error(`Invalid event '${event}' in state '${this.state}'`);
    }
    this.state = transition as StateOf<T>;
    this.listeners.forEach((l) => l(this.state));
    return this.state;
  }

  canHandle(event: EventOf<T>): boolean {
    return event in (this.transitions[this.state] ?? {});
  }

  subscribe(listener: (state: StateOf<T>) => void): () => void {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter((l) => l !== listener);
    };
  }
}

// Usage
type TrafficLightConfig = {
  green: { next: "yellow" };
  yellow: { next: "red" };
  red: { next: "green" };
};

const light = new StateMachine<TrafficLightConfig>(
  { green: { next: "yellow" }, yellow: { next: "red" }, red: { next: "green" } },
  "green"
);

light.subscribe((state) => console.log(`Light: ${state}`));
light.send("next"); // yellow
light.send("next"); // red
light.send("next"); // green

// Complex state machine
type OrderConfig = {
  pending: { confirm: "confirmed"; cancel: "cancelled" };
  confirmed: { ship: "shipped"; cancel: "cancelled" };
  shipped: { deliver: "delivered" };
  delivered: { review: "reviewed" };
  cancelled: {};
  reviewed: {};
};

const order = new StateMachine<OrderConfig>(
  {
    pending: { confirm: "confirmed", cancel: "cancelled" },
    confirmed: { ship: "shipped", cancel: "cancelled" },
    shipped: { deliver: "delivered" },
    delivered: { review: "reviewed" },
    cancelled: {},
    reviewed: {},
  },
  "pending"
);
```

---

## useReducer Typing

```typescript
// Advanced useReducer typing patterns
import { useReducer } from "react";

// Discriminated union actions
type FormAction =
  | { type: "SET_FIELD"; field: string; value: unknown }
  | { type: "SET_ERROR"; field: string; error: string }
  | { type: "CLEAR_ERROR"; field: string }
  | { type: "RESET" }
  | { type: "SUBMIT_START" }
  | { type: "SUBMIT_SUCCESS" }
  | { type: "SUBMIT_FAILURE"; error: string };

interface FormState<T extends Record<string, unknown>> {
  values: T;
  errors: Partial<Record<keyof T, string>>;
  touched: Partial<Record<keyof T, boolean>>;
  isSubmitting: boolean;
  submitError: string | null;
}

function formReducer<T extends Record<string, unknown>>(
  state: FormState<T>,
  action: FormAction
): FormState<T> {
  switch (action.type) {
    case "SET_FIELD":
      return {
        ...state,
        values: { ...state.values, [action.field]: action.value },
      };
    case "SET_ERROR":
      return {
        ...state,
        errors: { ...state.errors, [action.field]: action.error },
      };
    case "CLEAR_ERROR": {
      const { [action.field]: _, ...rest } = state.errors;
      return { ...state, errors: rest };
    }
    case "RESET":
      return {
        values: {} as T,
        errors: {},
        touched: {},
        isSubmitting: false,
        submitError: null,
      };
    case "SUBMIT_START":
      return { ...state, isSubmitting: true, submitError: null };
    case "SUBMIT_SUCCESS":
      return { ...state, isSubmitting: false };
    case "SUBMIT_FAILURE":
      return { ...state, isSubmitting: false, submitError: action.error };
    default:
      return state;
  }
}

// Generic form hook
function useForm<T extends Record<string, unknown>>(initialValues: T) {
  const [state, dispatch] = useReducer(formReducer<T>, {
    values: initialValues,
    errors: {},
    touched: {},
    isSubmitting: false,
    submitError: null,
  });

  const setField = (field: keyof T & string, value: T[keyof T]) =>
    dispatch({ type: "SET_FIELD", field, value });

  const setError = (field: keyof T & string, error: string) =>
    dispatch({ type: "SET_ERROR", field, error });

  const reset = () => dispatch({ type: "RESET" });

  return { state, setField, setError, reset, dispatch };
}

// Usage
interface LoginForm {
  email: string;
  password: string;
}

const { state, setField } = useForm<LoginForm>({
  email: "",
  password: "",
});
```

---

## Atom-Based State

```typescript
// Atom-based state management (Jotai/Recoil style)
type Atom<T> = {
  key: string;
  default: T;
};

type AtomValue<T> = T;

function atom<T>(config: { key: string; default: T }): Atom<T> {
  return config;
}

// Store implementation
class AtomStore {
  private values = new Map<string, unknown>();
  private subscribers = new Map<string, Set<(value: unknown) => void>>();

  get<T>(atomConfig: Atom<T>): T {
    if (!this.values.has(atomConfig.key)) {
      this.values.set(atomConfig.key, atomConfig.default);
    }
    return this.values.get(atomConfig.key) as T;
  }

  set<T>(atomConfig: Atom<T>, value: T): void {
    this.values.set(atomConfig.key, value);
    this.subscribers.get(atomConfig.key)?.forEach((sub) => sub(value));
  }

  subscribe<T>(atomConfig: Atom<T>, callback: (value: T) => void): () => void {
    if (!this.subscribers.has(atomConfig.key)) {
      this.subscribers.set(atomConfig.key, new Set());
    }
    this.subscribers.get(atomConfig.key)!.add(callback as (value: unknown) => void);
    return () => {
      this.subscribers.get(atomConfig.key)?.delete(callback as (value: unknown) => void);
    };
  }
}

// Derived atoms
function derivedAtom<T, U>(
  config: {
    key: string;
    get: (get: <V>(atom: Atom<V>) => V) => U;
  },
  dependencies: Atom<T>[]
): Atom<U> {
  return { key: config.key, default: config.get(() => undefined as any) };
}

// Usage
const userAtom = atom<User | null>({ key: "user", default: null });
const themeAtom = atom<"light" | "dark">({ key: "theme", default: "light" });

const store = new AtomStore();
store.set(userAtom, { id: "1", name: "Alice" });
store.get(userAtom); // { id: "1", name: "Alice" }

store.subscribe(userAtom, (user) => {
  console.log("User changed:", user);
});
```

---

## Immutable Update Patterns

```typescript
// Type-safe immutable updates
function updateImmutable<T, K extends keyof T>(
  state: T,
  key: K,
  value: T[K]
): T {
  return { ...state, [key]: value };
}

function updateNested<T, K1 extends keyof T, K2 extends keyof T[K1]>(
  state: T,
  key1: K1,
  key2: K2,
  value: T[K1][K2]
): T {
  return {
    ...state,
    [key1]: {
      ...state[key1],
      [key2]: value,
    },
  };
}

// Generic immutable update
function immutableUpdate<T>(
  state: T,
  recipe: (draft: T) => void
): T {
  // Simplified Immer-like behavior
  const draft = JSON.parse(JSON.stringify(state));
  recipe(draft);
  return draft;
}

// Usage
interface UserState {
  user: {
    name: string;
    profile: {
      bio: string;
      avatar: string;
    };
  };
  settings: {
    theme: "light" | "dark";
    notifications: boolean;
  };
}

const state: UserState = {
  user: { name: "Alice", profile: { bio: "Hello", avatar: "url" } },
  settings: { theme: "light", notifications: true },
};

// Simple update
const newState = updateImmutable(state, "settings", {
  theme: "dark",
  notifications: false,
});

// Nested update
const newState2 = updateNested(
  state,
  "user",
  "profile",
  { bio: "Updated", avatar: "new-url" }
);

// Array updates
function addItem<T>(array: T[], item: T): T[] {
  return [...array, item];
}

function removeItem<T>(array: T[], predicate: (item: T) => boolean): T[] {
  return array.filter((item) => !predicate(item));
}

function updateItem<T>(
  array: T[],
  predicate: (item: T) => boolean,
  updater: (item: T) => T
): T[] {
  return array.map((item) => (predicate(item) ? updater(item) : item));
}
```

---

## Typed Selectors

```typescript
// Memoized typed selectors
function createSelector<TState, TResult>(
  selector: (state: TState) => TResult
): (state: TState) => TResult {
  let lastState: TState | undefined;
  let lastResult: TResult;

  return (state: TState) => {
    if (state === lastState) return lastResult;
    lastState = state;
    lastResult = selector(state);
    return lastResult;
  };
}

// Composed selectors
function createStructuredSelector<T, S extends Record<string, (state: T) => any>>(
  selectors: S
): (state: T) => { [K in keyof S]: ReturnType<S[K]> } {
  return (state: T) => {
    const result = {} as any;
    for (const [key, selector] of Object.entries(selectors)) {
      result[key] = selector(state);
    }
    return result;
  };
}

// Usage
interface AppState {
  user: User | null;
  posts: Post[];
  notifications: Notification[];
}

const selectUser = createSelector((state: AppState) => state.user);
const selectPosts = createSelector((state: AppState) => state.posts);
const selectPostCount = createSelector((state: AppState) => state.posts.length);
const selectUnreadNotifications = createSelector(
  (state: AppState) => state.notifications.filter((n) => !n.read)
);

// Structured selector
const selectDashboard = createStructuredSelector({
  user: (state: AppState) => state.user,
  postCount: (state: AppState) => state.posts.length,
  unreadCount: (state: AppState) =>
    state.notifications.filter((n) => !n.read).length,
});
```

---

## Interview Questions

1. **What is the difference between local state and global state?**
   Local state is component-scoped (useState). Global state is shared across components (Redux, Zustand, Context).

2. **When would you use Zustand over Redux?**
   For simpler state management, less boilerplate, and when you don't need Redux DevTools or middleware ecosystem.

3. **How do you type a React Context?**
   Create an interface for the context value and use `createContext<T | undefined>(undefined)`.

4. **What is the advantage of useReducer over useState?**
   Better for complex state logic, easier to test, and supports action-based state updates.

5. **How do you implement immutable updates?**
   Use spread operator, structuredClone, or libraries like Immer for nested updates.

6. **What are atoms in state management?**
   Individual pieces of state that can be composed and derived. Used in Jotai and Recoil.

7. **How do you memoize selectors?**
   Use createSelector with reference equality checking or libraries like Reselect.

8. **What is the difference between Redux and Zustand?**
   Redux is more structured with actions/reducers/middleware. Zustand is simpler with direct state mutations.

9. **How do you handle async state?**
   Use createAsyncThunk (Redux), async actions (Zustand), or custom hooks with useState/useReducer.

10. **What are the performance implications of state management?**
    Unnecessary re-renders, memory leaks from subscriptions, and serialization overhead.
