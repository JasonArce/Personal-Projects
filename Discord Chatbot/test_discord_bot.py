import os
import urllib
from urllib.request import urlopen
import discord
from discord.utils import get
import json
import asyncio
import discord.member
import random
import nest_asyncio
#from mtgsdk import Card
#from mtgsdk import Set
#from mtgsdk import Type
#from mtgsdk import Supertype
#from mtgsdk import Subtype
#from mtgsdk import Changelog
import scrython
from requests import get
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
votes_dict = {'Subject': 'No Subject'}

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    channel = bot.get_channel(818948765762453564)

    #TODO: Make Channel private -> execute following -> make channel public
    guild = discord.utils.get(bot.guilds, name='Test')
    await channel.set_permissions(guild.default_role, read_messages=False)
    #end TODO

    await channel.purge(limit=10)
    await asyncio.sleep(1);
    await channel.send("Welcome to the Discord! Please react below to set your access to which channels you'd like to view:")
    text= "📈 - stonks \n 👾 - game shit \n 🕴 - job shit \n 🎼 - music shit \n 🏕 - cabin planning"
    msg = await channel.send(text)
    await msg.add_reaction(emoji='📈')
    await msg.add_reaction(emoji='👾')
    await msg.add_reaction(emoji='🕴')
    await msg.add_reaction(emoji='🎼')
    await msg.add_reaction(emoji='🏕')

    await channel.set_permissions(guild.default_role, read_messages=True)

@bot.event
async def on_reaction_add(reaction, user):
    guild = discord.utils.get(bot.guilds, name='Test')
    member = guild.get_member(user.id)
    channel = bot.get_channel(818948765762453564)
    if (reaction.message.channel.id != channel.id):
        print("Incorrect result")
        return
    if (reaction.emoji == "📈" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "📈", id=825039844731650048)
        await member.add_roles(role)
    elif(reaction.emoji == "👾" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "👾", id=825042574112325652)
        await member.add_roles(role)
    elif(reaction.emoji == "🕴" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "🕴", id=825042713581846588)
        await member.add_roles(role)
    elif(reaction.emoji == "🎼" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "🎼", id=825042778496827473)
        await member.add_roles(role)
    elif(reaction.emoji == "🏕" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "🏕", id=825042828525830184)
        await member.add_roles(role)


@bot.event
async def on_reaction_remove(reaction, user):
    guild = discord.utils.get(bot.guilds, name='Test')
    member = guild.get_member(user.id)
    channel = bot.get_channel(818948765762453564)
    if (reaction.message.channel.id != channel.id):
        print("Incorrect result")
        return
    if (reaction.emoji == "📈" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "📈", id=825039844731650048)
        await member.remove_roles(role)
    elif(reaction.emoji == "👾" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "👾", id=825042574112325652)
        await member.remove_roles(role)
    elif(reaction.emoji == "🕴" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "🕴", id=825042713581846588)
        await member.remove_roles(role)
    elif(reaction.emoji == "🎼" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "🎼", id=825042778496827473)
        await member.remove_roles(role)
    elif(reaction.emoji == "🏕" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "🏕", id=825042828525830184)
        await member.remove_roles(role)

@bot.command()
async def remind_me(ctx, arg1, arg2, arg3):
        duration = arg3.lower();
        ## Seconds
        if(str(arg3).startswith('sec') and int(arg2) <= 60):
            await asyncio.sleep(int(arg2));
        ## Minutes
        elif(str(arg3).startswith('min') and int(arg2) <= 60):
            await asyncio.sleep(int(arg2) * 60);
        ## Hours
        elif(str(arg3).startswith('hour') and int(arg2) <= 60):
            await asyncio.sleep(60 * 60 * int(arg2));
        ## Days
        elif(str(arg3).startswith('day')):
            await asyncio.sleep(60 * 60 * 24 * int(arg2))

        await ctx.send('Reminder for {}'.format(ctx.author.mention));
        await ctx.send(arg1);

@bot.command()
async def vote(ctx, arg1, arg2):
    new_value = "";
    if(len(votes_dict) == 0 or votes_dict['Subject'] == 'No Subject' or str(arg1) ==votes_dict['Subject']):
        votes_dict['Subject'] = arg1;
        for x in votes_dict.keys():
            print("This is x: " + str(x));
            print("This is arg2: " + arg2);
            if(x == str(arg2)):
                new_value = int(votes_dict.get(x)) + 1;
                print(new_value);
                votes_dict.update({str(arg2) : new_value});
        if(new_value == ""):
            votes_dict.update({str(arg2) : 1})

        for a, b in votes_dict.items():
            await ctx.send(a + " : " + str(b));
    else:
        await ctx.send("Please clear the poll before starting a new vote.")

@bot.command()
async def poll(ctx):
    print(ctx.channel.id)
    result = "";
    if(votes_dict['Subject'] == "No Subject"):
        await ctx.send("There is no active poll.")
    else:
        for x, y in votes_dict.items():
            await ctx.send(x + " : " + str(y));

@bot.command()
async def clear_poll(ctx):
    votes_dict['Subject'] = 'No Subject'
    temp_dict = votes_dict['Subject']
    votes_dict.clear()
    votes_dict['Subject'] = temp_dict
    await ctx.send("The poll has been cleared.")

@bot.command()
async def schedule_message(ctx, arg1, arg2, arg3):

    await ctx.message.delete();

    duration = arg3.lower();
    ## Seconds
    if(str(arg3).startswith('sec') and int(arg2) <= 60):
        await asyncio.sleep(int(arg2));
    ## Minutes
    elif(str(arg3).startswith('min') and int(arg2) <= 60):
        await asyncio.sleep(int(arg2) * 60);
    ## Hours
    elif(str(arg3).startswith('hour') and int(arg2) <= 60):
        await asyncio.sleep(60 * 60 * int(arg2));
    ## Days
    elif(str(arg3).startswith('day')):
        await asyncio.sleep(60 * 60 * 24 * int(arg2))

    await ctx.send(arg1);

@bot.command()
async def card(ctx, input):
    list = []
    nest_asyncio.apply()
    query = input
    auto = ""

    await asyncio.sleep(0.05)
    card = scrython.cards.Named(exact=query)
    url_dict = card.image_uris()

    try:
        await ctx.send(url_dict['normal'])
        await ctx.send(card)
        await ctx.send(card.oracle_text())
    except Exception:
        await asyncio.sleep(0.05)
        auto = scrython.cards.Autocomplete(q=query, query=query)
        if auto:
            await ctx.send("Did you mean?")
            for item in auto.data():
                list.append(item)
            await ctx.send(auto.data())
            ctx.send({ embed: {color: 3447003,description: "A very simple Embed!"}})

@bot.command()
async def kill(ctx):
    if(str(ctx.author) == "Oblivion7845#9136"):
        await ctx.bot.logout()

@bot.command()
async def seating(ctx, seats):
    ##seed = random.seed();
    if(int(seats) == 6):
        seatingChart = [1,2,3,4,5,6]
        random.shuffle(seatingChart)
        await ctx.send(seatingChart)
    else:
        seatingChart = [1,2,3,4,5,6,7,8]
        random.shuffle(seatingChart)
        await ctx.send(seatingChart)



@bot.command(pass_context=True)
async def ticker(ctx, ticker):
    url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + str(ticker) + '?includePrePost=false&interval=1d&useYfid=true&range=1d'
    response = urlopen(url)

    # Convert bytes to string type and string type to dict
    result = response.read().decode('utf-8')
    json_obj = json.loads(result)

    current_price = json_obj['chart']['result'][0]['meta']['regularMarketPrice']
    previous_close_price = json_obj['chart']['result'][0]['meta']['chartPreviousClose']
    difference_price = float(int(((current_price) - (previous_close_price)) * 10000)) / 10000
    difference_percentage = (float(int(((difference_price) / float(previous_close_price)) * 10000)) / 10000) * 100

    await ctx.send("Current ticker price for " + str(ticker) + ": " + str(current_price))

    if(difference_price < 0):
        await ctx.send(str(difference_price) + " ( " + str(difference_percentage) + "%) :chart_with_downwards_trend:")

    else:
        await ctx.send("+" +  str(difference_price) + " (+ " + str(difference_percentage) + "%) :chart_with_upwards_trend:")


@bot.command()
async def commands(ctx):
    await ctx.send("```Here are a list of commands: \n \n !remind_me (str message) (int duration) (str time_unit) \n Sets a reminder message. Choose seconds, minutes, hours, or days \n \n !vote (str subject) (str choice) \n Initiate a vote \n \n !poll \n Poll the responses of the vote \n \n !clear_poll \n Clears the current poll and allows a new vote to go underway \n \n !schedule_message (str message) (int duration) (str time_unit) \n Schedules a message. Choose seconds, minutes, hours, or days```")

bot.run('ODE4ODgyMzYyMDQwNzc4ODEy.YEehoQ.mrtZcUXUq6Ji8o2jXRNTeWr7S8s')
