import platform

from setuptools import setup, find_packages

if platform.system() == "Windows":
    data_files=[(".", ["libhunspell.dll"]),]
else:
    data_files=[]

setup(
        name="Hunspell-CFFI",
        version="1.1.0",
        description="A CFFI binding for the Hunspell spellcheck library",
        url="https://github.com/Sentynel/hunspell-cffi",
        author="Sam Lade",
        author_email="hunspell-cffi@sentynel.com",
        license="MIT",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
        ],
        keywords="spelling,spellcheck",
        packages=["hunspell_cffi"],
        setup_requires=["cffi>=1.0.0",],
        cffi_modules=["hunspell_cffi/build.py:ffi"],
        install_requires=["cffi>=1.0.0",],
        data_files=data_files,
)
