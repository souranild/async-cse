# async-cse
Asyncio API wrapper for the [Google Custom Search JSON API](https://developers.google.com/custom-search/v1/overview).
# Installation
`pip3 install async_cse`
# Usage
```python
import async_cse

s = async_cse.search.Search("Your API Key") # create the Search client (uses Google by default!)
r = await s.search("Python") # returns a list of async_cse.search.Result objects
print(r.title, r.description) # Title text
print(r.url) # URL of the search result
```
To use Search objects with a custom search engine, provide the ID of the search engine.
```python
async_cse.search.Search("Your API Key", engine_id="015786823554162166929:mywctwj8es4")
```
SafeSearch can also be turned off by setting `safesearch="off"`.
# Getting an API key
You can get an API key by going [here](https://developers.google.com/custom-search/v1/overview) and scrolling down to the **API key** section.
![API key](https://i.imgur.com/pHXFiI8.png "Getting an API key")
