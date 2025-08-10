<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

[![Pypi][pypi-img]][pypi-url]
[![CICD][cicd-img]][cicd]
[![Code Quality][quality-img]][quality-url]
[![Coverage][coverage-img]][coverage-url]



[contributors-shield]: https://img.shields.io/github/contributors/yaninsanity/django-user-starter.svg?style=for-the-badge
[contributors-url]: https://github.com/yaninsanity/django-user-starter/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/yaninsanity/django-user-starter.svg?style=for-the-badge
[forks-url]: https://github.com/yaninsanity/django-user-starter/forks
[stars-shield]: https://img.shields.io/github/stars/yaninsanity/django-user-starter.svg?style=for-the-badge
[stars-url]: https://github.com/yaninsanity/django-user-starter/stargazers
[issues-shield]: https://img.shields.io/github/issues/yaninsanity/django-user-starter.svg?style=for-the-badge
[issues-url]: https://github.com/yaninsanity/django-user-starter/issues
[license-shield]: https://img.shields.io/github/license/yaninsanity/django-user-starter.svg?style=for-the-badge
[license-url]: https://github.com/yaninsanity/django-user-starter/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/zerenyan/
[pypi-img]: https://badge.fury.io/py/django-user-starter.svg
[cicd-img]: https://github.com/yaninsanity/django-user-starter/actions/workflows/deploy.yml/badge.svg
[quality-img]: https://github.com/yaninsanity/django-user-starter/actions/workflows/quality.yml/badge.svg
[coverage-img]: https://img.shields.io/badge/coverage-91%25-brightgreen
[pypi-url]: https://pypi.org/project/django-user-starter/
[cicd]: https://github.com/yaninsanity/django-user-starter/actions/workflows/deploy.yml
[quality-url]: https://github.com/yaninsanity/django-user-starter/actions/workflows/quality.yml
[coverage-url]: https://github.com/yaninsanity/django-user-starter/actions/workflows/quality.yml






# Project Detail
This repository contains two shell scripts (`starter-en.sh` && `starter-zh.sh`) that automates the setup of a Django project with a custom user system and integrates django-avatar for avatar management. The script is designed to simplify the process of creating a Django project with common configurations, including user authentication, avatar management, and basic templates.

# Features
- **Python3 Check**: Ensures Python3 is installed before proceeding.
- **Virtual Environment**: Creates and activates a virtual environment.
- **Dependencies Installation**: Installs Django, django-avatar, Pillow, and now also django-jazzmin via requirements.txt.
- **Interactive Setup**: Prompts for project and app names.
- **Custom User Model**: Optionally creates a custom user model with additional fields (bio, birth_date, phone, address, role). The avatar field is intentionally omitted to avoid conflicts with django-avatar.
- **Admin Configuration**: Configures the Django admin to support the custom user model.
- **Basic Views and Templates**: Generates login, logout, register, and homepage views with corresponding templates.
- **URL Configuration**: Sets up URL routing for the admin, avatar, and user app.
- **Database Migrations**: Runs initial database migrations.
- **Superuser Creation**: Optionally creates a superuser for the Django admin.


# Distribution & CI/CD
Our CI/CD pipeline automatically publishes releases to [TestPyPI](https://test.pypi.org/project/django-user-starter/) and [PyPI](https://pypi.org/project/django-user-starter/) based on semantic commits!

## Automated Release Features
- **Semantic Versioning**: Uses conventional commits (`feat:`, `fix:`, `feat!:`) to automatically determine version bumps
- **Automatic Publishing**: 
  - `dev` branch → TestPyPI (snapshot releases)
  - `main` branch → PyPI (stable releases)
  - PR merges to `main` → Automatic release
- **Skip Release**: Add `[skip-release]` to commit messages to prevent publishing
- **Zero Manual Work**: Just commit with proper format and push!

# CLI Quick Start
For an even quicker start, install the package via pip and use the CLI entry points:
- **English CLI**:  
  `django-starter-en = "django_user_starter.cli:main_en"`
- **中文 CLI**:  
  `django-starter-zh = "django_user_starter.cli:main_zh"`

To launch the English version, simply run🚀🚀🚀:
```bash
django-starter-en
```
中文版 快速启动🚀🚀🚀 
```bash
django-starter-zh
```
# Prerequisites
Python3: Ensure Python3 is installed on your system.

Bash: The scripts are designed for Unix-like systems (Linux, macOS).

# Getting Started
Clone the Repository:

```bash
git clone https://github.com/yaninsanity/django-user-starter
cd django-user-starter
```
Make the Script Executable:

```bash
chmod +x starter-en.sh
# Run the Script, run with English Prompt
sh starter-en.sh
# Run the Script, run with Chinese Prompt
chmod +x starter-zh.sh
sh starter-zh.sh
```

## Follow the Prompt Flow

Enter the virtual environment directory name (default: venv).

Enter the Django project name (default: myproject).

Enter the user system app name (default: users).

Choose whether to create a custom user model (default: y).

Optionally create a superuser (default: y).

Start the Development Server:

```bash
source venv/bin/activate
python3 <myproject>/manage.py runserver
```

## Access the Project:

Admin Panel: http://localhost:8000/admin/

Homepage: http://localhost:8000/

Login Page: http://localhost:8000/users/login/

Register Page: http://localhost:8000/users/register/

## Custom User Model
If you choose to create a custom user model, the script will generate a CustomUser model with the following fields:

bio: A text field for the user's biography.

birth_date: A date field for the user's birth date.

phone: A character field for the user's phone number.

address: A text field for the user's address.

role: A character field for the user's role (e.g., admin, editor).

The avatar field is intentionally omitted to avoid conflicts with django-avatar.

## Templates
The script generates the following templates:

Login Template: users/templates/users/login.html

Register Template: users/templates/users/register.html

Homepage Template: templates/home.html

These templates are basic and can be customized further as needed.

## Media Files
The script configures MEDIA_URL and MEDIA_ROOT in settings.py to handle media files, which are required by django-avatar for avatar management.


## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request. Any contributions, whether bug fixes, feature additions, or documentation improvements, are welcome.

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yaninsanity/django-user-starter.git
   cd django-user-starter
   ```

2. **Set up development environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   make install-dev PYTHON=.venv/bin/python
   ```

3. **Run code quality checks:**
   ```bash
   make lint PYTHON=.venv/bin/python      # Check code style
   make format PYTHON=.venv/bin/python    # Format code
   make test PYTHON=.venv/bin/python      # Run tests
   ```

4. **Build package:**
   ```bash
   make build PYTHON=.venv/bin/python
   ```

### Code Standards
- **Code Formatting**: We use `black` and `isort` for consistent code formatting
- **Linting**: We use `flake8` for code linting
- **Testing**: We use `pytest` for testing with coverage reporting
- **Security**: We use `bandit` and `safety` for security scanning
- **Version Control**: We use semantic versioning with `python-semantic-release`

### Commit Convention
This project follows conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

**Automatic Release Examples**:
- `fix: resolve login issue` → Patch release (0.1.7 → 0.1.8)
- `feat: add new authentication` → Minor release (0.1.7 → 0.2.0)
- `feat!: breaking API changes` → Major release (0.1.7 → 1.0.0)
- `chore: update docs [skip-release]` → No release

## Test Snapshot
To test the latest development version, push to the `dev` branch which automatically publishes timestamped snapshots to TestPyPI:

```bash
pip install -i https://test.pypi.org/simple/ django-user-starter --extra-index-url https://pypi.org/simple
```

For a specific dev version (format: `0.1.7.dev20250809143000`):
```bash
pip install -i https://test.pypi.org/simple/ django-user-starter==0.1.7.dev20250809143000 --extra-index-url https://pypi.org/simple
```

<b>Note:</b> Dev versions use timestamp format and are automatically generated from the `dev` branch.

## Semantic Version Control
Current project is using a tool called "python-semantic-release", which will auto detect the commit pattern from following list to adjust project version.

PSR attempts to support all variants of issue closure text prefixes, but not all will work for your VCS. PSR supports the following case-insensitive prefixes and their conjugations (plural, present, & past tense):

- close (closes, closing, closed)

- fix (fixes, fixing, fixed)

- resolve (resolves, resolving, resolved)

- implement (implements, implementing, implemented)

PSR also allows for a more flexible approach to identifying more than one issue number without the need of extra git trailers (although PSR does support multiple git trailers). PSR support various list formats which can be used to identify more than one issue in a list. This format will not necessarily work on your VCS. PSR currently support the following list formats:

- comma-separated (ex. Closes: #123, #456, #789)

- space-separated (ex. resolve: #123 #456 #789)

- semicolon-separated (ex. Fixes: #123; #456; #789)

- slash-separated (ex. close: #123/#456/#789)

- ampersand-separated (ex. Implement: #123 & #789)

- and-separated (ex. Resolve: #123 and #456 and #789)

- mixed (ex. Closed: #123, #456, and #789 or Fixes: #123, #456 & #789)

For more details you can find from [PSR commit parsing document](https://python-semantic-release.readthedocs.io/en/latest/commit_parsing.html)
## Local Build 

For local development and testing:

```bash
# Install development dependencies
make install-dev PYTHON=.venv/bin/python

# Run all quality checks
make lint test PYTHON=.venv/bin/python

# Build the package
make build PYTHON=.venv/bin/python
```

Or manually with virtual environment:
```bash
.venv/bin/pip install --upgrade pip build twine
.venv/bin/python -m build
.venv/bin/twine check dist/*
```


## License
This project is licensed under the MIT License. See the LICENSE file for details.
