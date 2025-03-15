#!/bin/bash
# setup_django_full.sh
#
# 这个脚本自动创建一个 Django 项目，包含一个定制的用户系统（不再使用冲突的 avatar 字段）
# 并集成 django-avatar 用于头像管理。
#
# 功能：
#   - 检查 Python3 是否存在，并创建/激活虚拟环境。
#   - 创建 requirements.txt（依赖 Django、django-avatar、Pillow、django-jazzmin）并安装依赖。
#   - 交互式地询问 Django 项目名称和用户系统 App 名称。
#   - 创建 Django 项目和 App。
#   - 修改 settings.py：添加 'jazzmin'、用户 App 和 'avatar' 到 INSTALLED_APPS，
#     并配置 MEDIA_URL 和 MEDIA_ROOT。
#   - 可选：创建自定义用户模型（添加 bio、birth_date、phone、address、role 字段，不再使用 avatar 字段）。
#   - 配置 admin 以支持自定义用户模型。
#   - 生成基本的 URLs、views 和模板（登录、注销、注册和主页）。
#   - 修改主 URL 配置，包含 admin、avatar 和用户 App 的路由。
#   - 运行数据库迁移，并可选创建超级用户。
#
# 使用方法：
#   chmod +x setup_django_full.sh
#   ./setup_django_full.sh

set -e

# -------------------------
# 辅助函数

die() {
  echo "Error: $1" >&2
  exit 1
}

safe_cd() {
  cd "$1" || die "无法切换目录到 $1"
}

# 通用的 sed in-place 操作（支持 macOS 和 Linux）
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
# Step 0. 检查 Python3
if ! command -v python3 &> /dev/null; then
  die "未找到 Python3，请先安装 Python3."
fi

# -------------------------
# Step 1. 虚拟环境设置
read -p "请输入虚拟环境目录名称 (默认: venv): " venv_dir
venv_dir=${venv_dir:-venv}

if [[ ! -d "$venv_dir" ]]; then
  echo "正在创建虚拟环境 '$venv_dir'..."
  python3 -m venv "$venv_dir" || die "创建虚拟环境失败."
fi

echo "激活虚拟环境..."
source "$venv_dir/bin/activate"

# -------------------------
# Step 2. 安装依赖
req_file="requirements.txt"
cat <<EOF > "$req_file"
Django>=3.2
django-avatar
pillow
django-jazzmin
EOF

echo "升级 pip 并安装依赖..."
pip install --upgrade pip || die "升级 pip 失败."
pip install -r "$req_file" || die "依赖安装失败."

# -------------------------
# Step 3. 创建 Django 项目
read -p "请输入 Django 项目名称 (默认: myproject): " project_name
project_name=${project_name:-myproject}

echo "创建 Django 项目: $project_name"
django-admin startproject "$project_name" || die "项目创建失败."
safe_cd "$project_name"

# -------------------------
# Step 4. 创建用户系统 App
read -p "请输入用户系统 App 名称 (默认: users): " app_name
app_name=${app_name:-users}

echo "创建 Django App: $app_name"
python manage.py startapp "$app_name" || die "App 创建失败."

# -------------------------
# Step 5. 修改 settings.py
settings_file="$project_name/settings.py"
echo "更新 $settings_file：将 'jazzmin'、'$app_name' 和 'avatar' 添加到 INSTALLED_APPS..."
# 仅在这里添加 'jazzmin'
for app in "'jazzmin'" "'$app_name'" "'avatar'"; do
  if ! grep -q "$app" "$settings_file"; then
    sed_append "INSTALLED_APPS = \[" "$settings_file" "    $app,"
    echo "已添加 $app 到 INSTALLED_APPS."
  fi
done

if ! grep -q "MEDIA_URL" "$settings_file"; then
  cat <<EOF >> "$settings_file"

# 媒体文件设置（django-avatar 需要）
import os
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
EOF
  echo "已追加 MEDIA_URL 和 MEDIA_ROOT 设置."
fi

# -------------------------
# Step 6. 自定义用户模型（可选）
read -p "是否创建包含额外字段（bio, birth_date, phone, address, role）的自定义用户模型？(y/n, 默认: y): " use_custom_user
use_custom_user=${use_custom_user:-y}

if [[ "$use_custom_user" =~ ^[Yy] ]]; then
  echo "在 $app_name/models.py 中创建自定义用户模型..."
  # 注意：移除了 avatar 字段，避免与 django-avatar 冲突
  cat <<EOF > "$app_name/models.py"
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True, help_text="用户简介")
    birth_date = models.DateField(blank=True, null=True, help_text="出生日期")
    phone = models.CharField(max_length=20, blank=True, null=True, help_text="电话号码")
    address = models.TextField(blank=True, null=True, help_text="联系地址")
    role = models.CharField(max_length=50, blank=True, null=True, help_text="用户角色（如 admin, editor 等）")

    def __str__(self):
        return self.username
EOF

  if ! grep -q "AUTH_USER_MODEL" "$settings_file"; then
    {
      echo ""
      echo "# 使用自定义用户模型"
      echo "AUTH_USER_MODEL = '$app_name.CustomUser'"
    } >> "$settings_file"
    echo "已在 settings.py 中设置 AUTH_USER_MODEL 为 '$app_name.CustomUser'."
  fi

  echo "配置 admin 管理自定义用户模型..."
  cat <<EOF > "$app_name/admin.py"
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # 注意：从 fieldsets 和 add_fieldsets 中移除了 avatar 字段，避免与 django-avatar 冲突
    fieldsets = UserAdmin.fieldsets + (
        ('自定义字段', {'fields': ('bio', 'birth_date', 'phone', 'address', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'birth_date', 'phone', 'address', 'role')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
EOF
else
  echo "使用 Django 默认的 User 模型."
fi

# -------------------------
# Step 7. 创建 App 的 URL 配置
echo "创建 $app_name/urls.py..."
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
# Step 8. 创建基础视图
echo "在 $app_name/views.py 中创建基础视图..."
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
# Step 9. 创建模板
echo "创建模板文件..."
mkdir -p "$app_name/templates/$app_name"

cat <<EOF > "$app_name/templates/$app_name/login.html"
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>登录</title>
</head>
<body>
  <h2>登录</h2>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">登录</button>
  </form>
  <p>没有账号？<a href="{% url '$app_name:register' %}">注册</a></p>
  <p><a href="{% url 'avatar:change' %}">更换头像</a></p>
</body>
</html>
EOF

cat <<EOF > "$app_name/templates/$app_name/register.html"
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>注册</title>
</head>
<body>
  <h2>注册</h2>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">注册</button>
  </form>
  <p>已有账号？<a href="{% url '$app_name:login' %}">登录</a></p>
</body>
</html>
EOF

mkdir -p "templates"
cat <<EOF > "templates/home.html"
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>主页</title>
</head>
<body>
  <h2>欢迎, {% if user.is_authenticated %}{{ user.username }}{% else %}访客{% endif %}!</h2>
  {% if user.is_authenticated %}
    <p><a href="{% url '$app_name:logout' %}">退出登录</a></p>
    {% load avatar_tags %}
    <p>您的头像:</p>
    {% avatar user 80 class="img-thumbnail" %}
  {% else %}
    <p><a href="{% url '$app_name:login' %}">登录</a> | <a href="{% url '$app_name:register' %}">注册</a></p>
  {% endif %}
</body>
</html>
EOF

# -------------------------
# Step 10. 修改主 URL 配置
echo "更新主 URL 配置..."
main_urls="$project_name/urls.py"
cat <<EOF > "$main_urls"
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('avatar/', include('avatar.urls')),
    path('$app_name/', include('$app_name.urls', namespace='$app_name')),
    # 可选：你可以取消下面一行的注释，将主页指向自定义模板
    # path('', TemplateView.as_view(template_name="home.html"), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
EOF

# -------------------------
# Step 11. 数据库迁移
echo "运行数据库迁移..."
python manage.py makemigrations || die "生成迁移文件失败."
python manage.py migrate || die "数据库迁移失败."

# -------------------------
# Step 12. 创建超级用户（可选）
read -p "是否创建超级用户？(y/n, 默认: y): " create_su
create_su=${create_su:-y}
if [[ "$create_su" =~ ^[Yy] ]]; then
  python manage.py createsuperuser || echo "超级用户创建被取消."
fi

# -------------------------
# Step 13. 最后说明
echo "-------------------------------------------------"
echo "Django 项目设置完成！"
echo "当前虚拟环境 '$venv_dir' 已激活."
echo ""
echo "接下来你可以执行以下操作："
echo "  - 启动开发服务器: python manage.py runserver"
echo "  - 管理后台: http://localhost:8000/admin/"
echo "  - 主页: http://localhost:8000/ （根据你的 URL 配置调整）"
echo "  - django-avatar 使用 MEDIA_URL 和 MEDIA_ROOT 配置管理用户头像."
echo "  - 已安装 django-jazzmin，可在 settings.py 中进一步配置 (INSTALLED_APPS 中已包含 'jazzmin')."
echo "-------------------------------------------------"
