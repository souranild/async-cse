"""
MIT License

Copyright (c) 2018 Chris Rrapi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from urllib.parse import quote

import aiohttp


class CSEBaseException(Exception):
    """Base class for all async_cse Exceptions."""


class NoResults(CSEBaseException):
    """Query yielded no results."""


class APIError(CSEBaseException):
    """Internal API error."""


class NoMoreRequests(CSEBaseException):
    """Out of requests for today."""


GOOGLE_FAVICON = "https://image.flaticon.com/teams/slug/google.jpg"


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
        return "<async_cse.search.Result object, url: {}, image_url: {}>".format(
            self.url, self.image_url
        )

    def __repr__(self):
        return "<async_cse.search.Result object, url: {}, image_url: {}>".format(
            self.url, self.image_url
        )

    @classmethod
    def from_raw(cls, data, img):
        """Converts a dict to Result objects"""
        results = list()
        for item in data["items"]:
            title = item["title"]
            desc = item["snippet"]
            if img:
                image_url = item["link"]
                try:
                    url = item["image"]["contextLink"]
                except KeyError:
                    url = image_url
            else:
                url = item["link"]
                i = item.get("pagemap")
                if not i:
                    image_url = GOOGLE_FAVICON
                else:
                    img = i.get("cse_image")
                    if not i:
                        image_url = GOOGLE_FAVICON
                    else:
                        try:
                            image_url = img[0]["src"]
                            if image_url.startswith("x-raw-image"):
                                image_url = i["cse_thumbnail"][0]["src"]
                        except TypeError:
                            image_url = GOOGLE_FAVICON
            results.append(cls(title, desc, url, image_url))
        return results


class Search:
    """Client for custom searches."""

    def __init__(
        self,
        api_key: str,
        engine_id: str = "015786823554162166929:mywctwj8es4",
        image_engine_id: str = "015786823554162166929:szgrbbrrox0",
        session: aiohttp.ClientSession = None,
    ):
        self.api_key = api_key  # API key for the CSE API
        self.engine_id = engine_id
        self.image_engine_id = image_engine_id
        self.search_url = (
            "https://www.googleapis.com/customsearch/v1?key={}&cx={}&q={}&safe={}"
        )  # URL for requests
        self.session = session or None

    def __repr__(self):
        return "<async_cse.search.Search object, engine_id: {}>".format(self.engine_id)

    def __str__(self):
        return "<async_cse.search.Search object, engine_id: {}>".format(self.engine_id)

    async def close(self):
        """Properly close the client."""
        await self.session.close()

    async def search(self, query: str, *, safesearch=True, image_search=False):
        """Searches Google for a given query."""
        if not self.session:
            self.session = aiohttp.ClientSession()  # Session for requests
        # ---- compatibility ---- #
        if safesearch:
            safesearch = "active"
        else:
            safesearch = "off"
        if image_search:
            image_search = "image"
        # ----------------------- #
        url = self.search_url.format(
            self.api_key,
            self.image_engine_id if image_search else self.engine_id,
            quote(query),
            safesearch,
        )
        if image_search:
            url += "&searchType=image"
        async with self.session.get(url) as resp:
            j = await resp.json()
            error = j.get("error")
            if error:
                if error["errors"][0]["domain"] == "usageLimits":
                    raise NoMoreRequests(
                        "[100 Request Limit]\
                        You have to wait a day before you can make more requests."
                    )
                else:
                    raise APIError(
                        ", ".join([error["message"] for err in error["errors"]])
                    )
            if not j.get("items"):
                raise NoResults("Your query {} returned no results.".format(query))
        return Result.from_raw(j, img=image_search)
