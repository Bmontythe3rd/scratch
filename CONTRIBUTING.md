# Contributing to Scratch

Thanks for your interest! Scratch is intentionally small and approachable.

## Setup

```bash
git clone https://github.com/BRYAN_USERNAME/scratch.git
cd scratch
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Running

```bash
scratch              # empty buffer
scratch README.md    # open a file
```

## Tests & lint

```bash
pytest          # run the test suite
ruff check .    # lint
```

## Guidelines

- Keep v1 simple. New features should preserve the "no docs needed" feel.
- Match desktop-editor muscle memory for any new keybinding.
- Add a test for any pure logic; document TUI behavior in the PR description.
- Update `docs/ARCHITECTURE.md` when you make a notable design decision.

## Workflow

1. Create a branch: `git checkout -b feature/find-replace`
2. Commit in small, descriptive chunks.
3. Open a PR against `main` describing the change and how you tested it.

Happy hacking! ✏️
