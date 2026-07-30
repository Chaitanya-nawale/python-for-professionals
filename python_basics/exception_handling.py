import traceback

# Some common built-in exceptions to be aware of:
# KeyError: The requested dictionary key does not exist.
# IndexError: The list or tuple index is out of bounds.
# TypeError: An operation was applied to the wrong object type.
# ValueError: The object is the right type, but has an invalid value.
# AttributeError: The object lacks the requested attribute or method.
# FileNotFoundError: The specified file path does not exist.
# ModuleNotFoundError: The requested package or module is not installed.
# ConnectionError: The network connection was refused or dropped.
# TimeoutError: The operation exceeded the designated time limit.
# NotImplementedError: An abstract method requires subclass implementation.
# NameError: The variable or function name is not defined in scope.
# ZeroDivisionError: Attempted to divide or modulo a number by zero.
# StopIteration: Raised by next() to signal that an iterator has no more items.
# KeyboardInterrupt: The user manually stopped the program (usually via Ctrl+C).
# OSError: A system-level error occurred, such as a full disk or an I/O failure.
# AssertionError: An assert statement evaluated to False.
# PermissionError: OS denied file or system access due to lack of privileges.
# UnboundLocalError: A local variable was used before it was assigned a value.
# RuntimeError: A generic error when an issue doesn't fit any specific category.
# RecursionError: A function exceeded maximum recursion depth.
# ImportError: A module was found, but a specific target failed to load.


# ==========================================
# 1. Custom Exceptions
# ==========================================
class InsufficientFundsError(Exception):
    """Custom exception raised for invalid banking operations."""

    pass


class ApplicationStartupError(Exception):
    """Custom exception used to demonstrate exception chaining."""

    pass


# ==========================================
# 2. The Core Block & Catching Multiple Errors
# ==========================================
def demonstrate_core_blocks():
    print("--- 2. Core Try/Except Block ---")
    try:
        # Code that might crash
        result = 10 / int(
            "2"
        )  # Try changing "2" to "0" to see different results

    except (TypeError, ValueError) as e:
        # Catching multiple errors at once and capturing the error object ('e')
        print(f"Caught a type or value error: {e}")

    except ZeroDivisionError:
        # Stacking multiple except blocks
        print("You can't divide by zero!")

    else:
        # Runs ONLY if the try block succeeded without crashing
        print(f"Success! The result is {result}")

    finally:
        # Runs NO MATTER WHAT
        print("Cleaning up resources...\n")


# ==========================================
# 3. Manually Triggering Errors (raise)
# ==========================================
def set_age(age):
    print("--- 3. Raising Exceptions ---")
    try:
        if age < 0:
            # Stop the program and throw an error intentionally
            raise ValueError("Age cannot be negative!")
        print(f"Age successfully set to {age}\n")

    except ValueError as e:
        print(f"Validation failed: {e}\n")


# ==========================================
# 4. Using Custom Exceptions
# ==========================================
def withdraw(balance, amount):
    print("--- 4. Custom Exceptions ---")
    try:
        if amount > balance:
            raise InsufficientFundsError(
                f"Tried to withdraw {amount}, but only have {balance}"
            )

        new_balance = balance - amount
        print(f"Withdrawal successful. Remaining balance: {new_balance}\n")

    except InsufficientFundsError as e:
        print(f"Transaction denied: {e}\n")


# ==========================================
# 5. Exception Chaining (raise ... from ...)
# ==========================================
def demonstrate_chaining():
    print("--- 5. Exception Chaining ---")
    try:
        try:
            # Simulate a low-level error (e.g., database connection fails)
            1 / 0  # type: ignore
        except ZeroDivisionError as original_error:
            # Wrap it in a higher-level application error,
            # preserving the root cause
            raise ApplicationStartupError(
                "Failed to start the application"
            ) from original_error

    except ApplicationStartupError as e:
        print(f"Caught Chained Error: {e}")
        print(f"The original cause was: {e.__cause__}\n")


# ==========================================
# 6. Catching 'Exception' (Avoiding bare except)
# ==========================================
def demonstrate_proper_catch_all():
    print("--- 6. Proper Catch-All ---")
    try:
        # Some unknown error occurs
        x = "apple" + 5  # type: ignore
        print(f"Result: {x}")
    # ❌ BAD: Bare except catches everything, including system exit and
    #  keyboard interrupts
    # except:
    #     print("Caught an unexpected error (but this is unsafe!)\n")
    except Exception as e:
        # ✅ GOOD: Catches standard errors but allows sys.exit()
        # and Ctrl+C to pass
        print(f"Caught an unexpected error safely: {type(e).__name__} - {e}\n")


# ==========================================
# 7. Logging Tracebacks Silently
# ==========================================
def demonstrate_traceback():
    print("--- 7. Logging Tracebacks Silently ---")
    try:
        int("Not a number")
    except ValueError:
        # Capture the red error text as a string without crashing the app
        error_details = traceback.format_exc()
        print("Whoops, something broke! Here is the hidden traceback:")
        print(error_details)


# ==========================================
# 8. Exception Groups (Python 3.11+)
# ==========================================
def demonstrate_exception_groups():
    print("--- 8. Exception Groups (Python 3.11+) ---")
    try:
        # Simulating multiple errors happening at once (e.g., in async code)
        raise ExceptionGroup(
            "Multiple failures occurred",
            [ValueError("Invalid data format"), TypeError("Expected a string")],
        )
    # The except* (except-star) syntax allows multiple except* blocks to run for
    # a single try block. Python will look inside your ExceptionGroup, pull out
    # the errors one by one, and route them to the correct blocks.
    except* ValueError as e:
        print(f"Handled the ValueErrors inside the group: {e.exceptions}")
    except* TypeError as e:
        print(f"Handled the TypeErrors inside the group: {e.exceptions}\n")


# ==========================================
# 9. Advanced Generator Control
# ==========================================
def demonstrate_generators():
    print("--- 9. Advanced Generator Exceptions ---")

    def interactive_gen():
        try:
            val1 = yield "Ready"
            print(f"Received via send(): {val1}")
            val2 = yield "Second Step"
            print(f"Received via send(): {val2}")
        except ValueError:
            print("Caught ValueError inside the generator!")
            yield "Recovered"
        finally:
            print("Generator cleanup triggered.")

    # Instantiate the generator (Starts in 'GEN_CREATED' state)
    gen = interactive_gen()

    # Prime the generator to reach the first yield
    # (Must send None or call next(gen) first!)
    first_res = gen.send(None)
    print(f"1. Initial yield: {first_res}")

    second_res = gen.send("Hello Python")
    print(f"2. Second yield: {second_res}")

    # Use throw() to inject an exception into the generator
    recovered_res = gen.throw(ValueError)
    print(f"3. After throw: {recovered_res}")

    # Close the generator to trigger the finally block
    gen.close()


# ==========================================
# Main Execution
# ==========================================
def main():
    demonstrate_core_blocks()
    set_age(-5)
    withdraw(100, 500)
    demonstrate_chaining()
    demonstrate_proper_catch_all()
    demonstrate_traceback()

    # Check Python version to prevent crashes on older systems
    import sys

    if sys.version_info >= (3, 11):
        demonstrate_exception_groups()
    else:
        print("--- 8. Exception Groups ---")
        print("Skipping... ExceptionGroups require Python 3.11+\n")

    demonstrate_generators()


if __name__ == "__main__":
    main()
