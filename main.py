"""
What is this?
--
A discord bot for creating an FAQ for NovelAI, (the gpt powered storyteller :p).

What is NovelAI?
--
Go to Novelai.net!
It can write stories, create speech, and make images. And the community is great.
Invite link to their discord: https://discord.com/invite/novelai

Credits
--
server stuff (in backend_server.py)
    Thank you mister Fizal Sarif for teaching me how to do the uptime robot stuff for getting a free permanent server for the bot. Article: https://dev.to/fizal619/so-you-want-to-make-a-discord-bot-4f0n

The code
--
nothing here. kinda pointless since im refactoring.
"""

# imports from this project
from secrets import bot_token
import backend_server
# frontend_openai and frontend_qa are imported in MyBot.setup_hook

from discord import app_commands
from discord.ext import commands
import discord

class MyBot(commands.Bot):
    def __init__(self, extension_files: list, description='(no description)') -> None:
        """loads discord commands from python files in extension_files argument.
        
        Example extension:
        `extension_files = ['my_extension.py']` <-- passed as an argument
        
        my_extension.py:
            ```python

                from discord.ext import commands
                
                @commands.command()
                async def do_a_thing(ctx, input):
                    '''Sends "Your message was sup" in the same channel when someone sends "-do_a_thing sup".
                    (assuming "-" is the command prefix)'''
                    
                    await ctx.send(f'Your message was: {input}')
                
                async def setup(bot):
                    '''When await bot.load_extension('my_extension') is called, this function will add discord commands.'''
                    
                    bot.add_command(do_a_thing)
            ```
            
        """
        
        self.extension_files = extension_files
        
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        
        super().__init__(command_prefix='-', description=description, intents=intents)

        #bot = commands.Bot(command_prefix='-', description=description, intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def setup_hook(self) -> None:
        for filename in self.extension_files:
            arg = filename.partition('.')[0]
            await bot.load_extension(arg)
            print(f'loaded extension:{arg}')

if __name__ == '__main__':
    backend_server.awake(r'https://replit.com/@AtillaYasar/NovelAI-faq#main.py', False)
    
    description = 'FAQ bot (plus fun stuff) for NovelAI. (in the process of refactoring)'
    extension_files = [
        'frontend_qa.py',
    ]
    bot = MyBot(extension_files=extension_files, description=description)

    bot.run(bot_token)

