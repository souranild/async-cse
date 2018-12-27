import async_cse
import asyncio
import os

API_KEY = os.environ.get("API_KEY")
client = async_cse.Search(API_KEY)


async def main():
    result = (await client.search("Google"))[0]
    await client.close()
    print(result.title)
    print(result.description)
    print(result.image_url)
    print(result.url)


asyncio.get_event_loop().run_until_complete(main())
