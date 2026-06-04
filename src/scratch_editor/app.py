"""Scratch — a dead-simple terminal text editor.

Scratch wraps Textual's TextArea widget to give you a non-modal editing
experience that feels like Notepad++: arrow keys, mouse, selection, and
familiar Ctrl-based shortcuts. No modes, no `:wq`, no surprises.
"""

from __future__ import annotations

from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Footer, Label, TextArea
from textual.widgets.text_area import Selection


# Map common file extensions to Textual/Tree-sitter language names so we get
# syntax highlighting for free. Unknown extensions fall back to plain text.
EXTENSION_LANGUAGES = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "javascript",   # close enough for v1 highlighting
    ".json": "json",
    ".html": "html",
    ".css": "css",
    ".md": "markdown",
    ".markdown": "markdown",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".sh": "bash",
    ".sql": "sql",
    ".xml": "xml",
    ".rs": "rust",
    ".go": "go",
    ".java": "java",
}


def language_for(path: Path | None) -> str | None:
    """Return the highlight language for a file path, or None for plain text."""
    if path is None:
        return None
    return EXTENSION_LANGUAGES.get(path.suffix.lower())


class ConfirmQuitScreen(ModalScreen[str]):
    """A small modal asking whether to save before quitting/closing.

    Dismisses with one of: "save", "discard", or "cancel".
    """

    BINDINGS = [
        Binding("s", "choose('save')", "Save & quit"),
        Binding("d", "choose('discard')", "Discard"),
        Binding("escape", "choose('cancel')", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Label("You have unsaved changes.", id="dialog-title")
            yield Label("[b]S[/b]ave & quit   [b]D[/b]iscard   [b]Esc[/b] Cancel")

    def action_choose(self, choice: str) -> None:
        self.dismiss(choice)


class StatusBar(Label):
    """Bottom status line showing filename, position, and modified state."""

    filename = reactive("untitled")
    line = reactive(1)
    column = reactive(1)
    modified = reactive(False)

    def render(self) -> str:
        flag = " ●" if self.modified else ""
        return f" {self.filename}{flag}   Ln {self.line}, Col {self.column} "


class ScratchApp(App):
    """The Scratch editor application."""

    CSS = """
    Screen {
        layout: vertical;
    }
    TextArea {
        height: 1fr;
    }
    StatusBar {
        height: 1;
        dock: bottom;
        background: $panel;
        color: $text;
    }
    #dialog {
        align: center middle;
        background: $surface;
        border: round $primary;
        padding: 1 2;
        width: auto;
        height: auto;
    }
    #dialog-title {
        text-style: bold;
        margin-bottom: 1;
    }
    ConfirmQuitScreen {
        align: center middle;
    }
    """

    # Notepad++-style keybindings. show=False keeps the footer uncluttered;
    # we surface the essentials in the footer and the rest in the README.
    BINDINGS = [
        Binding("ctrl+s", "save", "Save"),
        Binding("ctrl+o", "open_prompt", "Open"),
        Binding("ctrl+q", "quit_editor", "Quit"),
    ]

    def __init__(self, file_path: str | None = None) -> None:
        super().__init__()
        self.path: Path | None = Path(file_path) if file_path else None
        self._saved_text: str = ""

    # ---- UI construction -------------------------------------------------

    def compose(self) -> ComposeResult:
        text = ""
        if self.path and self.path.exists():
            text = self.path.read_text(encoding="utf-8", errors="replace")
        self._saved_text = text

        self.editor = TextArea.code_editor(
            text,
            language=language_for(self.path),
            show_line_numbers=True,
            id="editor",
        )
        yield self.editor
        self.status = StatusBar()
        yield self.status
        yield Footer()

    def on_mount(self) -> None:
        self.editor.focus()
        self._refresh_status()
        self._update_title()

    # ---- Status / title helpers -----------------------------------------

    def _is_modified(self) -> bool:
        return self.editor.text != self._saved_text

    def _refresh_status(self) -> None:
        row, col = self.editor.cursor_location
        self.status.filename = self.path.name if self.path else "untitled"
        self.status.line = row + 1
        self.status.column = col + 1
        self.status.modified = self._is_modified()

    def _update_title(self) -> None:
        name = self.path.name if self.path else "untitled"
        self.title = f"Scratch — {name}"

    # React to cursor movement / edits to keep the status bar live.
    def on_text_area_selection_changed(
        self, _event: TextArea.SelectionChanged
    ) -> None:
        self._refresh_status()

    def on_text_area_changed(self, _event: TextArea.Changed) -> None:
        self._refresh_status()

    # ---- Actions ---------------------------------------------------------

    def action_save(self) -> None:
        if self.path is None:
            # No filename yet — for v1 we save to "untitled.txt" in CWD.
            # (v2: a proper save-as prompt.)
            self.path = Path("untitled.txt")
            self.editor.language = language_for(self.path)
        try:
            self.path.write_text(self.editor.text, encoding="utf-8")
            self._saved_text = self.editor.text
            self._refresh_status()
            self._update_title()
            self.notify(f"Saved {self.path.name}", timeout=2)
        except OSError as exc:
            self.notify(f"Save failed: {exc}", severity="error", timeout=4)

    def action_open_prompt(self) -> None:
        # v1 keeps open simple: re-open the file passed at launch.
        # A full file-picker is planned for v2 (see ARCHITECTURE.md roadmap).
        if self.path and self.path.exists():
            self.editor.load_text(
                self.path.read_text(encoding="utf-8", errors="replace")
            )
            self._saved_text = self.editor.text
            self._refresh_status()
            self.notify(f"Reloaded {self.path.name}", timeout=2)
        else:
            self.notify("Open a file by launching: scratch <file>", timeout=3)

    def action_quit_editor(self) -> None:
        if self._is_modified():
            def handle(choice: str | None) -> None:
                if choice == "save":
                    self.action_save()
                    self.exit()
                elif choice == "discard":
                    self.exit()
                # "cancel" / None -> stay in the editor

            self.push_screen(ConfirmQuitScreen(), handle)
        else:
            self.exit()


def run(file_path: str | None = None) -> None:
    """Entry point used by the CLI."""
    ScratchApp(file_path).run()
