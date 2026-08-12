# Priority 3 — Git & Version Control (Q466–Q480)

**Why these matter for micro1:** you'll collaborate on real PRs; expect branching strategy, merge vs rebase, reset/revert, conflict resolution, and general git fluency. These are also easy points — git is very learnable.

---

## Q466: What's the difference between a branch, a commit, and a merge?

- **Commit** — a snapshot of the working tree with a message, parent pointer(s), author, timestamp. Immutable once created.
- **Branch** — a movable pointer to a commit. "Creating a branch" = a pointer to the current commit; it advances as you commit.
- **Merge** — combines two lines of history into one. Creates a new "merge commit" with two parents (or fast-forwards if linear).

```text
main:    A──B──C──D
                \
feature:        E──F     (E, F on top of C)
merge →         ──────G   (merge commit with parents D and F)
```

- **HEAD** — pointer to the branch you're on. **Working tree** — the files you edit.

---

## Q467: Git merge vs git rebase?

| | **Merge** | **Rebase** |
|---|---|---|
| History | Preserves the real, branched history | Rewrites to a linear history |
| Merge commits | Yes (or fast-forward) | No |
| Conflicts | Resolve once, at merge | Resolve per-commit (could be many times) |
| Safety | Non-destructive | Rewrites commits — don't rebase shared/public branches |
| Best for | Public/shared branches, preserving context | Cleaning up your own local feature branch before merging |

```bash
# merge: keeps a record of the branch
git checkout main && git merge feature

# rebase: replays feature commits on top of main, linear
git checkout feature && git rebase main
```

**Rule of thumb:** merge to *integrate* shared work; rebase to *tidy* your own un-pushed branch. Never rebase commits others have pulled. For squashing PR history, use **interactive rebase** (`git rebase -i`) or a **squash merge**.

---

## Q468: What is a "detached HEAD"?

You're on a specific commit instead of a branch:

```bash
git checkout 8f3a2b1   # detached — HEAD points at a commit, not a branch
```

**Dangers/behavior:** commits you make belong to *no branch* and can be garbage-collected once you switch away. To keep work: create a branch immediately.

**Fixes:**
```bash
git switch -c rescue-branch   # save your detached work to a branch
# or
git checkout main             # throw it away
```

---

## Q469: How do you handle merge conflicts?

**When:** two branches change the same lines → git can't auto-merge.

**Steps:**
1. `git merge <branch>` → conflict markers appear:
```text
<<<<<<< HEAD
version in the current branch
=======
version being merged in
>>>>>>> feature
```
2. Edit the file to the correct combined result, remove the markers.
3. `git add <file>` and complete the merge (`git commit`, or `git merge --continue`).

**Tips:**
- Resolve *smallest units* first (a file, a hunk) — large conflicts are easier if you understand both sides' intent.
- Rebase conflicts resolve per-commit — often simpler if the conflict is with recent work.
- Use a merge tool (`git mergetool`) or editor conflict UI for complex ones.
- Never resolve by "keeping mine" blindly — the merge must preserve both branches' intent.

---

## Q470: git reset vs git revert — when do you use each?

- **`git revert`** — creates a *new* commit that undoes an old one. **Safe for shared/public history** (never rewrites). Use when the commit was pushed.
- **`git reset`** — *moves* HEAD backward, discarding commits. **Only for local/un-pushed work.** Three modes:
  - `--soft` — commits gone, changes **staged** (keep work).
  - `--mixed` (default) — commits gone, changes **unstaged** (keep work).
  - `--hard` — commits AND working-tree changes gone (dangerous, discards work).

```bash
git revert abc123           # new commit undoing abc123 (shared branch)
git reset --hard HEAD~3     # throw away last 3 local commits
git reset --soft HEAD~1     # undo last commit, keep changes staged
```

**Golden rule:** shared branch → revert; local only → reset.

---

## Q471: What is `git stash`?

Temporarily set aside uncommitted changes so you can switch branches or pull cleanly:

```bash
git stash            # save uncommitted changes, clean the working tree
git stash list
git stash pop        # restore the most recent stash and drop it
git stash apply      # restore but keep the stash
git stash -u         # include untracked files
git stash push -m "wip parsing" # named stash
```

**When:** "oh no, I'm on the wrong branch with half-written changes" → stash, switch, work, switch back, `stash pop`. Untracked files need `-u` (or they're left behind).

---

## Q472: Git merge strategy — how do you structure PRs in a team?

**Common flow (feature branch workflow):**
1. Branch from an up-to-date `main`: `git switch -c feat/apply-flow`.
2. Small, focused commits with clear messages.
3. Push, open a **PR**; reviewers comment; update with follow-up commits (or force-push to tidy your *own* branch before review).
4. Merge with **squash** (one clean commit per feature) or **merge commit** (preserve context) — squash is popular for tidy history.
5. Delete the branch after merge.

**Do:** tiny PRs (< ~400 lines), clear titles/descriptions, link issues, rebase on main before merging to avoid conflicts, keep `main` always deployable.
**Don't:** commit to `main` directly (no protected rules in small teams), leave WIP commits on the PR, resolve every conflict with force-push.

---

## Q473: What's the difference between `git fetch`, `git pull`, and `git clone`?

- **`git clone`** — copies a remote repo to your machine the first time (sets up origin).
- **`git fetch`** — downloads remote commits/branches into your local *remote-tracking* refs (`origin/main`) **without changing your working tree**.
- **`git pull`** — `fetch` **+ merge** (or rebase with `--rebase`) into your current branch.
- **`git push`** — uploads local commits to the remote.

```bash
git fetch origin          # see what's new, don't touch my work
git pull --rebase origin main   # fetch + replay my commits on top
```

**Why fetch separately:** to inspect remote state (`git log origin/main`) before integrating — avoids surprise merges.

---

## Q474: What is `HEAD`, `~` vs `^`, and how do you navigate history?

- **`HEAD`** — the commit you're currently on.
- **`HEAD~n`** — n commits *back along first-parent history*. `HEAD~1` = parent.
- **`HEAD^n`** — the nth *parent* (relevant on merge commits: `^1` = first parent, `^2` = second).
- `git log --oneline --graph --all` — see the whole picture.
- `git log -p <file>` / `git blame <file>` — who changed what and why.

```bash
git log --oneline -5
git diff HEAD~2 HEAD         # diff two commits back vs now
git show abc123              # what did this commit change
```

---

## Q475: How do you write good commit messages?

**Conventional style** (works with tooling, skimmable):
```text
feat(applications): add resume upload with presigned S3 URL
fix(screening): respect provider 429 before retrying
refactor(scoring): extract rubric parsing into service
test(security): assert PII is stripped before LLM prompt
```

- **Subject line:** imperative, ≤ ~50 chars, says *what + why* not "changes".
- **Body (when needed):** *why* this change, context, tradeoffs, links to issue.
- **One logical change per commit** — don't bundle a bug fix with a rename.
- Don't commit generated files, secrets, or WIP junk.

---

## Q476: What is `git reflog` and when do you need it?

**Reflog** — a local journal of every `HEAD` movement (commits, resets, checkouts, rebases) — your *undo log* for git operations.

```bash
git reflog
# abc123 HEAD@{0}: checkout: moving from main to feature
# deadbe HEAD@{1}: reset: moving to HEAD~3
git reset --hard abc123   # you just nuked work with --hard? reflog rescues it
```

**When:** after `git reset --hard`, botched rebase, or deleted branch — reflog shows where HEAD was, and you can restore it. Reflog is local-only and expires (~90 days default). **Rule:** if a commit existed locally once, reflog can usually find it.

---

## Q477: How do you collaborate without breaking main?

1. **Feature branches + PR review** — never push straight to main (Q472).
2. **Keep branches short-lived** — long-lived branches diverge and conflict.
3. **Rebase on main before merge** to keep merges clean; or merge main into your branch.
4. **Protected main** in CI: builds + tests + coverage must pass before merge.
5. **Small PRs**, clear scope — faster reviews, fewer conflicts.
6. **Agree on a strategy** (squash vs merge) and document it — consistency beats cleverness.
7. **Handle emergencies with revert**, not history surgery (Q470).

---

## Q478: Git workflow for a solo project vs a team?

**Solo:** still use branches + commits (history is your documentation and safety net). A simple `main` + feature branches is plenty; squash merge keeps it clean.

**Team:**
- **Trunk-based:** everyone branches off main, small fast merges, CI on every commit. Fastest, most popular in modern teams (GitHub flow is a form of this).
- **GitFlow** (`main` + `develop` + `feature/release/hotfix`): heavier ceremony, suited to scheduled releases. Overkill for most startups.
- **Release branches** only when you must ship from multiple lines simultaneously.

**Recommendation for the micro1 answer:** GitHub flow / trunk-based with feature branches, PR review, squash merges, and CI gating.

---

## Q479: What are tags, and how do they relate to releases?

- **Tag** — a named, immutable pointer to a commit, usually marking a release (`v1.2.0`). Annotated tags carry a message + signer; lightweight tags are just pointers.
```bash
git tag -a v1.2.0 -m "release screening v1"
git push origin v1.2.0
```
- Releases = a tag + release notes + artifacts (Docker image, changelog). CI can trigger a deploy when a `v*` tag is pushed.
- **Semver** discipline (`MAJOR.MINOR.PATCH`): bump MAJOR on breaking API changes, MINOR on features, PATCH on fixes (Q391).

---

## Q480: What would you do if you accidentally pushed a secret?

**Immediate — treat as compromised, don't just delete:**
1. **Revoke the secret now** — rotate the API key/password before anything else (it may already be scanned by bots).
2. Remove from the **current** file: `git rm --cached`, edit the file, commit.
3. **Purge history** — `git filter-repo` (preferred) or `git filter-branch` to scrub the secret from all commits.
4. **Force-push the scrubbed history** and tell collaborators to re-clone / re-fetch (`git filter-repo` automatically adds a tag for the leaked ref).
5. Scan with `gitleaks`/`trufflehog` to confirm it's gone from history.
6. Add **prevention**: pre-commit secret-scan hook, secret scanner in CI, gitignore `.env`, secret manager (Q417).

**Remember:** even after deletion, the secret is leaked — assume it's compromised and **rotate**.
