"""File I/O examples: text/binary, pathlib, tempfile, CSV/JSON.

Run: python -m app.utils.sample.files

This module is intentionally educational: small, explicit examples you can
run and modify. It avoids writing to important system locations — writes go
into a temporary directory or the repository working directory.
"""

from __future__ import annotations

import csv
import json
import os
import tempfile
from pathlib import Path
from typing import List


BASE = Path(".")


def text_file_example() -> None:
    p = BASE / "sample_text.txt"
    # write text
    with p.open("w", encoding="utf-8") as f:
        f.write("Line 1\nLine 2\n")

    # read text
    with p.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            print(f"{i}: {line.rstrip()}")

    # cleanup
    try:
        p.unlink()
    except FileNotFoundError:
        pass


def binary_file_example() -> None:
    p = BASE / "sample_bytes.bin"
    data = bytes(range(16))
    with p.open("wb") as f:
        f.write(data)

    with p.open("rb") as f:
        read = f.read()
        print("Read bytes length:", len(read))

    p.unlink(missing_ok=True)


def pathlib_examples() -> None:
    p = Path(".")
    print("CWD:", p.resolve())
    # create nested dir
    d = Path("tmp_dir_example")
    d.mkdir(exist_ok=True)
    (d / "x.txt").write_text("x")
    print("Created:", list(d.iterdir()))
    # cleanup
    for f in d.iterdir():
        f.unlink()
    d.rmdir()


def tempfile_example() -> None:
    # temporary file (auto-cleaned when closed)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir) / "t.txt"
        tmp.write_text("hello")
        print("Temp file path:", tmp)
        print("Temp content:", tmp.read_text())


def csv_json_examples() -> None:
    csv_path = BASE / "sample.csv"
    rows = [["name", "age"], ["alice", "30"], ["bob", "25"]]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    # read CSV into list of dicts
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)
        print("CSV rows:", data)

    json_path = BASE / "sample.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump({"users": data}, f, indent=2)

    print("JSON written:", json_path.read_text())

    # cleanup
    csv_path.unlink(missing_ok=True)
    json_path.unlink(missing_ok=True)


def safe_open_read(path: Path) -> str:
    """Open a file for reading, return empty string if missing.

    Demonstrates defensive file handling.
    """
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def demo() -> None:
    print("-- Text file example --")
    text_file_example()

    print("\n-- Binary file example --")
    binary_file_example()

    print("\n-- Pathlib example --")
    pathlib_examples()

    print("\n-- Tempfile example --")
    tempfile_example()

    print("\n-- CSV & JSON example --")
    csv_json_examples()


if __name__ == "__main__":
    demo()
