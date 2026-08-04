from dataclasses import dataclass

project_names = ["Payments API", "Developer Portal", "Ops Console"]

# Part 1: For Loops Into Comprehensions

# 1. Build a list of slugs from project names:
# slugs = []
# for name in project_names:
#     slugs.append(name.lower().replace(" ", "-"))

slugs = [name.lower().replace(" ", "-") for name in project_names]

print(f"Project names in slug format: {slugs}")

# 2. Build a list of titles for tasks that aren't done:

tasks = [
    {"title": "ship docs", "done": False},
    {"title": "cut release", "done": True},
    {"title": "announce launch", "done": False},
]

# open_titles = []
# for task in tasks:
#     if not task["done"]:
#         open_titles.append(task["title"])

open_titles = [task["title"] for task in tasks if not task["done"]]

print(f"Unfinished tasks: {open_titles}")

# Part 2: Raise and Catch an Exception


def validate_project_name(name):
    if name.strip() == "":
        raise ValueError("Project name cannot be blank.")
    return name.strip()


# Invalid call
try:
    print(validate_project_name("       "))
except ValueError as e:
    print(f"Caught ValueError: {e}")

# Valid call
try:
    print(validate_project_name("Valid Project Name"))
except ValueError as e:
    print(f"Caught ValueError: {e}")


# Part 3: A Simple Dataclass

@dataclass
class Project:
    name: str
    slug: str
    archived: bool = False

sample_project = Project("Sample Project", "sample-project")
print(sample_project)