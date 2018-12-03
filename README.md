[![Build Status](https://travis-ci.org/crrapi/async-cse.png?branch=master)](https://travis-ci.org/crrapi/async-cse)
<a href="https://github.com/crrapi/async-cse"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
# async-cse
Asyncio API wrapper for the [Google Custom Search JSON API](https://developers.google.com/custom-search/v1/overview).
# Installation
`pip3 install -U async_cse`
# Usage
```python
import async_cse

client = async_cse.Search("Your API Key") # create the Search client (uses Google by default!)
results = await client.search("Python", safesearch=False) # returns a list of async_cse.Result objects
print(results[0].title, results[0].description, results[0].url, results[0].image_url) # Title, snippet, URL, and Image URL
await client.close() # Run this when cleaning up.
```
To use Search objects with a custom search engine, provide the ID of the search engine.
```python
async_cse.search.Search("Your API Key", engine_id="015786823554162166929:mywctwj8es4")
```
SafeSearch can also be turned off by setting `safesearch=False` when using the `search()` method.
# Getting an API key
You can get an API key by going [here](https://developers.google.com/custom-search/v1/overview) and scrolling down to the **API key** section.
![API key](https://i.imgur.com/pHXFiI8.png "Getting an API key")
