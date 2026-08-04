import sys
from array import array
from collections import Counter, defaultdict, deque, namedtuple
from dataclasses import dataclass
from enum import IntFlag, StrEnum, auto
from queue import PriorityQueue
from types import SimpleNamespace
from typing import ChainMap, Iterable, Mapping, OrderedDict, Sequence

# This file had to be renamed to `collections_in_python.py` because
# `collections.py` is a standard library module in Python.
# Naming your file the same as a standard library module can lead to
# import conflicts and unexpected behavior.


# ==========================
# Enums
# ==========================
# Alternatively, you can use the IntEnum class if you want to have integer
# values for the enum members.
class Color(StrEnum):
    # Note: Using `auto()` will automatically assign values to the enum members.
    # The values will be the same as the member names, but in lowercase.
    RED = auto()
    GREEN = "Green"
    BLUE = "Blue"


@dataclass
class Point3D:
    x: float
    y: float
    z: float


# Remember that enums are immutable and unique. You cannot create new members or
# change existing ones after the enum class is defined. Enums are useful for
# representing a fixed set of related constants, and they can be used in
# comparisons, iterations, and as dictionary keys.
class Permission(IntFlag):
    # IntFlag allows for bitwise operations, making it suitable for
    # representing permissions or flags that can be combined.
    READ = 1
    WRITE = 2
    EXECUTE = 4


def main():

    # ==========================
    # Basic Collections
    # ==========================

    print([1, 2, 3])  # [1, 2, 3] (list)
    print({"lang": "Python"})  # {'lang': 'Python'} (dict)
    print((10, 20))  # (10, 20) (tuple)
    print({1, 2, 2, 3})  # {1, 2, 3} (set)

    # Shadowing built-in types (not recommended)
    # list = [10, 20]  # Shadowing

    data = [1, 2, 3]
    # Removes your variable from the current namespace
    del data

    # Use type() to check the type of a variable
    print(type(108989))  # <class 'int'>

    # --- Memory Usage ---
    a_list = [1, 2, 3, 4, 5]
    a_tuple = (1, 2, 3, 4, 5)

    print(sys.getsizeof(a_list))  #  ~104 bytes (varies by platform)
    print(sys.getsizeof(a_tuple))  #  ~88 bytes (less memory)

    print(range(5))  # range(0, 5)
    print(list(range(5)))  # [0, 1, 2, 3, 4]
    print(frozenset({1, 2, 3}))  # frozenset({1, 2, 3})

    # =========================
    # List Operations
    # =========================

    # List comprehension
    squares = [x**2 for x in range(5)]
    print(squares)  # [0, 1, 4, 9, 16]

    # Adding elements to a list
    squares.append(25)
    print(squares)  # [0, 1, 4, 9, 16, 25]

    # Not recommended: Using `*` to repeat lists creates a new list and
    # can be less efficient.
    # squares = squares * 2  # Output: [0, 1, 4, 9, 16, 25, 0, 1, 4, 9, 16, 25]

    # Not recommended: Using `+` to concatenate lists creates a new list and
    # can be less efficient.
    # squares = squares + [36, 49]  # Creates a new list

    # Extending a list with another list
    squares.extend([36, 49])
    print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49]

    squares.remove(25)  # Removes the first occurrence of 25
    print(squares)  # [0, 1, 4, 9, 16, 36, 49]

    squares.pop()  # Removes and returns the last item (49)
    print(squares)  # [0, 1, 4, 9, 16, 36]

    squares.sort(reverse=True)  # Sorts the list in descending order
    print(squares)  # [36, 16, 9, 4, 1, 0]
    # However, using `sorted()` is often preferred for creating a new sorted
    # list without modifying the original.
    sorted_squares = sorted(squares)  # Returns a new sorted list
    print(sorted_squares)  # [0, 1, 4, 9, 16, 36]
    print(squares)  # Original list remains unchanged: [36, 16, 9, 4, 1, 0]

    squares.reverse()  # Reverses the list in place
    print(squares)  # [0, 1, 4, 9, 16, 36]

    squares.insert(3, 10)  # Inserts 10 at index 3
    print(squares)  # [0, 1, 4, 10, 9, 16, 36]

    squares[2] = 5  # Updates the value at index 2
    print(squares)  # [0, 1, 5, 10, 9, 16, 36]

    squares.index(10)  # Returns the index of the first occurrence of 10
    squares.count(9)  # Returns the number of occurrences of 9

    # Shallow copy is a copy of the list that contains references to the same
    # objects as the original list. Changes to mutable objects in the copied
    # list will affect the original list.
    squares.copy()  # Returns a shallow copy of the list
    squares[:]  # Returns a shallow copy of the list (slice notation)

    squares.clear()  # Removes all items from the list
    print(squares)  # []

    # Allowed but not recommended: Using multiple data types in a list can lead
    # to confusion and errors.
    mixed_list = [1, "two", 3.0, [4], (5,), {6}]
    print(mixed_list)  # [1, 'two', 3.0, [4], (5,), {6}]

    # =============================
    # List and String Compatibility
    # =============================

    # Strings are immutable sequences of characters, while lists are mutable
    # sequences of elements. You can convert between them using the `list()`
    # and `str.join()` methods but be cautious about the types of elements in
    # the list when converting to a string.
    name = "Python"
    name_list = list(name)  # Converts string to list of characters
    print(name_list)  # ['P', 'y', 't', 'h', 'o', 'n']
    print(" ".join(name_list))  # "P y t h o n"

    # =========================
    # Tuple Operations
    # =========================
    # Tuples are immutable, but they can contain mutable objects like lists.
    # Tuples can be used as keys in dictionaries if they contain only immutable
    # objects. They are also more memory-efficient than lists and can be used to
    # represent fixed collections of items.
    mixed_tuple = (1, "two", 3.0, [4], (5,), {6})
    print(mixed_tuple)  # (1, 'two', 3.0, [4], (5,), {6})

    mixed_tuple[3].append(99)  # Modifies the list inside the tuple
    print(mixed_tuple)  # (1, 'two', 3.0, [4, 99], (5,), {6})

    # Raises TypeError: 'tuple' object does not support item assignment
    # mixed_tuple[4] = (7,)

    mixed_tuple.index(3.0)  # Returns the index of the first occurrence of 3.0
    mixed_tuple.count(1)  # Returns the number of occurrences of 1

    # Tuples can be concatenated and repeated, but this creates new tuples and
    # can be less efficient than using lists for dynamic collections.
    new_tuple = mixed_tuple + (7, 8)
    print(new_tuple)  # (1, 'two', 3.0, [4, 99], (5,), {6}, 7, 8)

    print((2) * 2)  # Output: 4 (int, not tuple)
    print((2,) * 2)  # Output: (2, 2)

    # =========================
    # Set Operations
    # =========================

    # Sets are unordered collections of unique elements.
    # They support mathematical set operations like union, intersection,
    # difference, and symmetric difference. Sets are mutable, but they can only
    # contain immutable (hashable) elements.

    a_set = {1, 2, 3, 4, 2, 1}  # Duplicates are removed
    print(a_set)  # Output: {1, 2, 3, 4}

    a_set.add(7)  # Adds 7 to the set
    a_set.remove(1)  # Removes 1 from the set
    print(a_set)  # Output: {2, 3, 4, 7}

    b_set = {3, 4, 5, 6}

    # Returns a new set with all unique elements from both sets
    print(a_set.union(b_set))  # Output: {2, 3, 4, 5, 6, 7}

    # Returns a new set with elements common to both sets
    print(a_set.intersection(b_set))  # Output: {3, 4}

    # Returns a new set with elements in a_set but not in b_set
    print(a_set.difference(b_set))  # Output: {2, 7}

    # Returns a new set with elements in either a_set or b_set but not in both
    print(a_set.symmetric_difference(b_set))  # Output: {2, 5, 6, 7}

    # Returns True if a_set is a subset of b_set
    print(
        a_set.issubset(b_set)
    )  # False, because a_set has elements not in b_set

    # Returns True if a_set is a superset of b_set
    print(
        a_set.issuperset(b_set)
    )  # False, because b_set has elements not in a_set

    # Returns True if a_set and b_set have no elements in common
    print(a_set.isdisjoint(b_set))  # False, because they share elements 3 and 4

    # Removes and returns an arbitrary element from the set
    print(a_set.pop())  # Output: 2 (or any other element, sets are unordered)

    # Adds symmetric difference of b_set to a_set (modifies a_set in place)
    a_set.symmetric_difference_update(b_set)  # Output: {2, 5, 6, 7}

    # Removes all elements of b_set from a_set (modifies a_set in place)
    a_set.difference_update(b_set)  # Output: {2, 7}

    # Modifies a_set to keep only elements also in b_set
    a_set.intersection_update(b_set)

    # Adds all elements from b_set to a_set
    a_set.update(b_set)

    # Returns a shallow copy of the set
    a_set.copy()

    # Removes 10 from the set if it exists, does nothing otherwise
    # This is safer than `remove()` which raises a KeyError
    # if the element is not found.
    a_set.discard(10)

    # Removes all elements from the set
    a_set.clear()

    # ==========================
    # Dictionary Operations
    # ==========================

    dict_data = {"lang": "Python", "version": 3.12}
    print(dict_data)  # Output: {'lang': 'Python', 'version': 3.12}

    # Accessing values using keys
    print(dict_data["lang"])  # Output: Python

    # Adding a new key-value pair
    dict_data["creator"] = "Guido"
    print(
        dict_data
    )  # Output: {'lang': 'Python', 'version': 3.12, 'creator': 'Guido'}

    # Removing a key-value pair
    del dict_data["version"]
    print(dict_data)  # Output: {'lang': 'Python', 'creator': 'Guido'}

    print(dict_data.get("version", "Not Found"))  # Output: Not Found
    print(dict_data.keys())  # Output: dict_keys(['lang', 'creator'])
    print(dict_data.values())  # Output: dict_values(['Python', 'Guido'])
    print(
        dict_data.items()
    )  # Output: dict_items([('lang', 'Python'), ('creator', 'Guido')])

    # Updating a dictionary with another dictionary,
    # simply adds new key-value pairs or updates existing ones.
    dict_data.update({"version": 3.12, "release": "stable"})

    # The `setdefault()` method is useful for initializing a key with a default
    # value if it doesn't already exist in the dictionary. If the key exists,
    # it returns the existing value; if not, it adds the key with the specified
    # default value and returns that value.
    dict_data.setdefault("license", "PSF")  # Adds 'license' if not present

    dict_data.pop("creator")  # Removes and returns the value for 'creator'

    dict_data.popitem()  # Removes and returns the last inserted key-value pair

    # Creates a new dict with specified keys and default values
    # Here, all new keys will have the same default value of "default_value".
    dict_data.fromkeys(["new_key1", "new_key2"], "default_value")

    dict_data.clear()  # Removes all key-value pairs from the dictionary

    # ====================================================
    # Collections Comprehensions, Generators and Iterators
    # ====================================================

    # Comprehension Example 1
    projects = ["Project A", "Project B", "Project C"]
    slugified_projects = [name.lower().replace(" ", "-") for name in projects]
    print(slugified_projects)  # Output: ['project-a', 'project-b', 'project-c']

    # Comprehension Example 2
    tasks = [
        {"name": "Task 1", "completed": False},
        {"name": "Task 2", "completed": False},
        {"name": "Task 3", "completed": True},
    ]
    pending_tasks = [task["name"] for task in tasks if not task["completed"]]
    print(pending_tasks)

    # More effective way is to use a generator expression,
    # which avoids creating an intermediate list and is more memory-efficient.
    pending_tasks_gen = (
        task["name"] for task in tasks if not task["completed"]
    )
    print(list(pending_tasks_gen))  # Output: ['Task 1', 'Task 2']

    # More suitable for large datasets, as it generates items on-the-fly and
    # doesn't store them all in memory at once. They are disposable and can only
    # be iterated over once.
    any_pending = any(task["completed"] is False for task in tasks)
    print(any_pending)  # Output: True

    all_completed = all(task["completed"] for task in tasks)
    print(all_completed)  # Output: False

    # If you need to iterate twice or index into the result, use a list
    # comprehension. Generators give up random access in exchange for not
    # allocating the whole sequence up front.

    sum_pending = sum(not task["completed"] for task in tasks)
    print(sum_pending)  # Output: 2

    # Iterators are objects that implement the iterator protocol, which consists
    # of the methods `__iter__()` and `__next__()`. They allow you to traverse
    # through all the elements of a collection, one element at a time.
    itr = iter([1, 2, 3])
    print(f"Iterator:  {itr} -> next: {next(itr)}")  # Output: 1
    # Generators are a simple and powerful tool for creating iterators. They are
    # written like regular functions but use the `yield` statement whenever they
    # want to return data. Each time `next()` is called on it, the generator
    # resumes where it left off (it remembers all the data values and which
    # statement was last executed). Generators are a convenient way to implement
    # the iterator protocol without having to write a class with `__iter__()`
    # and `__next__()` methods.
    gen = (x**2 for x in range(3))
    print(f"Generator: {gen} -> values: {list(gen)}")  # Output: [0, 1, 4]

    # ==========================
    # Zip and Unzip
    # ==========================
    names = ["Alice", "Bob", "Charlie"]
    scores = [85, 90, 95]

    # Two lists can be zipped together to create an iterator of tuples, where
    # each tuple contains one element from each of the input lists. The `zip()`
    # function stops creating tuples when the shortest input iterable is
    # exhausted. If you need to handle iterables of different lengths,
    # you can use `itertools.zip_longest()` to fill in missing values with a
    # specified fill value.
    zipped = zip(names, scores)  # Creates an iterator of tuples
    print(list(zipped))  # Output: [('Alice', 85), ('Bob', 90), ('Charlie', 95)]

    # To make a dictionary from zipped data, you can use the `dict()` function.
    zipped_dict = dict(zip(names, scores))
    print(zipped_dict)  # Output: {'Alice': 85, 'Bob': 90, 'Charlie': 95}

    # To unzip a zipped object, you can use the `zip(*iterable)` idiom. This
    # effectively transposes the list of tuples.
    unzipped = zip(*zip(names, scores))  # Unzips the zipped object
    print(list(unzipped))  # Output: [('Alice', 'Bob', 'Charlie'), (85, 90, 95)]

    # Zipping different types of iterables together is also possible.
    stuff = ["Red", 1.0, True]
    other_stuff = ("blue", 3, False)
    stuff_dict = dict(zip(stuff, other_stuff))
    print(stuff_dict)  # Output: {'Red': 'blue', 1.0: 3, True: False}

    # ==========================
    # Specialized Collections
    # ==========================

    # Enum
    print(Color.RED)  # red
    print(Color.BLUE)  # Blue

    # defaultdict
    counts = defaultdict(int)  # Missing keys default to int() -> 0
    for char in "abracadabra":
        counts[char] += 1  # No need to write counts.get(char, 0) + 1
    print(counts["a"])  # Output: 5

    # Counter
    freq = Counter(["a", "a", "b"])
    print(freq)  # Counter({'a': 2, 'b': 1})

    # namedtuple
    Point = namedtuple("Point", ["x", "y"])
    p = Point(10, 20)
    print(p)  # Point(x=10, y=20)

    # deque
    dq = deque([1, 2, 3])
    dq.appendleft(0)
    dq.append(4)
    print(dq)  # deque([0, 1, 2, 3])

    # array: Space-efficient C-style numeric array ('i' = signed int)
    num_array = array("i", [1, 2, 3, 4])
    print(f"array:     {num_array}")

    pq = PriorityQueue()
    pq.put((1, "high priority"))
    print(f"PriorityQueue:     {pq}")

    Point2D = namedtuple("Point2D", ["x", "y"])
    p2 = Point2D(10, 20)
    print(f"namedtuple:  {p2} -> p2.x = {p2.x}")

    dd = defaultdict(list)
    dd["missing_key"].append("auto-created")
    print(f"defaultdict: dict(dd) -> {dict(dd)}")

    od = OrderedDict(a=1, b=2, c=3)
    od.move_to_end("a")
    print(f"OrderedDict: {od}")

    cm = ChainMap({"primary": 1}, {"fallback": 2})
    print(f"ChainMap:    {cm} -> cm['fallback'] = {cm['fallback']}")

    p3 = Point3D(1.0, 2.0, 3.0)
    print(f"dataclass: {p3}")

    ns = SimpleNamespace(config="test", retries=3)
    print(f"SimpleNamespace: {ns}")

    # ============================================
    # Abstract Base Classes (ABCs) for Collections
    # ============================================
    # using isinstance() rather than creating concrete objects.
    print(f"Is list a Sequence? {isinstance([], Sequence)}")
    print(f"Is dict a Mapping?  {isinstance({}, Mapping)}")
    print(f"Is range Iterable?  {isinstance(range(5), Iterable)}")

    # ============================================
    # Type Hints for Collection Declarations
    # ============================================
    # Type hints are optional and do not enforce type checking at runtime.
    # They are primarily used for static type checking and code readability.
    # Example of type hints for collection declarations
    my_list: list[str] = ["1", "2", "3"]  # a list of strings.
    my_dict: dict[str, int] = {
        "a": 1,
        "b": 2,
    }  # a dictionary mapping strings to integers.
    my_tuple: tuple[int, int] = (1, 2)  # a fixed-size pair(tuple) of integers.
    my_set: set[str] = {"apple", "banana", "cherry"}  # a set of strings.
    print(f"Type hints for lists: {my_list}")
    print(f"Type hints for dictionaries: {my_dict}")
    print(f"Type hints for tuples: {my_tuple}")
    print(f"Type hints for sets: {my_set}")


if __name__ == "__main__":
    main()
