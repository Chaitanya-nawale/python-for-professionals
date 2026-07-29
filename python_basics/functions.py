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
    tags.append(name)
    return tags


def slugify(text, separator="-"):
    """
    Converts a string into a URL-friendly slug.
    Example: "Hello World!" -> "hello-world"
    """

    # Lowercase the text and strip leading/trailing whitespace
    text = text.lower()
    text = text.strip()

    # Replace spaces and special characters with separator
    text = text.replace(" ", separator)

    # Alternatively, you can use the `re` module to handle more complex cases.
    # import re
    # text = re.sub(r'[\s\W]+', '-', text)

    return text


"""
        This acts as a multiline comment.
        Python will parse this as a string, but since it isn't assigned 
        to a variable, it gets discarded at execution time.
"""


# Slugify function with type hints
def slugify_with_hints(name: str, separator: str = "-") -> str:
    # This is a comment which will be ignored by the Python interpreter.
    # It is used to explain the code.
    """
    This is a docstring for the slugify_with_hints function.
    It provides information about the function's purpose, parameters,
    and return type.
    """
    cleaned = name.strip().lower()
    return cleaned.replace(" ", separator)


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
    pass


if __name__ == "__main__":
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

    print(
        project_function(
            "My Project",
            description="A sample project",
            tags=["python", "sample"],
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
