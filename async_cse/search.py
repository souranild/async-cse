import aiohttp
from urllib.parse import quote

class NoResults(Exception):
    pass


class Result:
    """
    Represents a result from a search query.
    You do not make these on your own, you usually get them from async_cse.Search.search.
    """
    
    def __init__(self, title, description, url):
        self.title = title
        self.description = description
        self.url = url

    @classmethod
    def from_raw(cls, data):
        results = list()
        for item in data["items"]:
            title = item["title"]
            desc = item["snippet"]
            url = item["link"]
            results.append(cls(title, desc, url))
        return results


class Search:
    """Client for searching Google."""

    def __init__(self, api_key: str, *, engine_id: str = None, safesearch: bool = None):
        self.api_key = api_key # API key for the CSE API 
        self.engine_id = engine_id or "015786823554162166929:mywctwj8es4" # CSE for searching Google
        self.safesearch = safesearch or "active" # can be set to 'off' or 'active' by default
        self.search_url = "https://www.googleapis.com/customsearch/v1?key={}&cx={}&q={}&safe={}" # URL for requests
        self.session = aiohttp.ClientSession() # Session for requests

    async def search(self, query: str):
        """Searches Google for a given query."""
        url = self.search_url.format(self.api_key, self.engine_id, quote(query), self.safesearch)
        async with self.session.get(url) as r:
            j = await r.json()
            if not j.get("items"):
                raise NoResults("Your query {} returned no results.".format(query))
        return Result.from_raw(j)
