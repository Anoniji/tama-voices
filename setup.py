#!/usr/bin/env python3
import setuptools
import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

setuptools.setup(
    name="tama-voices",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Niji Ano",
    author_email="github@anoniji.dev",
    description="Tools for creating voicepacks for Tama",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Creative Commons Zero v1.0 Universal",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=requirements,
)
