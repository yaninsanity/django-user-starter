#!/bin/bash
# starter-en.sh
#
# This script automatically creates a Django project with a custom user system (no conflicting avatar field),
# integrates django-avatar for avatar management, and now also installs & configures jazzmin.
#
# Features:
#   - Checks if Python3 is available and creates/activates a virtual environment.
#   - Creates a requirements.txt (including Django, django-avatar, Pillow, and django-jazzmin) and installs dependencies.
#   - Interactively prompts for Django project name and user system App name.
#   - Creates a Django project and App.
#   - Modifies settings.py: Adds jazzmin, the user App and 'avatar' to INSTALLED_APPS,
#     and configures MEDIA_URL and MEDIA_ROOT.
#   - Optionally creates a custom user model (adding bio, birth_date, phone, address, role fields, removing avatar field).
#   - Configures admin to support the custom user model.
#   - Generates basic URLs, views, and templates (login, logout, register, and homepage).
#   - Modifies the main URL configuration to include routes for admin, avatar, and user App.
#   - Runs database migrations and optionally creates a superuser.
#
# Usage:
#   chmod +x starter-en.sh
#   ./starter-en.sh

set -e

# -------------------------
# Helper functions

die() {
  echo "Error: $1" >&2
  exit 1
}

safe_cd() {
  cd "$1" || die "Failed to change directory to $1"
}

# Generic sed in-place operation (supports macOS and Linux)
sed_append() {
  local pattern="$1" file="$2" line="$3"
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "/$pattern/ a\\
$line
" "$file"
  else
    sed -i "/$pattern/ a\\
$line" "$file"
  fi
}

# -------------------------
# Step 0. Check Python3
if ! command -v python3 &> /dev/null; then
  die "Python3 not found, please install Python3 first."
fi

# -------------------------
# Step 1. Virtual environment setup
read -p "Enter virtual environment directory name (default: venv): " venv_dir
venv_dir=${venv_dir:-venv}

if [[ ! -d "$venv_dir" ]]; then
  echo "Creating virtual environment '$venv_dir'..."
  python3 -m venv "$venv_dir" || die "Failed to create virtual environment."
fi

echo "Activating virtual environment..."
# shellcheck disable=SC1090
source "$venv_dir/bin/activate"

# -------------------------
# Step 2. Install dependencies
req_file="requirements.txt"
cat <<EOF > "$req_file"
Django>=3.2
django-avatar
pillow
django-jazzmin
EOF

echo "Upgrading pip and installing dependencies..."
pip install --upgrade pip || die "Failed to upgrade pip."
pip install -r "$req_file" || die "Failed to install dependencies."

# -------------------------
# Step 3. Create Django project
read -p "Enter Django project name (default: myproject): " project_name
project_name=${project_name:-myproject}

echo "Creating Django project: $project_name"
django-admin startproject "$project_name" || die "Project creation failed."
safe_cd "$project_name"

# -------------------------
# Step 4. Create user system App
read -p "Enter user system App name (default: users): " app_name
app_name=${app_name:-users}

echo "Creating Django App: $app_name"
python manage.py startapp "$app_name" || die "App creation failed."

# -------------------------
# Step 5. Modify settings.py
settings_file="$project_name/settings.py"
echo "Updating $settings_file: Adding 'jazzmin', '$app_name' and 'avatar' to INSTALLED_APPS..."

for app in "'jazzmin'" "'$app_name'" "'avatar'"; do
  if ! grep -q "$app" "$settings_file"; then
    sed_append "INSTALLED_APPS = \[" "$settings_file" "    $app,"
    echo "Added $app to INSTALLED_APPS."
  fi
done

if ! grep -q "MEDIA_URL" "$settings_file"; then
  cat <<EOF >> "$settings_file"

# Media file settings (required by django-avatar)
import os
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
EOF
  echo "Appended MEDIA_URL and MEDIA_ROOT settings."
fi

# -------------------------
# Step 6. Custom user model (optional)
read -p "Would you like to create a custom user model with additional fields (bio, birth_date, phone, address, role) instead of using the default user model? (y/n, default: y): " use_custom_user
use_custom_user=${use_custom_user:-y}

if [[ "$use_custom_user" =~ ^[Yy] ]]; then
  echo "Creating custom user model in $app_name/models.py..."
  # Note: Removed avatar field to avoid conflict with django-avatar
  cat <<EOF > "$app_name/models.py"
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True, help_text="User biography")
    birth_date = models.DateField(blank=True, null=True, help_text="Date of birth")
    phone = models.CharField(max_length=20, blank=True, null=True, help_text="Phone number")
    address = models.TextField(blank=True, null=True, help_text="Contact address")
    role = models.CharField(max_length=50, blank=True, null=True, help_text="User role (e.g., admin, editor, etc.)")

    def __str__(self):
        return self.username
EOF

  if ! grep -q "AUTH_USER_MODEL" "$settings_file"; then
    {
      echo ""
      echo "# Use custom user model"
      echo "AUTH_USER_MODEL = '$app_name.CustomUser'"
    } >> "$settings_file"
    echo "Set AUTH_USER_MODEL to '$app_name.CustomUser' in settings.py."
  fi

  echo "Configuring admin for custom user model..."
  cat <<EOF > "$app_name/admin.py"
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Note: Removed avatar field from fieldsets and add_fieldsets to avoid conflict with django-avatar
    fieldsets = UserAdmin.fieldsets + (
        ('Custom fields', {'fields': ('bio', 'birth_date', 'phone', 'address', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'birth_date', 'phone', 'address', 'role')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
EOF
else
  echo "Using Django's default User model."
fi

# -------------------------
# Step 7. Create App URL configuration
echo "Creating $app_name/urls.py..."
cat <<EOF > "$app_name/urls.py"
from django.urls import path
from . import views

app_name = '$app_name'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
EOF

# -------------------------
# Step 8. Create basic views
echo "Creating basic views in $app_name/views.py..."
cat <<EOF > "$app_name/views.py"
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, '$app_name/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, '$app_name/register.html', {'form': form})
EOF

# -------------------------
# Step 9. Create templates
echo "Creating template files..."
mkdir -p "$app_name/templates/$app_name"

cat <<EOF > "$app_name/templates/$app_name/login.html"
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Login</title>
</head>
<body>
  <h2>Login</h2>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Login</button>
  </form>
  <p>Don't have an account? <a href="{% url '$app_name:register' %}">Register</a></p>
  <p><a href="{% url 'avatar:change' %}">Change Avatar</a></p>
</body>
</html>
EOF

cat <<EOF > "$app_name/templates/$app_name/register.html"
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Register</title>
</head>
<body>
  <h2>Register</h2>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Register</button>
  </form>
  <p>Already have an account? <a href="{% url '$app_name:login' %}">Login</a></p>
</body>
</html>
EOF

mkdir -p "templates"
cat <<EOF > "templates/home.html"
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Homepage</title>
</head>
<body>
  <h2>Welcome, {% if user.is_authenticated %}{{ user.username }}{% else %}Guest{% endif %}!</h2>
  {% if user.is_authenticated %}
    <p><a href="{% url '$app_name:logout' %}">Logout</a></p>
    {% load avatar_tags %}
    <p>Your avatar:</p>
    {% avatar user 80 class="img-thumbnail" %}
  {% else %}
    <p><a href="{% url '$app_name:login' %}">Login</a> | <a href="{% url '$app_name:register' %}">Register</a></p>
  {% endif %}
</body>
</html>
EOF

# -------------------------
# Step 10. Modify main URL configuration
echo "Updating main URL configuration..."
main_urls="$project_name/urls.py"
cat <<EOF > "$main_urls"
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('avatar/', include('avatar.urls')),
    path('$app_name/', include('$app_name.urls', namespace='$app_name')),
    # Optional: Uncomment the following line to make the homepage point to your custom template
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
EOF

# -------------------------
# Step 11. Run database migrations
echo "Running database migrations..."
python manage.py makemigrations || die "Failed to create migration files."
python manage.py migrate || die "Database migration failed."

# -------------------------
# Step 12. Create superuser (optional)
read -p "Would you like to create a superuser? (y/n, default: y): " create_su
create_su=${create_su:-y}
if [[ "$create_su" =~ ^[Yy] ]]; then
  python manage.py createsuperuser || echo "Superuser creation cancelled."
fi

# -------------------------
# Step 13. Final instructions
echo "-------------------------------------------------"
echo "Django project setup is complete!"
echo "The current virtual environment '$venv_dir' is active."
echo ""
echo "Next, you can run the following commands:"
echo "  - Start the development server: python manage.py runserver"
echo "  - Admin panel: http://localhost:8000/admin/"
echo "  - Homepage: http://localhost:8000/ (adjust according to your URL configuration)"
echo "  - Use django-avatar to manage user avatars with MEDIA_URL and MEDIA_ROOT settings."
echo "  - Jazzmin is installed. You can further configure it in settings.py if needed."
echo "-------------------------------------------------"
