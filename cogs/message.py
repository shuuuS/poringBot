import os
import discord
from discord.ext import commands
import random

class MessageEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name='Polowanie na wrogów ojczyzny'))
        print('Aaaaaaaaa, siemanko!:3')

    # server join
    @commands.Cog.listener()
    async def joined(self, member):
        channel = discord.utils.get(member.guild.channels, name='w-s-t-ę-p')
        await channel.send(f'{member.mention} nas odwiedzil')

    # server leave
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.channels, name='w-s-t-ę-p')
        await channel.send(f'{member.mention} nas olal, htfu')

    # on-message
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

    # rolling images
        if message.content.startswith('foczka'):
            images = os.path.join(os.getcwd(), "resources")

            def select_random_image_path():
                return os.path.join(images, random.choice(os.listdir(images)))
            await message.channel.send("Bark bark", file=discord.File(select_random_image_path()))

    # giga ulta super rare rank
        if message.content == 'jp2':
            print("jp2 detected") 
            role = discord.utils.get(message.author.guild.roles, name='Jan Paweł 2')
            print(f"Role found: {role}")
            await message.author.add_roles(role)
            await message.channel.send('Brawo, zostałeś nowym katolikiem')

        if message.content == 'segz':
            print("segz detected")
            role = discord.utils.get(message.author.guild.roles, name='Jan Paweł 2')
            print(f"Role found: {role}")
            await message.author.remove_roles(role)
            await message.channel.send('Straciłeś zaufanie kościoła')


    # private message from bot - modmail
        empty_array = []
        modmail_channel = discord.utils.get(self.client.get_all_channels(), name='mod-mail')

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

    # prevent spam
        if str(message.channel) == 'memy' and message.content != '':
            await message.channel.purge(limit=1)
        if str(message.channel) == 'mod-mail' and message.content != '':
            await message.channel.purge(limit=1)

    # random thing
        if message.content.startswith('kiedy nostale'):
            if str(message.author) == 'shuS#2539':
                await message.channel.send('Czerwony przyjaciel, twierdzi, że ' + str(message.author)+'nigdy nie zagra')
            else:
                await message.channel.send('Czerwony przyjaciel twierdzi, że nie warto :)')
                await message.channel.send(file=discord.File('uwuPoring.png'))
        if message.content == 'gupi poring':
            await message.channel.send('Sam jesteś głupi, ' + str(message.author))

        await self.client.process_commands(message)

    # verification - auto_ranks
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 1002549710579568650:
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)

            if payload.emoji.name == '🐣':
                role = discord.utils.get(guild.roles, name='Lunatic(｡◕‿◕｡)')
                await member.add_roles(role)
            if payload.emoji.name == '🐒':
                role = discord.utils.get(guild.roles, name='Lig of Licz')
                await member.add_roles(role)
            if payload.emoji.name == '🐶':
                role = discord.utils.get(guild.roles, name='Cisgoł')
                await member.add_roles(role)
            if payload.emoji.name == '🐝':
                role = discord.utils.get(guild.roles, name='Tifi Tifi')
                await member.add_roles(role)

    # remove ranks
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 1002549710579568650:
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)

            if payload.emoji.name == '🐣':
                role = discord.utils.get(guild.roles, name='Lunatic(｡◕‿◕｡)')
                await member.remove_roles(role)
            if payload.emoji.name == '🐒':
                role = discord.utils.get(guild.roles, name='Lig of Licz')
                await member.remove_roles(role)
            if payload.emoji.name == '🐶':
                role = discord.utils.get(guild.roles, name='Cisgoł')
                await member.remove_roles(role)
            if payload.emoji.name == '🐝':
                role = discord.utils.get(guild.roles, name='Tifi Tifi')
                await member.remove_roles(role)

async def setup(client):
    await client.add_cog(MessageEvents(client))
