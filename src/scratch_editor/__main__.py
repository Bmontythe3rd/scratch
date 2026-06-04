"""CLI entry point: scratch [file]"""

from __future__ import annotations

import argparse

from .app import run


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="scratch",
        description="A dead-simple terminal text editor.",
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="File to open (creates on save if it doesn't exist).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )
    args = parser.parse_args()
    run(args.file)


if __name__ == "__main__":
    main()
