# Watch Mode

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — `tsc --watch` keeps the compiler running and re-checks or re-emits whenever source files change.

## Syntax
```bash
tsc --watch
tsc -w -p tsconfig.json
```

## Examples
### Basic
```bash
npx tsc -w -p tsconfig.json
```

```text
[12:00:01 PM] Starting compilation in watch mode...
[12:00:02 PM] Found 0 errors. Watching for file changes.
```

### Practical
```json
{
  "scripts": {
    "dev": "tsc -w -p tsconfig.json",
    "dev:types": "tsc -w -p tsconfig.json --noEmit",
    "build": "tsc -p tsconfig.json"
  }
}
```

```bash
# Terminal 1: emit on every change
npm run dev

# Terminal 2: run the latest output
node --watch dist/index.js
```

### Advanced / edge cases
```bash
# Keep old output instead of clearing the screen each rebuild
npx tsc -w -p tsconfig.json --preserveWatchOutput

# Use polling for containers, network drives, or flaky file events
npx tsc -w -p tsconfig.json --watchFile useFsEvents --watchDirectory useFsEvents

# Force polling when native events are unavailable
npx tsc -w -p tsconfig.json --watchFile fixedPollingInterval
```

```bash
# Type-check only while a bundler handles the actual build
npx tsc -w -p tsconfig.json --noEmit --preserveWatchOutput
```

## Key points
- Watch mode watches the config, source files, and directories for new files.
- It rebuilds only what changed and reuses prior program state.
- Watch mode implies incremental compilation and writes `.tsbuildinfo`.
- `--preserveWatchOutput` prevents the terminal from being cleared between builds.
- Combine with `node --watch`, `tsx watch`, or `nodemon` to restart the runtime.

## Gotchas
- Watch mode compiles; it does not execute or restart your application.
- Filesystem events can be unreliable in Docker/WSL; switch to polling if changes are missed.
- Deleting `outDir` while watching can leave the watcher confused until restart.

## Best practice
- Use a separate `--noEmit` watcher when a bundler already emits JavaScript.
- Keep `preserveWatchOutput` on in long-lived dev terminals to retain history.
