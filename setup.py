import setuptools
import os

# Read the long description from the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Get the version from the VERSION environment variable; default to '0.0.1' if not set
version = os.getenv('VERSION', '0.0.1')

setuptools.setup(
    name="logflow",  # Replace with your package name
    version=version,  # Use the dynamically set version
    author="libertyiskey",
    author_email="your.email@example.com",
    description="A logging utility for data engineers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/libertyiskey/logflow",
    project_urls={
        "Bug Tracker": "https://github.com/libertyiskey/logflow/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
    install_requires=[],  # Add any dependencies your package needs
    entry_points={
        'console_scripts': [
            'logflow=logflow.cli:main',  # Ensure this points to your main CLI entry point
        ],
    },
)
