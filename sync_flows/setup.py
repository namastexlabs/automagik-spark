from setuptools import setup, find_packages

setup(
    name="sync_flows",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy>=1.4.0",
        "python-dotenv>=1.0.0",
        "httpx>=0.24.0",
    ],
    python_requires=">=3.8",
)
