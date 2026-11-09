# TypeScript Versions and Release Channels

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — TypeScript publishes stable minor releases roughly quarterly, with beta, release-candidate, and nightly channels for early testing.

## Syntax

```ts
const version = "5.9.3"; // illustrative stable release
const [major, minor, patch] = version.split(".").map(Number);
console.log({ major, minor, patch });
```

## Examples

### Basic

```ts
const dependencyRange = {
  typescript: "~5.9.3", // patch updates only
} as const;
```

### Practical

```ts
const releaseChannels = ["stable", "beta", "rc", "nightly"] as const;
type ReleaseChannel = (typeof releaseChannels)[number];

function isPrerelease(channel: ReleaseChannel): boolean {
  return channel === "beta" || channel === "rc" || channel === "nightly";
}
```

### Advanced / edge cases

```ts
// Pin the compiler used by CI and the editor to the same version.
const toolchain = {
  typescript: "5.9.3",
  editor: "5.9.3",
} as const;

const versionsMatch =
  toolchain.typescript === toolchain.editor; // => true
```

## Key points

- Minor releases can add language features and compiler options.
- Patch releases are intended for fixes and should be low risk.
- Beta and release-candidate builds preview the next stable release.
- `typescript@next` tracks nightly builds and can change daily.
- Editor integrations may bundle their own TypeScript version.
- Type definitions for new JavaScript APIs often arrive with a TypeScript release.

## Gotchas

- Using `latest` in CI makes builds non-reproducible.
- Minor versions can include breaking changes for edge-case code.
- An editor on a different version may accept or reject code that CI does not.

## Best practice

- Pin an exact TypeScript version in applications and CI; test upgrades deliberately.
- Try beta or RC builds in a branch before adopting a new minor release.
