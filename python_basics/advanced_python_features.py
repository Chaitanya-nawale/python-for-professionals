from typing import Callable

import numpy as np

# ==========================================
# Advanced Python Features
# ==========================================


def main():

    # ==========================================
    # Ellipsis (`...`) in Python
    # ==========================================
    print(f"Ellipsis:  {...} (Used for slicing, typing, pass stubs)")
    # 1. Advanced Multi-Dimensional Slicing (NumPy / PyTorch)
    # Creates a 4D array: shape (batch, channels, height, width)
    tensor = np.zeros((2, 3, 4, 4))

    # Slices all batches for channel 0, expanding '...' across height and width
    channel_zero = tensor[:, 0, ...]  # Same as tensor[:, 0, :, :]
    print("1. NumPy Slicing shape:", channel_zero.shape)  # (2, 4, 4)

    # 2. Type Hinting (Indefinite Lengths & Arguments)
    # Tuple of ANY number of integers
    number_list: tuple[int, ...] = (1, 2, 3, 4, 5)

    # Function taking ANY arguments (...) and returning a string
    logging_func: Callable[..., str] = lambda *args, **kwargs: "Done"  # noqa: E731

    print("2. Type Hinting:", number_list, "|", logging_func(1, "test", a=10))

    # 3. Unimplemented Code Stubs (Cleaner alternative to 'pass')
    class AbstractDatabase:
        def connect(self) -> None: ...  # Stub to be overridden in subclass

    print("3. Code Stub:", AbstractDatabase().connect())  # Returns None

    # ==========================================
    # Slice and NotImplemented
    # ==========================================

    # Slice object for advanced slicing
    # slice(start, stop, step) allows dynamic slicing of sequences.
    s = slice(1, 5, 2)
    list_example = [10, 20, 30, 40, 50, 60]
    sliced_list = list_example[s]  # Equivalent to list_example[1:5:2]
    print("4. Sliced List:", sliced_list)  # Output: [20, 40]

    print(f"slice:     {s} (Used dynamically for list[1:5:2])")

    # A built-in singleton returned by binary special methods
    # (e.g., __eq__) when an operation isn't implemented.
    print(f"NotImpl:   {NotImplemented} (Returned by binary magic methods)")


if __name__ == "__main__":
    main()
