# description:
a bot for creating a database of questions and answers about NovelAI  (the gpt powered storyteller pog)

# basic testing environment:
https://github.com/AtillaYasar/random-collection-of-things/tree/main/discord_testing

# seperation: backend and frontend
- backend: discord-independent code
- frontend: discord-specific code

The discord-specific code is further split into main.py, and extensions, which are loaded in `main.py` from their respective files, using `await bot.load_extension(arg)`, and this in each extension file:
my_extension.py
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

## **backend**

### backend_server.py
    uptimerobot setup (thank you Fizal Sarif)
### backend_storage.py
    saving and loading data between sessions, so that things don't get lost when the bot reboots.
### backend_openai.py
    (offline for now)
    (uses backend_storage.py) handles openai api
### backend_qa.py
    (uses backend_storage.py)
    handles Q&A data (adding, searching, removing)

## **frontend**

### main.py
    feels weird to call this frontend, but not sure where to put it anyway.
### frontend_qa.py
    commands:
        - addqa
        - searchqa
        - deleteq
### frontend_openai.py
    commands:
        - talk
        - make_bot
        - system

# screenshots of commands
(slightly outdated but mostly it's like this)
- searchqa
  + ![image](https://user-images.githubusercontent.com/112716905/216347702-dc447667-5937-4b37-b62e-9af5c0e57e21.png)
- addqa
  + ![image](https://user-images.githubusercontent.com/112716905/216808915-dfa1643e-ff9b-4e18-8631-a70dea68879f.png)
- deleteqa
  + ![ligma](https://user-images.githubusercontent.com/112716905/219903094-1d0cc1cc-b8a1-454d-85f1-fae884791716.png)

