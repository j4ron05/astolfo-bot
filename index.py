import discord
import random
import time
import requests
import json
import os
from dotenv import load_dotenv
import git


bot = discord.Bot()
load_dotenv()

randomText = open("topix.txt", "r", encoding="utf-8").read().split("\n")

randomTextIndex = random.randint(0, len(randomText) - 1)

@bot.command(description="Sends the bot's latency.") 
async def ping(ctx): 
    await ctx.respond(f"Pong! Latency is {bot.latency}")
    print(f"Command 'ping' used by {ctx.author.name}")

@bot.command(description="gives a topic to talk about")
async def topic(ctx):
    randomTextIndex = random.randint(0, len(randomText) - 1)
    await ctx.respond(f"Here is a topic: {randomText[randomTextIndex]}")
    print(f"Command 'topic' used by {ctx.author.name}")

@bot.command(description="ban a user")
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        if ctx.author.guild_permissions.ban_members:
            await member.ban(reason=reason)
            await ctx.respond(f"{member} has been banned")
            print(f"Command 'ban' used by {ctx.author.name}")
        else:
            await ctx.respond("You do not have permission to ban members.")
    except Exception as e:
        await ctx.respond(f"An error occurred while banning the user: {e}")

@bot.command(description="kick a user")
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        if ctx.author.guild_permissions.kick_members:
            await member.kick(reason=reason)
            await ctx.respond(f"{member} has been kicked")
            print(f"Command 'kick' used by {ctx.author.name}")
        else:
            await ctx.respond("You do not have permission to kick members.")
    except Exception as e:
        await ctx.respond(f"An error occurred while kicking the user: {e}")


    
@bot.command(description="unban a user")
async def unban(ctx, *, member):
    try:
        if ctx.author.guild_permissions.ban_members:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split("#")

            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.respond(f"{user.mention} has been unbanned")
                    print(f"Command 'unban' used by {ctx.author.name}")
                    return

            await ctx.respond(f"User {member} is not banned.")
        else:
            await ctx.respond("You do not have permission to unban members.")
    except Exception as e:
        await ctx.respond(f"An error occurred while unbanning the user: {e}")

@bot.command(description="clears messages")
async def clear(ctx, amount: int = 5):
    try:
        if ctx.author.guild_permissions.manage_messages:
            await ctx.channel.purge(limit=amount)
            print(f"Command 'clear' used by {ctx.author.name}")
        else:
            await ctx.respond("You do not have permission to clear messages.")
    except Exception as e:
        await ctx.respond(f"An error occurred while clearing messages: {e}")

@bot.command(description="sends a random image from the folder 'pictures'")
async def image(ctx):
    try:
        images = os.listdir("pictures")
        randomImage = random.choice(images)
        await ctx.respond(file=discord.File(f"pictures/{randomImage}"))
        print(f"Command 'image' used by {ctx.author.name}")
    except Exception as e:
        await ctx.respond(f"An error occurred while sending the image: {e}")

@bot.command(description="Sends a joke.")
async def joke(ctx):
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        data = json.loads(response.text)
        await ctx.respond(data["setup"])
        time.sleep(3)
        await ctx.respond(data["punchline"])
        print(f"Command 'joke' used by {ctx.author.name}")
    except Exception as e:
        await ctx.respond(f"An error occurred while sending the joke: {e}")


@bot.command(description="pulls the latest edits from GitHub for the entire folder")
async def pull(ctx):
    try:
        g = git.cmd.Git("/C:/Users/jarom/code/astolfo/disc-bot")
        g.pull()
        await ctx.respond("Successfully pulled the latest edits from GitHub.")
        print(f"Command 'pull' used by {ctx.author.name}")
    except Exception as e:
        await ctx.respond(f"An error occurred while pulling the latest edits: {e}")


@bot.event
async def on_command_error(ctx, error):
    await ctx.respond(f"An error occurred: {error}")

@bot.event
async def on_guild_join(guild):
    print(f"Bot added to server: {guild.name} (ID: {guild.id})")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

bot.run(os.getenv('DISCORD_TOKEN'))