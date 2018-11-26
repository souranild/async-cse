import async_cse
import asyncio

async def main():
    google = async_cse.Search("AIzaSyCyBo7wlv-6VFxcM4WxCuBGK6V2kUmKfWY")
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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())