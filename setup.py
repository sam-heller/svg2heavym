import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="svg2heavym", # Replace with your own username
    version="0.0.1",
    author="Sam Heller",
    author_email="sam@faitaccomp.li",
    description="Package to import external SVG files into HeavyM (https://heavym.net)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sam-heller/svg2heavym",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities"
    ],
    python_requires='>=3.6',
)