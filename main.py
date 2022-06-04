import os

import discord
from discord.ext import commands, tasks
from utils import *
from functions import *
from model import *
from enviroments import *

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


@Bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)


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


@Bot.command()
async def work(ctx):
    discord_id = ctx.message.author.id
    now = datetime.now()
    user = get_user_or_false(discord_id)
    if user:
        if is_more_than_one_hour(user.work):
            user.money = user.money + 1000
            user.work = now.strftime(TIME_STAMP_PATTERN)
            user.update()
            await ctx.send(f" 1000$ hesabınıza eklendi, şu an toplam {user.money}$ bakiyeniz var!! ")
        else:
            await ctx.send(f"tekrar çalışabilmen için 1 saat beklemen gerekli")
    else:
        person = Person(discord_id, 1000, now.strftime(TIME_STAMP_PATTERN), 0).save()
        await ctx.send(f"Hoş geldiniz!!, {person.money}$ paranız var!!")
    db.commit()


@Bot.command()
async def money(ctx):
    user = get_user_or_false(ctx.message.author.id)
    if user:
        await ctx.send(f"bakiyeniz {user.money}$, Banka hesabı: {user.bank}$")
    else:
        await ctx.send(f"önce çalışmanız gerekli")


@Bot.command()
async def bank(ctx, transfer: int):
    user = get_user_or_false(ctx.message.author.id)
    if user:
        if transfer > user.money:
            await ctx.send(f"transfer miktarı bakiyenizden fazla olamaz")
            return
        user.bank, user.money = transfer, user.money - transfer
        user.update()
        db.commit()
        await ctx.send(f"bakiyeniz {user.money}$, Banka hesabı: {user.bank}$")
    else:
        await ctx.send(f"önce çalışmanız gerekli")


@Bot.command()
async def gamble(ctx, amount=0):
    import random
    user = get_user_or_false(ctx.message.author.id)
    if user:
        if amount > user.money:
            await ctx.send(f"yeterli bakiyeniz yoktur bakiyeniz:{user.money}")
        if random.randint(0, 2):
            user.money = user.money + amount
            await ctx.send(f"Kazandınız!! anlık bakiyenizz: {user.money}$")

        else:
            user.money = user.money - amount
            await ctx.send(f"Kaybettin :( anlık bakiyeniz: {user.money}$")

        user.update()
        db.commit()

    else:
        await ctx.send(f"önce çalışmanız gerekli")


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
