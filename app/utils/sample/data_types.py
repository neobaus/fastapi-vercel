"""Sample: Python data types and examples

This module provides short examples and explanations for common Python
data types. It's intended as a lightweight learning/demo file you can run
directly (python -m app.utils.sample.data_types) or import from your code.

Contents covered (non-exhaustive):
- primitives: int, float, bool, complex, None
- text & binary: str, bytes, bytearray
- sequences: list, tuple, range
- sets and dicts
- functions, lambdas, generators, iterators
- typing examples, dataclasses, enums

Keep this file small and easy to read. Each section includes a short
example and a comment explaining the behavior being demonstrated.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Generator, Iterable, List, Optional, Tuple
from collections import namedtuple


def describe(obj: Any) -> str:
    """Return a one-line description of the object's type and repr."""
    return f"{type(obj).__name__}: {repr(obj)}"


# --- Primitives -------------------------------------------------------------


def primitive_examples() -> None:
    i: int = 42
    large_int = 10**30  # Python ints are arbitrary precision

    f: float = 3.14159
    c: complex = 1 + 2j

    b_true: bool = True
    n = None

    print("-- Primitives --")
    print(describe(i), "+ large =>", describe(large_int))
    print(describe(f), "(float) precision example")
    print(describe(c), "(complex number)")
    print(describe(b_true), "None is ->", describe(n))


# --- Text and binary -------------------------------------------------------


def text_and_binary_examples() -> None:
    s: str = "hello, world"
    # f-strings, slicing, immutability
    s2 = f"{s.title()}!"  # "Hello, World!"

    b: bytes = b"abc\x00\x01"
    ba: bytearray = bytearray(b)
    ba.append(0xFF)

    print("\n-- Text & Binary --")
    print("str:", s, "-> modified copy:", s2)
    print("bytes:", b, "bytearray (mutated):", bytes(ba))


# --- Sequences: list, tuple, range ----------------------------------------


def sequence_examples() -> None:
    lst: List[int] = [1, 2, 3]
    lst.append(4)
    tup: Tuple[int, ...] = (1, 2, 3)
    rng = range(5)

    # mutability
    tup2 = tup + (4,)  # creates a new tuple

    print("\n-- Sequences --")
    print("list (mutable):", lst)
    print("tuple (immutable):", tup, "-> new tuple", tup2)
    print("range (lazy sequence):", list(rng))


# --- Sets and dicts --------------------------------------------------------


def sets_and_dicts_examples() -> None:
    s = {1, 2, 3, 2}  # duplicates removed
    d: Dict[str, int] = {"a": 1, "b": 2}
    d2 = {k: v * 2 for k, v in d.items()}  # dict comprehension

    print("\n-- Sets & Dicts --")
    print("set unique values:", s)
    print("dict:", d)
    print("dict comprehension:", d2)


# --- Equality vs identity --------------------------------------------------


def identity_vs_equality() -> None:
    a = [1, 2, 3]
    b = a
    c = a.copy()

    print("\n-- Equality vs Identity --")
    print("a == b ->", a == b, "; a is b ->", a is b)
    print("a == c ->", a == c, "; a is c ->", a is c)


# --- Functions, lambdas, map/filter, iterators -----------------------------


def functional_examples() -> None:
    squares = list(map(lambda x: x * x, range(5)))
    evens = list(filter(lambda x: x % 2 == 0, range(10)))

    # generator: lazy values, lower memory usage
    def gen(n: int) -> Generator[int, None, None]:
        for i in range(n):
            yield i * i

    print("\n-- Functional & Generators --")
    print("squares:", squares)
    print("evens:", evens)
    print("generator (first 5):", list(gen(5)))


# --- Data classes, namedtuple, enum ----------------------------------------


@dataclass
class Person:
    name: str
    age: int


Point = namedtuple("Point", ["x", "y"])  # lightweight immutable record


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


def advanced_examples() -> None:
    p = Person("Alice", 30)
    pt = Point(1.0, 2.0)
    c = Color.RED

    print("\n-- Data class / namedtuple / enum --")
    print("Person:", p)
    print("Point:", pt)
    print("Color:", c, c.value)


# --- Typing examples -------------------------------------------------------


def typing_examples(values: Optional[List[int]] = None) -> None:
    values = values or [1, 2, 3]

    def accept_iterable(it: Iterable[int]) -> int:
        return sum(it)

    total = accept_iterable(values)
    maybe: Optional[int] = total if total > 0 else None

    print("\n-- Typing examples --")
    print("values:", values, "sum:", total, "maybe:", maybe)


# --- Small utilities / contract --------------------------------------------


def first_even(nums: Iterable[int]) -> Optional[int]:
    """Return the first even number or None.

    Contract:
    - Input: any iterable of ints
    - Output: Optional[int] (first even) or None if none found
    - Error modes: raises if items aren't ints
    """
    for n in nums:
        if n % 2 == 0:
            return n
    return None


def run_demo() -> None:
    """Run quick demo printing example results. Useful for manual testing."""
    primitive_examples()
    text_and_binary_examples()
    sequence_examples()
    sets_and_dicts_examples()
    identity_vs_equality()
    functional_examples()
    advanced_examples()
    typing_examples()

    # small contract test
    print("\n-- Utilities --")
    print("first_even([1,3,5,6,7]) ->", first_even([1, 3, 5, 6, 7]))
    print("first_even([]) ->", first_even([]))


if __name__ == "__main__":
    run_demo()
