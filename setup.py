from setuptools import setup, find_packages

setup(
    name="automagik",
    version="0.1.0",
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
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-asyncio>=0.21.0',
            'black>=23.0.0',
            'isort>=5.12.0',
            'flake8>=6.1.0',
            'mypy>=1.5.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'automagik=automagik.cli.main:cli',
        ],
    },
    python_requires='>=3.9',
)