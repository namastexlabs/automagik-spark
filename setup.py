from setuptools import setup, find_packages

setup(
    name="automagik",
    version="0.1.0",
    packages=find_packages(include=['automagik_cli*', 'core*']),
    package_data={
        'automagik_cli': ['templates/*'],
    },
    include_package_data=True,
    install_requires=[
        'click>=8.0.0',
        'sqlalchemy>=2.0.0',
        'python-dotenv>=1.0.0',
        'tabulate>=0.9.0',
        'croniter>=1.4.1',
        'pytz>=2023.3',
        'setuptools>=65.0.0',
        'httpx>=0.24.0',
        'inquirer>=3.1.3',
        'celery>=5.3.0',
        'redis>=4.5.0',
        'psycopg2-binary>=2.9.0',  # PostgreSQL adapter
        'alembic>=1.12.0',  # Database migrations
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'isort>=5.12.0',
            'flake8>=6.1.0',
            'mypy>=1.5.0',
        ],
    },
    entry_points='''
        [console_scripts]
        automagik=automagik_cli.cli:cli
    ''',
    python_requires='>=3.9',
)