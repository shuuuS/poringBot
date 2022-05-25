import discord
from discord.ext import commands
import os
from music import Player


from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.messages = True

client = commands.Bot(command_prefix='.', intents=intents)
client.remove_command('help')


#information about bot activate
@client.event
async def on_ready():
    print('Aaaaaaaaa, siemanko!:3')
    await client.change_presence(activity=discord.Game(name='Polowanie na wrogów ojczyzny'))

#memberJoin
@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='w-s-t-ę-p')
    await channel.send(f'{member.mention} nas odwiedzil')

#memberLeave
@client.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, name='w-s-t-ę-p')
    await channel.send(f'{member.mention} nas olal, htfu')

#onMessage
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    words = ['jp2']
    for i in words:
        role = discord.utils.get(message.author.guild.roles, name='Jan Paweł 2')
        await message.author.add_roles(role)
        await message.channel.send('Brawo, zostałeś nowym katolikiem')


#modmail
    empty_array = []
    modmail_channel = discord.utils.get(client.get_all_channels(), name='mod-mail')

    if str(message.channel.type) == 'private':
        if message.attachments != empty_array:
            files = message.attachments
            await modmail_channel.send('[' + message.author.display_name + ']')

            for file in files:
                await modmail_channel.send(file.url)
        else:
            await modmail_channel.send('[' + message.author.display_name + '] ' + message.content)

    elif str(message.channel) == 'mod-mail' and message.content.startswith('<'):
        member_object = message.mentions[0]
        if message.attachments != empty_array:
            files = message.attachments
            await member_object.send('[' + message.author.display_name + ']')

            for file in files:
                await member_object.send(file.url)
        else:
            index = message.content.index(' ')
            string = message.content
            mod_message = string[index:]
            await member_object.send('[' + message.author.display_name + ']' + mod_message)

#Anti-spam
    if str(message.channel) == 'memy' and message.content != '':
        await message.channel.purge(limit=1)
    if str(message.channel) == 'mod-mail' and message.content != '':
        await message.channel.purge(limit=1)

#randomThings
    if message.content.startswith('kiedy nostale'):
        if str(message.author) == 'shuS#2539':
            await message.channel.send('Czerwony przyjaciel, twierdzi, że ' + str(message.author)+'nigdy nie zagra')
        else:
            await message.channel.send('Czerwony przyjaciel twierdzi, że nie warto :)')
            await message.channel.send(file=discord.File('uwuPoring.png'))
    if message.content == 'gupi poring':
        await message.channel.send('Sam jesteś głupi, ' + str(message.author))

#important
    await client.process_commands(message)


#banCommand
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, reason='W imie Polski podziemnej'):
    await member.ban(reason=reason)
    await ctx.channel.send(f'{ctx.author} ustrzelił {member.mention}')

#unbanCommand
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned = await ctx.guild.bans()
    member_name, member_discriminator = member.split()

    for ban_entry in banned:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.name} przeprasza za swojego zachowanie o.o')

#kickCommand
@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member, reason='Bez powodu'):
    await member.kick(reason=reason)
    await ctx.channel.send(f'{ctx.author} wykopał {member.mention}')

#commandList
@client.command()
async def list(ctx):
    commandList = ['Prefix:[.]: ',
                   'server',
                   'poring']
    onMessageList = ['kiedy nostale',
                     'gupi poring']
    embed = discord.Embed(
        title='List of commands'

    )
    embed.add_field(name='Command list: ', value=commandList, inline=False)
    embed.add_field(name='On Message list: ', value=onMessageList, inline=False)


    await ctx.send(embed=embed, delete_after = 10)

#serverInfo
@client.command()
async def server(ctx):
    name = str(ctx.guild.name)
    description = 'Niech żyje reżim!'
    owner = str(ctx.guild.owner)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

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

    await ctx.send(embed=embed, delete_after = 10)

#cleanChat
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, limit: int):
        await ctx.channel.purge(limit=limit+1)
        await ctx.message.delete()

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Chyba śnisz! Wszystko widziałem i zawiadomiłem policje!")


#informationAboutPoring
@client.command(aliases=['poring'])
async def glut(ctx):
    await ctx.send('Poringi są słodkimi dropsami pochodzącymi z ogromnej krainy zwanej Ymir.')

#botActivity
@client.command()
async def stramuj(ctx, game):
    await client.change_presence(activity=discord.Streaming(name=game, url="https://twitch.tv/shuuuS"))

#weryfikacja
@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 975358574928736276:
        if payload.emoji.name == '✅':
            guild = client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            rola = discord.utils.get(guild.roles, name='Jan Paweł 2')
            await member.add_roles(rola)

@client.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == 975358574928736276:
        if payload.emoji.name == '✅':
            guild = client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            rola = discord.utils.get(guild.roles, name='Jan Paweł 2')
            await member.remove_roles(rola)

#musicBot
async def setup():
    await client.wait_until_ready()
    client.add_cog(Player(client))

client.loop.create_task(setup())



client.run(DISCORD_TOKEN)
