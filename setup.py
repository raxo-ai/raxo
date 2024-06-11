from setuptools import setup, find_packages

setup(
    name="raxo",
    version="0.0.1",
    author="Bipul Kumar Singh",
    author_email="bipulsinghkashyap@gmail.com",
    description="Raxo is a Python package designed to streamline the process of converting natural language queries "
                "into SQL queries.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/raxo-ai/raxo",
    packages=find_packages(where="src", include=["raxo*"]),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "openai>=1.30.1",
        "chromadb>=0.5.0"
    ],
    extras_require={
        "mysql": ["mysql-connector-python>=8.4.0"],
        "vertica": ["vertica-python>=1.3.8"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
