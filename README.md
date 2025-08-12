# Django User Starter

Minimal intelligent Django project generator - **One command, zero configuration, complete projects**

## Features

- 🎯 **Minimal CLI** - Single command, auto-inferred dependencies
- ✅ **Zero errors** - String-based generation, 100% reliable
- 🧠 **Smart configuration** - Auto-detect feature dependencies
- 🚀 **Production ready** - Docker + security configuration
- 🗄️ **Multi-database** - SQLite/PostgreSQL/MySQL
- 📦 **Complete features** - Authentication system/API/Admin themes/Avatar support
- 🌍 **Multi-language** - Chinese/English interface support

## Installation & Usage

```bash
pip install django-user-starter

# Basic project
django-starter myproject

# API project (auto-includes Token auth + Custom user + Docker)
django-starter myproject --api

# Full features + English interface
django-starter myproject --api --admin jazzmin --db postgresql --lang en
```

## Complete Feature Set

### 🔐 Authentication System (Shell script functionality parity)
- Complete login/register/logout views
- User profile pages
- Custom user model (bio, birth_date, phone, address, role)
- django-avatar support
- Bootstrap responsive templates

### 🚀 Smart Inference
Tool automatically detects and adds dependent features:
- `--api` → Auto-enables Token auth, Custom user model, Docker
- `--admin jazzmin` → Auto-enables Custom user model, Docker
- JWT auth → Auto-includes DRF and related configurations

### 🌍 Multi-language Support
```bash
# Chinese interface (default)
django-starter myproject --lang zh

# English interface
django-starter myproject --lang en

# Auto-detect system language
export LANG=en_US && django-starter myproject
```

## Generated Content

```
myproject/
├── manage.py
├── requirements.txt          # Precise dependencies, no bloat
├── Dockerfile               # Multi-stage build, security optimized
├── docker-compose.yml
├── myproject/
│   ├── settings.py          # Production-ready configuration
│   ├── urls.py
│   └── wsgi.py
├── main/                    # Main application
│   ├── models.py           # Custom user model (optional)
│   ├── admin.py            # Enhanced admin interface
│   ├── views.py            # Complete authentication views
│   ├── migrations/         # Auto-generated migrations
│   ├── templates/          # Login/register/profile templates
│   └── api/                # REST API (optional)
├── templates/              # Bootstrap base templates
│   ├── base.html
│   └── home.html
```

## Why Choose This Tool?

- **Minimalist** - 500 lines of code, full functionality, no bloat
- **Intelligent** - Auto-infer dependencies, zero configuration
- **Production grade** - Secure Docker, optimized settings
- **Complete features** - Shell script parity authentication system
- **Multi-language** - Chinese/English interface, international friendly

## Complete Command Options

```bash
django-starter <project_name> [options]

--db {sqlite,postgresql,mysql}  Database type
--api                           Include REST API
--auth {session,token,jwt}      Authentication method
--admin {default,jazzmin}       Admin theme
--user                          Custom user model
--docker                        Docker containerization
--lang {en,zh}                  Interface language
```

## License

MIT
