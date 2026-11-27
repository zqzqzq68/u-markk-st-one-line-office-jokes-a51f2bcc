#!/usr/bin/env python3
"""One-Line Office Jokes — make.fun entry (program/v1).

Writes a single one-line joke about office life to
``<output_dir>/entry.txt`` (``MAKEFUN_OUTPUT_DIR`` or ``/output``).

The gate requires UTF-8 text of 1 to 199 characters, not only
whitespace, on a single line. The program is fully deterministic:
it always writes the same line, so two runs produce byte-identical
output.
"""

import os
import sys

# The joke. It turns on a real office detail (the broken printer and
# the IT ticket queue) and lands the laugh in the last few words.
JOKE = (
    "I asked IT to fix the printer and they sent me a ticket number, "
    "which is now the closest thing I have to a promotion."
)

OUTPUT_FILENAME = "entry.txt"
MAX_CHARS = 199


def output_dir() -> str:
    """Return the directory the entry must be written to."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def validate(text: str) -> None:
    """Check the joke against the gate rules; raise ValueError if bad."""
    if not text or not text.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def write_entry(text: str) -> str:
    """Write the joke to <output_dir>/entry.txt, return the path."""
    validate(text)
    directory = output_dir()
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    return path


def verify_entry(path: str, expected: str) -> None:
    """Read the written file back and confirm it matches exactly.

    Guards against a partial write or an encoding surprise: the file
    on disk must be byte-for-byte the joke, and it must still pass
    the gate rules when read back.
    """
    with open(path, "r", encoding="utf-8", newline="") as handle:
        on_disk = handle.read()
    if on_disk != expected:
        raise ValueError(
            f"read-back mismatch: file holds {len(on_disk)} characters, "
            f"expected {len(expected)}"
        )
    validate(on_disk)


def main() -> int:
    path = write_entry(JOKE)
    verify_entry(path, JOKE)
    print(f"wrote {len(JOKE)} characters to {path} (read-back verified)")
    print(JOKE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
