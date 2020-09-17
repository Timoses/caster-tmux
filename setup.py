import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="caster-plugins",
    version="0.0.1",
    author="Timo Funke",
    author_email="timosesu@gmail.com",
    description="Plugins for Caster",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timoses/caster-plugins",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
    python_requires='>=3.6',
    install_requires=[
        "libtmux",
    ]
)
