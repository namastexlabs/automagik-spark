from setuptools import setup, find_packages

setup(
    name="automagik-cli",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click>=8.0.0',
        'python-dotenv>=1.0.0',
        'sqlalchemy>=1.4.0',
        'tabulate>=0.8.0',
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