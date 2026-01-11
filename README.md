# Git Clone (Python)

A minimal implementation of the Git Version Control System, built from scratch in Python to understand how Git works under the hood.

---

## Overview

This project implements the core functionality of Git—reading, writing, and storing data—without using the official Git libraries.  
It interacts directly with the file system to manage the `.git` directory, binary object storage, SHA-1 hashing, and the Merkle DAG (Directed Acyclic Graph).

The goal is **deep systems-level understanding**, not feature parity.

---

## Project Structure

The project is architected as a modular Python system, separating the storage engine (**plumbing**) from the business logic.

```
Git_Clone/
├── main.py            # Command Line Interface (CLI) & Dispatcher
├── README.md          # Project Documentation
└── lib/               # Core Libraries
    ├── data.py        # Storage Engine (File I/O, Hashing, Compression)
    └── base.py        # Logic Layer (Trees, Commits, Object Parsing)
```

---

## Features Implemented

- **Repository Initialization**  
  Creates the `.git` directory structure from scratch.

- **Blob Storage (CAS)**  
  Hashes and compresses file contents using SHA-1 and zlib.

- **Tree Snapshots**  
  Recursively scans directories to construct Merkle Trees.

- **Commit History**  
  Links snapshots with metadata (author, timestamp, message).

- **Log Graph Traversal**  
  Walks commit history backwards via parent pointers.

- **Checkout (Time Travel)**  
  Restores the working directory to any previous commit state.

---

## How to Run

Requires **Python 3**.  
All commands are executed via `main.py`.

---

### 1. Initialize a Repository

```bash
python3 main.py init
```

Creates the `.git` directory and required internal structure.

---

### 2. Save a Snapshot (Commit)

This mimics `git add .` + `git commit` by snapshotting the entire directory.

#### Step 1: Create the Tree Object

```bash
python3 main.py write-tree
```

Output:
```
<tree_hash>
```

#### Step 2: Create the Commit Object

```bash
python3 main.py commit-tree <tree_hash> -m "My Commit Message"
```

---

### 3. View Commit History

```bash
python3 main.py log
```

Traverses commits starting from `HEAD`.

---

### 4. Time Travel (Checkout)

⚠️ **WARNING**: This overwrites files in your working directory.

```bash
python3 main.py checkout <commit_hash>
```

Restores the directory state exactly as it existed at that commit.

---
## Notes

- No Git libraries are used.
- All objects are stored and read in raw Git-compatible formats.
- Designed for learning internals, not production use.
