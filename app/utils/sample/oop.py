"""OOP samples: classes, inheritance, composition, polymorphism.

Run as a script: python -m app.utils.sample.oop

Sections:
- Basic class and instance
- Inheritance and method overriding
- Abstract base class (interface)
- Composition (has-a relationship)
- Polymorphism: different classes implementing same API
- Operator overloading and dunder methods
- Dataclass example for immutable/simple models
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


class Animal:
    """A simple base class representing an animal."""

    def __init__(self, name: str, age: int = 0) -> None:
        self.name = name
        self.age = age

    def speak(self) -> str:
        """Default speak implementation (can be overridden)."""
        return "..."

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, age={self.age})"


class Dog(Animal):
    def speak(self) -> str:
        return "woof"


class Cat(Animal):
    def speak(self) -> str:
        return "meow"


class Vehicle(ABC):
    """Abstract base class to show interface/contract via ABC."""

    @abstractmethod
    def move(self) -> str:
        pass


class Car(Vehicle):
    def __init__(self, model: str) -> None:
        self.model = model

    def move(self) -> str:
        return f"Car({self.model}) driving"


class Engine:
    """Component for composition example."""

    def __init__(self, horsepower: int) -> None:
        self.horsepower = horsepower

    def start(self) -> str:
        return f"Engine with {self.horsepower} HP started"


class Bike(Vehicle):
    def __init__(self, engine: Engine) -> None:
        # composition: Bike has an Engine
        self.engine = engine

    def move(self) -> str:
        return self.engine.start() + " -> Bike rolling"


# Polymorphism: different objects implementing same API (speak/move)
def animal_sounds(animals: List[Animal]) -> None:
    for a in animals:
        print(f"{a.name} says {a.speak()}")


# Operator overloading example: 2D vector
class Vec2:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> "Vec2":
        return Vec2(self.x * scalar, self.y * scalar)

    def __repr__(self) -> str:
        return f"Vec2({self.x}, {self.y})"


@dataclass
class User:
    username: str
    email: str


def demo() -> None:
    print("-- Basic classes & inheritance --")
    d = Dog("Buddy", age=4)
    c = Cat("Mittens", age=2)
    print(d, "->", d.speak())
    print(c, "->", c.speak())

    print("\n-- Polymorphism (animals) --")
    animal_sounds([d, c])

    print("\n-- Abstract base class & composition --")
    car = Car("sedan")
    engine = Engine(15)
    bike = Bike(engine)
    print(car.move())
    print(bike.move())

    print("\n-- Operator overloading --")
    a = Vec2(1, 2)
    b = Vec2(3, 4)
    print("a + b =", a + b)
    print("a * 3 =", a * 3)

    print("\n-- Dataclass --")
    user = User("alice", "alice@example.com")
    print(user)


if __name__ == "__main__":
    demo()
