# Git & GitHub - 150+ Interview Q&A

### Q1: What is Git? How is it different from GitHub?
**Answer:** Git: distributed version control system. Tracks file changes, branching, offline work. GitHub: cloud hosting for Git repos with collaboration features (PRs, issues, Actions, wikis). Alternatives to GitHub: GitLab, Bitbucket. Git is the tool, GitHub is the platform.

### Q2: Git merge vs rebase - when to use which?
**Answer:** merge: creates merge commit, preserves all history (including exactly when branches diverged). Good for public/shared branches. rebase: replays commits on top of target, linear history. Good for local/feature branches. Golden rule: never rebase shared branches. "Merge for public, rebase for private."

### Q3: How does Git staging area work?
**Answer:** Three areas: Working Directory (actual files) → `git add` → Staging Area (index) → `git commit` → Local Repository → `git push` → Remote Repository. Staging allows: selective commits (part of file), reviewing changes before commit, splitting work into multiple commits. `git add -p` stages interactively.

### Q4: How to undo a commit in Git?
**Answer:** git reset --soft HEAD~1: undo commit, keep changes staged. --mixed (default): undo commit, keep changes unstaged. --hard: discard changes completely. Never reset public commits! Use git revert <commit> for public branches (creates inverse commit). git revert is safe for shared history.

### Q5: What is a merge conflict? How to resolve?
**Answer:** Occurs when same file section changed in both branches. Git marks conflict: `<<<<<<< HEAD` (current), `=======` (separator), `>>>>>>> branch-name` (incoming). Resolve: manually edit to keep correct version(s), remove conflict markers, git add, git commit. Use mergetool (vs code, vimdiff, beyond compare) for complex conflicts.

### Q6: Git stash explained?
**Answer:** Temporarily save uncommitted changes. git stash (save with message), git stash pop (apply top and drop), git stash apply (keep in stash), git stash list (see all stashes), git stash drop (remove), git stash branch (create branch from stash). Useful for: switching branches mid-work, pulling before commit, trying alternatives.

### Q7: What is git bisect?
**Answer:** Binary search through commits to find where bug was introduced. Start: git bisect start + git bisect good (known good commit) + git bisect bad (current bad). Git checks out middle commit. You mark good/bad. Repeats until single commit found. Powerful debugging when you know commit works at some point.

### Q8: Cherry-pick - when to use?
**Answer:** Apply specific commit(s) to current branch. Useful for: hotfix from main to release branch, selective feature porting. Creates duplicate commit (different hash). Can cause conflicts. git cherry-pick <commit-hash>. Avoid overuse - indicates branching structure issues.

### Q9: GitFlow vs trunk-based development?
**Answer:** GitFlow: main (production), develop (integration), feature/, release/, hotfix/ branches. Structured, supports releases. Complex. Good for release-cycle software. Trunk-based: short-lived feature branches → merge to main (trunk) frequently. Feature flags for incomplete features. Simpler, supports CI/CD. Recommended for modern teams.

### Q10: GitHub Actions - core concepts?
**Answer:** Workflow (YAML file in .github/workflows/), triggers (push, pull_request, schedule, workflow_dispatch), jobs (run in parallel), steps (sequential commands), actions (reusable units). Runners (GitHub-hosted or self-hosted). Matrix builds (multiple OS/lang versions). Caching dependencies. Services (PostgreSQL, Redis). Your CI/CD experience is with GitHub Actions.

### Q11: Conventional commits - what are they?
**Answer:** Standardized commit format: `type(scope): description`. Types: feat, fix, chore, docs, style, refactor, perf, test, ci, build, revert. Enables automatic versioning (semantic-release), changelog generation. Example: `feat(auth): add OAuth2.0 login support`.

### Q12: Interactive rebase - what is it used for?
**Answer:** `git rebase -i HEAD~n` - edit, squash, reorder, split commits. Use cases: clean up commit history before PR, combine fixup commits ("squash"), split large commit, edit commit message. Powerful but rewrite history - only for local/feature branches.

### Q13: What is .gitignore for?
**Answer:** Specifies intentionally untracked files Git should ignore. Patterns: node_modules/, .env, *.log, __pycache__/, .next/, dist/, build/. Use gitignore.io for templates. `git check-ignore -v file` debugs why file is ignored.

### Q14: GitHub workflows for FastAPI - typical setup?
**Answer:** ```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env: POSTGRES_PASSWORD: postgres
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest --cov
```

### Q15: How to revert a merge commit?
**Answer:** `git revert -m 1 <merge-commit-hash>`. -m 1 tells Git to revert to parent 1 (the mainline branch). Reverting a merge is safe but subsequent re-merge can be tricky (need to revert the revert).
