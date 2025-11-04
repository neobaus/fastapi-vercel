"""Decorator examples: function decorators, parametric, class decorators.

Run as a module: python -m app.utils.sample.decorators
"""

from __future__ import annotations

import functools
import time
from typing import Callable, Any


def simple_logging(func: Callable) -> Callable:
    """A simple decorator that logs before/after a call."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling {func.__name__} with args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result

    return wrapper


def timed(func: Callable) -> Callable:
    """Measure execution time of a function."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        t0 = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            dt = time.perf_counter() - t0
            print(f"{func.__name__} took {dt:.6f}s")

    return wrapper


def retry(times: int = 3, delay: float = 0.1) -> Callable:
    """A parametric decorator that retries a function on exception."""

    def deco(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exc = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:  # pylint: disable=broad-except
                    last_exc = e
                    print(f"Attempt {attempt}/{times} failed: {e}")
                    time.sleep(delay)
            # re-raise the last exception
            raise last_exc

        return wrapper

    return deco


def simple_decorator_demo() -> None:
    @simple_logging
    def add(a: int, b: int) -> int:
        return a + b

    print(add(2, 3))


def timed_and_retry_demo() -> None:
    import random

    @timed
    @retry(times=4, delay=0.05)
    def flaky(n: int) -> int:
        """Randomly fails to demonstrate retry."""
        if random.random() < 0.6:
            raise RuntimeError("flaky failure")
        return n * 2

    try:
        print("flaky ->", flaky(5))
    except Exception as e:
        print("Final failure after retries:", e)


# Class decorator example: add a method
def add_repr(cls: type) -> type:
    """Class decorator that adds a __repr__ if missing."""

    if "__repr__" not in cls.__dict__:

        def __repr__(self) -> str:  # type: ignore[override]
            props = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
            return f"{cls.__name__}({props})"

        cls.__repr__ = __repr__  # type: ignore[arg-type]
    return cls


@add_repr
class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


def demo() -> None:
    print("-- Simple logging decorator --")
    simple_decorator_demo()

    print("\n-- Timed + Retry decorator --")
    timed_and_retry_demo()

    print("\n-- Class decorator example --")
    p = Point(1, 2)
    print(p)


if __name__ == "__main__":
    demo()
