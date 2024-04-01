import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Logflow",  # Replace with your own username
    version="0.0.1",
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
    package_dir={"": "src"},  
    packages=setuptools.find_packages(where="src"),,
    python_requires=">=3.6",
    install_requires=[], 
    entry_points={
        'console_scripts': [
            'logflow=logflow.cli:main',
        ],
    },
)
