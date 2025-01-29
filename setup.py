from setuptools import setup, find_packages

# Read the contents of README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="automagik",
    version="0.1.0",
    author="NamasteX Labs",
    author_email="dev@namastexlabs.com",
    description="AI-driven workflow automation with LangFlow integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/namastexlabs/automagik",
    project_urls={
        "Bug Tracker": "https://github.com/namastexlabs/automagik/issues",
        "Documentation": "https://github.com/namastexlabs/automagik/tree/main/docs",
    },
    packages=find_packages(include=['automagik*']),
    include_package_data=True,
    install_requires=[
        'click>=8.0.0',
        'sqlalchemy[asyncio]>=2.0.0',
        'asyncpg>=0.28.0',  # Async PostgreSQL adapter
        'python-dotenv>=1.0.0',
        'tabulate>=0.9.0',
        'croniter>=1.4.1',
        'httpx>=0.24.0',
        'alembic>=1.12.0',  # Database migrations
        'fastapi>=0.100.0',  # API framework
        'uvicorn>=0.23.0',  # ASGI server
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-asyncio>=0.21.0',
            'black>=23.0.0',
            'isort>=5.12.0',
            'flake8>=6.1.0',
            'mypy>=1.5.0',
            'build>=1.0.0',
            'twine>=4.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'automagik=automagik.cli.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: FastAPI",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Automation",
    ],
    python_requires='>=3.9',
    keywords='automation, workflow, langflow, ai, llm',
)