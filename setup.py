import os
import shutil
import site
import subprocess
import sys
import urllib.request

from setuptools import setup, find_packages
from setuptools.command.install import install

matlab_runtime_url = ("https://ssd.mathworks.com/supportfiles/downloads/R2023a/Release/6/deployment_files"
                      "/installer/complete/glnxa64/MATLAB_Runtime_R2023a_Update_6_glnxa64.zip")
name = 'PyPetaKit5D'
version = '1.1.0'


class CustomInstall(install):
    def download_and_extract_matlab_runtime(self, install_dir):
        petakit5d_url = "https://github.com/abcucberkeley/PetaKit5D/archive/refs/heads/main.zip"
        petakit5d_github_dir = os.path.join(install_dir, "PetaKit5D-main")
        petakit5d_dir = os.path.join(install_dir, "PetaKit5D")
        petakit5d_zip_loc = os.path.join(install_dir, "PetaKit5D.zip")

        matlab_runtime_tmp_dir = os.path.join(install_dir, "matlabRuntimeTmp")
        matlab_runtime_dir = os.path.join(install_dir, "MATLAB_Runtime")
        matlab_runtime_zip_loc = os.path.join(install_dir, "matlabRuntime.zip")

        # Download and extract PetaKit5D and the MATLAB runtime
        try:
            if os.path.exists(petakit5d_dir):
                shutil.rmtree(petakit5d_dir)
            os.makedirs(os.path.dirname(petakit5d_zip_loc), exist_ok=True)
            if not os.path.exists(petakit5d_zip_loc):
                urllib.request.urlretrieve(petakit5d_url, petakit5d_zip_loc)
            process = subprocess.Popen(
                f"unzip -o -q \"{petakit5d_zip_loc}\" -d \"{install_dir}\"", shell=True)
            process.wait()
            os.rename(petakit5d_github_dir, petakit5d_dir)
            os.remove(petakit5d_zip_loc)

            matlab_runtime_ver_dir = os.path.join(matlab_runtime_dir, "R2023a")
            if not os.path.exists(matlab_runtime_ver_dir) or not os.listdir(matlab_runtime_ver_dir):
                os.makedirs(os.path.dirname(matlab_runtime_zip_loc), exist_ok=True)
                # Download MATLAB runtime
                if not os.path.exists(matlab_runtime_zip_loc):
                    urllib.request.urlretrieve(matlab_runtime_url, matlab_runtime_zip_loc)
                process = subprocess.Popen(
                    f"unzip -o -q \"{matlab_runtime_zip_loc}\" -d \"{matlab_runtime_tmp_dir}\"", shell=True)
                process.wait()

                install_file_loc = f"{matlab_runtime_tmp_dir}/install"

                process = subprocess.Popen(
                    f"\"{install_file_loc}\" -agreeToLicense yes -destinationFolder \"{matlab_runtime_dir}\"",
                    shell=True)
                process.wait()
                os.remove(matlab_runtime_zip_loc)
                shutil.rmtree(matlab_runtime_tmp_dir)
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
