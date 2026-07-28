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


print(slugify("  Python is Awesome!  "))  # Output: python-is-awesome!
print(slugify("Python is Awesome!", separator="_"))  # Output:python_is_awesome!
print(slugify_with_hints("Slugify With Hints"))  # Output: slugify-with-hints
# Type hints are not enforced at runtime. Hence, the following call will not
# raise an error, but it may lead to unexpected behavior or runtime errors.
# print(slugify_with_hints(1, 3))

print(add_tag("python"))  # Output: ['python']
print(add_tag("javascript"))  # Output: ['javascript']
print(add_tag_with_default("python"))  # Output: ['python']
print(add_tag_with_default("javascript"))  # Output: ['python', 'javascript']
