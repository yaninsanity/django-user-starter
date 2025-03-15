import os
import sys
import subprocess
from time import sleep

def run_script(script_name):
    """
    Helper function to execute a shell script from the package directory.
    """
    base_dir = os.path.dirname(__file__)
    script_path = os.path.join(base_dir, script_name)
    
    if not os.path.exists(script_path):
        sys.exit(f"Error: {script_name} not found.")
    
    os.chmod(script_path, 0o755)
    subprocess.call(['bash', script_path])

def main_zh():
    """Call starter-zh.sh."""
    print_banner()
    run_script('starter-zh.sh')

def main_en():
    """Call starter-en.sh."""
    run_script('starter-en.sh')

def print_banner():
    print('''
        _____  _     _             _                        _             
    / __  \| |   | |           (_)                      (_)  _         
    | | /   ) |___| |_____ ____  _ ____   ___ _____ ____  _ _| |_ _   _ 
    | | \__/|_____  (____ |  _ \| |  _ \ /___|____ |  _ \| (_   _) | | |
    | |____  _____| / ___ | | | | | | | |___ / ___ | | | | | | |_| |_| |
                                                                (____/
          
    ''')
    sleep(3)
    print('''
    Github Repo: https://github.com/yaninsanity/django-user-starter
          '''   
    )
    sleep(2)