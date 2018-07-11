import discord
from discord.ext import commands
import operator
defaultColour = 0x36393e

class WhosPlaying:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def whosplaying(self, ctx, *, game):
        """Shows who's playing a specific game"""
        if len(game) <= 1:
            await ctx.send("```The game should be at least 2 characters long...```", delete_after=5.0)
            return

        user = ctx.message.author
        guild = ctx.message.guild
        members = guild.members
        playing_game = ""
        count_playing = 0

        for member in members:
            if not member:
                continue
            if not member.activity or not member.activity.name:
                continue
            if member.bot:
                continue
            if game.lower() in member.activity.name.lower():
                count_playing += 1
                if count_playing <= 15:
                    playing_game += ":trident: {} ({})\n".format(member.name, member.activity.name)

        if playing_game == "":
            await self.bot.say("```Search results:\nNo users are currently playing that game.```")
        else:
            msg = playing_game
            if count_playing > 15:
                showing = "(Showing 15/{})".format(count_playing)
            else:
                showing = "({})".format(count_playing)

            em = discord.Embed(description=msg, colour=defaultColour)
            em.set_author(name=f"""Who's playing "{game}"? {showing}""", icon_url='https://cdn.discordapp.com/attachments/323045050453852170/465813711664316417/spectrumRainbow.gif')
            await ctx.send(embed=em)

    @commands.command(pass_context=True, no_pm=True)
    async def currentgames(self, ctx):
        """Shows the most played games right now"""
        user = ctx.message.author
        guild = ctx.message.guild
        members = guild.members

        freq_list = {}
        for member in members:
            if not member:
                continue
            if not member.activity or not member.activity.name:
                continue
            if member.bot:
                continue
            if member.activity.name not in freq_list:
                freq_list[member.activity.name] = 0
            freq_list[member.activity.name] += 1

        sorted_list = sorted(freq_list.items(),
                             key=operator.itemgetter(1),
                             reverse=True)

        if not freq_list:
            await self.bot.say("```Search results:\nNo users are currently playing any games. Odd...```")
        else:
            # Create display and embed
            msg = ""
            max_games = min(len(sorted_list), 10)

            em = discord.Embed(description=msg, colour=defaultColour)
            for i in range(max_games):
                game, freq = sorted_list[i]
                if int(freq_list    [game]) < 2:
                    ammount = "1 person"
                else:
                    ammount = f"{int(freq_list[game])} people"
                em.add_field(name=game, value=ammount)
            em.set_thumbnail(url=guild.icon_url)
            em.set_footer(text="Do $whosplaying <game> to see whos playing a specific game")
            em.set_author(name="Top games being played right now in the server:", icon_url='https://cdn.discordapp.com/attachments/323045050453852170/465813711664316417/spectrumRainbow.gif')
            await ctx.send(embed=em)



def setup(bot):
    n = WhosPlaying(bot)
    bot.add_cog(n)