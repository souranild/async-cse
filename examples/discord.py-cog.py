# Example Google cog for discord.py@rewrite bots.
# Made by chr1s#7185
import discord
from discord.ext import commands
import async_cse

class Google:

    def __init__(self, bot):
        self.bot = bot
        self.google = async_cse.Search("API KEY HERE") # insert your key here

    @commands.command(name="google", aliases=['g'])
    async def google_(self, ctx, *, query: str):
        """Searches things on Google."""
        try:
            r = (await self.google.search(query))[0]
        except async_cse.NoResults:
            return await ctx.send("Oops, your query returned no results.")
        except (async_cse.NoMoreRequests, async_cse.APIError):
            return await ctx.send("An internal error occurred, please try again later.")
        else:
            e = discord.Embed(title=r.title, description=r.description, color=discord.Color.blurple(), url=r.url)
            url = ctx.author.avatar_url_as(static_format="png", size=128)
            e.set_footer(text="Requested by {}".format(ctx.author), icon_url=url)
            e.set_image(url=r.image_url)
            await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Google(bot))
