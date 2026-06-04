# Scratch ✏️

**A dead-simple terminal text editor — as easy as editing a note in Notepad++.**

No modes. No `:wq`. No memorizing arcane commands. Just open a file and start
typing, with the familiar shortcuts you already know.

```
$ scratch notes.txt
```

---

## Why Scratch?

Vim and Nano are powerful, but they make you stop and think. Vim is modal
(press `i` to type, `Esc` then `:wq` to save). Nano works but feels dated and
clumsy. **Scratch** aims for the experience of a graphical notepad, in your
terminal:

- ⌨️ **Type immediately** — no insert mode, no modes at all
- 🖱️ **Mouse support** — click to place the cursor, drag to select
- 📋 **Familiar shortcuts** — `Ctrl+S` to save, `Ctrl+Z` to undo
- 🔢 **Line numbers** on by default
- 🎨 **Syntax highlighting** for common languages, automatically
- 💾 **"Save changes?" prompt** so you never lose work on quit

## Install

Scratch requires **Python 3.9+**.

```bash
# Clone the repo
git clone https://github.com/Bmontythe3rd/scratch.git
cd scratch

# Install (editable, so you can hack on it)
pip install -e .
```

That installs a `scratch` command on your PATH.

> **Tip:** prefer an isolated install? Use [pipx](https://pipx.pypa.io/):
> `pipx install .`

## Usage

```bash
scratch                # start with an empty buffer
scratch file.txt       # open an existing file (or create on save)
scratch --version      # print version
```

## Keybindings

| Shortcut   | Action                          |
|------------|---------------------------------|
| `Ctrl+S`   | Save                            |
| `Ctrl+O`   | Reload current file             |
| `Ctrl+Q`   | Quit (prompts if unsaved)       |
| `Ctrl+Z`   | Undo                            |
| `Ctrl+Y`   | Redo                            |
| `Ctrl+C`   | Copy selection                  |
| `Ctrl+X`   | Cut selection                   |
| `Ctrl+V`   | Paste                           |
| Arrow keys | Move cursor                     |
| Mouse      | Click to position, drag to select |

> Undo/redo/copy/cut/paste are provided by the underlying text widget, so they
> behave just like you'd expect from a desktop editor.

## Project layout

```
scratch/
├── README.md
├── LICENSE
├── pyproject.toml
├── src/scratch_editor/
│   ├── __init__.py
│   ├── __main__.py      # CLI entry point
│   └── app.py           # the editor itself
├── tests/
│   └── test_language.py
└── docs/
    └── ARCHITECTURE.md  # design decisions + roadmap
```

## Roadmap

v1 (this release) is intentionally minimal. Planned next:

- [ ] File-picker dialog for `Ctrl+O` and Save-As
- [ ] Find & replace (`Ctrl+F` / `Ctrl+H`)
- [ ] Multiple tabs / buffers
- [ ] Configurable themes
- [ ] Standalone binary (port core to Go)

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full design.

## Contributing

Issues and PRs welcome! Run the test suite with `pytest`.

## License

MIT — see [LICENSE](LICENSE).
