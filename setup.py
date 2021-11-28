import setuptools

setuptools.setup(
    name="fake_git",
    version="0.0.13",
    url="https://github.com/brosiak/fake_git",
    author="Bartosz Rosiak",
    author_email="rosiakbartosz0@gmail.com",
    description="Allows to fake git repository",
    # long_description=open('DESCRIPTION.rst').read(),
    packages=setuptools.find_packages(),
    install_requires=['docopt'],
    entry_points={
        'console_scripts': [
            'fake_git = fake_git.fake_git_main:main',
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)
