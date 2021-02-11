import setuptools

VERSION = 6.2.0

def get_description():
    with open("README.md", "r") as md:
        long_description = md.read()
    return long_description


def get_requirements():
    with open("requirements.txt") as f:
        requirements = f.readlines()
    return [i.replace(r"\n", "") for i in requirements]


setuptools.setup(
    name="onigmo",
    version=VERSION,
    author="Scodeman",
    author_email="scodeman@scode.io",
    description="Provide onigmo regexp support",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/scodeman/py-onigmo",
    keywords=["onigmo", "regular expression"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=get_requirements(),
)
