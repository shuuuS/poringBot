
import youtube_dl
import pafy
import discord
from discord.ext import commands


class Player(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.song_queue = {}

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
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("Paused")


    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("Resume")

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send('Nie jestes polaczony z voice chanelem.')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)


    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()
        else:
            await ctx.send('Nie jestem na voice chanelu.')

    @commands.command()
    async def play2(self, ctx, url):
        ctx.voice_client.stop()
        FFMEPG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max5', 'options': '-vn'}
        YDL_OPTIONS = {'format': "bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMEPG_OPTIONS)
            vc.play(source)

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










