# Architecture & Design Decisions

This document explains *why* Scratch is built the way it is, so future
contributors (including future-you) understand the reasoning.

## Goal

Recreate the feel of a graphical notepad (think Notepad++) inside a terminal.
The north-star requirement: **a first-time user should be able to open a file,
type, and save without reading any docs.**

## Why Python + Textual

We evaluated three stacks:

| Stack             | Verdict                                                  |
|-------------------|----------------------------------------------------------|
| Python + Textual  | ✅ Chosen — fastest path to a usable, non-modal editor   |
| Go + tview/tcell  | Great for a single binary; more code for v1              |
| Rust + ratatui    | Best performance; steepest path, slowest to iterate      |

[Textual](https://textual.textualize.io/) ships a `TextArea` widget that
already provides the hard parts of a text editor:

- Non-modal editing (you just type)
- Mouse support (click to position, drag to select)
- Selection, copy / cut / paste, undo / redo
- Line numbers and Tree-sitter syntax highlighting

Building these from scratch in any language would be weeks of work. By standing
on `TextArea`, v1 becomes a thin, comprehensible layer: load a file, wire up
save/quit, show a status bar. That tradeoff (runtime dependency vs. development
speed and UX quality) is the right call for v1. A standalone binary is on the
roadmap for a later version.

## Module overview

- **`app.py`** — the entire application:
  - `ScratchApp` — the Textual `App`. Owns the `TextArea`, the status bar, and
    the file path. Handles save / open / quit actions and keybindings.
  - `StatusBar` — a reactive `Label` showing filename, modified flag, and
    cursor position. Reactive attributes auto-refresh the render.
  - `ConfirmQuitScreen` — a modal shown on quit when there are unsaved changes.
  - `language_for()` — maps file extension → highlight language.
- **`__main__.py`** — argparse CLI; `scratch [file]`.
- **`__init__.py`** — public exports + version.

## Key design choices

**Tracking "modified" state.** Rather than hooking every keystroke into a dirty
flag, we keep a snapshot of the last-saved text (`_saved_text`) and compare it
to the live buffer. Simple, correct, and cheap for the file sizes Scratch
targets. For very large files this could be optimized later.

**Save semantics.** With no filename, v1 saves to `untitled.txt` in the current
directory. This is a deliberate simplification — a proper Save-As dialog is the
first roadmap item. We document the behavior rather than hide it.

**Keybindings.** Only Save / Open / Quit are declared as app-level bindings and
shown in the footer; editing shortcuts (undo, copy, paste, etc.) come from
`TextArea` itself so they match desktop muscle memory.

## Known v1 limitations (intentional)

- `Ctrl+O` reloads the launch file rather than opening an arbitrary one.
- No Save-As dialog yet (see save semantics above).
- `.ts` files highlight using the JavaScript grammar (close enough for v1).

## Testing strategy

- **Unit tests** cover pure logic that needs no terminal — e.g. the
  extension→language mapping in `language_for()`.
- **Manual / snapshot tests** are the right tool for TUI behavior. Textual
  provides a `Pilot` test harness (`App.run_test()`) for driving key presses;
  adding Pilot-based tests for save/quit flows is a good next step once the
  dependency is installed locally.

## Roadmap

1. File-picker dialog (Open + Save-As)
2. Find & replace
3. Tabs / multiple buffers
4. Theme configuration
5. Standalone binary (Go port of the core)
