import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cqh_file_watcher",  # Replace with your own username
    version="0.0.10",
    author="chenqinghe",
    author_email="1832866299@qq.com",
    description="tools like vscode file-watcher but for command only",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
        "click",
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
