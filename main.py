import discord
from discord.ext import commands
from view import viewSendCog

with open("token.txt" ,"r", encoding="utf-8") as file:
    token = file.readline()

#Bot Setup Variables
#-------------------------------------------------------------------------------------
bot_token = token


intents = discord.Intents.default()
intents.message_content = True
description = "Bot Development Test"
activity = discord.CustomActivity(name=".help")


bot = commands.Bot(command_prefix=commands.when_mentioned_or('.'), description=description, intents=intents, case_insensitive=True, activity=activity)
#-------------------------------------------------------------------------------------


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

    await bot.add_cog(viewSendCog(bot))

    print('----------\nReady!')
    


bot.run(bot_token)