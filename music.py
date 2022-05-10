import asyncio
import youtube_dl
import pafy
import discord
from discord.ext import commands


class Player(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.song_queue = {}

        self.setup()

    def setup(self):
        for guild in self.client.guilds:
            self.song_queue[guild.id] = []

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            ctx.voice_client.stop()
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.client.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({'format' : 'bestaudio', 'quiet' : True}).extract_info(f'ytsearch{amount}:{song}', download=False, ie_key='YoutubeSearch'))
        if len(info['entries']) == 0: return None

        return [entry['webpage_url'] for entry in info['entries']] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.client.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 50
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send('Nie jestes polaczony z voice chanelem.')

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send('Nie jestem na voice chanelu.')

    @commands.command()
    async def play(self, ctx, *, song=None):
        if song is None:
            return await ctx.send('Musisz podac piosenke.')

        if ctx.voice_client is None:
            return await ctx.send('Musisz być na voice chanelu.')

        #when song is not url
        if not ('youtube.com/watch?' in song or 'https://youtu.be/' in song):
            await ctx.send('Niuhanie, proszę czekać')

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send('Taki sheeeeeeet nie istnieje.')

            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(f'Mordo twoja perelka zostala dodana do mojej listy zabaw c: : {queue_len+1}.')

            else:
                return await ctx.send(f'Daj mi odpocząć :v')

        await self.play_song(ctx, song)
        await ctx.send(f"Teraz leci: {song}")

    @commands.command()
    async def search(self, ctx, *, song=None):
        if song is None: return await ctx.send('Zapomniales podac nute')

        await ctx.send('Szukam nuty, czekaj')

        info = await self.search_song(10, song)

        embed = discord.Embed(title=f'Wynik dla "{song}":', description='*Mozesz uzyc tego linka, aby puscic nute.*\n', colour=discord.Colour.red())

        amount = 0
        for entry in info["entries"]:
            embed.description += f'[{entry["title"]}]({entry["webpage_url"]})\n'
            amount += 1

        embed.set_footer(text=f'Pokazuje pierwszy {amount} piosenek')
        await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send('Nic obecnie nie jest grane')

        embed = discord.Embed(title='Song Queue', description='', colour=discord.Colour.dark_gold())
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f'{i}) {url}\n'

            i += 1

        embed.set_footer(text='Dzięki za wykorzystanie mnie :)')
        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send('O co ci chodzi, przeciez odpoczywam')

        if ctx.author.voice is None:
            return await ctx.send('Nie ma cie na voice chacie.')

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send('Nic obecnie dla ciebie nie gram')

        poll = discord.Embed(title=f'Glosowanie po skipa piosenki od - {ctx.author.name}#{ctx.author.descriminator}', description='**80% voice channelu musi sie zgodzic', colour=discord.Colour.blue())
        poll.add_field(name='Skip', value=':busiolek:')
        poll.add_field(name='Stay', value=':gr:')
        poll.set_footer(text="Glosowanie konczy sie za 15min")

        poll_msg = await ctx.send(embed=poll)
        poll_id = poll_msg.id

        await poll_msg.add_reaction(u'\u2705') #yes
        await poll_msg.add_reaction(u'\U0001F6AB') #no

        await asyncio.sleep(15) #15s to vote

        poll_msg = await ctx.channel.fetch_message(poll_id)

        votes = {u'\u2705': 0, u'\U0001F6AB': 0}
        reacted = []

        for reaction in poll_msg.reactions:
            if reaction.emoji in [u'\u2705', u'\U0001F6AB']:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                        votes[reacted.emoji] += 1

                        reaction.append(user.id)

        skip = False

        if votes[u'\u2705'] > 0:
            if votes[u'\U0001F6AB'] == 0 or votes[u'\u2705'] / (votes[u'\u2705'] + votes[u'\U0001F6AB']) > 0.79: #80 or higher
                skip = True
                embed = discord.Embed(title='Skip sie powiodl', description='***Glosowanie na skipa bylo udane, skipowankoooo.***', colour=discord.Colour.darker_grey())

            if not skip:
                embed = discord.Embed(title='Skip sie powiodl', description='***Glosowanie na skipa bylo udane, skipowankoooo.***', colour=discord.Colour.blurple())

            embed.set_footer(text='Glosowanie sie zakonczylo')

            await poll_msg.clear_reactions()
            await poll_msg.edit(embed=embed)












