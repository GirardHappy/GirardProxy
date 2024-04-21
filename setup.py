from setuptools import setup, find_packages

setup(
    name = "GirardProxy",
    version = "0.9.41",
    author = "Girard",
    author_email = "girardhappy.it@gmail.com",
    description = ("Python module that scrape and retrive working proxy addresses"),
    license = "MIT",
    keywords = "proxy scraper",
    packages=['src'],
    long_description="""A module that offer you the possibility to create an object that continuosly request proxies addresses, verify if they work using multithreading and retrive to you one of them <3""",
    install_requires=[
          'requests[socks]'
      ],
    classifiers=[
        'Development Status :: 4 - Beta',
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License"
    ]
)
