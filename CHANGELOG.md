# CHANGELOG

## v1.0.0 (2025-08-09) - MAJOR REFACTOR

### 🚀 Breaking Changes

- **Complete architecture rewrite** - Replaced complex template system with simple string replacement
- **Removed all bloat** - Eliminated 90% of redundant files and complex enterprise naming
- **New clean CLI** - Simple, focused command-line interface without confusing options
- **No more template errors** - Fixed all Jinja2 rendering issues by removing templates entirely

### ✨ Features

- **Simple string-based generation** - No more complex template engine, just clean string replacement
- **Flexible database support** - SQLite, PostgreSQL, MySQL with environment-based configuration
- **Optional REST API** - Clean DRF integration when needed
- **Smart Docker support** - Optimized Dockerfiles with proper security and multi-stage builds
- **Docker Compose included** - Ready-to-use development environment
- **Clean project structure** - Only generates necessary files, no bloat

### 🗑️ Removed

- Complex Jinja2 templates (source of all rendering errors)
- Enterprise-grade naming and unnecessary complexity
- Redundant configuration files
- Examples folder and test pollution files
- Complex CLI with too many options

### 📁 New Structure

```
django_user_starter/
├── __init__.py
├── _version.py
├── cli.py          # Clean, simple CLI
├── generator.py    # String-based generator
└── requirements.txt
```

### 🎯 Usage

```bash
# Basic project
django-starter myproject

# With PostgreSQL and API
django-starter webapp --database postgresql --api

# MySQL without Docker
django-starter blog --database mysql --no-docker
```

---

## v0.2.0 (2025-08-10)

### Bug Fixes

- Improve CI/CD pipeline and add release automation
  ([`f5a9b5a`](https://github.com/yaninsanity/django-user-starter/commit/f5a9b5aaccdad328e08d6f3720278c17440999c0))

- Fix semantic-release configuration with angular parser - Improve deploy.yml workflow with better
  conditions - Add manual workflow dispatch with branch selection - Fix dev version generation logic
  - Add release.sh script for automated releases - Update GitHub release creation to use proper
  action

- Improve consistency
  ([`3b2c88c`](https://github.com/yaninsanity/django-user-starter/commit/3b2c88c59546eb4400162f49eb691b38c6d8851d))

### Features

- Fully automate CI/CD pipeline
  ([`0cb9820`](https://github.com/yaninsanity/django-user-starter/commit/0cb982026563e1f15e6136d5d6439193cdcaa4cc))

- Remove manual release.sh script for complete automation - Update deploy.yml to trigger on PR
  merges to main - Simplify Makefile by removing manual upload commands - Update README with
  automated release workflow examples - CI/CD now handles everything: dev→TestPyPI, main→PyPI


## v0.1.7 (2025-03-16)

### Bug Fixes

- Add back missing version_file_regex
  ([`f38808c`](https://github.com/yaninsanity/django-user-starter/commit/f38808c4dbf1bf7413e84092a381bbdfd43ad3b9))

- Add commit version file to true
  ([`b2ac63f`](https://github.com/yaninsanity/django-user-starter/commit/b2ac63f099c26b208af356059b098be82ada3bdc))

- Fix commit version file order and desc
  ([`8399fcb`](https://github.com/yaninsanity/django-user-starter/commit/8399fcb390780f072af2945cda2a28b32c4067cc))

- Remove dynamic version to see if version file been trigger
  ([`83ceae0`](https://github.com/yaninsanity/django-user-starter/commit/83ceae0a0d1cf02c6f28e2e0a19bdbe8f2c5531a))


## v0.1.6 (2025-03-15)

### Bug Fixes

- Reset version init value
  ([`f36f4cf`](https://github.com/yaninsanity/django-user-starter/commit/f36f4cfb3548a45e5042057e9840a37b2272da44))


## v0.1.5 (2025-03-15)

### Bug Fixes

- Dynamic versioning
  ([`16d9463`](https://github.com/yaninsanity/django-user-starter/commit/16d94635bfcdcb19f6db6a5712dc06a4d09547c8))


## v0.1.4 (2025-03-15)

### Bug Fixes

- Remove unuse library
  ([`05b1a32`](https://github.com/yaninsanity/django-user-starter/commit/05b1a321a23b1063195c53a94ba335febb28229e))


## v0.1.3 (2025-03-15)

### Bug Fixes

- Add missing dependencies wheel
  ([`78368f0`](https://github.com/yaninsanity/django-user-starter/commit/78368f0eee1cec79f452ac22f3f072a2b2079418))

- Ease workflow and use psr build
  ([`eaa82fd`](https://github.com/yaninsanity/django-user-starter/commit/eaa82fd42544042052887c0cdf4a897d29901005))

- Fix build by ensure build exist before build
  ([`9b43b27`](https://github.com/yaninsanity/django-user-starter/commit/9b43b278b92cc3406c48d9e83d33460abd63f822))

- Improve pipeline and fix concurrency group
  ([`03f3d8d`](https://github.com/yaninsanity/django-user-starter/commit/03f3d8db2b2f958d891193ee39bc8ccacd03e2de))

- No isolation in build
  ([`4ba5a7a`](https://github.com/yaninsanity/django-user-starter/commit/4ba5a7ab4e4d1e1c80b360467c2088c7433524b6))

- Reset Branch to Workflow SHA”--cicd
  ([`da29140`](https://github.com/yaninsanity/django-user-starter/commit/da29140a20ae8d74bdd180b453d0544447854aa8))


## v0.1.2 (2025-03-15)

### Bug Fixes

- Remove duplicated scm requirement and improve cicd with ls dist
  ([`509af88`](https://github.com/yaninsanity/django-user-starter/commit/509af888323f71af09175208cc7335b720588143))


## v0.1.1 (2025-03-15)

### Bug Fixes

- Improve doc with PSR instructions
  ([`a862b0a`](https://github.com/yaninsanity/django-user-starter/commit/a862b0a5da876eb31900f8b1c4778cf8b6b17d46))


## v0.1.0 (2025-03-15)

### Bug Fixes

- Missing dependencies
  ([`cc3a3c7`](https://github.com/yaninsanity/django-user-starter/commit/cc3a3c7b7189d8371dc331c2174b3fb4a0e18ad1))

### Features

- Add banner
  ([`3db6a15`](https://github.com/yaninsanity/django-user-starter/commit/3db6a15210123776a0fb5b31bef7d2b4b0ccf40b))

- Add jazzmin empty comit force verison
  ([`e399ebf`](https://github.com/yaninsanity/django-user-starter/commit/e399ebf5afa33f31240cfd43a2ce3355a41d6c6f))


## v0.0.1 (2025-03-01)
