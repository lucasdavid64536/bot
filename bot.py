#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import discord
import random
from discord.ext import commands
import logging
import traceback
import asyncio
import os
from discord import opus
from asyncio import sleep



logging.basicConfig(level='INFO')
bot = commands.Bot(command_prefix='g_')
bot.load_extension("admin")
bot.remove_command('help')
bot.load_extension("music")
OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        return True
    for opus_lib in opus_libs:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass
    raise RuntimeError('Could not load an opus lib. Tried %s' % (', '.join(opus_libs)))
load_opus_lib()


@bot.listen()
async def on_error(message, event, *args, **kwargs):
    await ctx.send(':o: | You __don`t__ have acces to this command!')
    
@bot.listen()
async def on_ready():
          print('Logging in as', bot.user.name)
          
@commands.cooldown(1, 5, commands.BucketType.user)  
@bot.command()
async def help(ctx):
    """Help"""
    em = discord.Embed(title="".format(ctx.guild.name), description="", color=discord.Colour.blue())
    em.set_author(name="Gaming High Help")
    em.add_field(name="Moderation", value='`mass(owner)`', inline=False)
    em.add_field(name="Music", value='`play,stop,queue,skip,pause,resume,join`', inline=False)
    em.set_thumbnail(url=ctx.me.avatar_url)
    msg = await ctx.send(embed=em)
    
@bot.listen()
async def on_message(message : discord.Message):
    if bot.user.mentioned_in(message):
        await message.channel.send(':sleeping: | You woke me up :( . My prefix is `d_` , for a list of commands type `d_help`', delete_after=10)
        
@bot.command()
@commands.has_permissions(administrator=True)
async def mass(ctx, *, message):
    async def maybe_send(member):
        try:
            await member.send(message)
        finally:
            await ctx.message.delete()

    await asyncio.gather(*[maybe_send(m) for m in ctx.guild.members])
    
@bot.listen()
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        return await ctx.send(f':no_entry: | Hey, You are being ratelimited! Try again in** {int(error.retry_after)} **seconds!', delete_after=5)
    if isinstance(error, commands.CommandNotFound):
        return await ctx.message.add_reaction('\N{BLACK QUESTION MARK ORNAMENT}')
    error = error.__cause__ or error
    tb = traceback.format_exception(type(error), error, error.__traceback__, limit=2, chain=False)
    tb = ''.join(tb)
    fmt = 'Error in command {}\n\n{}:\n\n{}\n'.format(ctx.command, type(error).__name__, tb)
    print(fmt)
    
async def presence():
    await bot.wait_until_ready()
    while not bot.is_closed():
        a = 0
        for i in bot.guilds:
            for u in i.members:
                if u.bot == False:
                    a = a + 1

       
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playning, name='Minecraft'))
        

bot.loop.create_task(presence())
bot.run(os.getenv("TOKEN"))
