import os
import sys
import subprocess

def main_zh():
    """
    call starter-zh.sh
    """
    base_dir = os.path.dirname(__file__)
    script_path = os.path.join(base_dir, 'starter-zh.sh')

    if not os.path.exists(script_path):
        sys.exit("Error: starter-zh.sh not found.")

    os.chmod(script_path, 0o755)
    
    subprocess.call(['bash', script_path])

def main_en():
    """
    call starter-en.sh
    """
    base_dir = os.path.dirname(__file__)
    script_path = os.path.join(base_dir, 'starter-en.sh')

    if not os.path.exists(script_path):
        sys.exit("Error: starter-en.sh not found.")

    os.chmod(script_path, 0o755)
    
    subprocess.call(['bash', script_path])
