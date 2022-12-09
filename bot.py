import time, math, requests, discord
from discord import app_commands
from discord.ext import commands
from requests.structures import CaseInsensitiveDict
from reactionmenu import ViewMenu, ViewButton
import key

MY_GUILD = discord.Object(id=719546155649859654)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


headers = CaseInsensitiveDict()
headers["X-Tycoon-Key"] = (key.key)
url = "http://v1.api.tycoon.community/main/"

bot = commands.Bot(command_prefix="??", intents=discord.Intents.all())





@bot.event
async def on_ready():
    print("Hello World!")
    #channel = bot.get_channel(CHANNEL_ID)
    #await channel.send("Hello World!")
    #print(f'We have logged in as {bot.user}')



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
async def charges(ctx):
    endpoint = "charges.json"
    ans = requests.get(url=url+endpoint, headers=headers).json()
    await ctx.send(f"{ans[0]} charges left.")

@bot.command()
async def inv(ctx):
    endpoint = f"data/{id}"
    ans = requests.get(url=url+endpoint, headers=headers).json()
    print(ans)
    await ctx.send(ans)

@bot.command()
async def endpoints(ctx):
    endpoint = "endpoints.json"
    ans = requests.get(url=url+endpoint, headers=headers).json()
    await ctx.send(ans)


@bot.command()
async def streak(ctx):
    """Gives your current login streak, streak record and total logged in days"""
    dc_id = ctx.author.id
    id_ep = f"snowflake2user/{dc_id}"
    ans_id = requests.get(url=url+id_ep, headers=headers).json()
    userid = ans_id["user_id"]
    
    embed_time= math.trunc(time.time())
    endpoint = f"streak/{userid}"
    ans = requests.get(url=url+endpoint, headers=headers).json()
    streak_embed=discord.Embed(color=0x42c0ff)
    streak_embed.set_author(name="Your streak data")
    streak_embed.add_field(name="Your current' streak :", value=ans["data"]["streak"], inline=False)
    streak_embed.add_field(name="Your streak record :", value=ans["data"]["record"], inline=False)
    streak_embed.add_field(name="Total days logged in :", value=ans["data"]["days"], inline=False)
    streak_embed.add_field(name="\u200b", value=f"<t:{embed_time}:R>")
    await ctx.send(embed=streak_embed)


@bot.command()
async def sotd(ctx):
    
    
    embed_time= math.trunc(time.time())
    endpoint = f"/sotd.json"
    ans = requests.get(url=url+endpoint, headers=headers).json()
    sotd_embed=discord.Embed(color=0x42c0ff)
    sotd_embed.set_author(name="Current SoTD")
    sotd_embed.add_field(name="The current Skill Of The Day is :", value=ans["skill"], inline=False)
    sotd_embed.add_field(name="The bonus is :", value=ans["bonus"], inline=False)
    sotd_embed.add_field(name="message sent", value=f"<t:{embed_time}:R>")
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
    wallet = ans["wallet"]
    bank = ans["bank"]
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

'''
@bot.tree.command()
@app_commands.describe
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
'''

@bot.tree.command() 
@app_commands.describe(first_value='The first value you want to add something to',second_value='The value you want to add to the first value',)
async def add(interaction: discord.interactions, first_value: int, second_value: int ): 
    await interaction.response.send_message(f'{first_value:,} + {second_value:,} = {first_value + second_value:,}')


bot.run(key.BOT_TOKEN)