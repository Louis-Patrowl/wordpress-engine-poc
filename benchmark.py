import sys
import subprocess


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('URL is required as argument')
    subprocess.popen(f'python3 main.py {sys.argv[1]} -m passive')