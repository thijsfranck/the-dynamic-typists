# How to Contribute

To ensure a smooth collaboration, we have outlined some guidelines to follow when making contributions. Your adherence to these guidelines helps us maintain the quality and clarity of the project.

## Getting Started

See the [installation](./README.md#installation) section of the README on how to get started with this repository.

## Branching

Always create a new branch for your changes. This makes it easier to handle multiple contributions simultaneously.

1. Pull the latest changes from the main branch:

```bash
git pull main
```

2. Create a new branch. Name it descriptively:

```bash
git checkout -b BRANCH_NAME
```

3. Push the branch to the repository:

```bash
git push -u origin BRANCH_NAME
```

## Pull Requests

1. **Creating a Pull Request**: Once you've pushed your branch, navigate to the GitHub repository page and click on the "Pull request" button. Make sure the "base" repository is the main branch and the "compare" branch is the one you've just pushed.

2. **Describe Your Changes**: In the pull request description, explain the changes you've made, any related issues, and provide any additional information or screenshots that might be necessary.

3. **Required Approvals**: Before merging, your pull request must be reviewed and approved by at least one other team member.

4. **Checks**: Ensure that all checks (like CI tests) are passing. If they're not, understand why and make the necessary changes.

## Commit Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or fewer.
- Describe what you did in the commit, why you did it, and how, in the commit details.

## Code Documentation

Good code documentation aids understanding and speeds up the development process. It also helps boost our final score 😁. For consistency and clarity, we've chosen to use numpy-style docstrings. When documenting your code, please adhere to this style. You can find a complete set of examples in this [style guide](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html).

### Basic Guidelines

Always document the following elements of your code:

1. **Classes**: including their **attributes and public methods**
2. **Module-level functions and constants**

For classes, functions, and methods, docstrings should start on the line directly below the signature, at the first indent level. For attributes and constants, docstrings should start on the first line after their declaration. Use triple double quotes (`"""`) to enclose your docstrings.

Python type annotations in the function or method signatures are encouraged for clarity. When using type annotations in the signature, it's not necessary to repeat the type in the docstring.

Your docstrings should include these sections in the following order (if applicable):

1. One-line summary
2. Detailed functional description (can span multiple lines, separated by a blank line from the one-line summary)
3. Parameters
4. Returns
5. Raises
6. Examples

For reference, here's a complete example of a function docstring in numpy-style:

```python
def example_function(param1: int, param2: str):
    """One-line summary of the function.

    Detailed functional description of what the function does. Can span
    multiple lines.

    Parameters
    ----------
    param1 : int
        Description of the first parameter.
    param2 : str
        Description of the second parameter.

    Returns
    -------
    bool
        Description of the return value.

    Raises
    ------
    ValueError
        Description of the error.

    Examples
    --------
    >>> example_function(1, "test")
    True
    """
    return True
```

For classes and attributes:

```python
class Example:
    """Class-level docstring describing the class."""

    attribute: int
    """Description of the class attribute."""
```

Prioritize documenting public methods and attributes (those not starting with an underscore). However, private methods with complex logic should also be documented for clarity.

## Unit Testing

Unit tests are key to our success, since they allow us to catch bugs early, run sections of code in isolation, and accelerate our development pace. We use the `unittest` framework for writing and running our tests.

### Basic Guidelines

Test modules should be located in the same directory as the module they cover. Test modules should be named `test__*.py` (e.g.,` test__math_ops.py`). Individual test methods within those modules should be prefixed with `test__` (e.g., `test__my_function`). See the example below:

```
project_root/
├── utils/
│   ├── __init__.py
│   ├── math_ops.py
│   └── test__math_ops.py
├── main.py
└── ...
```

As a general rule, unit tests should cover the following aspects of your code:

- Input validation
- Validation of output (or outcome) given a particular input
- Error handling

### Unit Testing and Type Hints

You can reduce the need for unit tests by indicating the expected types of input arguments and return values as type hints. While they don't replace unit tests, type hints can reduce the number of tests you might need to write, particularly those related to input validation.

For instance, consider the following function without type hints:

```python
def add(a, b):
    return a + b
```

Without type hints, you might write multiple tests to ensure that the function behaves correctly with different types of input, like strings, integers, or floats. But with type hints:

```python
def add(a: int, b: int) -> int:
    return a + b
```

The function's expected behavior is clearer. You know that both `a` and `b` should be integers, and the return value will also be an integer. With these type hints in place, there's less need to write unit tests checking for behaviors with non-integer inputs since the static type checker can catch those mistakes for you.

### Writing Tests

1. **Import Dependencies**: Start by importing `unittest` and the module, class or function you're testing.
2. **Create Test Cases**: For each set of related tests, create a class that inherits from `unittest.TestCase`.
3. **SetUp and TearDown**: Use `setUp` and `tearDown` methods to define instructions that will be executed before and after each test method, respectively.

### Running Tests

To run the tests, use the following command from the root of the project:

```bash
python -m unittest discover -p "test__*.py"
```

This command will discover and run all the tests that match the pattern `test__*.py`.

### Example

Suppose we have a function add in a module named `math_ops.py` located in the `utils` directory. Here's how the test might look:

```python
import unittest
from .math_ops import add

class Test__Addition(unittest.TestCase):

    def setUp(self):
        # Code that will run before each test method
        self.num1 = 3
        self.num2 = 2

    def test__addition(self):
        # Check if 3 + 2 equals 5
        self.assertEqual(add(self.num1, self.num2), 5)

    def tearDown(self):
        # Code that will run after each test method
        pass

if __name__ == '__main__':
    unittest.main()
```
