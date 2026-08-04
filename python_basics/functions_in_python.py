"""
Python Functions Master Class File (21 Core Paradigms)
Covers: Signatures, Defaults, Type Hints, Scopes, Closures, Generators, Lambdas,
Unpacking, Functional Tools, Recursion, Functools, Async/Await, Advanced
Generators, Introspection, Recursion Limits, Callables (__call__), Decorators
(Standard, Class-Based, and With Arguments), Type Hinting Callables, Async
Generators, Context Managers, Overloading, and Single Dispatch.
"""

# In Python, functions are just objects (like strings or integers).
# You can assign them to variables, pass them as arguments to other functions,
# and return them from functions.

import asyncio
import functools
import inspect
import sys
import time
from contextlib import contextmanager
from functools import singledispatch
from typing import Callable, Union, overload

# ==========================================
# 1. BASIC SIGNATURES & DEFAULT ARGUMENTS
# ==========================================


# Defaults are evaluated once, when the function is defined.
# Don't use a mutable object like a list or dict as a default value.
# Sample function to demonstrate mutable default arguments in Python.
def add_tag(name, tags=None):
    if tags is None:
        tags = []
    tags.append(name)
    return tags


# This function demonstrates the use of a mutable default argument.
# If you call this function multiple times without providing the `tags`
# argument, it will keep appending to the same list, which can lead to
# unexpected behavior. So, it's generally recommended to use `None` as the
# default value and create a new collection inside the function if needed,
# as shown in the `add_tag` function above.
def add_tag_with_default(name, tags=[]):
    """Mutable default argument trap."""
    tags.append(name)
    return tags


def slugify(text, separator="-"):
    """
    Converts a string into a URL-friendly slug.
    Example: "Hello World!" -> "hello-world"
    """
    text = text.lower().strip()
    return text.replace(" ", separator)


"""
        This acts as a multiline comment.
        Python will parse this as a string, but since it isn't assigned 
        to a variable, it gets discarded at execution time.
"""


# Function parameters and return values can carry type hints.
# They don't change runtime behavior, but they document intent and let editors
# and type checkers catch bugs before the code runs.
# Return None explicitly if no return statement is present.
def slugify_with_hints(name: str, separator: str = "-") -> str:
    # This is a comment which will be ignored by the Python interpreter.
    """
    This is a docstring for the slugify_with_hints function.
    It provides information about the function's purpose, parameters,
    and return type.
    """
    cleaned = name.strip().lower()
    return cleaned.replace(" ", separator)


# ==========================================
# 2. ADVANCED ARGUMENT PARSING
# ==========================================


def project_function(name, *, description=None, tags=None):
    """
    A sample function to demonstrate the use of keyword-only arguments.
    The `*` in the parameter list indicates that all following parameters
    must be specified as keyword arguments. The parameters before the `*`
    can be specified positionally or as keywords.
    """
    if tags is None:
        tags = []
    return {"name": name, "description": description, "tags": tags}


def project_function_with_kwargs(name, **kwargs):
    """
    A sample function to demonstrate the use of keyword arguments.
    The `**kwargs` allows you to pass a variable number of keyword arguments
    to the function. These arguments are captured in a dictionary.
    """
    return {"name": name, **kwargs}


# If a function reaches the end without hitting a return, it returns None.
def full_spec(p1, /, p_or_k=2, *, k_only=3, **kwargs):
    #           ^          ^        ^
    #     Pos-Only    Pos-or-KW   KW-Only
    """
    This function demonstrates the use of positional-only, positional-or-
    keyword, and keyword-only parameters in Python. The `/` indicates that all
    parameters before it are positional-only, while the `*` indicates that all
    parameters after it are keyword-only. The `**kwargs` allows for additional
    keyword arguments.
    """
    pass


def any_pos_or_kw(*args, **kwargs):
    """
    This function demonstrates the use of arbitrary positional and keyword
    arguments. The `*args` allows for any number of positional arguments, while
    the `**kwargs` allows for any number of keyword arguments. Both are captured
    in tuples and dictionaries, respectively.
    """
    return f"Args: {args}, Kwargs: {kwargs}"


# ==========================================
# 3. FUNCTIONS AS FIRST-CLASS CITIZENS & LAMBDAS
# ==========================================


# Functions in Python are first-class citizens, meaning they can be passed
# around as arguments, returned from other functions, and assigned to variables.
def apply_operation(x, y, operation_func):
    return operation_func(x, y)


# Lambdas are anonymous functions that can be defined in a single line.
# Syntax: lambda arguments: expression. They are often used for short, throwaway
# functions. However, for more complex operations or assigning to a variable,
# it's better to define a regular function.
multiply_lambda = lambda a, b: a * b  # noqa: E731


# ==========================================
# 4. SCOPE AND CLOSURES (nonlocal / global)
# ==========================================

GLOBAL_STATE = "I am a global variable"


# By default, Python functions can read variables from the global scope, but
# they cannot modify them unless explicitly declared as global. The `nonlocal`
# keyword allows a nested function to modify a var from its enclosing scope.
def scope_demonstrator():
    # global allows us to modify the global variable from within this function.
    global GLOBAL_STATE
    GLOBAL_STATE = "Global variable modified by scope_demonstrator!"

    counter = 0

    def increment_closure():
        # nonlocal allows us to modify the variable from the enclosing scope
        nonlocal counter
        counter += 1
        return counter

    return increment_closure


# ==========================================
# 5. GENERATORS (yield)
# ==========================================


# Generators are a special type of iterator that allow you to iterate over data
# without storing the entire dataset in memory. They are defined using the
# `yield` keyword, which allows the function to return a value and pause its
# execution, resuming from that point when the next value is requested.
def countdown_generator(start):
    print(f"Starting countdown from {start}...")
    while start > 0:
        yield start
        start -= 1
    print("Countdown finished!")


# ==========================================
# 6. BUILT-IN FUNCTIONAL TOOLS (map, filter, zip)
# ==========================================


def demonstrate_functional_tools():
    """
    Python provides built-in tools for functional programming patterns.
    These take a function and an iterable as arguments.
    """
    numbers = [1, 2, 3, 4, 5]
    names = ["Alice", "Bob", "Charlie"]

    # map(): Applies a function to all items in an input list
    # Here we use a lambda to double the numbers
    doubled = list(map(lambda x: x * 2, numbers))

    # filter(): Creates a list of elements for which a function returns True
    evens = list(filter(lambda x: x % 2 == 0, numbers))

    # zip(): Combines iterables element by element into tuples
    paired = list(zip(names, numbers))

    return doubled, evens, paired


# ==========================================
# 7. RECURSION
# ==========================================


def factorial(n):
    """
    A function that calls itself. Must always have a "base case"
    to stop the recursion and prevent RecursionError.
    """
    # Base case
    if n <= 1:
        return 1
    # Recursive case
    return n * factorial(n - 1)


# ==========================================
# 8. THE functools MODULE
# ==========================================


# @lru_cache saves the results of expensive function calls.
# If we call this again with the same arguments, it returns the cached result
# instantly. maxsize=128 means it will cache the last 128 unique calls.
@functools.lru_cache(maxsize=128)
def expensive_fibonacci(n):
    if n < 2:
        return n
    return expensive_fibonacci(n - 1) + expensive_fibonacci(n - 2)


def power(base, exponent):
    return base**exponent


# functools.partial creates a new function with some arguments pre-filled.
# This is useful for creating specialized versions of a function without
# rewriting it.
square = functools.partial(power, exponent=2)
cube = functools.partial(power, exponent=3)


# ==========================================
# 9. ASYNCHRONOUS FUNCTIONS (async / await)
# ==========================================


# async functions are defined with the `async` keyword. They allow you to write
# code that can pause and resume, making it easier to handle I/O-bound tasks
# like network requests or file operations without blocking the entire program.
async def fetch_data(id):
    """
    An asynchronous function. The 'await' keyword pauses this function,
    giving control back to the event loop to run other code while
    waiting for this operation (like a network request) to finish.
    """
    print(f"Start fetching data {id}...")
    # asyncio.sleep simulates a time-consuming I/O operation
    await asyncio.sleep(1)
    print(f"Finished fetching data {id}!")
    return {"id": id, "data": "Sample JSON data"}


# Note: async functions return a coroutine object when called. To actually run
# them, you need to use an event loop, which is what asyncio.run() does.
# asyncio.run() is used to run the main async function in a synchronous context.
async def main_async_runner():
    """
    Runs multiple async tasks concurrently.
    """
    print("\n--- 9. Asynchronous Functions ---")
    # asyncio.gather runs all these awaitables at the same time
    results = await asyncio.gather(fetch_data(1), fetch_data(2), fetch_data(3))
    print("All async tasks completed:", results)


# ==========================================
# 10. ADVANCED GENERATORS (yield from, send)
# ==========================================


def sub_generator():
    """A smaller generator to be consumed by another."""
    yield "A"
    yield "B"


def main_generator():
    """
    'yield from' establishes a transparent bidirectional connection
    between the caller and the sub-generator. It flattens nested generators.
    """
    yield "Start"
    yield from sub_generator()
    yield "End"


def interactive_generator():
    """
    Generators don't just produce data; they can consume it using .send().
    This was how Python did asynchronous programming before async/await!
    """
    print("Generator started.")
    while True:
        # The generator pauses here and waits to be sent a value
        received = yield "Waiting for input..."
        yield f"I received: {received}"


# ==========================================
# 11. FUNCTION INTROSPECTION & ATTRIBUTES
# ==========================================


def secret_function(x: int, y: int = 10) -> int:
    """I have a secret."""
    return x + y


# 11a. Function Attributes
# Because functions are objects, you can literally attach variables to them!
secret_function.author = "Python Master"  # type: ignore[attr-defined]
secret_function.version = 1.2  # type: ignore[attr-defined]


def demonstrate_introspection():
    """
    The 'inspect' module lets Python look at its own code at runtime.
    You can analyze signatures, read docstrings, and even see the raw source
    code.
    """
    # 1. Read custom attributes
    print(f"Function Author: {secret_function.author}")  # type: ignore[attr-defined]
    # Ideal way to access attributes is using getattr() to avoid AttributeError
    # print(f"Function Author: {getattr(secret_function, 'author', 'Unknown')}")

    # 2. Inspect the signature programmatically
    sig = inspect.signature(secret_function)
    print(f"Signature: {sig}")
    for name, param in sig.parameters.items():
        print(
            f"- Param: {name}, Default: {param.default}, "
            f"Type: {param.annotation}"
        )

    # 3. Check what kind of function it is
    print(
        f"Is interactive_generator a generator? {
            inspect.isgeneratorfunction(interactive_generator)
        }"
    )


# ==========================================
# 12. MANAGING RECURSION LIMITS
# ==========================================


def demonstrate_recursion_limit():
    """
    Python protects your memory by limiting how many times a function
    can call itself recursively. You can view and change this limit.
    """
    current_limit = sys.getrecursionlimit()
    print(f"Current maximum recursion depth: {current_limit}")

    # You can change it if you have a massive recursive algorithm:
    # sys.setrecursionlimit(2000)
    # Be careful: setting this too high will crash Python (Stack Overflow)!


# ==========================================
# 13. CALLABLES (__call__)
# ==========================================


class RateLimiter:
    """
    By defining the __call__ magic method, you can make an instance of a class
    behave exactly like a function. This is incredibly useful when your
    "function" needs to remember complex state across multiple calls.
    """

    def __init__(self, max_calls):
        self.max_calls = max_calls
        self.calls_made = 0

    def __call__(self, *args, **kwargs):
        if self.calls_made >= self.max_calls:
            return "Error: Rate limit exceeded!"

        self.calls_made += 1
        return f"Call successful! ({self.calls_made}/{self.max_calls})"


# ==========================================
# 14. DECORATORS (@)
# ==========================================


def timer_decorator(func):
    """
    A decorator is a function that takes another function, extends its behavior,
    and returns a new function (a closure) without altering the original code.
    """

    # @functools.wraps ensures the original function's name and docstring are
    # preserved. If we don't use this, introspection will break!
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        # Execute the original function
        result = func(*args, **kwargs)

        end_time = time.time()
        print(
            f"[{func.__name__}] executed in {end_time - start_time:.4f} seconds"
        )
        return result

    return wrapper


# The @ syntax is just syntactic sugar for:
# slow_greeting = timer_decorator(slow_greeting)
@timer_decorator
def slow_greeting(name):
    """Greets the user after a brief pause."""
    time.sleep(0.5)
    return f"Hello, {name}!"


# ==========================================
# 15. CLASS-BASED DECORATORS (Combining both!)
# ==========================================


class CountCalls:
    """
    Because a class with __call__ acts like a function, we can use it AS a
    decorator! This is much cleaner than using `global` or `nonlocal` for a
    decorator's state.
    """

    def __init__(self, func):
        self.func = func
        self.num_calls = 0
        functools.update_wrapper(self, func)  # Similar to @functools.wraps

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"[{self.func.__name__}] has been called {self.num_calls} times")
        return self.func(*args, **kwargs)


@CountCalls
def say_hi():
    return "Hi!"


# ==========================================
# 16. DECORATORS WITH ARGUMENTS
# ==========================================


def repeat(num_times):
    """
    To pass arguments to a decorator, you need an outer function that takes
    the arguments, which returns the actual decorator, which returns
    the wrapper!
    """

    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # We can access `num_times` here thanks to closures!
            for _ in range(num_times - 1):
                func(*args, **kwargs)
            return func(*args, **kwargs)  # Return the result of the final call

        return wrapper

    return decorator_repeat


@repeat(num_times=3)
def say_hello(name):
    print(f"Hello, {name}!")


# ==========================================
# 17. TYPE HINTING FUNCTIONS (Callable)
# ==========================================


# Callable[[ArgType1, ArgType2], ReturnType]
def execute_math_callback(
    a: int, b: int, callback: Callable[[int, int], int]
) -> int:
    """
    Using the typing module, we can specify exactly what kind of function
    is allowed to be passed in as an argument.
    """
    return callback(a, b)


# ==========================================
# 18. ASYNCHRONOUS GENERATORS
# ==========================================


async def async_countdown():
    """
    Combines async/await with yield. Useful for streaming data over a network
    where each chunk takes time to fetch.
    """
    for i in range(3, 0, -1):
        await asyncio.sleep(0.5)  # Simulate network delay
        yield i


async def consume_async_generator():
    """To consume an async generator, we must use 'async for'."""
    print("\n--- 18. Async Generators ---")
    async for number in async_countdown():
        print(f"Async yielded: {number}")


# ==========================================
# 19. FUNCTIONS AS CONTEXT MANAGERS (with block)
# ==========================================


@contextmanager
def temporary_file_editor(filename):
    """
    Combines a decorator and a generator to create a context manager!
    This allows a normal function to be used with the 'with' statement.
    Everything before 'yield' is the setup (__enter__).
    Everything after 'yield' is the cleanup (__exit__).
    Your generator function must yield exactly once.
    """
    print(f"\n[Context] Opening {filename}...")
    # Yield passes control (and optionally data) to the 'with' block
    yield f"--- Data inside {filename} ---"
    # This runs automatically when the 'with' block finishes,
    # even if it crashes!
    print(f"[Context] Safely closing {filename}...")


# ==========================================
# 20. FUNCTION OVERLOADING (Type Checking Only)
# ==========================================


# Python doesn't allow multiple functions with the same name.
# But using @overload, we can tell mypy (the type checker) that this function
# behaves differently depending on the input types.
@overload
def process_data(data: int) -> int: ...


@overload
def process_data(data: str) -> str: ...


# The actual implementation goes last, without the @overload decorator.
def process_data(data: Union[int, str]) -> Union[int, str]:
    """Multiplies ints, but repeats strings."""
    if isinstance(data, int):
        return data * 2
    return data + data


# ==========================================
# 21. SINGLE DISPATCH (Runtime Overloading)
# ==========================================


# While @overload is just for type-checkers, @singledispatch actually changes
# runtime behavior based on the FIRST argument's type!
@singledispatch
def display_info(arg):
    """The default behavior if no specific type matches."""
    print(f"Generic Object: {arg}")


@display_info.register
def _(arg: int):
    """How to handle integers."""
    print(f"Integer processing: {arg * 100}")


@display_info.register
def _(arg: list):
    """How to handle lists."""
    print(f"List processing: {len(arg)} items found -> {arg}")


# ==========================================
# EXECUTION BLOCK
# ==========================================

if __name__ == "__main__":
    print("--- 1. Basics ---")
    print(slugify("  Python is Best!  "))  # Output: python-is-best!
    print(slugify("Python is Best!", separator="_"))  # Output:python_is_best!
    print(slugify_with_hints("Hello World"))  # Output: hello-world

    # Type hints are not enforced at runtime. Hence, the following call will not
    # raise an error, but it may lead to unexpected behavior or runtime errors.
    # print(slugify_with_hints(1, 3))

    print(add_tag("python"))  # Output: ['python']
    print(add_tag("java"))  # Output: ['java']

    print(add_tag_with_default("python"))  # Output: ['python']
    print(add_tag_with_default("java"))  # Output: ['python', 'java']

    print("\n--- 2. Advanced Arguments ---")
    print(
        project_function(
            "My Project", description="A sample project", tags=["python"]
        )
    )

    # The following call will raise a TypeError because `description` and `tags`
    # are keyword-only arguments and must be specified as such.
    # print(project_function("My Project", "A sample project", ["python"]))

    print(
        project_function_with_kwargs(
            "My Project",
            description="A sample project",
            tags=["python", "sample"],
            anything_else="This is a test",
        )
    )

    print("\n--- 3. First-Class Functions & Lambdas ---")
    print(
        f"5 * 4 using lambda callback: {apply_operation(5, 4, multiply_lambda)}"
    )

    print("\n--- 4. Scope and Closures ---")
    print(f"Global state before: {GLOBAL_STATE}")
    my_counter = scope_demonstrator()  # This modifies the global variable
    print(f"Closure call 1: {my_counter()}")
    print(f"Closure call 2: {my_counter()}")
    print(f"Global state after: {GLOBAL_STATE}")

    print("\n--- 5. Generators ---")
    for number in countdown_generator(2):
        print(f"Yielded: {number}")

    print("\n--- 6. Functional Tools ---")
    doubled, evens, paired = demonstrate_functional_tools()
    print(f"Mapped (Doubled): {doubled}")
    print(f"Filtered (Evens): {evens}")
    print(f"Zipped (Pairs): {paired}")

    print("\n--- 7. Recursion ---")
    print(f"Factorial of 5: {factorial(5)}")

    print("\n--- 8. functools Module ---")
    # Notice how fast this is with lru_cache!
    # Without it, fibonacci(35) takes seconds.
    print(f"Fibonacci of 35 (Cached): {expensive_fibonacci(35)}")

    # Using our partial functions
    print(f"Square of 5 using partial: {square(5)}")
    print(f"Cube of 5 using partial: {cube(5)}")

    # To run async code in a normal script, we must pass it to asyncio.run()
    asyncio.run(main_async_runner())

    print("\n--- 10. Advanced Generators ---")
    # yield from
    for item in main_generator():
        print(f"Yielded from chain: {item}")

    # generator.send()
    gen = interactive_generator()
    print(next(gen))  # Advance to the first 'yield'
    print(gen.send("Hello Data!"))  # Send data INTO the generator

    print("\n--- 11. Introspection ---")
    demonstrate_introspection()

    print("\n--- 12. Recursion Limits ---")
    demonstrate_recursion_limit()

    print("\n--- 13. Callables (__call__) ---")
    # We instantiate the class, but use it like a function
    api_limit = RateLimiter(max_calls=2)
    print(api_limit())  # Call 1
    print(api_limit())  # Call 2
    print(api_limit())  # Call 3 (Fails)

    # Prove that Python sees it as callable
    print(f"Is api_limit callable? {callable(api_limit)}")

    print("\n--- 14. Decorators (@) ---")
    # The timer_decorator automatically runs around slow_greeting
    print(slow_greeting("Alice"))

    # Because we used @functools.wraps, the original docstring is safe!
    print(f"Docstring: {slow_greeting.__doc__}")

    print("\n--- 15. Class-Based Decorators ---")
    print(say_hi())
    print(say_hi())
    print(say_hi())

    print("\n--- 16. Decorators with Arguments ---")
    say_hello("World")  # Will print 3 times

    print("\n--- 17. Type Hinting Callables ---")
    # Passing a lambda that matches Callable[[int, int], int]
    result = execute_math_callback(10, 5, lambda x, y: x + y)
    print(f"Callback result: {result}")

    # We have to run the async generator via the event loop
    # If you already have asyncio.run(main_async_runner()) in your block,
    # you would add await consume_async_generator() inside that main runner!
    asyncio.run(consume_async_generator())

    print("\n--- 19. Context Manager Functions ---")
    # Using our function as a 'with' block
    with temporary_file_editor("my_secret_data.txt") as file_content:
        print(f"Working with: {file_content}")
        print("Doing some operations...")

    print("\n--- 20. Type-Hint Overloading ---")
    print(process_data(10))  # IDE knows this returns an int
    print(process_data("Echo"))  # IDE knows this returns a str

    print("\n--- 21. Single Dispatch ---")
    display_info("Hello!")  # Falls back to default
    display_info(5)  # Routes to the int handler
    display_info(["a", "b", "c"])  # Routes to the list handler
