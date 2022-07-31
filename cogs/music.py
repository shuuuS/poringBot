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

            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.client.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f'ytsearch{amount}:{song}', download=False, ie_key='YoutubeSearch'))
        if len(info['entries']) == 0: return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.client.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

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
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("Paused")

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("Resume")



    @commands.command()
    async def play(self, ctx, *, song=None):
        if song is None:
            return await ctx.send('Musisz podac piosenke.')

        if ctx.voice_client is None:
            return await ctx.send('Może najpierw jakieś spotkanie? <wink><wink>.')

        #when song is not url
        if not ('youtube.com/watch?' in song or 'https://youtu.be/' in song):
            await ctx.send('<Sniff> <sniff>, proszę czekać')

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send('Taki sheeeeeeet nie istnieje.')

            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(f'Daj mi skończyć!~! Twoja piosenka zostala dodana:  {queue_len+1}.')

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

        if ctx.author.voice.channel.id == ctx.voice_client.channel.id:
            return await ctx.send('Skipowanie...')


def setup(client):
    client.add_cog(Player(client))












