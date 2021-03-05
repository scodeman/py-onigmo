from setuptools import setup, Extension
from setuptools.command.build_py import build_py
import os
import sys
import pathlib
import tarfile
import subprocess
from urllib import request

VERSION = '6.2.0'

ONIGMO_VERSION = f'Onigmo-{VERSION}'

ONIGMO_URL = f"https://github.com/k-takata/Onigmo/archive/{ONIGMO_VERSION}.tar.gz"

ONIGMO_TAR_GZ = pathlib.Path("onigmo.tar.gz")

ONIGMO_SRC = pathlib.Path(f"Onigmo-{ONIGMO_VERSION}")

def get_description():
    with open("README.md", "r") as md:
        long_description = md.read()
    return long_description

def download_onigmo():
    if not ONIGMO_TAR_GZ.exists():
        response = request.urlopen(ONIGMO_URL)
        if response.status != 200:
            raise Exception("failed to download Omigmo")
        ONIGMO_TAR_GZ.write_bytes(response.read())

def move_from(source_dir,target_dir):
    import shutil
    file_names = os.listdir(source_dir)
    for file_name in file_names:
        try: shutil.move(os.path.join(source_dir, file_name), target_dir)
        except: pass

class CustomBuild(build_py):
    def run(self):
        if not ONIGMO_SRC.exists():
          download_onigmo()
          with tarfile.open(ONIGMO_TAR_GZ, "r:gz") as onigmo_tar_gz:
               onigmo_tar_gz.extractall(path=".")
        if sys.platform == "win32":
            from distutils import _msvccompiler
            from distutils.util import get_platform
            platform_name = self.compiler.plat_name or get_platform()
            platform_spec = _msvccompiler.PLAT_TO_VCVARS[platform_name]
            environ = _msvccompiler._get_vc_env(platform_spec)
            subprocess.check_call(
                ["build_nmake.cmd"], shell=True, cwd=ONIGMO_SRC, env=environ
            )
        elif sys.platform in ["linux","darwin"]:
            environ = dict(os.environ)
            subprocess.check_call(["./autogen.sh"], cwd=ONIGMO_SRC, env=environ)
            subprocess.check_call(["./configure"], cwd=ONIGMO_SRC, env=environ)
            subprocess.check_call(["make"], cwd=ONIGMO_SRC, env=environ)
            subprocess.check_call(["make", "install"], cwd=ONIGMO_SRC, env=environ)
        else:
            raise Exception(f"cannot build Onigmo for platform {sys.platform!r}")
        build_py.run(self)

setup(
    name="py-onigmo",
    version=VERSION,
    author="Scodeman",
    author_email="scodeman@scode.io",
    description="Provide onigmo regexp support",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/scodeman/py-onigmo",
    keywords=["onigmo", "regular expression"],
    packages=["onigmo"],
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    cmdclass={'build_py': CustomBuild}
)
