# Contributing to Image Slicer

First off, thankyou for thinking about contributing to `image-slicer`! Any contribution, whether it's a bug report, a new feature, or an improvement to the documentation, is greatly appreciated.

## Development Setup

To get started, you'll need to have a recent version of Python installed. We recommend using a virtual environment to manage your dependencies.

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/image-slicer.git
    cd image-slicer
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    # Using venv
    python -m venv .venv
    source .venv/bin/activate

    # Or using uv
    uv venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**

    This project uses `uv` for package management, but you can also use `pip`.

    ```bash
    # Using uv
    uv pip install -e ".[dev]"

    # Or using pip
    pip install -e ".[dev]"
    ```

## Running Tests

We use `pytest` for testing. To run the test suite, simply run the following command:

```bash
pytest
```

## Code Style and Linting

We use `ruff` for linting and formatting. Before committing your changes, please make sure to run the linter:

```bash
# Check for linting errors
ruff check .

# Automatically fix formatting issues
ruff format .
```

## Submitting a Pull Request

1.  Create a new branch for your changes:
    ```bash
    git checkout -b my-feature-branch
    ```
2.  Make your changes and commit them with a clear and descriptive commit message.
3.  Push your branch to your fork on GitHub.
4.  Open a pull request to the `main` branch of the original repository.

Thank you for your contribution!
