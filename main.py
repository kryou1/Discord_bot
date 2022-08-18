from urllib import response
import discord as dc
import discord.ext.commands as cmds
import matplotlib.pyplot as plt
from pycoingecko import CoinGeckoAPI
import json
import pandas as pd
from datetime import datetime
import requests

token = 'token'    # Change it
cmd_prefix = '!'            # Change it
bot = cmds.Bot(command_prefix=cmd_prefix, intents=dc.Intents.all(), help_command=None)
cg = CoinGeckoAPI()

response = requests.get("https://newsapi.org/v2/everything?q=crypto&apiKey=9b1c168489af417989b3f963ff294f6d")
data = json.loads(response.text)
all_articles = data['articles']

def get_crypto_chart(token, name):
        chart_data = cg.get_coin_market_chart_by_id(id=f'{token}', vs_currency='usd', days='7')

        def unix_to_date(unix_time):
            timestamp = datetime.fromtimestamp((unix_time/1000))
            return f"{timestamp.strftime('%d-%m-%Y %H:%M:%S')}"

        new_data = {}

        for each in chart_data['prices']:
            date = unix_to_date(each[0])
            new_data[date] = each[1]

        df = pd.DataFrame({'Dates': new_data.keys(), 'Prices': new_data.values()})
        print(df.head())

        df.plot(x ='Dates', y='Prices', kind = 'line', legend = None)	
        plt.axis('off')
        plt.title(f'7-day historical market price of {name}', fontsize=15, color= 'white', fontweight='bold');

        filename =  "C:/Users/kairong0213/Desktop/test.png"
        plt.savefig(filename, transparent=True)
        plt.close()

def getInfo(xp):
    if xp < 100:
        lvl = 0
        xpNeeded = 100
        xpNow = xp
    elif xp >= 100 and xp < 255:
        lvl = 1
        xpNeeded = 255
        xpNow = xp-100
    elif xp >= 255 and xp < 475:
        lvl = 2
        xpNeeded = 475
        xpNow = xp-255
    elif xp >= 475 and xp < 770:
        lvl = 3
        xpNeeded = 770
        xpNow = xp-475
    elif xp >= 770 and xp < 1150:
        lvl = 4
        xpNeeded = 1150
        xpNow = xp-770
    elif xp >= 1150 and xp < 1625:
        lvl = 5
        xpNeeded = 1625
        xpNow = xp-1150
    elif xp >= 1625 and xp < 2205:
        lvl = 6
        xpNeeded = 2205
        xpNow = xp-1625
    elif xp >= 2205:
        lvl = 7
        xpNow = 9999
        xpNeeded = 9999
    return lvl, xpNow, xpNeeded

class Coin:
    def __init__(self, name):
        self.name = name.lower()
        
        self.coin_data = cg.get_coins_markets(vs_currency='usd', ids=f'{self.name}')
        
        self.coin_name = self.coin_data[0]['name']
        self.coin_image = self.coin_data[0]["image"]
        self.coin_price = "${:,}".format(self.coin_data[0]['current_price'])

        self.coin_circulating_supply = "{:,}".format(self.coin_data[0]["circulating_supply"])
        self.coin_market_cap = "{:,}".format(self.coin_data[0]['market_cap'])

        self.coin_high_24h = "${:,}".format(self.coin_data[0]['high_24h'])
        self.coin_low_24h = "${:,}".format(self.coin_data[0]['low_24h'])

        self.coin_price_change_percent = "{:,}%".format(round(self.coin_data[0]['price_change_percentage_24h'], 2))
        
        self.coin_ath_price = "${:,}".format(self.coin_data[0]["ath"])
        self.coin_ath_change_percent = "{:,}%".format(self.coin_data[0]["ath_change_percentage"])
        self.coin_atl = "${:,}".format(self.coin_data[0]["atl"])

btc = Coin('bitcoin')
eth = Coin('ethereum')
xrp = Coin('ripple')
link = Coin('chainlink')
avax = Coin('avalanche-2')
doge = Coin('dogecoin')

trending_data = cg.get_search_trending()
trending_tokens = []
count_1 = 1
for each in trending_data["coins"]:
    item = each["item"]["name"]
    trending_tokens.append(f"({count_1}). {item} \n")
    count_1 += 1

trending_coins = ''.join(trending_tokens)

market_percent_data = cg.get_global()
upcoming_ico_data = None
ongoing_ico_data = None
ended_ico_data = None

upcoming_ico_data = market_percent_data["upcoming_icos"]
ongoing_ico_data = market_percent_data["ongoing_icos"]
ended_ico_data = market_percent_data["ended_icos"]


market_cap_percentage_data = cg.get_search_trending()
market_cap_percentage = []
count_2 = 1
for k, v in market_percent_data["market_cap_percentage"].items():
    market_cap_percentage.append(f"({count_2}). {k}: {round(v, 2)}% \n")
    count_2 += 1


#####################################################################################
####  discord bot  ##################################################################
#####################################################################################

@bot.event
async def on_ready():
    print('>> 機器人上線！ <<')
    c = bot.get_channel(1008978638181507132)
    await c.send('>> 逼啵逼啵 機器人啟動 <<')

# @bot.event
# async def on_reaction_add(reaction, user):
#     Channel = bot.get_channel(1006464738185707544)
#     if reaction.emoji == "✅":
#         if reaction.message.channel == Channel:
#             Role = dc.utils.get(user.guild.roles, name="平民")
#             await user.add_roles(Role)
#             print('user: ' + str(user.name) + ' gets role "平民"')

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    reaction = dc.utils.get(message.reactions, emoji=payload.emoji.name)

    if payload.user_id == bot.user.id:
        return
    if payload.message_id == 1009836808621793300:
        if str(payload.emoji.name) == '✅':
            role = dc.utils.get(guild.roles, name="平民")
            await member.add_roles(role)
            print('user: ' + str(member) + ' gets role "平民"')

@bot.command()
async def first(ctx: cmds.Context):
    c = bot.get_channel(1006464738185707544)
    embed = dc.Embed(description="請點擊:white_check_mark:來解鎖其他頻道！", color=dc.Colour.brand_red())
    await c.send(embed=embed)

@bot.command(description="Show this message")
async def help(ctx: cmds.Context):
    await ctx.send("""
```
Commands:
  help                Show this message
  greeting            Greetings!
  img                 Show img
  img_with_caption    Show img with a caption
  level               Check your level and exp
  price               Use "!price list" to show the list  &  Use "!price {coin}" to show the information of specific coin
```
""")

@bot.command(description="Greetings!")
async def greeting(ctx: cmds.Context):
    await ctx.send(format(ctx.author.mention) + ' 尼豪')    # change it

img_path = ['imgs\\wall-e.jpg', 'imgs\\eve.jpg']    # Change it
@bot.command(description="Show imgs")
async def img(ctx: cmds.Context, id: int):
    pic = dc.File(img_path[id])
    await ctx.send(file=pic)

captions = ['瓦ㄚㄚㄚㄚ力', '伊一一一一一芙']     # Change it
@bot.command(description="Show imgs with some caption")
async def img_with_caption(ctx: cmds.Context, id: int):   # Finish it
    pic = dc.File(img_path[id])   # 選擇圖片
    await ctx.send(file=pic)   # 印出圖片
    cap = captions[id]               # 選擇文字
    await ctx.send(cap)           # 印出文字
    pass

messageCount = {}
@bot.event
async def on_message(message):
    author = str(message.author)

    if message.content.startswith('!') and message.content != '!':
        tmp = message.content.split("!", 2)
        print('user: ' + author + ' called command "' + tmp[1] + '"')
    else:
        if author in messageCount:
            messageCount[author] += 1
            print(messageCount)

            if messageCount[author] == 2205:
                member = message.author
                role = dc.utils.get(member.guild.roles, name="WL")
                await member.add_roles(role)
                c = bot.get_channel(1008978638181507132)
                await c.send('Congrates! ' + format(member.mention) + ' just got role "WL".')
                print('user: ' + author + ' gets role "WL"')

        elif author != 'SocialFi_bot#5593':
            messageCount[author] = 1
            print(messageCount)

    await bot.process_commands(message)

@bot.command(description="Check your level and exp")
async def level(ctx: cmds.Context):
    member = ctx.author
    author = str(ctx.author)
    c = bot.get_channel(1008978638181507132)
    if ctx.channel == c:
        embed = dc.Embed(color=dc.Color.dark_green())
        embed.set_thumbnail(url=member.avatar)
        if author in messageCount:
            lvl, xpNow, xpNeeded = getInfo(messageCount[author])
        else:
            lvl, xpNow, xpNeeded = 0, 0, 100
        
        embed.add_field(name = "ID", value = member, inline = False)
        embed.add_field(name = "伺服器暱稱", value = member.nick if hasattr(member, "nick") else "None", inline = False)
        embed.add_field(name = "當前等級", value = str(lvl), inline = False)
        embed.add_field(name = "當前經驗值", value = str(xpNow)+'/'+str(xpNeeded), inline = False)
        await ctx.send(content = format(ctx.author.mention), embed = embed)

@bot.command(description="Use '!price list' to show the list")
async def price(ctx: cmds.Context):
    tmp = ctx.message.content.split(" ", 2)
    coinCalled = tmp[1]
    if coinCalled == "BTC":
        get_crypto_chart('bitcoin', coinCalled)
        
        embed=dc.Embed(color=dc.Color.blue())

        embed.set_author(name=f"{coinCalled}", icon_url=btc.coin_image)

        embed.add_field(name="當前價格", value=btc.coin_price, inline=True)
        embed.add_field(name="歷史最高", value=btc.coin_ath_price, inline=True)
        embed.add_field(name="市值", value= f"${btc.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High", value= btc.coin_high_24h, inline=True)
        embed.add_field(name="24h-low", value= btc.coin_low_24h, inline=True)
        embed.add_field(name="24h價格變化", value= btc.coin_price_change_percent, inline=True)

        file = dc.File("C:/Users/kairong0213/Desktop/test.png", filename="image.png")
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=file, embed=embed)

    elif coinCalled == "ETH":
        get_crypto_chart('ethereum', coinCalled)
        
        embed=dc.Embed(color=dc.Color.blue())

        embed.set_author(name=f"{coinCalled}", icon_url=eth.coin_image)

        embed.add_field(name="當前價格", value=eth.coin_price, inline=True)
        embed.add_field(name="歷史最高", value=eth.coin_ath_price, inline=True)
        embed.add_field(name="市值", value= f"${eth.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High", value=eth.coin_high_24h, inline=True)
        embed.add_field(name="24h-low", value=eth.coin_low_24h, inline=True)
        embed.add_field(name="24h價格變化", value=eth.coin_price_change_percent, inline=True)

        file = dc.File("C:/Users/kairong0213/Desktop/test.png", filename="image.png")
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=file, embed=embed)

    elif coinCalled == "XRP":
        get_crypto_chart('ripple', coinCalled)
        
        embed=dc.Embed(color=dc.Color.blue())

        embed.set_author(name=f"{coinCalled}", icon_url=xrp.coin_image)

        embed.add_field(name="當前價格", value=xrp.coin_price, inline=True)
        embed.add_field(name="歷史最高", value=xrp.coin_ath_price, inline=True)
        embed.add_field(name="市值", value= f"${xrp.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High", value=xrp.coin_high_24h, inline=True)
        embed.add_field(name="24h-low", value=xrp.coin_low_24h, inline=True)
        embed.add_field(name="24h價格變化", value=xrp.coin_price_change_percent, inline=True)

        file = dc.File("C:/Users/kairong0213/Desktop/test.png", filename="image.png")
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=file, embed=embed)

    elif coinCalled == "LINK":
        get_crypto_chart('chainlink', coinCalled)
        
        embed=dc.Embed(color=dc.Color.blue())

        embed.set_author(name=f"{coinCalled}", icon_url=link.coin_image)

        embed.add_field(name="當前價格", value=link.coin_price, inline=True)
        embed.add_field(name="歷史最高", value=link.coin_ath_price, inline=True)
        embed.add_field(name="市值", value= f"${link.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High", value=link.coin_high_24h, inline=True)
        embed.add_field(name="24h-low", value=link.coin_low_24h, inline=True)
        embed.add_field(name="24h價格變化", value=link.coin_price_change_percent, inline=True)

        file = dc.File("C:/Users/kairong0213/Desktop/test.png", filename="image.png")
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=file, embed=embed)

    elif coinCalled == "AVAX":
        get_crypto_chart('avalanche-2', coinCalled)
        
        embed=dc.Embed(color=dc.Color.blue())

        embed.set_author(name=f"{coinCalled}", icon_url=avax.coin_image)

        embed.add_field(name="當前價格", value=avax.coin_price, inline=True)
        embed.add_field(name="歷史最高", value=avax.coin_ath_price, inline=True)
        embed.add_field(name="市值", value= f"${avax.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High", value=avax.coin_high_24h, inline=True)
        embed.add_field(name="24h-low", value=avax.coin_low_24h, inline=True)
        embed.add_field(name="24h價格變化", value=avax.coin_price_change_percent, inline=True)

        file = dc.File("C:/Users/kairong0213/Desktop/test.png", filename="image.png")
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=file, embed=embed)

    elif coinCalled == "DOGE":
        get_crypto_chart('dogecoin', coinCalled)
        
        embed=dc.Embed(color=dc.Color.blue())

        embed.set_author(name=f"{coinCalled}", icon_url=doge.coin_image)

        embed.add_field(name="當前價格", value=doge.coin_price, inline=True)
        embed.add_field(name="歷史最高", value=doge.coin_ath_price, inline=True)
        embed.add_field(name="市值", value= f"${doge.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High", value=doge.coin_high_24h, inline=True)
        embed.add_field(name="24h-low", value=doge.coin_low_24h, inline=True)
        embed.add_field(name="24h價格變化", value=doge.coin_price_change_percent, inline=True)

        file = dc.File("C:/Users/kairong0213/Desktop/test.png", filename="image.png")
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=file, embed=embed)

    elif coinCalled == "list":
        await ctx.send("""
```
現在支援的幣種有：

   BTC
   ETH
   XRP
   LINK
   AVAX
   DOGE

```
""")

    else:
        await ctx.send(content = format(ctx.author.mention), embed = embed)

bot.run(token)
