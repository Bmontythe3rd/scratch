"""Tests for pure logic that doesn't require a running terminal.

The extension->language mapping is the easiest piece to test in isolation.
TUI behavior (save/quit flows) is better covered with Textual's Pilot harness
once the dependency is installed locally — see docs/ARCHITECTURE.md.
"""

from pathlib import Path

import pytest

# Import only the pure function so these tests don't require Textual.
from scratch_editor.app import language_for


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("main.py", "python"),
        ("script.JS", "javascript"),     # case-insensitive
        ("data.json", "json"),
        ("notes.md", "markdown"),
        ("config.toml", "toml"),
        ("style.css", "css"),
        ("unknown.xyz", None),           # unknown extension -> plain text
        ("noextension", None),
    ],
)
def test_language_for_extensions(filename, expected):
    assert language_for(Path(filename)) == expected


def test_language_for_none():
    assert language_for(None) is None
