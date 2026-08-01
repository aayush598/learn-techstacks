# Chapter: Files and Directories

## What you'll learn
- What a **file** is: its attributes (name, type, size, timestamps, permissions, owner), the fundamental **operations** (create, open, read, write, seek, delete), and the access-method API.
- How **directories** organize files: single-level, two-level, tree, and acyclic-graph structures — and how paths/linking arise from them.
- **File access methods**: sequential (the default), direct/random (index-based), and indexed (index nodes) — and which workloads use which.

## Prerequisites (linked)
- [Part 08 README](../README.md) — storage stack overview.
- Part 01/02 — syscall model and process I/O context (file descriptors will reappear in Part 09).

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [File Concept, Attributes and Operations](section-01-file-concept-attributes-and-operations.md) | What IS a file, what metadata does the OS keep, and what operations define it? |
| 02 | [Directory Structures](section-02-directory-structures.md) | How are files organized/named, from flat lists to trees and graphs? |
| 03 | [File Access Methods](section-03-file-access-methods.md) | How do programs read files: sequentially, directly, or via indexes? |

## One-paragraph narrative connecting all sections
Files exist to give programs durable, named data that survives process lifetimes — Section 01 defines the object: a sequence of bytes plus metadata (attributes) and a contract of operations (open/read/write/seek/close) with open-file semantics shared across processes. Since a disk is just a flat sequence of blocks, files need *organization and naming*, which Section 02 provides: directories are themselves files whose entries map names to inodes/file IDs, structured from the simplest single list up to hierarchical trees and acyclic graphs (which introduce hard links and aliasing). Section 03 covers how content is actually read: sequential access (the default for tapes and streams), direct access (random seek by record index, the database standard), and indexed access (an index of keys→offsets, e.g., DBMS and file-system-level `seek`). These three sections give you the API-level mental model; Chapter 02 shows how the bytes are physically laid out.

## Common interview trap in this chapter
**Trap:** Confusing a *file descriptor* (an integer handle into the process's FD table — Part 09) with a *file* (the named object). Also: saying a directory "contains" files — it *contains names→inode mappings*, the content lives in data blocks. And assuming file content is the same as file metadata — attributes live in the inode (Chapter 02), which `stat()` reads, not in the data.

## Checklist before moving on
- [ ] I can list the core file attributes and the core file operations.
- [ ] I can explain the open-file table and sharing between processes.
- [ ] I can compare directory structure designs and name the one modern OSes use (tree).
- [ ] I can explain sequential vs direct vs indexed access with concrete examples.
- [ ] I can explain what a path traversal actually resolves (dir entries → inode).
