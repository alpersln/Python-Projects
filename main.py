import os

import discord
from discord.ext import commands, tasks
from utils import *
from functions import *

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True)
Bot = commands.Bot("!23 ", intents=intents)
game = Game()


class Social:
    INSTAGRAM = 'https://instagram.com/'
    TWITTER = 'https://twitter.com/'
    YOUTUBE = 'https://youtube.com/'


all_social_media = {
    'INSTAGRAM': 'kobe',
    'TWITTER': 'AlperSln5',
    'YOUTUBE': 'cansungur',

}


# python main.py

@Bot.event
async def on_ready():
    helpCommand.start()
    social_media_push.start()
    print("bot is ready!")


@Bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="hos-geldiniz")
    await channel.send(f"{member} aramıza katıldı hg!")
    print(f"{member} aramıza katıldı, Hoş geldin!")


ext_file_types = ['png', 'jpg', 'jpeg', 'gif']


@Bot.event
async def on_message(message):
    if len(message.attachments) > 0 and message.channel.name.startswith('memes'):
        for ext in ext_file_types:
            if message.attachments[0].filename.endswith(ext):
                await message.add_reaction("🤣")
                await message.add_reaction("💖")
                await message.add_reaction("🤮")
                await message.add_reaction("👍")
                break
    await Bot.process_commands(message)


@tasks.loop(hours=12)
async def helpCommand():
    for c in Bot.get_all_channels():
        if c.id == 980854914538422344:
            await c.send("Komutlar için !23 help")


@Bot.event
async def on_member_remove(member):
    print(f"{member} aramızdan ayrıldı :(")


@Bot.command(aliases=["game", "oyun", "roll", "zar at"])
async def selambot(ctx, *args):
    if "roll" in args:
        await ctx.send(game.roll_dice())
    else:
        await ctx.send('Merhaba, hoşgeldin!')


@Bot.command()
@commands.has_role("admin")
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)


@Bot.command()
@commands.has_role("admin")
async def kick(ctx, member: discord.Member, *args, reason="Yok"):
    await member.kick(reason=reason)


@Bot.command()
@commands.has_role("admin")
async def ban(ctx, member: discord.Member, *args, reason="Yok"):
    await member.ban(reason=reason)


@Bot.command()
@commands.has_role("admin")
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans
    member_name, member_discriminator = member.split("#")

    for bans in banned_users:
        user = bans.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned user {user.mention}')
            return


@Bot.command()
async def load(ctx, extension):
    Bot.load_extension(f'cogs.{extension}')


@Bot.command()
async def unload(ctx, extension):
    Bot.unload_extension(f'cogs.{extension}')


@Bot.command()
async def reload(ctx, extension):
    Bot.unload_extension(f'cogs.{extension}')
    Bot.load_extension(f'cogs.{extension}')


@Bot.command()
async def setSocial(ctx, s, absolute_path):
    """  :param s: MUST be TWITTER, Instagram or youtube   """
    all_social_media[s] = absolute_path


def getSocials() -> str:
    return f"""
    {Social.YOUTUBE}{all_social_media.get('YOUTUBE')}
    {Social.TWITTER}{all_social_media.get('TWITTER')}
    {Social.INSTAGRAM}{all_social_media.get('INSTAGRAM')}/
    """


@tasks.loop(minutes=5)
async def social_media_push():
    await Bot.get_channel(981183816611795055).send(getSocials())


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        Bot.load_extension(f'cogs.{filename[:-3]}')

Bot.run(TOKEN)
