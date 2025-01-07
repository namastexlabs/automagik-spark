from setuptools import setup, find_packages

setup(
    name="automagik-cli",
    version="0.1",
    packages=find_packages(),
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
        'setuptools>=65.0.0',  # For pkg_resources
        'httpx>=0.24.0',
        'inquirer>=3.1.3',
        'celery>=5.3.0',
        'redis>=4.5.0',
        'pytest>=7.0.0'
    ],
    entry_points='''
        [console_scripts]
        automagik=automagik_cli.cli:cli
    ''',
)