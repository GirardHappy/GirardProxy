from setuptools import setup, find_packages

setup(
    name = "GirardProxyScraper",
    version = "0.9.0",
    author = "Girard",
    author_email = "girardhappy.it@gmail.com",
    description = ("Python module that scrape retrive working proxy addresses"),
    license = "MIT",
    keywords = "proxy scraper",
    packages=find_packages('srcpython setup.py sdist bdist_wheel'),
    long_description="""A module that offer you the possibility to create an object that continuosly request a proxies address, verify if they work using multithreading and retrive to you one of them <3""",
    classifiers=[
        'Development Status :: 4 - Beta',
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License"
    ],
)
