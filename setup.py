import setuptools

with open("readme.MD", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ClassicLikeIguana",  # Replace with your own username
    version="0.1.0",
    author="Alexander Bigerl",
    author_email="bigerl@mail.upb.de",
    description="Benchmarking tool for SPARQL triple stores with an interactive commandline interface.adjectives ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dice-group/ClassicLikeIguana",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System  :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
    scripts=['ClassicLikeIguana.py'],
    install_requires=['pyyaml']

)
