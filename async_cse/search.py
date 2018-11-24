import aiohttp
from urllib.parse import quote

class NoResults(Exception):
    pass

class APIError(Exception):
    pass

class Result:
    """
    Represents a result from a search query.
    You do not make these on your own, you usually get them from async_cse.Search.search.
    """
    
    def __init__(self, title, description, url, image_url):
        self.title = title
        self.description = description
        self.url = url
        self.image_url = image_url

    def __str__(self):
        return "<async_cse.search.Result object, url: {}, image_url: {}>".format(self.url, self.image_url)

    def __repr__(self):
        return "<async_cse.search.Result object, url: {}, image_url: {}>".format(self.url, self.image_url)

    @classmethod
    def from_raw(cls, data):
        results = list()
        for item in data["items"]:
            title = item["title"]
            desc = item["snippet"]
            url = item["link"]
            i = item.get("pagemap")
            if not i:
                image_url = None
            else:
                img = i.get("cse_image")
                if not i:
                    image_url = None
                else:
                    try:
                        image_url = img[0]["src"]
                    except TypeError:
                        image_url = None
            results.append(cls(title, desc, url, image_url))
        return results

class Search:
    """Client for custom searches."""

    def __init__(self, api_key: str, engine_id: str="015786823554162166929:mywctwj8es4", session: aiohttp.ClientSession=None):
        self.api_key = api_key # API key for the CSE API 
        self.engine_id = engine_id
        self.search_url = "https://www.googleapis.com/customsearch/v1?key={}&cx={}&q={}&safe={}" # URL for requests
        self.session = session or None
    
    def __repr__(self):
        return "<async_cse.search.Search object, engine_id: {}>".format(self.engine_id)

    def __str__(self):
        return "<async_cse.search.Search object, engine_id: {}>".format(self.engine_id)

    async def close(self):
        """Properly close the client."""
        await self.session.close()

    async def search(self, query: str, safesearch=True):
        """Searches Google for a given query."""
        if not self.session:
            self.session = aiohttp.ClientSession() # Session for requests
        # ---- compatibility ---- #
        if safesearch == True:
            safesearch = "active"
        elif safesearch == False:
            safesearch = "off"
        # ----------------------- #
        url = self.search_url.format(self.api_key, self.engine_id, quote(query), safesearch)
        async with self.session.get(url) as r:
            j = await r.json()
            e = j.get("error")
            if e:
                raise APIError(e)
            if not j.get("items"):
                raise NoResults("Your query {} returned no results.".format(query))

        return Result.from_raw(j)
