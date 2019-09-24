import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="gym_tak",
    version='0.0.3',
    author='DrSmugleaf',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DrSmugleaf/gym-tak',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
