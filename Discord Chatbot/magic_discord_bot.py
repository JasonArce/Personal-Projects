import os
import urllib
from urllib.request import urlopen
import discord
from discord.utils import get
import json
import asyncio
import discord.member
import random
from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog
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

    channel = bot.get_channel(828018840923013171)
#TODO: Make Channel private -> execute following -> make channel public
    guild = discord.utils.get(bot.guilds, name='Tbell Grind')
    await channel.set_permissions(guild.default_role, read_messages=False)
#end TODO
    await channel.purge(limit=10)
    await asyncio.sleep(1);
    await channel.send("Welcome to the Discord! Please react below to set your access to which channels you'd like to view:")
 ##   text= "🧙 - magic \n 🧊 - magic - cube \n 💯 - magic - edh \n ⚙️ - gears \n 🎮 - non-magic games"
    text= "🧙 - magic \n 🧊 - magic - cube \n 💯 - magic - edh \n 🎮 - non-magic games"
    msg = await channel.send(text)
    await msg.add_reaction(emoji='🧙')
    await msg.add_reaction(emoji='🧊')
    await msg.add_reaction(emoji='💯')
    ##await msg.add_reaction(emoji='⚙️')
    await msg.add_reaction(emoji='🎮')

    await channel.set_permissions(guild.default_role, read_messages=True)

@bot.event
async def on_reaction_add(reaction, user):
    guild = discord.utils.get(bot.guilds, name='Tbell Grind')
    member = guild.get_member(user.id)
    channel = bot.get_channel(828018840923013171)
    if (reaction.message.channel.id != channel.id):
        print("Error")
        return
    if (reaction.emoji == "🧙" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "Magic Man", id=828015941098143755)
        await member.add_roles(role)
    elif(reaction.emoji == "🧊" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "Cuber", id=828016184947376150)
        await member.add_roles(role)
    elif(reaction.emoji == "💯" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "EDH-er", id=828016257675558942)
        await member.add_roles(role)
##    elif(reaction.emoji == "⚙️" and user.id != 818882362040778812):
##        role = discord.utils.get(guild.roles, name = "⚙️", id=825042778496827473)
##        await member.add_roles(role)
    elif(reaction.emoji == "🎮" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "Gheymer", id=828016540590800927)
        await member.add_roles(role)


@bot.event
async def on_reaction_remove(reaction, user):
    guild = discord.utils.get(bot.guilds, name='Tbell Grind')
    member = guild.get_member(user.id)
    channel = bot.get_channel(828018840923013171)
    if (reaction.message.channel.id != channel.id):
        print("Error")
        return
    if (reaction.emoji == "🧙" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "Magic Man", id=828015941098143755)
        await member.remove_roles(role)
    elif(reaction.emoji == "🧊" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "Cuber", id=828016184947376150)
        await member.remove_roles(role)
    elif(reaction.emoji == "💯" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "EDH-er", id=828016257675558942)
        await member.remove_roles(role)
##    elif(reaction.emoji == "⚙️" and user.id != 818882362040778812):
##        role = discord.utils.get(guild.roles, name = "⚙️", id=825042778496827473)
##        await member.remove_roles(role)
    elif(reaction.emoji == "🎮" and user.id != 818882362040778812):
        role = discord.utils.get(guild.roles, name = "Gheymer", id=828016540590800927)
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
    count = 0
    split_card = []
    ## Pull card
    data = Card.where(name=input).all()
    ## Iterate through returned card for exact matches
    for x in data:
        ## Look for exact match and find the split card on gatherer
        if(x.name == input and x.multiverse_id is not None):
            split_card  = x.name.split(" // ")
            card_type = x.type
            ## Front half of the card
            if(count == 0):
                await ctx.send(x.image_url)
                try:
                    await ctx.send(split_card[0] + " " + x.mana_cost)
                except TypeError:
                    await ctx.send(x.name)
                    await ctx.send(card_type)
            else: ## Back half of the card
                await ctx.send("\n ------------------------------------------------ \n")
                await ctx.send(x.image_url)
                try:
                    await ctx.send(split_card[1] + " " + x.mana_cost)
                except TypeError:
                    await ctx.send(x.name)
            await ctx.send(x.text)
            ## Creature Type
            if('Creature' in card_type):
                await ctx.send(x.power + "/" + x.toughness)
            ## Planeswalker
            if('Planeswalker' in card_type):
                await ctx.send("Loyalty: " + x.loyalty)
            ## End iteration
            if(count == 1 or " // " not in x.name):
                return
            ## If there is a back half
            count += 1

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
    #open_price = json_obj['chart']['result'][0]['indicators']['quote'][0]['open'][0]
    difference_price = float(int(((current_price) - (previous_close_price)) * 10000)) / 10000
    difference_percentage = (float(int(((difference_price) / float(previous_close_price)) * 10000)) / 10000) * 100

    await ctx.send("Current ticker price for " + str(ticker) + ": " + str(current_price))

    if(difference_price < 0):
        await ctx.send(str(difference_price) + " ( " + str(difference_percentage) + "%) :chart_with_downwards_trend:")

    else:
        await ctx.send("+" +  str(difference_price) + " (+ " + str(difference_percentage) + "%) :chart_with_upwards_trend:")


@bot.command()
async def commands(ctx):
    await ctx.send("```Here are a list of commands: \n \n !remind_me (str message) (int duration) (str time_unit) \n Sets a reminder message. Choose seconds, minutes, hours, or days \n \n !vote (str subject) (str choice) \n Initiate a vote \n \n !poll \n Poll the responses of the vote \n \n !clear_poll \n Clears the current poll and allows a new vote to go underway \n \n !schedule_message (str message) (int duration) (str time_unit) \n Schedules a message. Choose seconds, minutes, hours, or days \n !card (str card) \n Returns card associated with name \n !seating (int n) \n Randomizes seating for 6 or 8 people```")

bot.run('ODE4ODgyMzYyMDQwNzc4ODEy.YEehoQ.mrtZcUXUq6Ji8o2jXRNTeWr7S8s')
