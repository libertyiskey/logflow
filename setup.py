from setuptools import setup, find_packages

setup(
    name='logflow',
    version='0.1.0',
    packages=find_packages(),
    description='A logging tool for data engineers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    license='MIT',
    install_requires=[
        # List your project dependencies here.
        # For example: 'requests', 'argparse', etc.
    ],
    entry_points={
        'console_scripts': [
            'logflow=logflow.cli:main',  # Enables the `logflow` command.
        ],
    },
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
