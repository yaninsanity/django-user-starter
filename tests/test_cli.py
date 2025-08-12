"""Test CLI functionality."""

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from django_user_starter.main import Config, Generator, main


class TestMain(unittest.TestCase):
    """Test main CLI functionality."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_config_defaults(self):
        """Test configuration defaults."""
        config = Config(name="test")
        self.assertEqual(config.name, "test")
        self.assertEqual(config.db, "sqlite")
        self.assertFalse(config.api)
        self.assertEqual(config.auth, "session")
        self.assertEqual(config.admin, "default")
        self.assertFalse(config.user)
        self.assertFalse(config.docker)

    def test_config_auto_inference(self):
        """Test auto-inference functionality."""
        # API auto-infers token auth and custom user
        config = Config(name="test", api=True)
        self.assertEqual(config.auth, "token")
        self.assertTrue(config.user)
        self.assertTrue(config.docker)

        # Jazzmin auto-infers custom user and docker
        config = Config(name="test", admin="jazzmin")
        self.assertTrue(config.user)
        self.assertTrue(config.docker)

    def test_generator_init(self):
        """Test generator initialization."""
        os.chdir(self.test_dir)

        config = Config(name="testproject")
        generator = Generator(config)
        self.assertEqual(generator.cfg.name, "testproject")
        self.assertEqual(generator.dir.name, "testproject")

    def test_basic_project_generation(self):
        """Test basic project generation."""
        os.chdir(self.test_dir)

        config = Config(name="testproject")
        generator = Generator(config)
        generator.run()

        project_dir = Path(self.test_dir) / "testproject"
        self.assertTrue(project_dir.exists())
        self.assertTrue((project_dir / "manage.py").exists())
        self.assertTrue((project_dir / "requirements.txt").exists())
        self.assertTrue((project_dir / "testproject" / "settings.py").exists())
        self.assertTrue((project_dir / "main" / "models.py").exists())

    def test_api_project_generation(self):
        """Test API project generation."""
        os.chdir(self.test_dir)

        config = Config(name="apiproject", api=True)
        generator = Generator(config)
        generator.run()

        project_dir = Path(self.test_dir) / "apiproject"
        self.assertTrue((project_dir / "main" / "api").exists())
        self.assertTrue((project_dir / "main" / "api" / "views.py").exists())
        self.assertTrue((project_dir / "main" / "api" / "serializers.py").exists())

        # Check that requirements contain DRF
        requirements = (project_dir / "requirements.txt").read_text()
        self.assertIn("djangorestframework", requirements)

    def test_docker_project_generation(self):
        """Test Docker project generation."""
        os.chdir(self.test_dir)

        config = Config(name="dockerproject", docker=True)
        generator = Generator(config)
        generator.run()

        project_dir = Path(self.test_dir) / "dockerproject"
        self.assertTrue((project_dir / "Dockerfile").exists())
        self.assertTrue((project_dir / "docker-compose.yml").exists())
        self.assertTrue((project_dir / ".dockerignore").exists())

    def test_database_configurations(self):
        """Test different database configurations."""
        os.chdir(self.test_dir)

        # Test PostgreSQL
        config = Config(name="pgproject", db="postgresql")
        generator = Generator(config)
        generator.run()

        requirements = (
            Path(self.test_dir) / "pgproject" / "requirements.txt"
        ).read_text()
        self.assertIn("psycopg2-binary", requirements)

        # Test MySQL
        config = Config(name="mysqlproject", db="mysql")
        generator = Generator(config)
        generator.run()

        requirements = (
            Path(self.test_dir) / "mysqlproject" / "requirements.txt"
        ).read_text()
        self.assertIn("mysqlclient", requirements)

    def test_authentication_methods(self):
        """Test different authentication methods."""
        os.chdir(self.test_dir)

        # Test JWT authentication
        config = Config(name="jwtproject", api=True, auth="jwt")
        generator = Generator(config)
        generator.run()

        requirements = (
            Path(self.test_dir) / "jwtproject" / "requirements.txt"
        ).read_text()
        self.assertIn("djangorestframework-simplejwt", requirements)
        self.assertIn("djoser", requirements)

        # Test token authentication
        config = Config(name="tokenproject", api=True, auth="token")
        generator = Generator(config)
        generator.run()

        requirements = (
            Path(self.test_dir) / "tokenproject" / "requirements.txt"
        ).read_text()
        self.assertIn("djoser", requirements)
        self.assertNotIn("simplejwt", requirements)

    def test_admin_interface_configurations(self):
        """Test different admin interface configurations."""
        os.chdir(self.test_dir)

        # Test Jazzmin admin
        config = Config(name="jazzminproject", admin="jazzmin")
        generator = Generator(config)
        generator.run()

        requirements = (
            Path(self.test_dir) / "jazzminproject" / "requirements.txt"
        ).read_text()
        self.assertIn("django-jazzmin", requirements)

    def test_custom_user_model(self):
        """Test custom user model generation."""
        os.chdir(self.test_dir)

        config = Config(name="userproject", user=True)
        generator = Generator(config)
        generator.run()

        models_content = (
            Path(self.test_dir) / "userproject" / "main" / "models.py"
        ).read_text()
        self.assertIn("AbstractUser", models_content)
        self.assertIn("CustomUser", models_content)
        self.assertIn("bio", models_content)

    def test_existing_project_overwrite(self):
        """Test overwriting existing project."""
        os.chdir(self.test_dir)

        # Create initial project
        config = Config(name="existingproject")
        generator = Generator(config)
        generator.run()

        initial_time = (
            (Path(self.test_dir) / "existingproject" / "manage.py").stat().st_mtime
        )

        # Recreate same project (should overwrite)
        generator = Generator(config)
        generator.run()

        new_time = (
            (Path(self.test_dir) / "existingproject" / "manage.py").stat().st_mtime
        )
        self.assertGreater(new_time, initial_time)

    def test_language_configuration(self):
        """Test different language configurations."""
        os.chdir(self.test_dir)

        # Test English language
        config = Config(name="enproject", lang="en")
        generator = Generator(config)
        generator.run()

        readme_content = (Path(self.test_dir) / "enproject" / "README.md").read_text()
        self.assertIn("enproject", readme_content)

        # Test Chinese language (default)
        config = Config(name="zhproject", lang="zh")
        generator = Generator(config)
        generator.run()

        readme_content = (Path(self.test_dir) / "zhproject" / "README.md").read_text()
        self.assertIn("Django项目", readme_content)

    def test_full_feature_project(self):
        """Test project with all features enabled."""
        os.chdir(self.test_dir)

        config = Config(
            name="fullproject",
            db="postgresql",
            api=True,
            auth="jwt",
            admin="jazzmin",
            user=True,
            docker=True,
            lang="en",
        )
        generator = Generator(config)
        generator.run()

        project_dir = Path(self.test_dir) / "fullproject"

        # Check all files exist
        self.assertTrue((project_dir / "manage.py").exists())
        self.assertTrue((project_dir / "requirements.txt").exists())
        self.assertTrue((project_dir / "Dockerfile").exists())
        self.assertTrue((project_dir / "docker-compose.yml").exists())
        self.assertTrue((project_dir / "main" / "api" / "views.py").exists())

        # Check requirements
        requirements = (project_dir / "requirements.txt").read_text()
        self.assertIn("psycopg2-binary", requirements)
        self.assertIn("djangorestframework", requirements)
        self.assertIn("djangorestframework-simplejwt", requirements)
        self.assertIn("django-jazzmin", requirements)

    @patch("sys.argv", ["django-starter", "testproject"])
    def test_main_function_basic(self):
        """Test main function with basic arguments."""
        os.chdir(self.test_dir)

        with patch("builtins.print"):  # Suppress output during test
            main()

        project_dir = Path(self.test_dir) / "testproject"
        self.assertTrue(project_dir.exists())
        self.assertTrue((project_dir / "manage.py").exists())

    @patch(
        "sys.argv",
        ["django-starter", "apiproject", "--api", "--db", "postgresql", "--lang", "en"],
    )
    def test_main_function_with_options(self):
        """Test main function with multiple options."""
        os.chdir(self.test_dir)

        with patch("builtins.print"):  # Suppress output during test
            main()

        project_dir = Path(self.test_dir) / "apiproject"
        self.assertTrue(project_dir.exists())
        self.assertTrue((project_dir / "main" / "api").exists())

        requirements = (project_dir / "requirements.txt").read_text()
        self.assertIn("psycopg2-binary", requirements)
        self.assertIn("djangorestframework", requirements)

    @patch.dict(os.environ, {"LANG": "zh_CN.UTF-8"})
    @patch("sys.argv", ["django-starter", "zhproject"])
    def test_main_function_chinese_locale(self):
        """Test main function with Chinese locale."""
        os.chdir(self.test_dir)

        with patch("builtins.print"):  # Suppress output during test
            main()

        project_dir = Path(self.test_dir) / "zhproject"
        self.assertTrue(project_dir.exists())

    @patch.dict(os.environ, {"LANG": "en_US.UTF-8"})
    @patch("sys.argv", ["django-starter", "enproject"])
    def test_main_function_english_locale(self):
        """Test main function with English locale."""
        os.chdir(self.test_dir)

        with patch("builtins.print"):  # Suppress output during test
            main()

        project_dir = Path(self.test_dir) / "enproject"
        self.assertTrue(project_dir.exists())

    def test_edge_cases(self):
        """Test edge cases and error conditions."""
        os.chdir(self.test_dir)

        # Test with minimal configuration
        config = Config(name="minimal")
        generator = Generator(config)
        generator.run()

        project_dir = Path(self.test_dir) / "minimal"
        self.assertTrue(project_dir.exists())

        # Check that SQLite is used by default
        requirements = (project_dir / "requirements.txt").read_text()
        self.assertNotIn("psycopg2", requirements)
        self.assertNotIn("mysqlclient", requirements)

    def test_template_generation(self):
        """Test template file generation."""
        os.chdir(self.test_dir)

        config = Config(name="templateproject", user=True)
        generator = Generator(config)
        generator.run()

        project_dir = Path(self.test_dir) / "templateproject"

        # Check main templates exist (these are actually generated in templates/main/)
        self.assertTrue((project_dir / "templates" / "main" / "login.html").exists())
        self.assertTrue((project_dir / "templates" / "main" / "register.html").exists())
        self.assertTrue((project_dir / "templates" / "main" / "base.html").exists())

    def test_migration_generation(self):
        """Test migration file generation."""
        os.chdir(self.test_dir)

        config = Config(name="migrationproject", user=True)
        generator = Generator(config)
        generator.run()

        project_dir = Path(self.test_dir) / "migrationproject"
        migrations_dir = project_dir / "main" / "migrations"

        self.assertTrue(migrations_dir.exists())
        self.assertTrue((migrations_dir / "__init__.py").exists())
        self.assertTrue((migrations_dir / "0001_initial.py").exists())


if __name__ == "__main__":
    unittest.main()
