# encoding: utf-8

import re

import discord

try:
    from config import TOKEN
except ImportError:
    print('Please create a config.py with a TOKEN variable first.')
    exit(1)


class Dad(discord.Client):
    def __init__(self):
        super().__init__(status=discord.Status.idle)
    
    async def on_ready(self):
        print(f'Logged in as: {self.user} (ID: {self.user.id})')
        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Game(name='as Dad'))
    
    async def on_message(self, message: discord.Message):
        if message.author.id != self.user.id:
            word = re.search(r'\bi\'?m\s+(.*)', message.content, re.IGNORECASE)
            
            if word is None:
                return

            if len(word.group(1)) > 32:
                word = re.search(r'\bi\'?m\s+(\w+)', message.content, re.IGNORECASE)
            word = word.group(1)
            
            if len(word) > 32:
                word = '<LONG DADJOKE>'
            await message.channel.send(f"Hi {word}, I'm Dad!")
            
            try:
                await message.author.edit(nick=word)
            except:
                pass

    async def on_guild_join(self, guild: discord.Guild):
        try:
            await guild.system_channel.send(f"Hi {guild}, I'm DadBot!")
            if not guild.me.guild_permissions.manage_nicknames:
                await guild.system_channel.send("Sorry kiddo, but I need to be able to give you a nick.\n"
                                                "Invite me back with the Manage Nicknames permission:\n"
                                                f"{discord.utils.oauth_url(self.user.id, permissions=201329664)}")
                await guild.leave()
        except:
            pass


if __name__ == '__main__':
    Dad().run(TOKEN)
