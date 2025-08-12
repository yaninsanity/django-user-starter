# Contributing to Django User Starter

## Development Workflow

### Branch Strategy
- **main**: Production releases with semantic versioning
- **develop**: Development snapshots to TestPyPI
- **feature/***: Feature development branches

### Semantic Versioning

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for automatic semantic versioning:

#### Commit Message Format
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Types
- **feat**: New feature (MINOR version)
- **fix**: Bug fix (PATCH version)
- **perf**: Performance improvement (PATCH version)
- **docs**: Documentation changes (no version bump)
- **style**: Code style changes (no version bump)
- **refactor**: Code refactoring (no version bump)
- **test**: Test changes (no version bump)
- **build**: Build system changes (no version bump)
- **ci**: CI configuration changes (no version bump)
- **chore**: Maintenance tasks (no version bump)

#### Breaking Changes
Add `BREAKING CHANGE:` in the footer or `!` after type for MAJOR version:
```
feat!: remove deprecated API endpoint

BREAKING CHANGE: The old /api/v1/users endpoint has been removed
```

### Release Process

1. **Development**: Work on `develop` branch
   - Pushes trigger TestPyPI uploads with dev versions
   - Format: `1.2.3.dev20240101120000`

2. **Production**: Merge to `main` branch
   - Automatic semantic versioning
   - PyPI release
   - GitHub release with changelog

### Example Workflow

```bash
# Feature development
git checkout -b feature/new-awesome-feature develop
git commit -m "feat: add awesome new feature"
git push origin feature/new-awesome-feature

# Create PR to develop -> TestPyPI snapshot
# Create PR to main -> Production release
```

## Local Development

### Setup
```bash
git clone https://github.com/yaninsanity/django-user-starter.git
cd django-user-starter
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Quality Checks
```bash
black django_user_starter/ tests/
isort django_user_starter/ tests/
flake8 django_user_starter/ tests/
mypy django_user_starter/
bandit -r django_user_starter/
pytest --cov=django_user_starter
```

### Pre-commit Hooks
```bash
pre-commit install
pre-commit run --all-files
```

## Testing

- Maintain >80% test coverage
- All tests must pass on Python 3.9+
- Add tests for new features
- Update tests for bug fixes

## Documentation

- Update README.md for user-facing changes
- Add docstrings for public APIs
- Update CHANGELOG.md (automated via semantic-release)

## Questions?

Open an issue for questions, bug reports, or feature requests.
