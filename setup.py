import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="favapy",
    version="0.3.1",
    author="Mikaela Koutrouli",
    author_email="mikaela.koutrouli@cpr.ku.dk",
    description="Infer Functional Associations using Variational Autoencoders on -Omics data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikelkou/VAE_Functional_associations",
    project_urls={
        "Bug Tracker": "https://github.com/mikelkou/VAE_Functional_associations/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7", 
    install_requires=["tensorflow", "keras", "numpy", "pandas"]
)
