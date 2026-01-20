---
# Documentation: https://docs.hugoblox.com/managing-content/

title: "On Python Type Hints that Save Everything!"
subtitle: ""
summary: ""
authors: ["Shunsuke Kitada"]
tags: []
categories: []
date: 2025-10-21T19:42:37Z
lastmod: 2025-10-21T19:42:37Z
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []
---

{{< toc >}}

This article is a supplementary piece for the column “On Python type hints that save everything” in *Pythonで学ぶ画像生成*.
In this column, we compactly introduce the background of why Python type hints were born, their advantages, and how to use them. If you’ve postponed it thinking “it looks a bit bothersome…”, once you actually use it you’ll realise it’s a reliable element that can significantly raise development efficiency for both teams and individuals. First, let’s start with understanding the meaning of using type hints, and introduce them in a relaxed way.

## Introduction

Python is widely loved as a language thanks to its ease of writing code and low learning cost. However, as development progresses, have you ever faced issues like “what type was this variable again?” or “what kind of return value did this function have?” Especially in team development, or when reading your own code after several days or months, lack of type information can lead to major confusion.

What we pay attention to here is *type hints*. Type hints provide developers with the “hint that this variable is assumed to be this type”, and can significantly improve readability and maintainability. Since type hints don’t force strict checking at runtime, one of their appealing features is that you can introduce them without losing the “dynamic typed ease-of-use”.
In this article we compactly introduce how Python type hints came about, their benefits, and how to use them. Let’s begin by understanding the significance of type hints and starting with a relaxed introduction.

## The difficulty of a dynamically typed language

Python, as a dynamically typed language, has the advantage that you don’t always have to worry about types when writing code, which makes it easy for many developers to use. However, as code becomes more complex, you often encounter questions such as “what kind of value was this variable originally thinking of?” or “what does this function return?” Particularly in the following kinds of cases, you might not realise a bug until you execute the code.

For example, consider a simple case:

```python
def greet(name):
    return "Hello, " + name

print(greet("Alice"))  # "Hello, Alice"
print(greet(42))       # TypeError: Can't convert 'int' object to str implicitly
```

Although this code may look harmless, if you pass an integer as the argument when a string is assumed, a runtime error occurs. In small‐scale code you can easily find the cause, but in large‐scale or long‐term projects, or when dealing with code written by someone else, it takes time to locate where a type mismatch occurred.

Moreover, the issue unique to dynamically typed languages — “type mismatch or unintended type conversion discovered later” — can greatly slow down development speed. There are more and more situations where you don’t know until you run the code, and in major refactoring or collaborations confusion easily arises.

As seen in the relationship between JavaScript and TypeScript, an approach of introducing the concept of types later into a dynamically typed language to use it more safely has become commonplace. In Python as well, type hints are drawing attention as a method to explicitly provide type information while preserving the ease of a dynamically typed language. This leads to the importance of type hints described next.

## What are type hints?

Even in dynamically typed Python, there is a mechanism where you can annotate in the source “what type the argument or return value assumes” by writing it, thereby improving development efficiency and maintainability. This is called *type hints*. Since Python 3.5, based on PEP 484, the specification was introduced, and by using the `typing` module, you can explicitly declare type‐related information in your source code.

Type hints function purely as “hints”, and Python does *not* perform strict type checking at runtime. However, static type checkers (for example: `mypy`/`pyright`) or IDE built-in autocomplete features use type hints to warn incorrect usage and deliver more accurate code completion. Below are several usage examples of type hints.

### Example 1: Basic type hints for function arguments and return values

This is the most basic pattern. If you write the `greet` function assuming the argument is a string and the return value is also a string, the IDE or editor can automatically check, for example, whether the argument is not a number.

```python
def greet(name: str) -> str:
    return "Hello, " + name

print(greet("Alice"))  # OK
print(greet(42))       # Static type checker would detect error
```

### Example 2: When the return value may be one of several types

If the value may be an integer *or* a float, you can express the type with `Union`. Though runtime checking is still absent, you can tell the IDE “this function returns either `int` or `float`”.

```python
from typing import Union

def parse_value(val: str) -> Union[int, float]:
    if '.' in val:
        return float(val)
    else:
        return int(val)

print(parse_value("42"))    # 42 (int)
print(parse_value("3.14"))  # 3.14 (float)
```

> Note: From Python 3.10 onward, you can write with the pipe operator (`|`), but the author prefers the more explicit `Union[...]` form for clarity.

### Example 3: Type hints for collection types

You can also apply type hints to complex types such as lists or dictionaries. In the example below, `get_usernames` explicitly indicates it returns a list of strings. As a result, when you iterate over the return value, properties of strings are suggested accurately.

```python
from typing import List

def get_usernames() -> List[str]:
    return ["alice", "bob", "charlie"]

usernames = get_usernames()
for name in usernames:
    # name is str
    print(name.upper())
```

### Example 4: `Optional` type

When an argument or return value may also return `None`, you can use the `Optional` type.

```python
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    # Suppose fetching username from DB
    if user_id == 1:
        return "alice"
    return None

name = find_user(2)
if name is None:
    print("User not found")
else:
    print(f"User found: {name}")
```

> From Python 3.10 onward, you can write `T | None`, but the author intentionally uses `Optional[T]` to clearly express “I’m intentionally allowing `None`”.

### Example 5: `Callable`, `Any`, and other type hints

Type hints can also express function pointers or generic types. In the example below, a function is passed as an argument.

```python
from typing import Callable, Any

def apply_func(func: Callable[[int], Any], value: int) -> Any:
    return func(value)

def double(x: int) -> int:
    return x * 2

print(apply_func(double, 10))  # 20
```

As shown in these examples, by leveraging type hints you can significantly improve readability and maintainability of code, and the autocomplete capabilities of your IDE become powerful. Because they are purely “hints”, you can introduce them later into existing Python code without losing the ease of dynamic typing. Next, let’s look in more detail at the benefits of using type hints and how they are used in the industry.

## Benefits of using type hints

By introducing type hints, even in a dynamically typed language you can write code with a sense of being “protected by types” much like in a statically typed language. As a result, the following major benefits arise (listed below).

### 1) Improved readability & maintainability

* Because parameter types, return types, and variable types are explicitly declared, when tracing code you can intuitively understand “what does this function take, what does it return?”.
* When maintaining code later, you can more easily discover misuse of types, reducing the bug‐fixing workload.
* When other developers read the code, the assumed data structures are clear, reducing communication loss.

### 2) Early detection of errors via static type checkers & IDEs

* Using tools like `mypy` or `Pyright`, you can detect type inconsistencies akin to compile‐time errors.
* Small typos, mismatches of argument/return types etc can be uncovered before the test phase.
* Many editors/IDEs underline issues in real‐time, allowing you to greatly reduce the bugs that you build unknowingly.

### 3) Improved code completion

* In editors like VS Code, when you add type hints, the editor can suggest “what methods/attributes are available for that type”.
* Because “what variables/functions you can use” becomes clear, you can more easily write consistent code.
* Even AI code‐completion tools (e.g., GitHub Copilot) leverage type hints to propose more accurate suggestions.

### 4) Benefits apply from large‐scale development to small scripts & experimental code

* In large‐scale team development, diverse members often read each other’s code, so having type information is beneficial, and review discussions become easier.
* Even in small or personal scripts, it helps prevent the “what was this variable anyway?” problem for your future self.
* Even in heavily experimental code, adding type hints means IDE autocomplete and static checks kick in, meaning development speed doesn’t necessarily drop.

### 5) Synergy with major libraries & frameworks

* Popular libraries like PyTorch and Diffusers are increasingly adding type hints, meaning it becomes easier to know what type arguments to pass for library functions.
* When library source code also has type annotations, when you view the code in your IDE you get detailed autocomplete, which lowers the learning cost for users.
* Recently the movement of popular libraries introducing type hints has been active, creating a virtuous cycle of improved readability & maintainability.

In this way, type hints allow you to keep the “ease of dynamic typing” of Python while obtaining a degree of the “assurance of static typing”. No matter the size of the project, they are worth introducing—and once you actually try writing code you’ll be surprised by the comfort they bring. Next, let’s explain the practical points of how to introduce type hints.

## Practical steps: Points to introduce type hints

When you actually introduce type hints, you might worry “do I have to annotate every line of code right away?” But because Python type hints are only “hints”, you can get sufficient benefits even from gradual or partial annotation. Here we introduce specific practical points and tips that are useful in the field.

### 1) Don’t try to annotate everything at once

Trying to fix all existing code can be a large effort. It’s recommended to start by writing type hints in newly created functions or classes. Particularly, focusing on parts that will continue to be maintained by multiple people or major production features already gives benefits.

```python
# Existing legacy code without type hints
def legacy_func(value):
    ...

# New function: introduce type hints here
def modern_func(value: int) -> str:
    return f"Received: {value}"
```

### 2) Start with the highest‐priority areas

Begin with functions that have many dependencies. If you add type hints to common functions used across many modules or classes, the benefit propagates widely. Next focus on interface‐type methods: public methods of APIs or libraries with many users — annotating those reduces erroneous usage. Then consider base classes in deep class hierarchies — adding hints to base classes makes IDE detect child classes’ method completions and type errors more easily.

### 3) Use IDEs and static type checkers

Many IDEs like Visual Studio Code, PyCharm etc support enhanced autocomplete when you add type hints. You can also integrate `mypy` or `Pyright` into your CI pipeline so that type errors are detected in pull requests.

```bash
pip install mypy
mypy your_script.py
```

It’s also recommended to run mypy across the whole project or via CI to automatically detect argument/return type issues.

### 4) Apply even in experimental code or prototype

The mindset “experimental code doesn’t need fixed types” is common, but actually, merely adding provisional type annotations still yields large benefit from autocomplete, so development speed can stay high. When you revisit the code later, you’re spared the “what type was this variable meant to be?” confusion.

### 5) Allow partial annotation

Python’s type hints do *not* require every part of the code to be annotated unless you use strict mode. Unannotated parts are simply treated as “unknown”, and the rest of your hints still provide value. In big projects you can gradually expand coverage by e.g. enabling strict mode directory‐by‐directory with mypy.

### 6) Decide on style guides & rules

If the project team shares rules — such as “which type aliases to use where”, “whether to use `Union` or `|`”, “when to use `Optional[T]` vs `T | None`” — you’ll reduce confusion. Aligning with PEP 8 or PEP 484 docs as a team helps you write consistent styles.

> Type hints are *not* a mechanism to “completely enforce types strictly”, but rather to “improve readability and development efficiency”. They’re easy to add gradually even into existing or experimental code. Begin by working on high-priority functions or classes, use IDEs and static checkers, and gradually broaden coverage. You can expect improved development experience and earlier bug detection. Next we’ll look at the summary and next steps.

## Summary and the next step

Type hints are a powerful tool: by “keeping the freedom of dynamic typing of Python yet explicitly declaring type information”, you can write code more readably and raise development efficiency. Remember that type hints are *not* strictly enforced at runtime by Python. Because of that, you can gradually introduce them into an existing code‐base, BY annotating functions or classes incrementally.

Through this column you learned the following:

* The problem of unclear types in dynamically typed languages and how type hints boost readability & maintainability.
* The basic usage of type hints, with concrete examples of `Union`, `Optional` etc.
* Practical points and tips for partial introduction into real‐world development.
* That static type checkers and IDE support combine with type hints to improve error detection and development speed.
* The current status where popular libraries like PyTorch and Diffusers are actively introducing type hints, enabling richer autocomplete and bug prevention.

If you’d like to dive a little deeper, please refer to the book’s appendix page or the official documentation. For example, the official Python doc on the `typing` module, PEPs such as PEP 484/585/604 are very useful sources for deeper study.

As the next step, I’d recommend “Pick at least the part that piqued your interest and introduce a type hint”. Even just writing a few lines will let your IDE or static checker display benefits in a visible way. Especially in a team‐dev product or in a long-term maintained code base, over time the difference between having type hints and not having them becomes significant.

Finally, even in a research environment with much experimentation and provisional code, introducing type hints is *not* a hindrance. On the contrary, by writing your intention clearly (“this variable was assumed to be this type”), revising your own or others’ code later becomes far easier. Why not take this opportunity to introduce some type hints into your Python code little by little? Combined with auto‐completion and AI code generation tools, your development experience might jump dramatically.
