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
import asyncio
import async_cse

# ----
# Credit to https://github.com/XuaTheGrate
# ----


async def main():
    """Starts the Search session."""

    google = async_cse.Search("Your API key")
    try:
        results = await google.search(input("Type something to Google it! "))
    except async_cse.NoResults:
        print("Nothing found.")
        return
    except async_cse.NoMoreRequests:
        print("API is out of requests, please use another API key.")
    except async_cse.APIError:
        print("Something went wrong.")
    else:
        for result in results:
            print(result.title)
            print(result.description)
            print("\n", result.url)
            input("\n\nPress enter to go to next result.")
    await main()


if __name__ == "__main__":
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(main())
