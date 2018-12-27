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
# pylint: disable=R0903
import discord
from discord.ext import commands
import async_cse

class Google:
    """Commands for searching things on Google."""

    def __init__(self, bot):
        self.bot = bot
        self.google = async_cse.Search("API KEY HERE")  # insert your key here

    @commands.command(name="google", aliases=["g"])
    async def google_(self, ctx, *, query: str):
        """Searches things on Google."""
        try:
            resp = (await self.google.search(query))[0]
        except async_cse.NoResults:
            return await ctx.send("Oops, your query returned no results.")
        except (async_cse.NoMoreRequests, async_cse.APIError):
            return await ctx.send("An internal error occurred, please try again later.")
        else:
            embed = discord.Embed(
                title=resp.title,
                description=resp.description,
                color=discord.Color.blurple(),
                url=resp.url,
            )
            url = ctx.author.avatar_url_as(static_format="png", size=128)
            embed.set_footer(text="Requested by {}".format(ctx.author), icon_url=url)
            embed.set_image(url=resp.image_url)
            await ctx.send(embed=embed)


def setup(bot):
    """Adds the cog"""
    bot.add_cog(Google(bot))
