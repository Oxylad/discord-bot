import time, math, requests, discord, datetime, asyncio, youtube_dl, json, key
from discord import app_commands
from discord.ext import commands
from requests.structures import CaseInsensitiveDict
from reactionmenu import ViewMenu, ViewButton
from typing import Optional
datafile = open("data.json", "a+")


MY_GUILD = discord.Object(id=719546155649859654)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
bot = MyClient(intents=intents)

headers = CaseInsensitiveDict()
headers["X-Tycoon-Key"] = (key.key)
url = "http://v1.api.tycoon.community/main/"

bot = commands.Bot(command_prefix="??", intents=discord.Intents.all(), case_insesitive=True)

@bot.event
async def on_ready():
    print("Hello World!")

#change to slash command
@bot.command()
async def sendinchannel(ctx, channel: int, *, msg):
    await bot.get_channel(channel).send(msg)
    await ctx.send("Message sent!")


@bot.command(pass_context=True)
async def kill(ctx):
    await ctx.send("KMS now")
    await exit()

@bot.command()
async def add(ctx, *arr):
    result = 0
    for i in arr:
        result += int(i)
    await ctx.send(result)

@bot.command()
async def bee_movie(ctx):
        debut = datetime.time()
        with open("bee_movie_script.txt", "r") as f:
            for line in f:
                await ctx.send(line)
                await asyncio.sleep(0.2)  # delay for 0.5 seconds
            fin = datetime.time()
            print_time = fin - debut
            await ctx.reply(f"This is the whole script for Bee Movie, as you requested. This took +{print_time} seconds",mention_author=True)

@bot.command()
async def testcmd(ctx):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    await ctx.send("Current Time =", current_time)
    
@bot.command()
async def send_msg(channel: discord.channel, message):
    await channel.send(message)

@bot.command()
async def helptt(ctx):
    help_embed = discord.Embed()
    help_embed.set_author(name="Help commands")
    help_embed.add_field(name="help", value="show all commands this bot supports (this menu)")
    help_embed.add_field(name="ping", value="pong")
    help_embed.add_field(name="charges", value="show available charges on the key")
    help_embed.add_field(name="streak", value="gives login streak")
    help_embed.add_field(name="sotd", value="skill of the day")
    help_embed.add_field(name="endpoints", value="available endpoints of the api")
    await ctx.send(embed=help_embed)
    

@bot.command()
async def debug(ctx, endpoint):
    ans = requests.get(url=url+endpoint, headers=headers).json()
    
    datafile.write(json.dumps(ans, sort_keys=True, indent=4))
    await ctx.send(ans)

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms ping')

@bot.command()
async def charges(ctx):
    endpoint = "charges.json"
    ans = requests.get(url=url+endpoint, headers=headers).json()
    
    embed_time = math.trunc(time.time())

    charge_embed = discord.Embed(color=0x42c0ff)
    charge_embed.set_author(name="Remaining charges on key")
    charge_embed.add_field(name="Charges remaining", value=f"{ans[0]}")
    charge_embed.add_field(name="\u200b", value=f"<t:{embed_time}:R>")
    await ctx.send(embed=charge_embed)

@bot.command()
async def skills(ctx):
    dc_id = ctx.author.id
    id_ep = f"snowflake2user/{dc_id}"
    ans_id = requests.get(url=url+id_ep, headers=headers).json()
    userid = ans_id["user_id"]

    embed_time = math.trunc(time.time())

    wealth_embed=discord.Embed(color=0x42c0ff)
    wealth_embed.set_author(name="Your Skills Data")
    wealth_embed.add_field(name="Wallet Balance :", value=f"{wallet:,}", inline=False)
    wealth_embed.add_field(name="Bank Balance :", value=f"{bank:,}", inline=False)
    wealth_embed.add_field(name="Total Balance :", value=f"{wallet+bank:,}", inline=False)
    wealth_embed.add_field(name="\u200b", value=f"<t:{embed_time}:R>")

    

@bot.command()
async def inv(ctx):
    dc_id = ctx.author.id
    id_ep = f"snowflake2user/{dc_id}"
    ans_id = requests.get(url=url+id_ep, headers=headers).json()
    userid = ans_id["user_id"]
    
    embed_time = math.trunc(time.time())
    ans = requests.get(url=url+f"data/{userid}", headers=headers).json()
    print(ans)
    await ctx.send(ans["data"])

@bot.command()
async def endpoints(ctx):
    endpoint = "endpoints.json"
    ans = requests.get(url=url+endpoint, headers=headers).json()
    await ctx.send(ans)


@bot.command()
async def streak(ctx):
    dc_id = ctx.author.id
    id_ep = f"snowflake2user/{dc_id}"
    ans_id = requests.get(url=url+id_ep, headers=headers).json()
    userid = ans_id["user_id"]
    
    embed_time = math.trunc(time.time())
    ans = requests.get(url=url+f"streak/{userid}", headers=headers).json()
    
    streak_embed = discord.Embed(color=0x42c0ff)
    streak_embed.add_field(name="**Your streak data**", value="**Current streak: **"+str(ans["data"]["streak"])+"\n **Record streak: **"+ str(ans["data"]["record"])+ "\n **Total days logged in: **"+str(ans["data"]["days"])+"\n\n"+f"<t:{embed_time}:R>", inline=False)
    await ctx.send(embed=streak_embed)

@bot.command()
async def sotd(ctx):
    embed_time= math.trunc(time.time())
    ans = requests.get(url=url+f"/sotd.json", headers=headers).json()
    sotd_embed=discord.Embed(color=0x42c0ff)
    sotd_embed.add_field(name="\n Current SoTD:", value="The skill of the day is "+str(ans["bonus"])+"%  "+ str(ans["skill"])+ "\n\n"+f"<t:{embed_time}:R>", inline=False)
    await ctx.send(embed=sotd_embed)

@bot.command()
async def wealth(ctx):
    
    dc_id = ctx.author.id
    id_ep = f"snowflake2user/{dc_id}"
    ans_id = requests.get(url=url+id_ep, headers=headers).json()
    userid = ans_id["user_id"]
    
    embed_time= math.trunc(time.time())
    endpoint = f"wealth/{userid}"
    ans = requests.get(url=url+endpoint, headers=headers).json()
    try:
        wallet = ans["wallet"]
        bank = ans["bank"]
    except KeyError:
        await ctx.send("player is offline")
    wealth_embed=discord.Embed(color=0x42c0ff)
    wealth_embed.set_author(name="Your Wealth Data")
    wealth_embed.add_field(name="Wallet Balance :", value=f"{wallet:,}", inline=False)
    wealth_embed.add_field(name="Bank Balance :", value=f"{bank:,}", inline=False)
    wealth_embed.add_field(name="Total Balance :", value=f"{wallet+bank:,}", inline=False)
    wealth_embed.add_field(name="\u200b", value=f"<t:{embed_time}:R>")
    await ctx.send(embed=wealth_embed)
 
@bot.command()
async def stats(ctx):
    menu = ViewMenu(ctx, menu_type=ViewMenu.TypeEmbed)
    dc_id = ctx.author.id
    id_ep = f"snowflake2user/{dc_id}"
    ans_id = requests.get(url=url+id_ep, headers=headers).json()
    userid = ans_id["user_id"]
    
    embed_time= math.trunc(time.time())
    endpoint = f"stats/{userid}"
    ans = requests.get(url=url+endpoint, headers=headers).json()
    
    stats_embed1=discord.Embed(color=0x42c0ff)
    stats_embed1.set_author(name="Your Game Stats")
    lenstats = len(ans["data"])

    n=0
    while n < 24:
        stats = ans["data"][n]["amount"]
        stats_embed1.add_field(name=ans["data"][n]["name"], value=f"{stats:,}", inline=True)
        n+=1
    stats_embed1.add_field(name="\u200b", value=f"<t:{embed_time}:R>")
    menu.add_page(stats_embed1)

    stats_embed2=discord.Embed(color=0x42c0ff)    
    stats_embed2.set_author(name="Your Game Stats")
    while n < lenstats:
        stats = ans["data"][n]["amount"]
        stats_embed2.add_field(name=ans["data"][n]["name"], value=f"{stats:,}", inline=True)
        n+=1
        
    stats_embed2.add_field(name="\u200b", value=f"<t:{embed_time}:R>")
    menu.add_page(stats_embed2)
    
    menu.add_button(ViewButton.back())
    menu.add_button(ViewButton.next())
    await menu.start()



@bot.command()
async def play(ctx):
    queue = asyncio.Queue()
    global voice_client
    voice_client = None
    channel = ctx.author.voice.channel
    if voice_client is None:
        voice_client = await channel.connect()
        await ctx.channel.send("Bot has been connected to your voice channel")
    elif voice_client.channel != channel:
        await voice_client.move_to(channel)

    async def play_next(voice):
        song_url = await queue.get()
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song_url))
        voice.play(source, after=lambda e: queue.task_done())

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(ctx.message.content.split()[1], download=True)
        url = info['url']
        song_name = info['title']

    await queue.put(url)
    if queue.empty():
        await play_next(voice_client)
        await ctx.channel.send('Now playing {}'.format(song_name))

@bot.command()
async def disconnect(ctx):
    await ctx.voice_client.disconnect()
    await ctx.channel.send("")

@bot.command()
async def pause(ctx):
    await ctx.voice_client.pause()
    await ctx.send("Paused")

@bot.command()
async def resume(ctx):
    await ctx.voice_client.resume()
    await ctx.send("Resumed")



### SLASH COMMANDS UNDER HERE ###

@bot.tree.command() 
@app_commands.describe(first_value='The first value you want to add something to',second_value='The value you want to add to the first value',)
async def add(interaction: discord.interactions, first_value: int, second_value: int ): 
    await interaction.response.send_message(f'{first_value:,} + {second_value:,} = {first_value + second_value:,}')

@bot.tree.command()
@app_commands.describe(channel='the channel', msg='the message')
async def sendinchannel(interaction: discord.interactions, channel: int, msg: str):
    await bot.get_channel(channel).send(msg)
    await interaction.response.send_message("Message sent!")


bot.run(key.BOT_TOKEN)