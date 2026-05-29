# Section 04: Lockfile Management

## Overview

The lockfile (`pnpm-lock.yaml`) is the single source of truth for the exact dependency tree. It ensures that every developer and CI environment installs byte-identical `node_modules`. Proper lockfile management — validation, merge conflict resolution, and CI enforcement — is critical for build reproducibility.

## Lockfile Structure

pnpm's lockfile format differs from npm's `package-lock.json` or Yarn's `yarn.lock`:

```yaml
# pnpm-lock.yaml (simplified)
lockfileVersion: '9.0'
settings:
  autoInstallPeers: true
  excludeLinksFromLockfile: false

importers:
  .:
    devDependencies:
      turbo:
        specifier: ^2.0.0
        version: 2.0.3

  apps/web:
    dependencies:
      next:
        specifier: '14.2.3'
        version: 14.2.3(@babel/core@7.24.0)(react-dom@18.3.1)(react@18.3.1)
      react:
        specifier: '18.3.1'
        version: 18.3.1

  packages/db:
    dependencies:
      '@prisma/client':
        specifier: '5.14.0'
        version: 5.14.0(prisma@5.14.0)

packages:
  /@prisma/client@5.14.0(prisma@5.14.0):
    dependencies:
      prisma: 5.14.0
    dev: false
    requiresBuild: true
    resolution:
      integrity: sha512-...
      tarball: https://registry.npmjs.org/@prisma/client/-/client-5.14.0.tgz

  /next@14.2.3(@babel/core@7.24.0)(react-dom@18.3.1)(react@18.3.1):
    dependencies:
      '@next/env': 14.2.3
      react: 18.3.1
      react-dom: 18.3.1
    # ...
```

### Key Sections

- **importers**: Lists each workspace and its dependencies with specifier (semver range in package.json) and resolved version
- **packages**: The flat list of all resolved packages, including their dependencies, integrity hashes, and tarball URLs
- **lockfileVersion**: pnpm's lockfile version (not npm's). Incremented with pnpm major versions

## Lockfile Validation in CI

```yaml
# .github/workflows/ci.yml (lockfile validation step)
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - name: Validate lockfile
        run: |
          # Check lockfile is up to date with package.json
          pnpm install --frozen-lockfile

          # Verify lockfile hasn't changed
          if [[ -n $(git status --porcelain pnpm-lock.yaml) ]]; then
            echo "::error::Lockfile is not up to date!"
            echo "Run 'pnpm install' locally and commit pnpm-lock.yaml"
            exit 1
          fi

      - name: Check for duplicate packages
        run: |
          # Detect duplicate package versions in the lockfile
          pnpm dedupe --check

      - name: Verify lockfile integrity
        run: |
          # Verify all integrity hashes match
          pnpm verify
```

## Merge Conflict Resolution

Lockfile merge conflicts are common in monorepos. pnpm's lockfile is more merge-friendly than npm's but still requires care:

```bash
# Strategy 1: Regenerate lockfile
git checkout main -- pnpm-lock.yaml
pnpm install
# This regenerates the lockfile based on merged package.json files

# Strategy 2: Use pnpm's merge driver
git config merge.pnpm-lock.name "pnpm lockfile merge driver"
git config merge.pnpm-lock.driver "pnpm install --frozen-lockfile && git add pnpm-lock.yaml"
```

### Automated Merge Conflict Resolution in CI

```yaml
# .github/workflows/resolve-lockfile.yml
name: Resolve Lockfile Conflicts
on:
  pull_request:
    paths:
      - 'pnpm-lock.yaml'

jobs:
  resolve:
    runs-on: ubuntu-latest
    if: contains(github.event.pull_request.labels.*.name, 'lockfile-conflict')
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref }}

      - name: Regenerate lockfile
        run: |
          # Remove conflicted lockfile
          rm -f pnpm-lock.yaml
          # Regenerate from merged package.json files
          pnpm install
          # Commit regenerated lockfile
          git add pnpm-lock.yaml
          git commit -m "chore: regenerate lockfile after merge conflict"

      - name: Push changes
        uses: ad-m/github-push-action@v2
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          branch: ${{ github.head_ref }}
```

## Lockfile Diff Analysis

```bash
# Compare lockfile changes between branches
git diff main...HEAD -- pnpm-lock.yaml

# Extract added/removed packages
git diff main...HEAD -- pnpm-lock.yaml | grep '^+ ' | grep 'version:' | head -20
git diff main...HEAD -- pnpm-lock.yaml | grep '^- ' | grep 'version:' | head -20

# Check which packages were added
pnpm ls --depth=0 -r | grep -v "workspace"
```

## Lockfile Optimization

```bash
# Deduplicate packages (merge compatible versions)
pnpm dedupe

# Check if deduplication is needed
pnpm dedupe --check

# Prune unused packages from store
pnpm store prune

# List packages that can be deduplicated
pnpm dedupe --list-different
```

## Lockfile Enforcement Rules

```yaml
# .github/lockfile-policies.yml
rules:
  # Prevent adding packages with known vulnerabilities
  - rule: no-vulnerable-packages
    severity: error

  # Prevent duplicate versions of the same package
  - rule: no-duplicate-versions
    severity: warning
    allow:
      - "@types/node"       # Different minor versions okay
      - "typescript"        # Different major versions tracked

  # Enforce minimum resolutions
  - rule: enforce-minimum-versions
    severity: error
    packages:
      zod: 3.22.0
      next: 14.0.0
      "@prisma/client": 5.0.0

  # Prevent new GPL packages
  - rule: no-copyleft-licenses
    severity: error
    licenses:
      - GPL
      - AGPL
      - LGPL
```

## pnpm Store Management

```bash
# Status of the store
pnpm store status

# Prune unreferenced packages
pnpm store prune

# Add package to store
pnpm store add react@18.3.1

# Show store location
pnpm store path
```

## CI Store Caching

```yaml
# .github/actions/pnpm-setup/action.yml
name: pnpm setup
description: Setup pnpm with caching
inputs:
  node-version:
    description: Node.js version
    default: '20'

runs:
  using: composite
  steps:
    - uses: pnpm/action-setup@v4
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}

    - name: Get pnpm store directory
      id: pnpm-cache
      shell: bash
      run: |
        echo "STORE_PATH=$(pnpm store path)" >> $GITHUB_OUTPUT

    - name: Cache pnpm store
      uses: actions/cache@v4
      with:
        path: ${{ steps.pnpm-cache.outputs.STORE_PATH }}
        key: ${{ runner.os }}-pnpm-store-${{ hashFiles('**/pnpm-lock.yaml') }}
        restore-keys: |
          ${{ runner.os }}-pnpm-store-

    - name: Install dependencies
      shell: bash
      run: pnpm install --frozen-lockfile
```

## Design Decisions

### Why commit the lockfile?

The lockfile must be committed to version control for reproducible builds. Without it, two developers running `pnpm install` at different times could get different versions of transitive dependencies.

### pnpm-lock.yaml vs. npm's package-lock.json

pnpm's lockfile is more compact (~40% smaller for our monorepo) and more readable. It groups packages by their integrity hash, making it easier to review lockfile changes in PRs.

## Integration Points

- **CI**: `--frozen-lockfile` ensures lockfile consistency
- **Renovate**: Updates lockfile when applying dependency updates
- **Review**: Lockfile changes are reviewed in every PR that modifies dependencies
- **Audit**: Lockfile integrity is verified before deployment

## Production Considerations

1. **Lockfile age**: An old lockfile means you're missing security patches. Renovate's weekly lockfile maintenance keeps it fresh
2. **Store corruption**: If pnpm reports store integrity errors, run `pnpm store prune && pnpm install`
3. **Platform-specific packages**: The lockfile includes platform-specific dependencies (e.g., `esbuild-linux-64`). Adding a new platform (e.g., ARM Mac) requires regenerating the lockfile
4. **Git hooks**: Add a pre-push hook that validates the lockfile: `pnpm install --frozen-lockfile` must succeed before pushing
5. **Migration**: When upgrading pnpm major version, the lockfile version changes. Run `pnpm install` to upgrade the lockfile format, then commit it separately
