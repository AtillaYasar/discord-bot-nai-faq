## what is this?
# a very basic discord bot code. uses replit to host it, and UptimeRobot to wake up replit whenever it falls asleep.
# Thank you mister Fizal Sarif for teaching me how to do this. https://dev.to/fizal619/so-you-want-to-make-a-discord-bot-4f0n

## there are 3 special functions that can be operated via Discord:
    # -get_commands
    # -add_command
    # -delete_command

import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

commands = {}
def get_commands(a, b):
    return ', '.join(commands.keys())

def add_command(author,message):
    explanation = 'after add, write the command, starting with a -, and then the response that you want the bot to make, for example:-add -kek huehueuhueh lol teehee im a drunk bot.'
    
    words = message.split(' ')
    if len(words) < 3:
        return f'failed\nbecase you need at least 3 words in total: -add, -command, response\nexplanation:{explanation}'
    elif words[1] in ['-add', '-commands', '-delete', '-info']:
        return f'failed\nbecause you cannot change -add or -commands or -delete or -info\nexplanation:{explanation}'
    elif words[1][0] != '-':
        return f'failed\nbecause second word did not start with a -\nexplanation:{explanation}'
    else:
        command, response = words[1], ' '.join(words[2:])
        commands[command] = response
        return f'success\n"{command}" will now cause the response: {response}'

def delete_command(a, message):
    existing = get_commands(0,0).split(', ')
    explanation = 'after -delete, write the command you want to delete, for example:-delete -kek'
    words = message.split(' ')
    if len(words) != 2:
        return f'failed\nbecase you need at exactly 2 words in total: -delete, -command\nexplanation: {explanation}'
    elif words[1] in ['-add', '-commands', '-delete', '-info']:
        return f'failed\nbecause you cannot delete -add or -commands or -delete or -info\nexplanation: {explanation}'
    elif words[1] not in existing:
        return f'failed\nbecause {words[1]} is not an existing command\n existing commands:{existing}\nexplanation: {explanation}'
    else:
        to_delete = words[1]
        #return f'{existing}\n{to_delete}'
        del commands[to_delete]
        return f'success\nremoved {to_delete} from commands'

info = '''
- commands: will show the available commands
- add: lets you add a command. example: "-add -keepitreal for sure dawg" will make it respond to -keepitreal with for sure dawg. will overwrite the existing command
- delete: lets you delete a command. example: "-delete -keepitreal" to delete the -keepitreal command.
- info: that's me! pog.

- these 4 commands have more functionalities than just simple text responses. via Discord, i don't know how to let you program anything other than the text responses
- they will tell you what mistake you made
- you can't delete or overwrite these 4.

hosting:
this bot's code is in replit, because it can host the bot on a server. and i use UptimeRobot to tell repit not to fall asleep, every 30 minutes. i have not tested whether it wakes it up correctly, because i havent given replit enough time to fall asleep (1 hour)
'''[1:-1]
list_of_commands = [
    ('-info', info),
    ('-hello','hello'),
    ('-context','context is the amount of tokens the ai can remember'),
    ('-tokens','a token is a word or part of a word, depending on the word.'),
    ('-shitgibbon','congratulations for using the best insult ever'),
    ('-rtfm','Did you try reading the manual literally at the top of the page?'),
    ('-leader','@baka , AKA "Atilla", is the true singular supreme leader of this nefarious undertaking. All responsibility and culpably rests solely on his shoulders. The rest of us are mere pawns, grunts, and underlings to his glorious vision. All Hail Atilla the One!'),
    ('-commands',lambda author,message:get_commands(author,message)),
    ('-add',lambda author,message:add_command(author,message)),
    ('-delete',lambda author,message:delete_command(author,message))]

for tup in list_of_commands:
    commands[tup[0]] = tup[1]
    
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    author = message.author
    content = message.content
    
    if author == client.user:
        return
    
    if content.split(' ')[0] in commands:
        behavior = commands[content.split(' ')[0]]
        #print(behavior)
        if type(behavior) == str:
            response = f'{commands[content]}'
        else:
            response = behavior(author, content)
        await message.channel.send(f'{response}')
    else:
        pass
        #await message.channel.send(f'"{content}" is not a command. list of commands:\n{get_commands(0, 0)}')

bot_token = 'this is a secret token'

client.run(bot_token)












