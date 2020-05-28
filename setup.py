import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="cqh_file_watcher",  # Replace with your own username
    version="0.0.19",
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
