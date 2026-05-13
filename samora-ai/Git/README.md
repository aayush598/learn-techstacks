# Git Interview Questions and Answers

## Q1: What is Git?
**A:** Git is a distributed version control system (DVCS) created by Linus Torvalds in 2005. It tracks changes in source code, enables collaboration among developers, and supports branching, merging, and history rewrites. Unlike centralized systems, every developer has a full copy of the repository.

## Q2: What is the difference between Git and SVN?
**A:** Git is distributed (full local copy with offline capabilities); SVN is centralized (requires server connection). Git has cheap local branching; SVN branching is directory-based and expensive. Git stores snapshots; SVN stores file differences. Git uses cryptographic hashes for content integrity.

## Q3: What is a Git repository?
**A:** A Git repository is a data structure that stores metadata and object database for a project. It contains all commits, branches, tags, and configuration. It resides in the `.git` directory. Repositories can be local (on your machine) or remote (on GitHub, GitLab, etc.).

## Q4: What is the difference between a local and remote repository?
**A:** A local repository resides on your machine and contains the complete project history. A remote repository is hosted on a server (GitHub, GitLab, Bitbucket) for collaboration. You push local commits to remote and pull others' changes from remote.

## Q5: What is the `.git` directory?
**A:** The `.git` directory is the heart of a Git repository. It contains: `objects/` (all data blobs, trees, commits), `refs/` (branches and tags), `HEAD` (current branch), `config` (repo config), `index` (staging area), `hooks/` (scripts), `logs/` (reflog), and `description`.

## Q6: What is a commit in Git?
**A:** A commit is a snapshot of the repository at a specific point in time. Each commit has a unique SHA-1 hash, contains a pointer to the parent commit(s), and stores the author, committer, timestamp, and commit message. Commits are immutable once created.

## Q7: What is the difference between `git commit` and `git add`?
**A:** `git add` stages changes (adds them to the staging area/index). `git commit` creates a permanent snapshot of the staged changes in the repository history. You must stage before committing. `git commit -a` combines both for tracked files.

## Q8: What is the staging area (index) in Git?
**A:** The staging area (or index) is an intermediate area between the working directory and the repository. It holds the proposed next commit. You add changes to staging with `git add`, then commit them. It allows you to craft commits selectively.

## Q9: What is the working directory in Git?
**A:** The working directory (or working tree) is the directory on your filesystem where you edit files. Git tracks changes in this directory. Files can be in three states: modified (changed but not staged), staged (added to index), or committed (saved in repository).

## Q10: What is the difference between `git fetch` and `git pull`?
**A:** `git fetch` downloads changes from the remote but does NOT merge them into your working branch. `git pull` is `git fetch` + `git merge` (or `git rebase` with `--rebase`) — it downloads and integrates changes. Fetch is safer for reviewing changes before merging.

## Q11: What is `git pull --rebase`?
**A:** `git pull --rebase` fetches remote changes and then rebases your local commits on top of them instead of merging. This creates a linear history without merge commits. It avoids the "merge commit" clutter but rewrites local commit hashes.

## Q12: What is a branch in Git?
**A:** A branch is a lightweight, movable pointer to a specific commit. Branching allows parallel development without affecting the main codebase. Creating a branch is instantaneous (just creates a new pointer). The default branch is typically `main` (or `master`).

## Q13: What is the difference between `git branch` and `git checkout -b`?
**A:** `git branch <name>` creates a new branch but stays on the current branch. `git checkout -b <name>` creates a new branch AND switches to it. Modern Git also uses `git switch -c <name>` as an alternative to `checkout -b`.

## Q14: What is a merge commit?
**A:** A merge commit is a special commit with two (or more) parent commits, created when merging branches. It represents the integration of divergent histories. It has the combined changes from both branches. Fast-forward merges do not create a merge commit.

## Q15: What is a fast-forward merge?
**A:** A fast-forward merge occurs when the target branch has not diverged — the branch being merged is directly ahead. Git simply moves the branch pointer forward. No merge commit is created. Use `--no-ff` to force a merge commit even in this case.

## Q16: What is a three-way merge in Git?
**A:** A three-way merge occurs when both branches have diverged (have different commits since their common ancestor). Git compares three snapshots: the common ancestor, the current branch head, and the branch being merged. It combines changes from both branches.

## Q17: What is a merge conflict?
**A:** A merge conflict occurs when Git cannot automatically resolve differences between branches — typically when the same line(s) of the same file were modified differently in both branches. Git marks the conflict in the file with `<<<<<<<`, `=======`, and `>>>>>>>` markers, requiring manual resolution.

## Q18: How do you resolve a merge conflict?
**A:** (1) Identify conflicted files with `git status`. (2) Edit each conflicted file, choosing the correct code. (3) Remove conflict markers. (4) Stage the resolved file with `git add`. (5) Complete the merge with `git commit` (or `git merge --continue`).

## Q19: What is `git rebase`?
**A:** `git rebase` rewrites commit history by moving or combining a sequence of commits to a new base commit. It creates a linear history by applying commits from the current branch on top of the target branch. It is an alternative to merging for feature branch integration.

## Q20: What is the difference between `git merge` and `git rebase`?
**A:** Merge preserves history as-is, creating a merge commit for divergent branches. Rebase rewrites history by applying commits linearly on top of another branch, creating a cleaner, linear history. Rebase should not be used on shared/public branches as it rewrites commit hashes.

## Q21: What is an interactive rebase (`git rebase -i`)?
**A:** Interactive rebase allows modifying commits during a rebase. You can: `pick` (keep), `reword` (change message), `edit` (modify content), `squash` (combine with previous), `fixup` (combine discarding message), `drop` (delete), or `exec` (run commands). It is used for cleaning up history before merging.

## Q22: What is `git squash`?
**A:** Squash combines multiple commits into one during an interactive rebase. The squashed commits' changes are merged into the previous commit, and you can write a new commit message. It is used to clean up messy development history before merging to main.

## Q23: What is `git cherry-pick`?
**A:** `git cherry-pick` applies a specific commit (or range of commits) from one branch to the current branch. It creates a new commit with the changes from the cherry-picked commit. Useful for selectively applying bug fixes or features from another branch.

## Q24: What is `git revert`?
**A:** `git revert` creates a new commit that undoes the changes from a previous commit. Unlike `git reset`, it does not alter history — it adds a new commit that inverses the target commit's changes. This is the safe way to undo changes on shared branches.

## Q25: What is the difference between `git revert` and `git reset`?
**A:** `git revert` creates a new commit that undoes changes (safe for shared history). `git reset` moves the branch pointer and optionally modifies the working directory and staging area (destructive — rewrites history). Reset should not be used on public branches.

## Q26: What is `git reset --soft`, `--mixed`, and `--hard`?
**A:** `--soft`: moves HEAD but leaves staged changes and working directory unchanged. `--mixed` (default): moves HEAD and unstages changes (files remain modified in working directory). `--hard`: moves HEAD and discards all changes in both staging and working directory (irreversible without reflog).

## Q27: What is `git stash`?
**A:** `git stash` temporarily saves uncommitted changes (both staged and unstaged) and reverts the working directory to the last commit. You can later restore them with `git stash pop` or `git stash apply`. Useful for switching branches mid-task.

## Q28: What are different `git stash` commands?
**A:** `git stash` / `git stash push` (save changes). `git stash pop` (apply and remove from stash). `git stash apply` (apply but keep in stash). `git stash list` (list stashes). `git stash drop` (delete a stash). `git stash clear` (delete all stashes). `git stash branch <name>` (create branch from stash).

## Q29: What is `git log` and its useful options?
**A:** `git log` displays commit history. Useful options: `--oneline` (compact), `--graph` (ASCII branch graph), `--all` (all branches), `--author=<name>` (filter by author), `--since=`/`--until=` (date range), `-p` (show diffs), `--grep=` (search commit messages), `-S` (search code changes).

## Q30: What is `git diff`?
**A:** `git diff` shows changes between commits, branches, the working directory, and the staging area. `git diff` (unstaged changes). `git diff --staged` (staged changes). `git diff branch1..branch2` (between branches). `git diff commit1 commit2` (between commits).

## Q31: What is `git blame`?
**A:** `git blame` shows each line of a file annotated with the commit hash, author, and date of the last modification. It is used to find who changed a specific line and when. Useful for debugging and understanding code history.

## Q32: What is `git bisect`?
**A:** `git bisect` uses binary search to find the commit that introduced a bug. You mark a known good commit and a known bad commit. Git checks out the midpoint, you test, mark good/bad, and Git narrows down the search. It finds the buggy commit in O(log n) steps.

## Q33: What is `git tag`?
**A:** `git tag` marks a specific commit with a meaningful name (e.g., `v1.0.0`, `release-2024`). Tags are typically used for releases. Lightweight tags are just pointers. Annotated tags (`-a`) include metadata (tagger, date, message) and are cryptographically signable.

## Q34: What is the difference between lightweight and annotated tags?
**A:** Lightweight tags are just pointers to commits (like branches that don't move). Annotated tags are full objects in the Git database with tagger name, email, date, and message. Annotated tags can be signed and verified. Use annotated tags for releases.

## Q35: What is `git remote`?
**A:** `git remote` manages connections to remote repositories. Commands: `git remote add <name> <url>` (add remote), `git remote -v` (list remotes), `git remote remove <name>`, `git remote rename <old> <new>`, `git remote update` (fetch all remotes).

## Q36: What is the difference between `origin` and `upstream`?
**A:** `origin` is the default name for your fork/clone of a repository. `upstream` is a conventional name for the original repository you forked from. For example, if you fork a repo on GitHub, your fork is `origin`, the original is `upstream`.

## Q37: What is `git push` and its common flags?
**A:** `git push` uploads local commits to a remote repository. Common flags: `-u`/`--set-upstream` (set tracking), `--force`/`-f` (force push, overwrite remote), `--force-with-lease` (safer force — checks if remote has changes you haven't seen), `--tags` (push tags), `--delete` (delete remote branch).

## Q38: What is `git push --force-with-lease`?
**A:** `--force-with-lease` is a safer alternative to `--force`. It checks that the remote branch hasn't been updated by someone else since you last fetched. If it has, the push is rejected, preventing accidental overwriting of others' commits.

## Q39: What is a detached HEAD state?
**A:** Detached HEAD occurs when you checkout a specific commit, tag, or remote branch instead of a local branch. HEAD points directly to a commit rather than a branch. Any commits made in detached HEAD are not on any branch and can be lost. Create a branch to save them.

## Q40: How do you recover from a detached HEAD?
**A:** If you made commits in detached HEAD, create a branch to save them: `git checkout -b new-branch-name`. To return to a branch without saving: `git checkout <branch-name>`. The detached commits will eventually be garbage collected (90 days for reflog entries).

## Q41: What is the HEAD pointer in Git?
**A:** HEAD is a symbolic reference to the currently checked-out branch (or commit in detached mode). It points to the latest commit on the current branch. It is stored in `.git/HEAD`. Git uses HEAD to determine what to compare against and where to add new commits.

## Q42: What is `git reflog`?
**A:** `git reflog` (reference log) records every time HEAD changes — commits, checkouts, rebases, resets, merges. It shows a local history of your actions. The reflog is your safety net for recovering lost commits (up to 90 days by default).

## Q43: How do you recover a deleted commit using reflog?
**A:** Use `git reflog` to find the commit hash before deletion. Then `git checkout <hash>` (detached HEAD) and create a branch: `git branch recovery-branch`. Or directly `git reset --hard <hash>` if you want to move your current branch back.

## Q44: What is `git gc`?
**A:** `git gc` (garbage collection) compresses the repository by removing unreachable objects, packing refs, and consolidating loose objects into packfiles. It reduces disk usage and improves performance. Git runs it automatically, but manual invocation can be triggered when needed.

## Q45: What is `git fsck`?
**A:** `git fsck` (filesystem check) verifies the integrity of the Git database, checking for dangling objects, missing objects, and corruptions. It is used for repository health checks and recovery. `git fsck --lost-found` recovers dangling objects to `.git/lost-found/`.

## Q46: What is a Git hook?
**A:** Git hooks are scripts that execute automatically at specific points in the Git workflow. They reside in `.git/hooks/`. Types include: `pre-commit` (before commit), `post-commit`, `pre-push`, `post-merge`, `pre-receive`, `post-receive`, `prepare-commit-msg`, and `commit-msg`.

## Q47: What are common pre-commit hooks?
**A:** Common pre-commit hooks include: (1) Linting (ESLint, pylint). (2) Format checking (Prettier, black). (3) Code style enforcement. (4) Preventing commits to protected branches. (5) Secret detection (preventing credentials from being committed). (6) Running tests.

## Q48: What is a submodule in Git?
**A:** A submodule is a reference to another Git repository embedded within the current repository at a specific commit. It allows including external projects while maintaining their independent version history. Commands: `git submodule add`, `git submodule update --init --recursive`.

## Q49: What is a subtree merge in Git?
**A:** A subtree merge incorporates another project into a subdirectory of the current repository. Unlike submodules (which are external references), subtree merge copies the external project's history into the main repo. It is simpler for deployment but can bloat history.

## Q50: What is the difference between a fork and a branch?
**A:** A fork is a copy of an entire repository on a server (GitHub/GitLab), creating a separate remote repository. A branch is a lightweight pointer within the same repository. Forks are used for independent development or contributing to projects where you lack write access.

## Q51: What is a pull request (PR)?
**A:** A pull request is a feature in Git hosting platforms (GitHub, GitLab, Bitbucket) that proposes changes from one branch to another (typically to merge a feature branch into main). It enables code review, discussion, and automated checks before merging.

## Q52: What is the difference between a pull request and a merge request?
**A:** They are the same concept with different names. GitHub uses "Pull Request" (PR). GitLab uses "Merge Request" (MR). Both propose merging changes from one branch into another with review and discussion capabilities.

## Q53: What is `git worktree`?
**A:** `git worktree` allows checking out multiple branches simultaneously in separate directories, all sharing the same Git repository. Useful for working on different features without stashing or cloning the repo again. Example: `git worktree add ../feature-branch feature-branch`.

## Q54: What is `git clean`?
**A:** `git clean` removes untracked files from the working directory. `git clean -n` (dry run), `git clean -f` (force remove files), `git clean -fd` (remove files and directories), `git clean -fx` (remove files ignored by .gitignore too). Use with caution.

## Q55: What is `.gitignore`?
**A:** `.gitignore` specifies intentionally untracked files that Git should ignore. Patterns include: `*.log` (all log files), `build/` (directory), `/config.env` (root file only), `!.gitkeep` (negation — don't ignore). It should be committed to the repository.

## Q56: What is `.gitkeep`?
**A:** `.gitkeep` is a convention (not a Git feature) for keeping empty directories in a repository. Git does not track empty directories. Adding an empty `.gitkeep` file makes Git track the directory. The file itself has no special meaning.

## Q57: What is `git config`?
**A:** `git config` sets configuration values for Git. Levels: `--system` (all users), `--global` (current user), `--local` (current repository, default). Common settings: `user.name`, `user.email`, `core.editor`, `core.autocrlf`, `alias.*`, `credential.helper`.

## Q58: How do you set up Git aliases?
**A:** Git aliases create shortcuts for commands. Examples: `git config --global alias.st status`, `git config --global alias.ci commit`, `git config --global alias.lg "log --oneline --graph --all"`. Then use `git st` instead of `git status`.

## Q59: What is `git show`?
**A:** `git show` displays information about a Git object — typically a commit. It shows the commit hash, author, date, message, and diff. `git show <commit>` shows a specific commit. `git show --stat` shows only changed files. `git show :file` shows staged file content.

## Q60: What is the difference between `HEAD~1` and `HEAD^1`?
**A:** Both refer to the first parent of HEAD. `~N` means N generations back (direct parent chain). `^N` means the N-th parent (for merge commits with multiple parents). `HEAD~2` is grandparent; `HEAD^2` is the second parent of a merge commit.

## Q61: What is `git shortlog`?
**A:** `git shortlog` summarizes `git log` output grouped by author. It is commonly used for generating changelogs: `git shortlog -sn` (summary with commit counts), `git shortlog -sne` (with email), `git shortlog v1.0..v2.0` (changes between tags).

## Q62: What is `git describe`?
**A:** `git describe` generates a human-readable name for the current commit based on the most recent tag. Output format: `v1.0-5-gabc1234` (5 commits after tag v1.0, commit abc1234). Useful for version identification in builds.

## Q63: What is a bare repository?
**A:** A bare repository has no working directory — only the `.git` contents. It is used as a central hub for pushing/pulling (like on GitHub servers). Created with `git init --bare`. You cannot edit files directly in a bare repository.

## Q64: How do you create a new branch and push it to remote?
**A:** Local: `git checkout -b feature-branch`. Then: `git push -u origin feature-branch`. The `-u` flag sets upstream tracking. After that, you can use `git push` without arguments. To delete remote branch: `git push origin --delete feature-branch`.

## Q65: What is `git archive`?
**A:** `git archive` creates a compressed archive (tar or zip) of the repository at a specific commit or branch. It excludes `.git` directory. Example: `git archive --format=zip --output=project.zip main`. Useful for distributing source code without Git metadata.

## Q66: What is `git submodule update --init --recursive`?
**A:** This command initializes and updates all submodules recursively. `--init` initializes submodules that aren't yet, `--recursive` handles nested submodules. It is commonly used after cloning a repository with submodules.

## Q67: How do you change the last commit message?
**A:** If the commit hasn't been pushed: `git commit --amend -m "New message"`. If pushed: use `git commit --amend -m "New message"` then `git push --force-with-lease` (force pushing rewrites remote history — use with caution on shared branches).

## Q68: How do you add files to the last commit?
**A:** Stage the forgotten files with `git add <file>`, then `git commit --amend --no-edit` (keep existing message) or `git commit --amend`. This modifies the last commit. Only do this if the commit hasn't been shared with others.

## Q69: What is a Git blob?
**A:** A blob (Binary Large Object) is the Git object type that stores file content. Blobs are identified by their SHA-1 hash. They store only content, not file names or metadata. Files are reconstructed by tree objects that map names to blobs.

## Q70: What is a Git tree object?
**A:** A tree object stores directory structure — it maps filenames to blob objects (for files) or other tree objects (for subdirectories). Each entry includes the file mode, type (blob/tree), hash, and filename. A commit points to a tree object representing the root directory.

## Q71: How does Git store objects?
**A:** Git stores objects in `.git/objects/` as loose objects (one file per object, compressed with zlib). Each object is named by its SHA-1 hash (first 2 chars as subdirectory, remaining 38 as filename). When enough loose objects accumulate, Git packs them into packfiles for efficiency.

## Q72: What is a packfile in Git?
**A:** A packfile is a compressed, single-file format for storing multiple Git objects efficiently. It uses delta compression (storing differences between object versions). The corresponding `.idx` file provides quick lookup. `git gc` creates and optimizes packfiles.

## Q73: What is `git verify-pack`?
**A:** `git verify-pack` checks the integrity of Git packfiles and lists their contents. It shows objects in a packfile, their sizes, and delta chains. Useful for debugging repository size and object storage issues.

## Q74: What is the difference between `git fetch` and `git remote update`?
**A:** Both fetch from remotes. `git fetch` fetches from a specific remote (default `origin`). `git remote update` fetches from all configured remotes. `git remote update --prune` also removes stale remote-tracking branches.

## Q75: What is `git prune`?
**A:** `git prune` removes unreachable (dangling) objects from the object database. It is rarely called directly — `git gc` already includes pruning. `git prune --expire=now` immediately removes unreachable objects. Use with caution.

## Q76: What is `git replace`?
**A:** `git replace` allows replacing one object with another without changing the actual repository history. It creates a replace reference in `.git/refs/replace/`. Used for: grafting histories, fixing corrupted commits, or simulating merges without actual changes.

## Q77: What is `git filter-branch`?
**A:** `git filter-branch` rewrites Git history by applying a filter to branches. It can: remove files from history (`--index-filter`), change author info (`--env-filter`), or modify commit messages (`--msg-filter`). It is deprecated in favor of `git filter-repo`.

## Q78: What is `git filter-repo`?
**A:** `git filter-repo` is the recommended replacement for `git filter-branch`. It is faster, safer, and more versatile. It can remove large files, purge sensitive data, split/join repositories, and rewrite author information. It must be installed separately.

## Q79: What is Git LFS (Large File Storage)?
**A:** Git LFS replaces large files (binaries, assets) with text pointers in the repository while storing the actual file content on a remote server. It prevents repository bloat. Common for game assets, multimedia, and large datasets.

## Q80: How do you remove a file from Git history?
**A:** If the file is sensitive (e.g., credentials): (1) Add to `.gitignore`. (2) Use `git filter-repo --path <file> --invert-paths` or `git filter-branch` to purge from history. (3) Force push to remote. (4) Rotate any compromised credentials. This rewrites history for all collaborators.

## Q81: What is `git range-diff`?
**A:** `git range-diff` compares two commit ranges (e.g., before and after a rebase). It shows how commits changed — which were added, removed, or modified. Useful for reviewing the effects of a rebase or interactive rebase before force-pushing.

## Q82: What is `git bundles`?
**A:** `git bundle` packages Git objects and references into a single binary file. It is used for offline transfer or when direct network access is unavailable. Example: `git bundle create repo.bundle --all`, then transfer the file and `git clone repo.bundle`.

## Q83: What is a shallow clone?
**A:** A shallow clone (`git clone --depth 1`) downloads only the latest commit without history. It is faster for large repositories but limits operations that need history (blame, log, etc.). History can be deepened later with `git fetch --deepen=<n>`.

## Q84: What is a blobless clone?
**A:** A blobless clone (`git clone --filter=blob:none`) downloads all commits and trees but only fetches blob content on-demand. It saves bandwidth while preserving history. This is a partial clone feature of modern Git.

## Q85: What is a treeless clone?
**A:** A treeless clone (`git clone --filter=tree:0`) downloads only commits initially. Trees and blobs are fetched on-demand (during checkout, diff, etc.). It is the most bandwidth-efficient clone type but requires network access for many operations.

## Q86: What is `git maintenance`?
**A:** `git maintenance` (Git 2.30+) manages background maintenance tasks for Git repositories. It automates `git gc`, prefetching, commit-graph updates, and loose object packing. Used for optimizing large repositories. Configure with `git maintenance start`.

## Q87: What is `git sparse-checkout`?
**A:** `git sparse-checkout` allows checking out only a subset of files from a repository. It enables working with monorepos by limiting the working directory to specific directories. Configure with `git sparse-checkout set <path>`.

## Q88: What is Git protocol?
**A:** Git supports four protocols for data transfer: (1) Local — direct filesystem access. (2) HTTP/HTTPS — widely used, works with firewalls. (3) SSH — secure, authenticated. (4) Git — custom protocol, fastest but unauthenticated (port 9418). HTTPS and SSH are most common for remote operations.

## Q89: What is a Git hook for pre-push?
**A:** The `pre-push` hook runs before `git push` completes. It receives remote name, URL, and list of refs being pushed. Common uses: running tests, linting, checking for large files, or preventing pushes to protected branches.

## Q90: How do you share code between repositories without duplication?
**A:** Options: (1) Git submodules — reference external repos at pinned commits. (2) Git subtrees — merge external repo into a subdirectory. (3) Monorepo — keep everything in one repo. (4) Package managers (npm, pip) — extract shared code into packages.

## Q91: What is a monorepo and how does Git handle it?
**A:** A monorepo stores multiple projects in a single Git repository. Git handles it natively, but large monorepos benefit from: sparse checkout, partial clones, `git filter-repo`, Microsoft's VFS for Git (now Scalar), and Google's custom Git protocol.

## Q92: What is Git Scalar?
**A:** Scalar is Microsoft's tool for managing large Git repositories. It configures optimal settings (partial clone, sparse checkout, background maintenance), improves fetch performance with prefetching, and reduces CPU/memory usage for monorepo workflows.

## Q93: What is `git maintenance start` vs `git maintenance run`?
**A:** `git maintenance start` registers the repository for hourly, daily, and weekly background maintenance tasks (via cron/systemd timers). `git maintenance run` runs a specific task immediately (e.g., `git maintenance run --task=gc`).

## Q94: What is the `--orphan` flag in `git checkout`?
**A:** `git checkout --orphan <branch>` creates a new branch with no commit history (first commit will have no parent). It creates a clean working tree based on the current state. Useful for creating completely separate histories (e.g., `gh-pages` branches).

## Q95: What is `git notes`?
**A:** `git notes` attaches additional metadata to existing commits without changing the commit itself (and hence its SHA). Notes are stored as separate objects. Useful for adding review comments, build status, or supplementary information after commits are made.

## Q96: What is the difference between `--cached` and `--staged` in Git?
**A:** They are synonyms. Both refer to the staging area (index). For example, `git diff --staged` and `git diff --cached` both show changes staged for the next commit. Some commands (like `git rm --cached`) use `--cached` to indicate the index rather than working tree.

## Q97: How do you find which commit introduced a specific string?
**A:** Use `git log -S "string"` (pickaxe search) — finds commits that added or removed the string. Use `git log -G "regex"` for regex search. Use `git log --all -S "string"` to search all branches. `git log -p -S "string"` shows the actual diffs.

## Q98: How does Git handle line endings?
**A:** Configured with `core.autocrlf`: `true` (convert CRLF to LF on commit, LF to CRLF on checkout for Windows), `input` (convert CRLF to LF on commit, no conversion on checkout for Linux/Mac), `false` (no conversion). Use `.gitattributes` for per-file-type settings.

## Q99: What is a Git signing (commit signing)?
**A:** Git commits and tags can be cryptographically signed using GPG or SSH keys. Signed commits verify the identity of the author. Commands: `git commit -S` (sign commit), `git tag -s` (sign tag). Verification: `git log --show-signature`.

## Q100: What is the Git object model?
**A:** Git's object model consists of four object types: (1) **Blob** — file content. (2) **Tree** — directory listing (maps names to blobs/trees). (3) **Commit** — snapshot with author, message, parent pointers, and a root tree. (4) **Tag** — a named reference to a commit (annotated tags are objects). All objects are identified by SHA-1 hash and are immutable.
