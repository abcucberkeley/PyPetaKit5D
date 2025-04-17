import os
import shutil
import site
import subprocess
import sys
import urllib.request
from setuptools import setup, find_packages
from setuptools.command.install import install

name = 'PyPetaKit5D'
version = '1.4.0'


class CustomInstall(install):
    def download_and_extract_matlab_runtime(self, install_dir):
        petakit5d_url = "https://github.com/abcucberkeley/PetaKit5D/releases/download/v1.4.0/PetaKit5D-1.4.0-Linux-x64.tar.gz"
        petakit5d_dir = os.path.join(install_dir, "PetaKit5D")
        petakit5d_tar_loc = os.path.join(install_dir, "PetaKit5D.tar.gz")

        matlab_runtime_dir = os.path.join(install_dir, "MATLAB_Runtime")

        # Download and extract PetaKit5D and the MATLAB runtime
        try:
            if os.path.exists(petakit5d_dir):
                shutil.rmtree(petakit5d_dir)
            os.makedirs(os.path.dirname(petakit5d_tar_loc), exist_ok=True)
            if not os.path.exists(petakit5d_tar_loc):
                urllib.request.urlretrieve(petakit5d_url, petakit5d_tar_loc)
            process = subprocess.Popen(
                f"tar -xf \"{petakit5d_tar_loc}\" -C \"{install_dir}\"",
                shell=True
            )
            process.wait()
            os.remove(petakit5d_tar_loc)

            matlab_runtime_ver_dir = os.path.join(matlab_runtime_dir, "R2024b")
            if not os.path.exists(matlab_runtime_ver_dir) or not os.listdir(matlab_runtime_ver_dir):
                install_file_loc = f"{petakit5d_dir}/mcc/installMCR/installMCR.install"

                process = subprocess.Popen(
                    f"\"{install_file_loc}\" -agreeToLicense yes -destinationFolder \"{matlab_runtime_dir}\"",
                    shell=True)
                process.wait()
        except Exception as e:
            sys.stderr.write("Error downloading/extracting MATLAB runtime: {}\n".format(str(e)))
            sys.exit(1)

    def run(self):
        install.run(self)
        install_dir = os.path.join(site.getsitepackages()[0], name)
        self.download_and_extract_matlab_runtime(install_dir)


setup(
    name=name,
    version=version,
    description='A Python wrapper for PetaKit5D',
    url='https://github.com/abcucberkeley/PyPetaKit5D',
    author='Matthew Mueller',
    author_email='matthewmueller@berkeley.edu',
    license='GPL-3.0',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.11',
    ],
    cmdclass={
        'install': CustomInstall,
    }
)
