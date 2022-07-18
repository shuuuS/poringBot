import discord
from discord.ext import commands


class MessageEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name='Polowanie na wrogów ojczyzny'))
        print('Aaaaaaaaa, siemanko!:3')

    #memberJoin
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.channels, name='w-s-t-ę-p')
        await channel.send(f'{member.mention} nas odwiedzil')

    #memberLeave
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.channels, name='w-s-t-ę-p')
        await channel.send(f'{member.mention} nas olal, htfu')

    #onMessage
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.content == 'jp2':
            role = discord.utils.get(message.author.guild.roles, name='Jan Paweł 2')
            await message.author.add_roles(role)
            await message.channel.send('Brawo, zostałeś nowym katolikiem')
        if message.content == 'segz':
            role = discord.utils.get(message.author.guild.roles, name='Jan Paweł 2')
            await message.author.remove_roles(role)
            await message.channel.send('Straciłeś zaufajnie kościoła')


    #modmail
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

    # important
        await self.client.process_commands(message)

    # weryfikacja
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 977905122011148318:
            if payload.emoji.name == '✅':
                guild = self.client.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)
                rola = discord.utils.get(guild.roles, name='Jan Paweł 2')
                await member.add_roles(rola)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 977905122011148318:
            if payload.emoji.name == '❌':
                guild = self.client.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)
                rola = discord.utils.get(guild.roles, name='Jan Paweł 2')
                await member.remove_roles(rola)


def setup(client):
    client.add_cog(MessageEvents(client))
