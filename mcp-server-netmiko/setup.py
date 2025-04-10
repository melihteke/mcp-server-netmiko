from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='mcp-server-netmiko',
    version='1.0.0',
    author='Melih Teke',
    author_email='me@mteke.com',
    description='MCP Server for interacting with Network devices',
    long_description=f"{long_description}\n\nFor more information, visit the [PyPI page](https://pypi.org/project/mcp-server-netmiko/).\n\nYou can also connect with me on [LinkedIn](https://www.linkedin.com/in/melih-teke/).",
    long_description_content_type='text/markdown',
    url='https://github.com/melihteke/mcp-server-netmiko',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    install_requires=[
        'netmiko',
        'mcp[cli]',
    ],
)