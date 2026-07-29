"""
Python Classes & Inheritance Masterclass
A complete, self-contained cheat sheet covering everything from core OOP
basics to advanced dataclasses, ABCs, properties, and
metaprogramming hooks.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

# Python has two common shapes for grouping data and behavior together.
# For typed data, reach for a dataclass first. For classes with more substantial
# logic or full control over construction, write a regular class.

# =====================================================================
# SECTION 1: Standard Classes, Methods, Properties, & Dunders
# =====================================================================


# When a class needs more substantial logic in __init__, multiple constructors,
# or behavior that doesn't fit a "bag of fields" shape, write a regular class.


class Project:
    """Demonstrates class attributes, instance attributes, classmethods,
    staticmethods, properties, and custom dunder methods.
    """

    # Class attribute (shared across all instances)
    default_separator = "-"

    def __init__(self, name: str, budget: float):
        # Instance attributes (unique per instance)
        self.name = name
        self._budget = (
            budget  # Protected attribute intended for property access
        )

    # 1. Properties (Managed Attributes with Getters & Setters)
    # Use @property to create a getter
    @property
    def budget(self) -> float:
        """Getter for budget."""
        return self._budget

    # Use @budget.setter to create a setter
    @budget.setter
    def budget(self, amount: float):
        """Setter with validation."""
        if amount < 0:
            raise ValueError("Budget cannot be negative!")
        self._budget = amount

    # Use @budget.deleter to create a deleter,
    # which can be used to delete the attribute
    @budget.deleter
    def budget(self):
        """Optional deleter for budget."""
        print(f"Deleting budget for project '{self.name}'")
        del self._budget

    # 2. Class Method (Acts on the class itself, often used as alternate
    # constructors). Python only allows one __init__ method per class.
    # If you want to allow users to create objects from different data
    # formats, use @classmethod. Also useful for factory methods or
    # when you need to access/modify class-level data.
    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Project instance from a dictionary."""
        return cls(name=data["name"], budget=data["budget"])

    # 3. Static Method (Utility function in class namespace; receives no
    # self/cls)
    @staticmethod
    def is_valid_name(name: str) -> bool:
        """Validates if a project name contains no illegal characters."""
        return len(name.strip()) > 0 and "$" not in name

    # 4. Custom Dunder (Magic) Methods
    def __repr__(self) -> str:
        """Developer-friendly string representation."""
        return f"Project(name={self.name!r}, budget={self._budget})"

    def __eq__(self, other: object) -> bool:
        """Custom equality check between two Project instances."""
        if not isinstance(other, Project):
            return False
        return self.name == other.name and self._budget == other._budget


# =====================================================================
# SECTION 2: Dataclasses (Mutable, Frozen, Defaults, & Validation)
# =====================================================================


# Dataclasses are a way to define classes that are primarily used to store data.
# They automatically generate special methods like __init__(), __repr__(), and
# __eq__() based on the class attributes.
# Key Things to Know
# 1. Type Annotations are Required: Dataclasses use type hints
# (e.g., username: str) to identify which variables are intended to be fields.
# 2. Default Values: You can set default values directly (age: int = 0).
# Fields with defaults must come after fields without defaults.
# 3. It's Still a Regular Class: You can still add standard methods, properties,
#  and inheritance to a dataclass just like any normal Python class.
@dataclass
class Person:
    """Standard Dataclass with default values and __post_init__ validation."""

    name: str
    age: int
    email: str
    phone: str = "N/A"

    # The __post_init__ method is useful for any additional initialization or
    # validation.
    def __post_init__(self):
        """Runs automatically after __init__ to perform validation."""
        if self.age < 0:
            raise ValueError("Age cannot be negative")
        if "@" not in self.email:
            raise ValueError("Invalid email address")

    # A dataclass can also have methods, just like a regular class.
    def greet(self) -> str:
        return f"Hello, my name is {self.name} and I am {self.age} years old."


# For typed data with light behavior, dataclasses are the modern default.
# Pydantic and SQLModel extend the same pattern with runtime validation and
# database mapping.


@dataclass(frozen=True)
class Config:
    """Immutable Dataclass (frozen=True). Attributes cannot be changed
    after creation.
    """

    environment: str
    debug: bool = False


@dataclass
class Team:
    """Dataclass demonstrating field(default_factory=...) for mutable
    defaults.
    """

    team_name: str
    # NEVER use members: list = []! Mutable default arguments share state
    # globally.
    members: list[str] = field(default_factory=list)


# =====================================================================
# SECTION 3: ABCs, Inheritance, Name Mangling, & super()
# =====================================================================


# Inherit from ABC to mark the class as abstract
class Employee(ABC):
    """Abstract Base Class (ABC) representing a general employee.
    Cannot be instantiated directly because of @abstractmethod.
    """

    def __init__(self, name: str, salary: float):
        self.name = name
        self._department = "General"  # Protected (convention)
        self.__salary = salary  # Private (Triggers Name Mangling)

    @abstractmethod
    def calculate_bonus(self) -> float:
        """Subclasses MUST implement this method."""
        pass

    def get_salary(self) -> float:
        """Public getter for the private __salary attribute."""
        return self.__salary


class Developer(Employee):
    """Child class inheriting from Employee (Single Inheritance)."""

    def __init__(self, name: str, salary: float, programming_language: str):
        # super() invokes initialization logic from the parent class
        super().__init__(name, salary)
        self.programming_language = programming_language
        self._department = "Engineering"

    def calculate_bonus(self) -> float:
        # Implementation required by Employee (ABC)
        return self.get_salary() * 0.10


# =====================================================================
# SECTION 4: Multiple Inheritance, MRO, & Subclass Hooks
# =====================================================================


class PluginSystem:
    """Parent class using __init_subclass__ to auto-register child classes."""

    registry: list[type] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.registry.append(cls)


class Printable:
    """Mix-in class providing printing behavior."""

    def render(self) -> str:
        return "Rendering printable format..."


@dataclass
class ReportHeader:
    """Dataclass parent providing structured data."""

    title: str
    author: str


@dataclass
class PDFReport(ReportHeader, Printable, PluginSystem):
    """Child class using Multiple Inheritance + Dataclass Inheritance.

    Inherits:
      - Fields from ReportHeader (title, author)
      - Methods from Printable (render)
      - Auto-registration from PluginSystem (__init_subclass__)
    """

    pages: int = 1


# =====================================================================
# Section 5: Dataclass Inheritance
# =====================================================================
@dataclass
class Parent:
    parent_a: str
    parent_b: str = "default_b"


# Python automatically generates __init__(self, parent_a, parent_b, child_x)
@dataclass
class Child(Parent):
    # As parent_b has a default value, child_x must come after it in the
    # parameter list. Hence, it has to have a default value or be placed after \
    # all non-default parameters.
    # Following will raise a Error
    # child_x: int
    # Only option is to provide a default value for child_x
    child_x: int = 0


# =====================================================================
# DEMONSTRATION & RUNTIME EXECUTIONS
# =====================================================================

if __name__ == "__main__":
    print("--- 1. Properties, Methods, & Dunders ---")
    proj1 = Project("Alpha", 10000.0)
    print(repr(proj1))  # Project(name='Alpha', budget=10000.0)

    # Using @property getter and setter
    proj1.budget = 12000.0
    print(f"Updated Budget: ${proj1.budget:,.2f}")

    # Using @property deleter
    del proj1.budget  # Triggers deleter logic

    # Using @classmethod constructor
    proj2 = Project.from_dict({"name": "Beta", "budget": 5000.0})
    print(f"Created from dict: {proj2}")

    # Using @staticmethod
    print(
        f"Is 'Valid$Name' valid? {Project.is_valid_name('Valid$Name')}"
    )  # False

    print("\n--- 2. Dataclasses: Advanced Options ---")
    person = Person(name="Alice", age=30, email="alice@example.com")
    print(person.greet())

    # Frozen Dataclass
    cfg = Config(environment="production")
    # This will use the auto-generated __repr__ method
    print(f"Immutable Config: {cfg}")
    # cfg.debug = True  <-- Raises FrozenInstanceError if uncommented!

    # Mutable Field Factory
    team = Team(team_name="DevOps")
    team.members.append("Alice")
    print(f"Team Members: {team.members}")

    print("\n--- 3. ABCs, super(), & Name Mangling ---")
    dev = Developer("Bob", 95000.0, "Python")

    # Inherited & overridden properties
    print(f"Developer Name: {dev.name}")
    print(f"Department:     {dev._department}")
    print(f"Language:       {dev.programming_language}")

    # Abstract method implementation
    print(f"Bonus: ${dev.calculate_bonus():,.2f}")

    # Accessing mangled attribute directly
    # dev.__salary  <-- Raises AttributeError
    print(f"Mangled Private Salary Access: ${dev._Employee__salary:,.2f}")

    # Built-in type checks
    print(f"isinstance(dev, Employee)? {isinstance(dev, Employee)}")  # True

    print(
        f"issubclass(Developer, object)? {issubclass(Developer, object)}"
    )  # True

    print("\n--- 4. Multiple Inheritance & MRO ---")
    report = PDFReport(title="Q3 Financials", author="Charlie", pages=15)
    print(report)
    # Method inherited from mixin
    print(report.render())

    print("\nMethod Resolution Order (MRO):")
    for i, cls in enumerate(PDFReport.mro(), start=1):
        print(f"  {i}. {cls.__name__}")

    print(
        f"\nRegistered Plugin Classes: "
        f"{[cls.__name__ for cls in PluginSystem.registry]}"
    )

    print("\n--- 5. Dataclass Inheritance ---")
    child_instance = Child(parent_a="Value A", child_x=42)
    print(f"Child Instance: {child_instance}")
