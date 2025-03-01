import os
import sys
import subprocess

def main_zh():
    """
    入口函数：调用 starter-zh.sh
    """
    base_dir = os.path.dirname(__file__)
    script_path = os.path.join(base_dir, 'starter-zh.sh')

    if not os.path.exists(script_path):
        sys.exit("Error: starter-zh.sh not found.")

    os.chmod(script_path, 0o755)
    
    subprocess.call(['bash', script_path])

def main_en():
    """
    入口函数：调用 starter-en.sh
    """
    base_dir = os.path.dirname(__file__)
    script_path = os.path.join(base_dir, 'starter-en.sh')

    if not os.path.exists(script_path):
        sys.exit("Error: starter-en.sh not found.")

    os.chmod(script_path, 0o755)
    
    subprocess.call(['bash', script_path])
