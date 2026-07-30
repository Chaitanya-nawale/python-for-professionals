"""
Python Classes & Inheritance Masterclass
A complete, self-contained cheat sheet covering everything from core OOP
basics to advanced dataclasses, ABCs, properties, and
metaprogramming hooks.
"""

import functools
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
# SECTION 6: The "Deep Magic" (__slots__, __new__, __call__, & Descriptors)
# =====================================================================


# 1. __slots__: Memory Optimization
# In normal Python classes, each instance has a __dict__ that stores its
# attributes. Using __slots__ allows you to explicitly declare data members
# (like x and y). It disables the internal __dict__ to save massive amounts of
# RAM when creating millions of instances. Attributes are strictly locked to the
# slots defined. You cannot add new attributes to instances of a class that uses
# __slots__ unless you explicitly define them in the slots
class Point:
    __slots__ = ["x", "y"]

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


# 2. __new__: Object Allocation (The Singleton Pattern)
# __new__ is called BEFORE __init__. It actually creates and returns the memory
# instance. It's the only way to implement a true Singleton in Python.
class DatabaseConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Allocate memory only if an instance doesn't exist yet
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Note: __init__ runs every time you call DatabaseConnection(),
        # so in a real Singleton, you'd add a flag to ensure one-time setup.
        self.connected = True


# 3. __call__: Callable Instances
# Allows an instance of a class to be called like a regular function.
class Multiplier:
    def __init__(self, factor: float):
        self.factor = factor

    def __call__(self, value: float) -> float:
        return value * self.factor


# 4. Descriptors: Reusable Property Logic
# The protocol (__get__, __set__, __delete__) that powers @property under the
# hood. Useful when you want to reuse the exact same getter/setter logic across
# many classes.
class PositiveNumber:
    def __set_name__(self, owner, name):
        self.name = name  # Captures the variable name (e.g., 'price')

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError(f"{self.name} must be greater than zero")
        instance.__dict__[self.name] = value


class Product:
    price = PositiveNumber()  # Using the descriptor instead of @property
    weight = PositiveNumber()  # Reusing the exact same validation logic!

    def __init__(self, price: float, weight: float):
        self.price = price
        self.weight = weight


# 5. Metaclasses: Modifying Class Creation
# A metaclass intercepts the creation of the CLASS ITSELF (not the instance).
class UppercaseMeta(type):
    def __new__(mcs, name, bases, namespace):
        # mcs: The metaclass itself (like 'type')
        # name: The name of the class being created
        # bases: Tuple of base classes
        # namespace: Dictionary of class attributes and methods
        # Convert all class attributes that aren't dunder methods to UPPERCASE
        uppercase_attr = {}
        for key, val in namespace.items():
            if not key.startswith("__"):
                uppercase_attr[key.upper()] = val
            else:
                uppercase_attr[key] = val

        return super().__new__(mcs, name, bases, uppercase_attr)


# This class uses the metaclass above to intercept its creation
class Constants(metaclass=UppercaseMeta):
    pi = 3.14159
    gravity = 9.81


# =====================================================================
# SECTION 7: Container & Iterator Protocols
# =====================================================================


class CustomList:
    """Demonstrates how to make an object behave like a built-in Python list."""

    def __init__(self, *args):
        self._items = list(args)

    def __len__(self) -> int:
        """Allows the use of len(obj)."""
        return len(self._items)

    def __getitem__(self, index):
        """Allows indexing and slicing: obj[0] or obj[1:3]."""
        return self._items[index]

    def __setitem__(self, index, value):
        """Allows index assignment: obj[0] = 'new value'."""
        self._items[index] = value

    def __iter__(self):
        """Allows the object to be used in a for-loop."""
        return iter(self._items)


# =====================================================================
# SECTION 8: Operator Overloading & Hashing
# =====================================================================


class Vector:
    """Demonstrates mathematical operator overloading and hashing."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        """Allows vector1 + vector2 using the '+' operator"""
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        """Allows vector1 == vector2"""
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """
        By default, mutable objects shouldn't be hashed.
        If you define __eq__, Python sets __hash__ to None.
        To use this object as a dictionary key or in a set, we must define this.
        """
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


# =====================================================================
# SECTION 9: @cached_property
# =====================================================================


class DataProcessor:
    """Demonstrates lazy evaluation using cached_property."""

    def __init__(self, data: list):
        self.data = data

    @functools.cached_property
    def expensive_analysis(self) -> float:
        """
        This method will only execute ONCE per instance.
        Subsequent calls will instantly return the saved attribute, saving CPU.
        """
        print("Performing highly expensive computation...")
        # Simulate heavy lifting
        return sum(self.data) / len(self.data) if self.data else 0


# =====================================================================
# SECTION 10: Dynamic Attributes (__getattr__ & __getattribute__)
# =====================================================================


class DynamicProxy:
    """Demonstrates intercepting attribute access dynamically."""

    def __init__(self):
        self.real_attribute = "I exist!"

    def __getattr__(self, name: str):
        """
        Triggered ONLY if an attribute is NOT found via normal lookup.
        Great for building flexible APIs or proxy objects.
        """
        return f"You asked for '{name}', but I generated this on the fly!"

    def __getattribute__(self, name: str):
        """
        Triggered for EVERY attribute access, even if it exists.
        WARNING: You must use super().__getattribute__ here, or you will
        cause an infinite recursion crash!
        """
        # We can intercept or log access to real attributes here
        if name == "real_attribute":
            print("[LOG] Someone accessed 'real_attribute'")
        return super().__getattribute__(name)


# =====================================================================
# SECTION 11: Class Decorators
# =====================================================================


def add_timestamp(cls):
    """
    A class decorator. It takes a class, modifies it, and returns it.
    This is often simpler than using a Metaclass for light modifications.
    """
    import time

    # Dynamically inject a new attribute into the class
    cls.created_at = time.time()
    return cls


@add_timestamp
class EventLog:
    def __init__(self, message: str):
        self.message = message


# =====================================================================
# SECTION 12: Formatting, Truthiness, & Pattern Matching
# =====================================================================


class Temperature:
    # __match_args__ tells Python 3.10+ pattern matching which positional
    # arguments correspond to which attributes in a match/case statement.
    __match_args__ = ("celsius",)

    def __init__(self, celsius: float):
        self.celsius = celsius

    def __bool__(self) -> bool:
        """
        Dictates how the object evaluates in an 'if' statement.
        Let's say a Temperature is only 'True' if it's above absolute zero.
        """
        return self.celsius > -273.15

    def __format__(self, format_spec: str) -> str:
        """
        Allows custom f-string formatting behavior.
        """
        if format_spec == "f":
            fahrenheit = (self.celsius * 9 / 5) + 32
            return f"{fahrenheit:.1f}°F"
        elif format_spec == "c":
            return f"{self.celsius:.1f}°C"
        return str(self.celsius)


# =====================================================================
# SECTION 13: Destructors / Finalizers (__del__)
# =====================================================================


class TemporaryResource:
    """
    Demonstrates object destruction.
    WARNING: In Python, you cannot guarantee EXACTLY when __del__ will run
    because of the Garbage Collector. For critical cleanup (like closing files),
    always use Context Managers (__enter__/__exit__) instead.
    """

    def __init__(self, name: str):
        self.name = name
        print(f"[Resource] {self.name} created.")

    def __del__(self):
        """Runs when the object's reference count drops to zero."""
        print(f"[Resource] {self.name} is being destroyed and memory freed.")


# =====================================================================
# SECTION 14: Generics and Type Hinting (__class_getitem__)
# =====================================================================


class CustomBox:
    """
    Allows your custom class to be used with type hinting brackets,
    just like list[int] or dict[str, int].
    """

    def __init__(self, item):
        self.item = item

    @classmethod
    def __class_getitem__(cls, item_type):
        """
        This doesn't change runtime behavior; it just makes your class
        compatible with Python's typing system for IDEs and type checkers.
        """
        return f"{cls.__name__}[{item_type.__name__}]"


# =====================================================================
# SECTION 15: Customizing Autocomplete (__dir__)
# =====================================================================


class SecretAgent:
    """Demonstrates hiding attributes from standard introspection."""

    def __init__(self):
        self.public_name = "John Doe"
        self.clearance_level = "Level 1"
        self._secret_identity = "Agent 007"
        self._mission = "Classified"

    def __dir__(self):
        """
        Dictates what is returned when someone calls dir(obj).
        This controls what appears in IDE autocomplete dropdowns!
        We can use this to hide our internal '_' attributes entirely.
        """
        return ["public_name", "clearance_level"]


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
    print(f"Mangled Private Salary Access: ${dev._Employee__salary:,.2f}")  # type: ignore

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

    print("\n--- 6. The Deep Magic ---")
    # Testing __slots__
    p = Point(10, 20)
    print(f"Point coordinates: ({p.x}, {p.y})")
    # p.z = 30  <-- Would raise AttributeError

    # Testing __new__ (Singleton)
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"Are db1 and db2 the exact same object? {db1 is db2}")  # True

    # Testing __call__
    double = Multiplier(2.0)
    print(f"Calling instance as function (double 5): {double(5.0)}")  # 10.0

    # Testing Descriptors
    prod = Product(price=19.99, weight=2.5)
    print(f"Product price: ${prod.price}")
    # prod.weight = -5  <-- Would raise ValueError: weight must be > 0

    # Testing Metaclasses
    # Even though we defined 'pi' in lowercase, the metaclass transformed it!
    print(f"Metaclass transformed 'pi' to 'PI': {Constants.PI}")  # type: ignore

    print("\n--- 7. Container Protocols ---")
    my_list = CustomList("Apple", "Banana", "Cherry")
    print(f"Length: {len(my_list)}")
    print(f"Index 1: {my_list[1]}")
    for item in my_list:
        print(f"Iterating: {item}")

    print("\n--- 8. Operator Overloading & Hashing ---")
    v1 = Vector(2, 3)
    v2 = Vector(4, 1)
    v3 = v1 + v2
    print(f"Vector Addition: {v1} + {v2} = {v3}")

    # Because we implemented __hash__ and __eq__, we can put Vectors in a set!
    unique_vectors = {v1, v2, v1}
    print(f"Set of vectors (notice duplicates removed): {unique_vectors}")

    print("\n--- 9. Cached Property ---")
    processor = DataProcessor([10, 20, 30, 40, 50])
    print(f"Call 1: {processor.expensive_analysis}")
    print(
        f"Call 2: {processor.expensive_analysis}"
    )  # Notice it doesn't print the computation message again!

    print("\n--- 10. Dynamic Attributes ---")
    proxy = DynamicProxy()
    print(proxy.real_attribute)  # Triggers __getattribute__, then finds it
    print(proxy.fake_attribute)  # Fails to find it, falls back to __getattr__

    print("\n--- 11. Class Decorators ---")
    log = EventLog("System started")
    print(f"Event created at timestamp: {log.created_at}")  # type: ignore

    print("\n--- 12. Format, Bool, & Match ---")
    temp = Temperature(25.0)

    # 12a. Testing __bool__
    if temp:
        print("Temperature is physically possible (above absolute zero).")

    # 12b. Testing __format__
    print(f"Default string: {temp}")
    print(f"Formatted as Celsius: {temp:c}")
    print(f"Formatted as Fahrenheit: {temp:f}")

    # 12c. Testing Structural Pattern Matching (Python 3.10+)
    match temp:
        case Temperature(0):
            print("Water is freezing!")
        case Temperature(c) if c > 20:
            print(f"It's a warm {c}°C day.")
        case _:
            print("Just a normal temperature.")

    print("\n--- 13. Destructors ---")
    res = TemporaryResource("TempDB")
    # By deleting the variable, the reference count drops to 0; triggers __del__
    del res
    print("(Notice how the destruction statement happened immediately above)")

    print("\n--- 14. Generics (__class_getitem__) ---")
    # This allows developers to type hint: my_box: CustomBox[int]
    print(f"Type Hint Representation: {CustomBox[int]}")  # type: ignore

    print("\n--- 15. Custom Introspection (__dir__) ---")
    agent = SecretAgent()
    print("When you type 'agent.' in an IDE, it will only suggest:")
    print(dir(agent))
