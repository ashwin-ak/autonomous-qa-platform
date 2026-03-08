#!/usr/bin/env python
"""Setup script for Autonomous QA Platform."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = (this_directory / "requirements.txt").read_text(encoding="utf-8").strip().split("\n")
requirements = [req.strip() for req in requirements if req.strip() and not req.startswith("#")]

# Read dev requirements
dev_requirements = (this_directory / "requirements-dev.txt").read_text(encoding="utf-8").strip().split("\n")
dev_requirements = [req.strip() for req in dev_requirements if req.strip() and not req.startswith("#") and not req.startswith("-r")]

setup(
    name="autonomous-qa-platform",
    version="1.0.0",
    author="Ashwin Kulkarni",
    author_email="ashwin@example.com",
    description="An AI-driven Autonomous QA platform that generates tests, executes them, and performs root cause analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ashwin-qa/autonomous-qa-platform",
    project_urls={
        "Bug Tracker": "https://github.com/ashwin-qa/autonomous-qa-platform/issues",
        "Documentation": "https://github.com/ashwin-qa/autonomous-qa-platform/docs",
        "Source Code": "https://github.com/ashwin-qa/autonomous-qa-platform",
    },
    packages=find_packages(exclude=["tests", "examples", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Quality Assurance",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
    },
    entry_points={
        "console_scripts": [
            "autonomous-qa=examples.basic_workflow:main",
        ],
    },
    include_package_data=True,
    keywords="qa testing automation playwright openai llm agents",
    zip_safe=False,
)