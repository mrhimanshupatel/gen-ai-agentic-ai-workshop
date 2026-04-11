# Intermediate Python Core Concepts

> Reference guide for 6-month workshop (Sat/Sun, 3 hours/day)
> Last Updated: March 28, 2026

## Table of Contents
1. [Object-Oriented Programming](#object-oriented-programming)
2. [Advanced Data Structures](#advanced-data-structures)
3. [Functions & Decorators](#functions--decorators)
4. [Iterators & Generators](#iterators--generators)
5. [Context Managers](#context-managers)
6. [Error Handling](#error-handling)
7. [File I/O](#file-io)
8. [Modules & Packages](#modules--packages)
9. [Comprehensions](#comprehensions)
10. [Type Hints](#type-hints)
11. [Magic Methods](#magic-methods)
12. [Advanced Topics](#advanced-topics)

---

## Object-Oriented Programming

### Classes and Objects
```python
class Person:
    # Class variable (shared by all instances)
    species = "Homo sapiens"
    
    def __init__(self, name, age):
        # Instance variables
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hello, I'm {self.name}"
    
    @classmethod
    def from_birth_year(cls, name, birth_year):
        age = 2026 - birth_year
        return cls(name, age)
    
    @staticmethod
    def is_adult(age):
        return age >= 18

# Usage
p1 = Person("Alice", 30)
p2 = Person.from_birth_year("Bob", 1995)
```

### Inheritance
```python
class Employee(Person):
    def __init__(self, name, age, employee_id):
        super().__init__(name, age)  # Call parent constructor
        self.employee_id = employee_id
    
    def greet(self):  # Method overriding
        return f"{super().greet()}, ID: {self.employee_id}"

class Manager(Employee):
    def __init__(self, name, age, employee_id, team_size):
        super().__init__(name, age, employee_id)
        self.team_size = team_size
```

### Encapsulation
```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # Private attribute
    
    @property
    def balance(self):  # Getter
        return self.__balance
    
    @balance.setter
    def balance(self, amount):  # Setter
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self.__balance = amount
    
    def deposit(self, amount):
        self.__balance += amount

# Usage
account = BankAccount(1000)
print(account.balance)  # 1000
account.balance = 1500  # Uses setter
```

### Polymorphism
```python
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

def animal_sound(animal):
    return animal.speak()

# Same method name, different behavior
print(animal_sound(Dog()))  # Woof!
print(animal_sound(Cat()))  # Meow!
```

---

## Advanced Data Structures

### Collections Module
```python
from collections import defaultdict, Counter, deque, namedtuple

# defaultdict - no KeyError
word_count = defaultdict(int)
word_count['apple'] += 1  # No need to initialize

# Counter - counting elements
colors = ['red', 'blue', 'red', 'green', 'blue', 'blue']
counter = Counter(colors)
print(counter.most_common(2))  # [('blue', 3), ('red', 2)]

# deque - efficient append/pop from both ends
queue = deque([1, 2, 3])
queue.appendleft(0)  # [0, 1, 2, 3]
queue.pop()  # [0, 1, 2]

# namedtuple - lightweight class
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
print(p.x, p.y)  # 10 20
```

### Sets and Frozensets
```python
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

# Set operations
union = set1 | set2          # {1, 2, 3, 4, 5, 6}
intersection = set1 & set2   # {3, 4}
difference = set1 - set2     # {1, 2}
symmetric_diff = set1 ^ set2 # {1, 2, 5, 6}

# Frozenset - immutable set
fs = frozenset([1, 2, 3])  # Can be used as dict key
```

---

## Functions & Decorators

### Lambda Functions
```python
# Simple lambda
square = lambda x: x ** 2

# With map, filter, reduce
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))

from functools import reduce
sum_all = reduce(lambda x, y: x + y, numbers)  # 15
```

### Decorators
```python
# Simple decorator
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end-start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)
    return "Done"

# Decorator with arguments
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello():
    print("Hello!")
```

### Args and Kwargs
```python
def func_with_args(*args, **kwargs):
    print("Positional:", args)      # tuple
    print("Keyword:", kwargs)        # dict

func_with_args(1, 2, 3, name="Alice", age=30)
# Positional: (1, 2, 3)
# Keyword: {'name': 'Alice', 'age': 30}

# Unpacking
numbers = [1, 2, 3]
print(*numbers)  # 1 2 3

data = {'name': 'Bob', 'age': 25}
func_with_args(**data)  # Unpacks dict as kwargs
```

---

## Iterators & Generators

### Custom Iterator
```python
class Countdown:
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

# Usage
for num in Countdown(5):
    print(num)  # 5, 4, 3, 2, 1
```

### Generators
```python
# Generator function
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Usage
for num in fibonacci(10):
    print(num, end=' ')  # 0 1 1 2 3 5 8 13 21 34

# Generator expression
squares = (x ** 2 for x in range(10))
print(next(squares))  # 0
print(next(squares))  # 1

# Memory efficient
import sys
list_comp = [x for x in range(10000)]
gen_exp = (x for x in range(10000))
print(sys.getsizeof(list_comp))  # Large
print(sys.getsizeof(gen_exp))    # Small
```

---

## Context Managers

### Using Context Managers
```python
# File handling
with open('file.txt', 'r') as f:
    content = f.read()
# File automatically closed

# Multiple context managers
with open('input.txt', 'r') as infile, open('output.txt', 'w') as outfile:
    outfile.write(infile.read())
```

### Creating Context Managers
```python
# Using __enter__ and __exit__
class DatabaseConnection:
    def __enter__(self):
        print("Opening connection")
        self.conn = "Connected"
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing connection")
        return False  # Propagate exceptions

with DatabaseConnection() as conn:
    print(f"Using {conn}")

# Using contextlib
from contextlib import contextmanager

@contextmanager
def file_manager(filename, mode):
    try:
        f = open(filename, mode)
        yield f
    finally:
        f.close()

with file_manager('test.txt', 'w') as f:
    f.write("Hello World")
```

---

## Error Handling

### Exception Handling
```python
# Try-except-else-finally
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
except (TypeError, ValueError):
    print("Type or Value error")
except Exception as e:  # Catch all
    print(f"Unexpected: {e}")
else:
    print("No exceptions occurred")
finally:
    print("Always executed")
```

### Custom Exceptions
```python
class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Balance {balance} insufficient for {amount}")

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount

try:
    withdraw(100, 150)
except InsufficientFundsError as e:
    print(e)
```

### Assertions
```python
def divide(a, b):
    assert b != 0, "Divisor cannot be zero"
    return a / b

# Use for debugging, not production error handling
```

---

## File I/O

### Reading Files
```python
# Read entire file
with open('file.txt', 'r') as f:
    content = f.read()

# Read line by line
with open('file.txt', 'r') as f:
    for line in f:
        print(line.strip())

# Read all lines into list
with open('file.txt', 'r') as f:
    lines = f.readlines()
```

### Writing Files
```python
# Write (overwrite)
with open('file.txt', 'w') as f:
    f.write("Hello World\n")
    f.writelines(['Line 1\n', 'Line 2\n'])

# Append
with open('file.txt', 'a') as f:
    f.write("New line\n")
```

### Working with Paths
```python
from pathlib import Path

# Path operations
path = Path('data/file.txt')
print(path.exists())
print(path.is_file())
print(path.parent)
print(path.name)
print(path.suffix)

# Create directory
Path('new_folder').mkdir(parents=True, exist_ok=True)

# List files
for file in Path('.').glob('*.py'):
    print(file)
```

---

## Modules & Packages

### Creating a Module
```python
# mymodule.py
PI = 3.14159

def circle_area(radius):
    return PI * radius ** 2

class Circle:
    def __init__(self, radius):
        self.radius = radius

# Using the module
import mymodule
print(mymodule.circle_area(5))

from mymodule import Circle, PI
c = Circle(10)
```

### Package Structure
```
mypackage/
    __init__.py
    module1.py
    module2.py
    subpackage/
        __init__.py
        module3.py
```

### Import Types
```python
import math                      # Import module
from math import sqrt           # Import specific item
from math import *              # Import all (avoid!)
import numpy as np              # Alias
from . import module1           # Relative import
from ..package import module    # Parent package
```

---

## Comprehensions

### List Comprehensions
```python
# Basic
squares = [x ** 2 for x in range(10)]

# With condition
evens = [x for x in range(10) if x % 2 == 0]

# Nested
matrix = [[i + j for j in range(3)] for i in range(3)]

# Flatten
nested = [[1, 2], [3, 4], [5, 6]]
flat = [item for sublist in nested for item in sublist]
```

### Dict Comprehensions
```python
# Basic
squares_dict = {x: x ** 2 for x in range(5)}

# From two lists
keys = ['a', 'b', 'c']
values = [1, 2, 3]
d = {k: v for k, v in zip(keys, values)}

# Swap keys and values
original = {'a': 1, 'b': 2}
swapped = {v: k for k, v in original.items()}
```

### Set Comprehensions
```python
# Unique squares
unique_squares = {x ** 2 for x in [1, -1, 2, -2]}  # {1, 4}

# Filter duplicates
numbers = [1, 2, 2, 3, 3, 4]
unique = {x for x in numbers}
```

---

## Type Hints

### Basic Type Hints
```python
from typing import List, Dict, Tuple, Optional, Union, Any

def greet(name: str) -> str:
    return f"Hello, {name}"

def add_numbers(a: int, b: int) -> int:
    return a + b

# Collections
def process_items(items: List[int]) -> Dict[str, int]:
    return {'sum': sum(items), 'count': len(items)}

# Optional (can be None)
def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Alice"
    return None

# Union (multiple types)
def process_data(data: Union[int, str]) -> str:
    return str(data)

# Any (any type)
def flexible_function(param: Any) -> Any:
    return param
```

### Advanced Type Hints
```python
from typing import Callable, TypeVar, Generic

# Callable
def apply_operation(x: int, func: Callable[[int], int]) -> int:
    return func(x)

# TypeVar for generics
T = TypeVar('T')

def first_item(items: List[T]) -> T:
    return items[0]

# Generic class
class Stack(Generic[T]):
    def __init__(self):
        self.items: List[T] = []
    
    def push(self, item: T) -> None:
        self.items.append(item)
    
    def pop(self) -> T:
        return self.items.pop()
```

---

## Magic Methods

### Common Dunder Methods
```python
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages
    
    def __str__(self):
        # String representation for users
        return f"'{self.title}' ({self.pages} pages)"
    
    def __repr__(self):
        # String representation for developers
        return f"Book('{self.title}', {self.pages})"
    
    def __len__(self):
        # len(book)
        return self.pages
    
    def __eq__(self, other):
        # book1 == book2
        return self.title == other.title
    
    def __lt__(self, other):
        # book1 < book2
        return self.pages < other.pages
    
    def __add__(self, other):
        # book1 + book2
        return Book(
            f"{self.title} & {other.title}",
            self.pages + other.pages
        )
    
    def __getitem__(self, key):
        # book[key]
        return f"Page {key}"
    
    def __call__(self):
        # book() - make object callable
        return f"Reading: {self.title}"

# Usage
book = Book("Python Guide", 300)
print(len(book))      # 300
print(book())         # Reading: Python Guide
print(book[10])       # Page 10
```

---

## Advanced Topics

### List Slicing
```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Basic slicing [start:stop:step]
print(numbers[2:5])      # [2, 3, 4]
print(numbers[:5])       # [0, 1, 2, 3, 4]
print(numbers[5:])       # [5, 6, 7, 8, 9]
print(numbers[::2])      # [0, 2, 4, 6, 8]
print(numbers[::-1])     # Reverse
print(numbers[-3:])      # Last 3 elements
```

### Enumerate and Zip
```python
# enumerate - get index and value
fruits = ['apple', 'banana', 'cherry']
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

# zip - combine iterables
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(f"{name} is {age}")

# Unzip
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]
numbers, letters = zip(*pairs)
```

### Virtual Environments
```bash
# Using venv
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Mac/Linux

# Using uv (modern approach)
uv venv
uv sync
uv add package-name
```

### Common Built-in Functions
```python
# any() and all()
all([True, True, True])   # True
any([False, False, True]) # True

# sorted() with key
students = [('Alice', 25), ('Bob', 20), ('Charlie', 30)]
sorted(students, key=lambda x: x[1])  # Sort by age

# reversed()
for x in reversed(range(5)):
    print(x)  # 4, 3, 2, 1, 0

# map(), filter()
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
```

### F-Strings (Formatted Strings)
```python
name = "Alice"
age = 30
price = 19.99

# Basic formatting
print(f"Hello, {name}")

# Expressions
print(f"{name} will be {age + 1} next year")

# Formatting numbers
print(f"Price: ${price:.2f}")  # $19.99
print(f"{100:05d}")            # 00100

# Alignment
print(f"{name:>10}")  # Right align
print(f"{name:<10}")  # Left align
print(f"{name:^10}")  # Center

# Debug formatting (Python 3.8+)
print(f"{name=}")  # name='Alice'
```

---

## Best Practices

### Code Style (PEP 8)
- Use 4 spaces for indentation
- Max line length: 79 characters
- Use snake_case for functions and variables
- Use PascalCase for classes
- Meaningful variable names
- Add docstrings to functions/classes

### Documentation
```python
def calculate_area(radius: float) -> float:
    """
    Calculate the area of a circle.
    
    Args:
        radius (float): The radius of the circle
        
    Returns:
        float: The area of the circle
        
    Raises:
        ValueError: If radius is negative
        
    Example:
        >>> calculate_area(5)
        78.53981633974483
    """
    if radius < 0:
        raise ValueError("Radius cannot be negative")
    return 3.14159 * radius ** 2
```

### Testing with pytest
```python
# test_calculator.py
import pytest

def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_add_with_floats():
    assert add(2.5, 3.5) == 6.0

# Run: pytest test_calculator.py
```

---

## Essential Libraries to Know

- **NumPy**: Numerical computing, arrays
- **Pandas**: Data manipulation and analysis
- **Matplotlib/Seaborn**: Data visualization
- **Requests**: HTTP requests
- **pytest**: Testing framework
- **FastAPI/Flask**: Web frameworks
- **SQLAlchemy**: Database ORM
- **BeautifulSoup**: Web scraping

---

## Practice Resources

1. **LeetCode/HackerRank**: Coding challenges
2. **Real Python**: Tutorials and articles
3. **Python Docs**: Official documentation
4. **GitHub**: Read and contribute to open source
5. **Project Euler**: Mathematical problems

---

## Quick Reference Commands

```bash
# Check Python version
python --version

# Install package
pip install package-name
uv add package-name

# Run script
python script.py
uv run script.py

# Interactive Python
python
ipython

# Format code
black script.py

# Lint code
pylint script.py
flake8 script.py

# Type checking
mypy script.py
```

---

**Note**: This is a living document. Update as you learn new concepts during the workshop!
