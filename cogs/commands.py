import discord
from discord.ext import commands

class MiscCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    # ban
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, reason='W imie Polski podziemnej'):
        await member.ban(reason=reason)
        await ctx.channel.send(f'{ctx.author} ustrzelił {member.mention}', delete_after=5)

    # kick
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member : discord.Member, reason='Bez powodu'):
        await member.kick(reason=reason)
        await ctx.channel.send(f'{ctx.author} wykopał {member.mention}', delete_after=5)

    # unban
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        banned = await ctx.guild.bans()
        member_name, member_discriminator = member.split()
        for ban_entry in banned:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.name} przeprasza za swojego zachowanie o.o')

    # server information
    @commands.command()
    async def goals(self, ctx):
        name = str(ctx.guild.name)
        description = 'Niech żyje reżim!'
        owner = str(ctx.guild.owner)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)
        embed = discord.Embed(
            title=name,
            description=description,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name='Owner', value=owner, inline=False)
        embed.add_field(name='Member Count', value=memberCount, inline=False)
        embed.add_field(name='Icon', value=icon, inline=False)

        await ctx.send(embed=embed, delete_after=10)

    # clear chat
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, limit: int):
            await ctx.channel.purge(limit=limit+1)
            await ctx.message.delete(delete_after=0.1)

    # error handler
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Chyba śnisz! Wszystko widziałem i zawiadomiłem policje!")


    # poring.
    @commands.command()
    async def glut(self, ctx):
        await ctx.send('Poringi są słodkimi dropsami pochodzącymi z ogromnej krainy zwanej Ymir.', delete_after=5)

    # bot activity
    @commands.command()
    async def stramuj(self, ctx, game):
        await self.client.change_presence(activity=discord.Streaming(name=game, url="https://twitch.tv/shuuS", delete_after=5))

    @commands.command()
    async def sentence(self, ctx, mood):
        await self.client.change_presence(activity=discord.Activity(name=mood, delete_after=5))

async def setup(client):
    await client.add_cog(MiscCommands(client))
