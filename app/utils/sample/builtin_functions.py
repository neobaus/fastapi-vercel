"""Demonstrate common Python built-in functions with examples.

Run: python -m app.utils.sample.builtin_functions
"""

from __future__ import annotations

from functools import reduce
from typing import Any


def conversions() -> None:
    print("int('42') ->", int("42"))
    print("float('3.14') ->", float("3.14"))
    print("str(123) ->", str(123))
    print("bool(0) ->", bool(0), "bool(1) ->", bool(1))


def sequence_helpers() -> None:
    data = [3, 1, 4, 1, 5]
    print("len(data)", len(data))
    print("sum(data)", sum(data))
    print("min/max", min(data), max(data))
    print("sorted desc", sorted(data, reverse=True))
    print("enumerate", list(enumerate(data)))
    print("zip", list(zip(["a", "b", "c"], data)))


def functional_builtins() -> None:
    items = [1, 2, 3, 4]
    print("map x*2 ->", list(map(lambda x: x * 2, items)))
    print("filter even ->", list(filter(lambda x: x % 2 == 0, items)))
    print("reduce sum ->", reduce(lambda a, b: a + b, items))
    print("any(x>3)", any(x > 3 for x in items))
    print("all(x<10)", all(x < 10 for x in items))


def attributes_and_callables() -> None:
    class C:
        def __init__(self) -> None:
            self.x = 1

        def inc(self) -> None:
            self.x += 1

    c = C()
    print("hasattr(c, 'x') ->", hasattr(c, "x"))
    print("getattr(c,'x') ->", getattr(c, "x"))
    setattr(c, "y", 99)
    print("vars(c) ->", vars(c))
    print("callable(c.inc) ->", callable(c.inc))
    c.inc()
    print("after inc, x ->", c.x)


def iterators_and_next() -> None:
    it = iter([10, 20, 30])
    print("next(it) ->", next(it))
    print("list(iter(range(3))) ->", list(iter(range(3))))


def introspection_helpers() -> None:
    print("dir(list) sample (first 5):", dir(list)[:5])
    d = {"a": 1}
    print("globals contains 'd'?", "d" in globals())
    print("vars(d) ->", vars(d))


def eval_exec_example() -> None:
    # Use eval for expressions only and avoid untrusted input
    expr = "1 + 2 * 3"
    print("eval(expr) ->", eval(expr))
    # Exec example builds a dict of local variables
    loc: dict[str, Any] = {}
    exec("x = 5\ny = x * 2", {}, loc)
    print("exec created ->", loc)


def demo() -> None:
    print("-- Conversions --")
    conversions()

    print("\n-- Sequence helpers --")
    sequence_helpers()

    print("\n-- Functional builtins --")
    functional_builtins()

    print("\n-- Attributes & callables --")
    attributes_and_callables()

    print("\n-- Iterators & next --")
    iterators_and_next()

    print("\n-- Introspection --")
    introspection_helpers()

    print("\n-- Eval / Exec --")
    eval_exec_example()


if __name__ == "__main__":
    demo()
