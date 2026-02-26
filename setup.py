from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="print-statements-hook",
    version="0.1.0",
    author="Kuldeep Modh",
    author_email="kuldeepmodh1823@gmail.com",
    description="A pre-commit hook to detect and prevent print statements in Python code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kuldeepmodh/print-statements-hook",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "check-print-statements=print_statement_hook.hook:check_print_statements",
        ],
    },
)