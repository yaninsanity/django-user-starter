import os
import shutil
import subprocess  # nosec B404
import sys


def run_script(script_name):
    """
    Helper function to execute a shell script from the package directory.
    """
    base_dir = os.path.dirname(__file__)
    script_path = os.path.join(base_dir, script_name)

    if not os.path.exists(script_path):
        sys.exit(f"Error: {script_name} not found.")

    # Verify the script path is within our package directory for security
    if not script_path.startswith(base_dir):
        sys.exit("Error: Invalid script path.")

    # Use more restrictive permissions (0o744 = rwxr--r--)
    os.chmod(script_path, 0o744)  # nosec B103

    # Use absolute path to bash for security
    bash_path = shutil.which("bash")
    if not bash_path:
        sys.exit("Error: bash not found in PATH.")

    # Run with verified absolute path
    subprocess.call([bash_path, script_path])  # nosec B603 B607


def main_zh():
    """Call starter-zh.sh."""
    run_script("starter-zh.sh")


def main_en():
    """Call starter-en.sh."""
    run_script("starter-en.sh")
