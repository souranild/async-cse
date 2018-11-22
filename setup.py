import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(name='async_cse',
      version='0.1',
      description='API wrapper for the Google Custom Search JSON API. https://developers.google.com/custom-search/v1/overview',
      url='https://github.com/crrapi/async-cse',
      author='Chris Rrapi',
      author_email='toadawes12@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=['aiohttp'],
      classifiers=[
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ]
)