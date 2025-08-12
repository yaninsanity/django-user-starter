"""Django User Starter - Quick Django user authentication project generator.

A lightweight tool for generating Django projects with user authentication.
"""

import argparse
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

MESSAGES: Dict[str, Dict[str, str]] = {
    "zh": {
        "generating": "正在生成Django项目",
        "complete": "项目生成成功! 功能",
        "next_steps": "下一步:",
        "description": "快速生成Django用户认证项目",
        "name_help": "项目名称",
        "db_help": "数据库类型 (sqlite/postgresql/mysql)",
        "api_help": "启用DRF API",
        "auth_help": "认证方式 (session/token/jwt)",
        "admin_help": "管理界面 (default/jazzmin)",
        "user_help": "自定义用户模型",
        "docker_help": "包含Docker配置",
        "lang_help": "界面语言 (zh/en)",
    },
    "en": {
        "generating": "Generating Django project",
        "complete": "Project generated successfully! Features",
        "next_steps": "Next steps:",
        "description": "Quickly generate Django projects with user authentication",
        "name_help": "Project name",
        "db_help": "Database type (sqlite/postgresql/mysql)",
        "api_help": "Enable DRF API",
        "auth_help": "Authentication method (session/token/jwt)",
        "admin_help": "Admin interface (default/jazzmin)",
        "user_help": "Custom user model",
        "docker_help": "Include Docker configuration",
        "lang_help": "Interface language (zh/en)",
    },
}


@dataclass
class Config:
    """Project configuration."""

    name: str
    db: str = "sqlite"
    api: bool = False
    auth: str = "session"
    admin: str = "default"
    user: bool = False
    docker: bool = False
    lang: str = "zh"

    def __post_init__(self) -> None:
        """Auto-inference of dependent features."""
        if self.api and self.auth == "session":
            self.auth = "token"
        if self.api or self.admin == "jazzmin":
            self.user = True
            self.docker = True


class Generator:
    """Django project generator."""

    def __init__(self, cfg: Config):
        """Initialize generator with configuration.

        Args:
            cfg: Configuration object containing project settings.
        """
        self.cfg = cfg
        self.msg = MESSAGES[cfg.lang]
        self.dir = Path.cwd() / cfg.name

    def run(self) -> None:
        """Generate project."""
        print(f"🚀 {self.msg['generating']}: {self.cfg.name}")
        if self.dir.exists():
            shutil.rmtree(self.dir)
        self.dir.mkdir()
        self._create_dirs()
        self._write_files()
        features = [self.cfg.db.upper()]
        if self.cfg.api:
            features.append(f"API({self.cfg.auth.upper()})")
        if self.cfg.admin == "jazzmin":
            features.append("JAZZMIN")
        if self.cfg.user:
            features.append("CUSTOM_USER")
        if self.cfg.docker:
            features.append("DOCKER")
        print(f"✅ {self.msg['complete']}: {', '.join(features)}")
        print(f"💡 {self.msg['next_steps']}")
        print(f"   cd {self.cfg.name} && python manage.py runserver")

    def _create_dirs(self) -> None:
        """Create directory structure."""
        dirs = [self.cfg.name, "main", "templates/main", "static/css", "static/js"]
        if self.cfg.api:
            dirs.append("main/api")
        for d in dirs:
            (self.dir / d).mkdir(parents=True, exist_ok=True)

    def _write_files(self) -> None:
        """Write all project files."""
        self._manage()
        self._requirements()
        self._readme()
        self._settings()
        self._urls()
        self._wsgi()
        self._models()
        self._admin()
        self._views()
        self._base_template()
        self._home_template()
        self._login_template()
        self._register_template()
        self._profile_template()
        if self.cfg.user:
            self._migration()
        if self.cfg.api:
            self._api_urls()
            self._serializers()
            self._api_views()
        if self.cfg.docker:
            self._dockerfile()
            self._docker_compose()
            self._dockerignore()

    def _manage(self) -> None:
        content = '''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
if __name__ == '__main__':
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
'''.format(
            self.cfg.name
        )
        (self.dir / "manage.py").write_text(content)

    def _requirements(self) -> None:
        deps = ["Django>=4.2,<5.0", "whitenoise>=6.0"]
        if self.cfg.db == "postgresql":
            deps.append("psycopg2-binary>=2.9")
        elif self.cfg.db == "mysql":
            deps.append("mysqlclient>=2.1")
        if self.cfg.api:
            deps.extend(["djangorestframework>=3.14", "django-cors-headers>=3.14"])
        if self.cfg.auth in ["token", "jwt"]:
            if self.cfg.auth == "jwt":
                deps.append("djangorestframework-simplejwt>=5.2")
            deps.append("djoser>=2.2")
        if self.cfg.admin == "jazzmin":
            deps.append("django-jazzmin>=2.6")
        content = "\n".join(deps) + "\n"
        (self.dir / "requirements.txt").write_text(content)

    def _readme(self) -> None:
        content = f"""# {self.cfg.name}
Django项目，包含用户认证系统。
## 功能特性
- 用户注册/登录/登出
- 用户资料管理
- 响应式设计
- 管理后台
## 快速开始
1. 安装依赖：
```bash
pip install -r requirements.txt
```
2. 数据库迁移：
```bash
python manage.py migrate
```
3. 创建超级用户：
```bash
python manage.py createsuperuser
```
4. 运行开发服务器：
```bash
python manage.py runserver
```
访问 http://127.0.0.1:8000 查看网站。
"""
        (self.dir / "README.md").write_text(content)

    def _settings(self) -> None:
        apps = [
            "'django.contrib.admin'",
            "'django.contrib.auth'",
            "'django.contrib.contenttypes'",
            "'django.contrib.sessions'",
            "'django.contrib.messages'",
            "'django.contrib.staticfiles'",
            "'main'",
        ]
        if self.cfg.api:
            apps.extend(["'rest_framework'", "'corsheaders'"])
            if self.cfg.auth in ["token", "jwt"]:
                apps.append("'djoser'")
                if self.cfg.auth == "jwt":
                    apps.append("'rest_framework_simplejwt'")
        if self.cfg.admin == "jazzmin":
            apps.insert(0, "'jazzmin'")
        db_config = {
            "sqlite": "{'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}",
            "postgresql": "{'ENGINE': 'django.db.backends.postgresql', 'NAME': 'postgres', 'USER': 'postgres', 'PASSWORD': 'postgres', 'HOST': 'localhost', 'PORT': '5432'}",
            "mysql": "{'ENGINE': 'django.db.backends.mysql', 'NAME': 'mysql', 'USER': 'root', 'PASSWORD': 'root', 'HOST': 'localhost', 'PORT': '3306'}",
        }
        middleware = [
            "django.middleware.security.SecurityMiddleware",
            "whitenoise.middleware.WhiteNoiseMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ]
        if self.cfg.api:
            middleware.insert(2, "corsheaders.middleware.CorsMiddleware")
        content = f"""from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-change-this-in-production'
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    {', '.join(apps)}
]
MIDDLEWARE = {middleware}
ROOT_URLCONF = '{self.cfg.name}.urls'
TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]
WSGI_APPLICATION = '{self.cfg.name}.wsgi.application'
DATABASES = {{
    'default': {db_config[self.cfg.db]}
}}
AUTH_PASSWORD_VALIDATORS = [
    {{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}},
]
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'"""
        if self.cfg.user:
            content += "\nAUTH_USER_MODEL = 'main.CustomUser'"
        if self.cfg.api:
            rest_config = """
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ["""
            if self.cfg.auth == "session":
                rest_config += "'rest_framework.authentication.SessionAuthentication',"
            elif self.cfg.auth == "token":
                rest_config += "'rest_framework.authentication.TokenAuthentication',"
            elif self.cfg.auth == "jwt":
                rest_config += (
                    "'rest_framework_simplejwt.authentication.JWTAuthentication',"
                )
            rest_config += """
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]"""
            content += rest_config
        (self.dir / self.cfg.name / "settings.py").write_text(content)

    def _urls(self) -> None:
        content = """from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]"""
        (self.dir / self.cfg.name / "urls.py").write_text(content)

    def _wsgi(self) -> None:
        content = f"""import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{self.cfg.name}.settings')
application = get_wsgi_application()
"""
        (self.dir / self.cfg.name / "wsgi.py").write_text(content)

    def _models(self) -> None:
        if self.cfg.user:
            content = """from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(max_length=300, blank=True)
    role = models.CharField(max_length=20, default='user')
"""
        else:
            content = "from django.db import models\n\n# Create your models here.\n"
        (self.dir / "main" / "models.py").write_text(content)

    def _admin(self) -> None:
        if self.cfg.user:
            content = """from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('bio', 'birth_date', 'phone', 'address', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('bio', 'birth_date', 'phone', 'address', 'role')}),
    )
"""
        else:
            content = (
                "from django.contrib import admin\n\n# Register your models here.\n"
            )
        (self.dir / "main" / "admin.py").write_text(content)

    def _views(self) -> None:
        content = """from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
def home(request):
    return render(request, 'main/home.html')
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'账户创建成功，欢迎 {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})
@login_required
def profile_view(request):
    return render(request, 'main/profile.html')
"""
        (self.dir / "main" / "views.py").write_text(content)
        # URLs
        url_content = """from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
]"""
        (self.dir / "main" / "urls.py").write_text(url_content)
        (self.dir / "main" / "__init__.py").write_text("")

    def _base_template(self) -> None:
        content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Django用户系统{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">Django用户系统</a>
            <div class="navbar-nav ms-auto">
                {% if user.is_authenticated %}
                    <a class="nav-link" href="{% url 'profile' %}">个人资料</a>
                    <a class="nav-link" href="{% url 'logout' %}">退出</a>
                {% else %}
                    <a class="nav-link" href="{% url 'login' %}">登录</a>
                    <a class="nav-link" href="{% url 'register' %}">注册</a>
                {% endif %}
            </div>
        </div>
    </nav>
    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}
        {% block content %}
        {% endblock %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""
        (self.dir / "templates" / "main" / "base.html").write_text(content)

    def _home_template(self) -> None:
        content = """{% extends 'main/base.html' %}
{% block content %}
<div class="row">
    <div class="col-md-8 mx-auto">
        <div class="jumbotron">
            <h1 class="display-4">欢迎来到Django用户系统!</h1>
            <p class="lead">这是一个完整的用户认证系统示例。</p>
            {% if user.is_authenticated %}
                <p>你好, {{ user.username }}!</p>
                <a class="btn btn-primary btn-lg" href="{% url 'profile' %}">查看个人资料</a>
            {% else %}
                <p>请登录或注册账户。</p>
                <a class="btn btn-primary btn-lg" href="{% url 'register' %}">立即注册</a>
                <a class="btn btn-outline-primary btn-lg" href="{% url 'login' %}">登录</a>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}"""
        (self.dir / "templates" / "main" / "home.html").write_text(content)

    def _login_template(self) -> None:
        content = """{% extends 'main/base.html' %}
{% block title %}登录{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-6 mx-auto">
        <div class="card">
            <div class="card-header">
                <h3>登录</h3>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label for="{{ form.username.id_for_label }}" class="form-label">用户名</label>
                        {{ form.username }}
                    </div>
                    <div class="mb-3">
                        <label for="{{ form.password.id_for_label }}" class="form-label">密码</label>
                        {{ form.password }}
                    </div>
                    <button type="submit" class="btn btn-primary">登录</button>
                    <a href="{% url 'register' %}" class="btn btn-link">还没有账户？注册</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""
        (self.dir / "templates" / "main" / "login.html").write_text(content)

    def _register_template(self) -> None:
        content = """{% extends 'main/base.html' %}
{% block title %}注册{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-6 mx-auto">
        <div class="card">
            <div class="card-header">
                <h3>注册</h3>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label for="{{ form.username.id_for_label }}" class="form-label">用户名</label>
                        {{ form.username }}
                        {% if form.username.help_text %}
                            <div class="form-text">{{ form.username.help_text }}</div>
                        {% endif %}
                    </div>
                    <div class="mb-3">
                        <label for="{{ form.password1.id_for_label }}" class="form-label">密码</label>
                        {{ form.password1 }}
                        {% if form.password1.help_text %}
                            <div class="form-text">{{ form.password1.help_text }}</div>
                        {% endif %}
                    </div>
                    <div class="mb-3">
                        <label for="{{ form.password2.id_for_label }}" class="form-label">确认密码</label>
                        {{ form.password2 }}
                    </div>
                    <button type="submit" class="btn btn-primary">注册</button>
                    <a href="{% url 'login' %}" class="btn btn-link">已有账户？登录</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""
        (self.dir / "templates" / "main" / "register.html").write_text(content)

    def _profile_template(self) -> None:
        content = """{% extends 'main/base.html' %}
{% block title %}个人资料{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-8 mx-auto">
        <div class="card">
            <div class="card-header">
                <h3>个人资料</h3>
            </div>
            <div class="card-body">
                <table class="table">
                    <tr>
                        <th>用户名:</th>
                        <td>{{ user.username }}</td>
                    </tr>
                    <tr>
                        <th>邮箱:</th>
                        <td>{{ user.email|default:"未设置" }}</td>
                    </tr>
                    <tr>
                        <th>姓名:</th>
                        <td>{{ user.get_full_name|default:"未设置" }}</td>
                    </tr>
                    <tr>
                        <th>注册时间:</th>
                        <td>{{ user.date_joined }}</td>
                    </tr>
                    <tr>
                        <th>最后登录:</th>
                        <td>{{ user.last_login }}</td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""
        (self.dir / "templates" / "main" / "profile.html").write_text(content)

    def _migration(self) -> None:
        content = """# Generated migration for custom user model
from django.db import migrations, models
import django.contrib.auth.models
class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]
    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('address', models.TextField(blank=True, max_length=300)),
                ('role', models.CharField(default='user', max_length=20)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
"""
        migrations_dir = self.dir / "main" / "migrations"
        migrations_dir.mkdir(exist_ok=True)
        (migrations_dir / "__init__.py").write_text("")
        (migrations_dir / "0001_initial.py").write_text(content)

    def _api_urls(self) -> None:
        content = """from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls')),
]"""
        (self.dir / "main" / "api" / "urls.py").write_text(content)
        (self.dir / "main" / "api" / "__init__.py").write_text("")

    def _serializers(self) -> None:
        if self.cfg.user:
            content = """from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'birth_date', 'phone', 'address', 'role']
        read_only_fields = ['id']
"""
        else:
            content = """from rest_framework import serializers
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']
"""
        (self.dir / "main" / "api" / "serializers.py").write_text(content)

    def _api_views(self) -> None:
        content = """from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
User = get_user_model()
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
"""
        (self.dir / "main" / "api" / "views.py").write_text(content)

    def _dockerfile(self) -> None:
        content = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
"""
        (self.dir / "Dockerfile").write_text(content)

    def _docker_compose(self) -> None:
        db_service = ""
        if self.cfg.db == "postgresql":
            db_service = """
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
"""
        elif self.cfg.db == "mysql":
            db_service = """
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD: root
      MYSQL_ROOT_PASSWORD: root
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"
"""
        volumes = ""
        if self.cfg.db == "postgresql":
            volumes = "\nvolumes:\n  postgres_data:"
        elif self.cfg.db == "mysql":
            volumes = "\nvolumes:\n  mysql_data:"
        content = f"""version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=1{db_service}
{volumes}"""
        (self.dir / "docker-compose.yml").write_text(content)

    def _dockerignore(self) -> None:
        content = """.git
.gitignore
README.md
.env
.venv
venv/
__pycache__
*.pyc
.pytest_cache
htmlcov/
.coverage
"""
        (self.dir / ".dockerignore").write_text(content)


def main() -> None:
    """Command line entry point."""
    # Default language detection
    default_lang = "zh" if os.getenv("LANG", "").startswith("zh") else "en"
    parser = argparse.ArgumentParser(description=MESSAGES[default_lang]["description"])
    parser.add_argument("name", help=MESSAGES[default_lang]["name_help"])
    parser.add_argument(
        "--db",
        choices=["sqlite", "postgresql", "mysql"],
        default="sqlite",
        help=MESSAGES[default_lang]["db_help"],
    )
    parser.add_argument(
        "--api", action="store_true", help=MESSAGES[default_lang]["api_help"]
    )
    parser.add_argument(
        "--auth",
        choices=["session", "token", "jwt"],
        default="session",
        help=MESSAGES[default_lang]["auth_help"],
    )
    parser.add_argument(
        "--admin",
        choices=["default", "jazzmin"],
        default="default",
        help=MESSAGES[default_lang]["admin_help"],
    )
    parser.add_argument(
        "--user", action="store_true", help=MESSAGES[default_lang]["user_help"]
    )
    parser.add_argument(
        "--docker", action="store_true", help=MESSAGES[default_lang]["docker_help"]
    )
    parser.add_argument(
        "--lang",
        choices=["en", "zh"],
        default=default_lang,
        help=MESSAGES[default_lang]["lang_help"],
    )
    args = parser.parse_args()
    config = Config(
        name=args.name,
        db=args.db,
        api=args.api,
        auth=args.auth,
        admin=args.admin,
        user=args.user,
        docker=args.docker,
        lang=args.lang,
    )
    generator = Generator(config)
    generator.run()


if __name__ == "__main__":
    main()
