"""Regex examples for Python's `re` module.

Run: python -m app.utils.sample.regex

Includes:
- basic match/search
- groups and named groups
- findall, finditer
- split and sub
- compiled patterns and flags
- lookahead/lookbehind and greedy vs non-greedy
"""

from __future__ import annotations

import re
from typing import Iterator, Match


def basic_examples() -> None:
    text = "The price is $123.45 for item-42. Contact: jane.doe@example.com"

    # simple search
    m = re.search(r"\$\d+\.\d{2}", text)
    print("Price match:", m.group(0) if m else None)

    # find all numbers
    nums = re.findall(r"\d+", text)
    print("All numbers:", nums)


def groups_examples() -> None:
    text = "Name: John Doe, Email: john.doe@example.org"

    # groups and named groups
    pattern = re.compile(r"Name:\s*(?P<name>[A-Za-z ]+),\s*Email:\s*(?P<email>\S+)")
    m = pattern.search(text)
    if m:
        print("Captured name:", m.group("name"))
        print("Captured email:", m.group("email"))


def finditer_example() -> None:
    text = "Words: cat, caterpillar, scatter, dog"
    pat = re.compile(r"cat")
    print("Matches (positions):")
    for mm in pat.finditer(text):
        print("-", mm.group(0), "at", mm.span())


def split_and_sub_examples() -> None:
    text = "one,two;three four\tfive"
    parts = re.split(r"[,;\s]+", text)
    print("Split parts:", parts)

    # substitution
    cleaned = re.sub(r"[^\w.@+-]", "-", "user+tag@example.com")
    print("Sanitized email-like:", cleaned)


def compile_and_flags() -> None:
    text = "First LINE\nsecond line\nTHIRD Line"
    # re.IGNORECASE and re.MULTILINE
    p = re.compile(r"^second line$", re.IGNORECASE | re.MULTILINE)
    print("Multiline ignorecase match?", bool(p.search(text)))


def advanced_examples() -> None:
    # greedy vs non-greedy
    s = "<tag>first</tag><tag>second</tag>"
    greedy = re.findall(r"<tag>.*</tag>", s)
    nongreedy = re.findall(r"<tag>.*?</tag>", s)
    print("Greedy:", greedy)
    print("Non-greedy:", nongreedy)

    # lookahead / lookbehind
    s2 = "foo1bar foo2bar"
    la = re.findall(r"foo(?=\d)", s2)  # foo followed by digit (not included)
    lb = re.findall(r"(?<=foo)\d", "foo7 bar foo8")
    print("Lookahead matches:", la)
    print("Lookbehind digit matches:", lb)


def email_validator(candidate: str) -> bool:
    """A conservative email validation using regex.

    Not 100% RFC-compliant, but good for everyday use.
    """
    pattern = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    return bool(pattern.match(candidate))


def demo() -> None:
    print("-- Basic Examples --")
    basic_examples()

    print("\n-- Groups --")
    groups_examples()

    print("\n-- Finditer --")
    finditer_example()

    print("\n-- Split / Sub --")
    split_and_sub_examples()

    print("\n-- Compile & Flags --")
    compile_and_flags()

    print("\n-- Advanced --")
    advanced_examples()

    print("\n-- Email validator --")
    for e in ("alice@example.com", "bad@com", "user+tag@sub.domain.org"):
        print(e, "->", email_validator(e))


if __name__ == "__main__":
    demo()
