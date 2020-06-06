import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

import os
name = 'cqh_file_watcher'
_dir = os.path.dirname(os.path.abspath(__file__))

init_path = os.path.join(_dir, name, '__init__.py')


def read_version():
    d = {}
    code = open(init_path).read()
    code = compile(code, '<string>', 'exec', dont_inherit=True)
    exec(code, d, d)
    return d['__version__']

version = read_version()
print("version:{}".format(version))

setuptools.setup(
    name=name,  # Replace with your own username
    version=version,
    author="chenqinghe",
    author_email="1832866299@qq.com",
    description="tools like vscode file-watcher but for command only",
    long_description=long_description,
    url="https://github.com/chen19901225/cqh_file_watcher",
    packages=setuptools.find_packages(),
    install_requires=[
        "pyinotify"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    entry_points={
        "console_scripts": [
            "cqh_file_watcher = cqh_file_watcher.run:main",
        ],
    },
    python_requires='>=3.6',
)
