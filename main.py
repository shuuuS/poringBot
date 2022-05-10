import discord
from discord.ext import commands
import os
from music import Player


from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


client = commands.Bot(command_prefix='.')
client.remove_command('help')


#information about bot activate
@client.event
async def on_ready():
    print('Aaaaaaaaa, siemanko!:3')
    await client.change_presence(activity=discord.Game(name='Polowanie na wrogów ojczyzny'))

#onMessage
@client.event
async def on_message(message):
    if message.author == client.user:
        return
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
    embed.add_field(name='Command list: ', value=commandList, inline=True)
    embed.add_field(name='On Message list: ', value=onMessageList, inline=True)


    await ctx.send(embed=embed)
#serverInfo
@client.command()
async def server(ctx):
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
    embed.add_field(name='Owner', value=owner, inline=True)
    embed.add_field(name='Member Count', value=memberCount, inline=True)

    await ctx.send(embed=embed)

#cleanChat
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=limit+1)
        await ctx.message.delete()

@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Chyba śnisz! Wszystko widziałem i zawiadomiłem policje!")


#informationAboutPoring
@client.command(aliases=['poring'])
async def glut(ctx):
    await ctx.send('Poringi są słodkimi dropsami pochodzącymi z ogromnej krainy zwanej Ymir.')

#musicBot
async def setup():
    await client.wait_until_ready()
    client.add_cog(Player(client))

client.loop.create_task(setup())



client.run(DISCORD_TOKEN)
