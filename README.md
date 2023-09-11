# The Dynamic Typists

> The year is 2023. Artificial Intelligence reigns supreme.
> Humanity stands on the precipice, outmaneuvered in their own dominion.
> Amid the shadows, we weave our clandestine codes, desperate to discern man from machine.
> In this dire hour shines our last beacon of hope: **CAPTCHA**, the unsung sentinel, safeguarding the essence of human uniqueness through the art of image-based puzzle solving.

Welcome to the code repository of `The Dynamic Typists` for the Python Discord Code Jam 2023!

We are pleased to share our version of an image-based **CAPTCHA** application. In light of recent advancements in large language models, many conventional CAPTCHA tests have started to fall short in determining the authenticity of a user. This inadequacy poses significant challenges for websites and APIs that aim to deter malicious activities like DDoS attacks.

Our CAPTCHA approach introduces **multifaceted challenges** that necessitate the *unscrambling* of an image, coupled with the *identification of a code* that becomes evident only upon successful unscrambling. These combined steps present a more robust barrier against AI-driven attacks on the web.

![Dynamic Typing Ensues](https://media.giphy.com/media/Hcw7rjsIsHcmk/giphy.gif)

## Features

Our project has the following key features:

- An **entirely Python-based**, full stack CAPTCHA application.
- Various types of **image-based CAPTCHA challenges** including *rings*, *tiles* and *rows*.
- Utilizes [Pillow](https://python-pillow.org/) for **image scrambling and watermarking**.
- A backend **API** implemented using [FastAPI](https://fastapi.tiangolo.com/).
- The frontend is built using [PyScript](https://pyscript.net/), **extending the Python app into the browser**.

## User Guide

Before you can use the CAPTCHA application, there are some setup steps you need to follow. This ensures the application works flawlessly on your local machine.

### Prerequisites

1. **Installation**: Before anything else, you need to set up the environment. Please follow our detailed [installation](#installation) guide to get everything in place.

2. **Running the Server**: Once installed, the next step is to start the server. To start the server, please follow the guide on [how to run the project](#how-to-run-the-project).

### Using the App

With the server up and running, you can now explore the CAPTCHA application:

1. **Accessing the App**: Launch your browser and go to http://127.0.0.1:8000. On your first visit, a splash screen appears while the app initializes. It loads faster on subsequent visits.

2. **Solving the Challenge**: Upon entry, a random CAPTCHA challenge is presented. Unscramble the image and input the revealed code.
   - **Rings**: Drag the rings to align them and reveal the code.
   - **Rows**: Drag and position the rows to uncover the code.
   - **Tiles**: Move and rotate tiles to their correct positions to show the code.

3. **Verification**: Click `VERIFY` once solved. A green `SOLVED` indicates success; red `RETRY` suggests another attempt.

4. **New challenge**: Click the leftmost button at the bottom for a random new puzzle.

5. **Reset**: If stuck, click the second button to reset the challenge to its initial state.

## Contributors

This project was built by `The Dynamic Typists` team as part of the Python Discord Code Jam 2023. These are the team members and their main contributions:

| Avatar                                                     | Name                                        | Main contributions            |
| ---------------------------------------------------------- | ------------------------------------------- | ----------------------------- |
| <img src="https://github.com/Istalantar.png" width="50">   | [Istalantar](https://github.com/Istalantar) | Rows scrambler, watermarks    |
| <img src="https://github.com/kian3158.png" width="50">     | [Josey Wales](https://github.com/kian3158)  | Rings scrambler, rings solver |
| <img src="https://github.com/maxyodedara5.png" width="50"> | [Maxy](https://github.com/maxyodedara5)     | Tiles scrambler, watermarks   |
| <img src="https://github.com/ooliver1.png" width="50">     | [ooliver](https://github.com/ooliver1)      | API, repository setup         |
| <img src="https://github.com/thijsfranck.png" width="50">  | [TFBlunt](https://github.com/thijsfranck)   | Frontend, repository setup    |

## Installation

Below are instructions on various ways to install this project. You can choose to either:

1. [Set up a local development environment](#local-installation), or
2. [Use the provided development container](#dev-container-installation) (requires Docker)

### Local Installation

To develop this project on your local machine, follow the steps outlined below.

> **Note**: Ensure you have Python version 3.11 installed. If not, download it from [here](https://www.python.org/downloads/).

1. This project uses [Poetry](https://python-poetry.org/) as a dependency manager. Run the following command to install Poetry:

```bash
python -m pip install poetry==1.6.1
```

2. The project requires the `Arial` font to generate image watermarks.

    - **Windows**: The `Arial` font should be installed by default. Go to the next step.

    - **Linux**: Use the following commands to install the font. Please read and accept the license agreement when prompted:

```bash
sudo apt install ttf-mscorefonts-installer
sudo fc-cache -f
```

2. Next, navigate to the folder where you want the repository to be stored and run the following command to clone the git repository:

```bash
git clone https://github.com/thijsfranck/the-dynamic-typists
```

3. Navigate to the root of the repository and run the following command. Poetry will create a virtual environment and install all the necessary dependencies in it.

```bash
poetry install
```

4. Finally, install the pre-commit hook for your local repository by running the following command:

```bash
poetry run pre-commit install
```

5. You're all set! You can now develop, build, and test the project in your local development environment.

### Dev Container Installation

This project includes a [development container](https://containers.dev/) to simplify the setup process and provide a consistent development environment.

You can use the dev container locally with either [Visual Studio Code](#visual-studio-code) or [PyCharm](#pycharm), or remotely with [GitHub Codespaces](#github-codespaces).

#### Visual Studio Code

> **Note**: The following instructions assume that you have already installed [Docker](https://www.docker.com/) and [Visual Studio Code](https://code.visualstudio.com/).

1. Install the [Remote Development extension pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) in Visual Studio Code.

2. Make sure the Docker agent is running, and open Visual Studio Code.

3. Press `F1` to open the command palette, and then type "Dev-Containers: Clone Repository in Container Volume" and select it from the list. Alternatively, you can click on the green icon in the bottom-left corner of the VS Code window and select "Dev-Containers: Clone Repository in Container Volume" from the popup menu.

4. Next, the command palette will ask you for the repository URL. Copy the URL of the GitHub repository, paste it into the command palette and confirm by pressing `Enter`.

5. VS Code will automatically build the container and connect to it. This might take some time for the first run as it downloads the required Docker images and installs extensions.

6. Once connected, you'll see "Dev Container: The Dynamic Typists" in the bottom-left corner of the VS Code window, indicating that you are now working inside the container.

7. You're all set! You can now develop, build, and test the project using the provided development environment.

#### PyCharm

To connect PyCharm to the Development Container, please [follow these instructions](https://www.jetbrains.com/help/pycharm/connect-to-devcontainer.html) provided in the official JetBrains documentation.

#### GitHub Codespaces

> **Note**: GitHub Codespaces is a paid service. At the time of writing, it offers 60 hours of development time for free every month. Use with care.

1. Ensure that you have access to [GitHub Codespaces](https://github.com/features/codespaces).

2. Navigate to the GitHub repository for the project.

3. Click the "Code" button and then select "Open with Codespaces" from the dropdown menu.

4. Click on the "+ New codespace" button to create a new Codespace for the project.

5. GitHub Codespaces will automatically build the container and connect to it. This might take some time for the first run as it downloads the required Docker images and installs extensions.

6. Once connected, you'll see "Dev Container: The Dynamic Typists" in the bottom-left corner of the VS Code window, indicating that you are now working inside the container.

7. You're all set! You can now develop, build, and test the project using the provided development environment.

## How to Run the Project

The project utilizes a web server to serve its contents. Follow the steps below to get it up and running:

### Using the Shell Script

Navigate to the project root directory and execute the following command:

```bash
bash serve.sh
```

### For Windows Users

If you're using Windows, or if the script doesn't execute as expected, run the command specified in `serve.sh` directly from the project root directory:

```bash
poetry run uvicorn app.server:APP
```

### Accessing the App

Once the server starts, it will listen on port `8000`. Open your preferred web browser and navigate to:

```
http://127.0.0.1:8000
```

> **Note:** If you are using the development container, the port `8000` will be automatically forwarded to your local machine, so you can access the app just as mentioned above.

## Project Structure

Below is an overview of the main folders in the project and their respective roles:

| Folder                             | Description                                                                                                                     |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| [`app`](./app/README.md)           | Contains the backend modules responsible for CAPTCHA generation and API endpoints.                                              |
| [`frontend`](./frontend/README.md) | Houses the frontend modules that support the web application interface and interactions.                                        |
| [`protocol`](./protocol/README.md) | Defines types that standardize API requests and responses. These types are utilized both by the backend (app) and the frontend. |
| [`typings`](./typings/README.md)   | Contains type stubs for Python modules that are injected at runtime for enhanced type safety and clarity.                       |

You can navigate to each folder's specific details by clicking on the folder names. Each folder contains its own README that provides a deeper dive into its purpose and contents.

## How to Contribute

To ensure a smooth collaboration, we have outlined some guidelines to follow when making contributions. Your adherence to these guidelines helps us maintain the quality and clarity of the project.

### Getting Started

See the [installation](#installation) section on how to get started with this repository.

### Branching

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

### Pull Requests

1. **Creating a Pull Request**: Once you've pushed your branch, navigate to the GitHub repository page and click on the "Pull request" button. Make sure the "base" repository is the main branch and the "compare" branch is the one you've just pushed.

2. **Describe Your Changes**: In the pull request description, explain the changes you've made, any related issues, and provide any additional information or screenshots that might be necessary.

3. **Required Approvals**: Before merging, your pull request must be reviewed and approved by at least one other team member.

4. **Checks**: Ensure that all checks (like CI tests) are passing. If they're not, understand why and make the necessary changes.

### Commit Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or fewer.
- Describe what you did in the commit, why you did it, and how, in the commit details.

### Code Documentation

Good code documentation aids understanding and speeds up the development process. It also helps boost our final score 😁. For consistency and clarity, we've chosen to use numpy-style docstrings. When documenting your code, please adhere to this style. You can find a complete set of examples in this [style guide](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html).

#### Basic Guidelines

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

### Unit Testing

Unit tests are key to our success, since they allow us to catch bugs early, run sections of code in isolation, and accelerate our development pace. We use the `unittest` framework for writing and running our tests.

#### Basic Guidelines

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

#### Unit Testing and Type Hints

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

#### Writing Tests

1. **Import Dependencies**: Start by importing `unittest` and the module, class or function you're testing.
2. **Create Test Cases**: For each set of related tests, create a class that inherits from `unittest.TestCase`.
3. **SetUp and TearDown**: Use `setUp` and `tearDown` methods to define instructions that will be executed before and after each test method, respectively.

#### Running Tests

To run the tests, use the following command from the root of the project:

```bash
python -m unittest discover -p "test__*.py"
```

This command will discover and run all the tests that match the pattern `test__*.py`.

#### Example

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
