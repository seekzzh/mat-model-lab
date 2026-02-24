# Contributing Guide

Thank you for your interest in contributing to **Mat Model Lab**! We need your help to make this project better.

## 🌟 How to Contribute

You can contribute in several ways:

1.  **Report Bugs**: Found an error or crash? Please submit an Issue.
2.  **Suggest Features**: Have a great idea? Let us know.
3.  **Improve Documentation**: Fix typos or add clarifications.
4.  **Submit Code**: Fix bugs or implement new features.

## 🐛 Reporting Bugs

Before submitting a bug report, please search existing [Issues](https://github.com/seekzzh/mat-model-lab/issues) to avoid duplicates.

If it's a new bug, please create an Issue with the following information:

- **Title**: A concise description of the problem.
- **Environment**: OS (Windows/macOS/Linux), Python version, PyQt6 version.
- **Steps to Reproduce**: Detailed steps to reproduce the issue.
- **Expected Behavior**: What you expected to happen.
- **Actual Behavior**: What actually happened (include screenshots or error logs).

## 💡 Pull Requests

### 1. Development Environment Setup

```bash
# 1. Fork this repository and clone it locally
git clone https://github.com/yourusername/mat-model-lab.git
cd mat-model-lab

# 2. Create a virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### 2. Development Workflow

1.  **Create a Branch**: Create a new branch from `main`, with a name describing your changes (e.g., `fix-crash-on-load` or `feat-add-neohookean`).
    ```bash
    git checkout -b feat-new-feature
    ```
2.  **Make Changes**: Write code and ensure the application runs correctly.
    - Run the application to test: `python -m main`
    - Keep code style clean (follow PEP 8).
3.  **Commit Changes**: Commit messages should clearly describe what was done.
    ```bash
    git commit -m "feat: Add Neo-Hookean material model"
    ```
4.  **Push to GitHub**:
    ```bash
    git push origin feat-new-feature
    ```
5.  **Submit a PR**: Open a Pull Request on GitHub.

### 3. Code Conventions

- Use 4 spaces for indentation.
- Use `snake_case` for variables and functions, `CamelCase` for classes.
- Add comments for complex logic.
- Update relevant documentation if adding new features.

## 📄 License

By submitting code, you agree that your contributions will be licensed under the project's [GPLv3 License](LICENSE).
