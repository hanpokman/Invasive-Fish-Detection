# JUST DOUBLE CLICK ME - I'll install everything you need
# If this doesn't work, open terminal and run: pip install opencv-python numpy torch scikit-learn matplotlib

import subprocess
import sys
import os


def install_packages():
    packages = ['opencv-python', 'numpy', 'torch', 'scikit-learn', 'matplotlib', 'pillow']

    print("=" * 50)
    print("INSTALLING REQUIRED PACKAGES")
    print("=" * 50)
    print("This might take a minute...")
    print("A black window might pop up - that's normal!")
    print("")

    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except:
            print(f"Failed to install {package}, trying again...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--user"])

    print("")
    print("=" * 50)
    print("DONE! Close this window and double-click 'main_app.py'")
    print("=" * 50)
    input("Press Enter to exit...")


if __name__ == "__main__":
    install_packages()