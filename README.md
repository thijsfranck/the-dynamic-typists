# The Dynamic Typists

This is the code repository of The Dynamic Typists team for the Python Discord Code Jam 2023!

![Dynamic Typing Ensues](https://media.giphy.com/media/Hcw7rjsIsHcmk/giphy.gif)

## Installation

Below are instructions on various ways to install this project.

### Local installation

To get started developing on this project using your local machine, please follow the steps below.

> **Note**: Ensure you have Python version 3.11 installed. If not, you can download it from [here](https://www.python.org/downloads/).

1. This project uses [Poetry](https://python-poetry.org/) as a dependency manager. Run the following command to install Poetry:

```bash
pip install poetry==1.6.1
```

> **Note**: If you're on a system where `pip3` is the designated command for Python 3, you might need to use `pip3` instead of `pip`.

2. Next, navigate to the folder where you want the repository to be stored and run the following command to clone the git repository:

```bash
git clone https://github.com/thijsfranck/the-dynamic-typists
```

3. Finally, navigate to the root of the repository and run the following command. Poetry will create a virtual environment and install all the necessary dependencies in it.

```bash
poetry install
```

4. You're all set! You can now develop, build, and test the project in your local development environment.

### Using the Dev Container

This project also includes a Visual Studio Code development container to simplify the setup process and provide a consistent development environment. You can use the dev container with either Visual Studio Code locally or with GitHub Codespaces.

#### Using the Dev Container with Visual Studio Code

> **Note**: The following instructions assume that you have already installed [Docker](https://www.docker.com/) and [Visual Studio Code](https://code.visualstudio.com/).

1. Install the [Remote Development extension pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) in Visual Studio Code.

2. Make sure the Docker agent is running, and open Visual Studio Code.

3. Press `F1` to open the command palette, and then type "Dev-Containers: Clone Repository in Container Volume" and select it from the list. Alternatively, you can click on the green icon in the bottom-left corner of the VS Code window and select "Dev-Containers: Clone Repository in Container Volume" from the popup menu.

4. Next, the command palette will ask you for the repository URL. Copy the URL of the GitHub repository, paste it into the command palette and confirm by pressing `Enter`.

5. VS Code will automatically build the container and connect to it. This might take some time for the first run as it downloads the required Docker images and installs extensions.

6. Once connected, you'll see "Dev Container: The Dynamic Typists" in the bottom-left corner of the VS Code window, indicating that you are now working inside the container.

7. You're all set! You can now develop, build, and test the project using the provided development environment.

#### Using the Dev Container with GitHub Codespaces

> **Note**: GitHub Codespaces is a paid service. At the time of writing, it offers 60 hours of development time for free every month. Use with care.

1. Ensure that you have access to [GitHub Codespaces](https://github.com/features/codespaces).

2. Navigate to the GitHub repository for the project.

3. Click the "Code" button and then select "Open with Codespaces" from the dropdown menu.

4. Click on the "+ New codespace" button to create a new Codespace for the project.

5. GitHub Codespaces will automatically build the container and connect to it. This might take some time for the first run as it downloads the required Docker images and installs extensions.

6. Once connected, you'll see "Dev Container: The Dynamic Typists" in the bottom-left corner of the VS Code window, indicating that you are now working inside the container.

7. You're all set! You can now develop, build, and test the project using the provided development environment.

## How to contribute

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