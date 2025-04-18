import os
import shutil
import subprocess
import PyPetaKit5D


def main():
    d = os.path.dirname(PyPetaKit5D.__file__)
    for folder in ("MATLAB_Runtime", "PetaKit5D"):
        path = os.path.join(d, folder)
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"Removed: {path}")
        else:
            print(f"Not found, skipped: {path}")

    print("Uninstalling PyPetaKit5D...")
    subprocess.run(["pip", "uninstall", "-v", "-y", "PyPetaKit5D"])
