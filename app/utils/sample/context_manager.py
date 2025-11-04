"""Context manager examples.

Demonstrates:
- class-based context manager (__enter__/__exit__)
- generator-based with contextlib.contextmanager
- contextlib.suppress, closing, and ExitStack
- simple async context manager example

Run: python -m app.utils.sample.context_manager
"""

from __future__ import annotations

import contextlib
import time
from contextlib import ExitStack, closing, contextmanager
from typing import Iterator


class Timer:
    """A simple class-based context manager that measures elapsed time."""

    def __init__(self, label: str = "Timer") -> None:
        self.label = label
        self.start: float | None = None

    def __enter__(self) -> "Timer":
        self.start = time.perf_counter()
        print(f"{self.label} started")
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        elapsed = time.perf_counter() - (self.start or 0.0)
        print(f"{self.label} ended: {elapsed:.6f}s")
        # don't suppress exceptions
        return False


@contextmanager
def open_read(path: str) -> Iterator[str]:
    """Generator-based context manager that opens a file and yields its content.

    (This example keeps things simple and reads the whole file.)
    """
    f = open(path, "r", encoding="utf-8")
    try:
        yield f.read()
    finally:
        f.close()


def suppress_example() -> None:
    # suppress FileNotFoundError when trying to remove a missing file
    with contextlib.suppress(FileNotFoundError):
        (open("no_such_file.txt", "r")).close()
    print("suppress_example completed (no exception propagated)")


def exitstack_and_closing_example() -> None:
    # ExitStack is useful to manage a dynamic set of context managers
    with ExitStack() as stack:
        temp_files = [stack.enter_context(open(f"tmp_{i}.txt", "w")) for i in range(2)]
        for i, f in enumerate(temp_files):
            f.write(f"file {i}\n")

    # Use closing for objects that only have close() method
    class Dummy:
        def close(self) -> None:
            print("Dummy closed")

    with closing(Dummy()):
        print("Using Dummy within closing")


async def async_context_demo() -> None:
    # minimal demonstration of an async context manager
    class AsyncFake:
        async def __aenter__(self):
            print("Async enter")
            return self

        async def __aexit__(self, exc_type, exc, tb):
            print("Async exit")

    async with AsyncFake():
        print("Inside async context")


def demo() -> None:
    print("-- Timer (class-based) --")
    with Timer("Sleep timer"):
        time.sleep(0.05)

    print("\n-- Generator-based context manager (open_read) --")
    # create a file to read
    p = "cm_demo.txt"
    with open(p, "w", encoding="utf-8") as f:
        f.write("demo\n")

    with open_read(p) as content:
        print("Content:", content.strip())

    # cleanup
    import os

    os.unlink(p)

    print("\n-- suppress, ExitStack & closing --")
    suppress_example()
    exitstack_and_closing_example()

    print("\n-- async context demo (run in event loop) --")
    import asyncio

    asyncio.run(async_context_demo())


if __name__ == "__main__":
    demo()
