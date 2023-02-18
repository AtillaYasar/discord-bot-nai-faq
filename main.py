import neverSleep
neverSleep.awake(r'https://replit.com/@AtillaYasar/NovelAI-faq#main.py', False)

import discord, json, ast
from discord.ext import commands
import random

def make_json(dic, filename):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(dic, f, indent=2)
        f.close()

def open_json(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        contents = json.load(f)
        f.close()
    return contents

def clean_edges(string):
    dirty = [" ","\t","\n"]
    while True:
        if len(string) == 0:
            return string
        if string[0] in dirty:
            string = string[1:]
        else:
            break
    while True:
        if len(string) == 0:
            return string
        if string[-1] in dirty:
            string = string[:-1]
        else:
            break
    return string

bot_token = 'hey this is secret yo'

description = '''a q&a bot for answering questions about NovelAI  (the gpt powered storyteller pog)'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='-', description=description, intents=intents)

# first normal functions, then stuff from the discord py library

# parsing an input from the addqa command
def addqa_parser(input):
    input = clean_edges(input)
    lines = input.split('\n')
    q = clean_edges(lines[0])
    a = clean_edges('\n'.join(lines[1:]))
    
    if q == '' or a == '':
        valid = False
        result = {
            'question':'invalid input',
            'answer':'invalid input'
            }
    else:
        valid = True
        result = {
            'question':q,
            'answer':a
        }
    return valid, result

# probably by writing to the for-bot-only channel. not written yet.
def backup_qa():
    print('backup_qa is not getting used lol. (because you seem to need an async function to send stuff)')

# add a question/answer pair
def _addqa(q,a):
    qa = open_json('qa.json')
    d = {'question':q, 'answer':a}
    if d in qa:
        print('update_qa log: skipping update because d in qa')
    else:
        qa.append(d)
        make_json(qa, 'qa.json')
    backup_qa()

# deletes a question/answer pair. requires exact match to question
def _deleteqa(q):
    qa = open_json('qa.json')
    pair = next( (item for item in qa if item['question'] == q), None)
    
    # delete question if exact match, then send a response
    if pair == None:
        response = f'**failure**\nexact match to question "{q}" was not found'
    else:
        qa = [item for item in qa if item['question'] != q]
        make_json(qa, 'qa.json')
        backup_qa()
        response = f'**success**\nquestion "{q}" was deleted'
    return response

# case insensitive search, looks through questions and answers
def apply_searchterm(term):
    term = term.lower()
    findings = []
    qa = open_json('qa.json')
    for d in qa:
        q = d['question'].lower()
        a = d['answer'].lower()
        if term in q or term in a:
            # hotfix of duplicate questions and answers
            if d in findings:
                continue
                
            findings.append(d)
    return findings

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

    # get the last message in the bot channel
    botchannel_id = 1034163297529901148
    botchannel = bot.get_channel(botchannel_id)
    message = await botchannel.fetch_message(botchannel.last_message_id)
    
    # get the json in that message and store its contents as qa.json
    atts = message.attachments
    if len(atts) > 1:
        print('ERROR: more than 1 attachment!')
    att = atts[0]
    as_bytes = await att.read()
    as_list = ast.literal_eval(as_bytes.decode('utf-8'))
    make_json(as_list, 'qa.json')
    print('stored previous qa.json')
    print('---')

# deletes a question/answer pair. requires exact match to question
@bot.command()
async def deleteqa(ctx, *, input):
    response = _deleteqa(input)
    await ctx.send(response)
    
    # do backup
    botchannel_id = 1034163297529901148
    botchannel = bot.get_channel(botchannel_id)
    await botchannel.send(
        file=discord.File("qa.json"),
        content='backing up qa.json'
    )
    print('backup was done inside\n\tasync def addqa(ctx, *, input)\nbecause i dont know how to do it outside of this function.')

@bot.command()
async def addqa(ctx, *, input):
    valid, result = addqa_parser(input)
    input_explanation = '''
you just need an empty line between the question and the answer. so:
```
-addqa is this a question?

yes.
```
or
```
-addqa
is this a question?

yes.
```
    '''[1:-1]
    reason = None
    
    if valid == True:
        q = result['question']
        a = result['answer']
        _addqa(q, a)
        
        response = 'question added successfully'
    else:
        response = f'failed to add question\nreason:{reason}\ninput explanation:{input_explanation}'
        
    await ctx.send(response)

    # do backup
    botchannel_id = 1034163297529901148
    botchannel = bot.get_channel(botchannel_id)
    await botchannel.send(
        file=discord.File("qa.json"),
        content='backing up qa.json'
    )
    print('backup was done inside\n\tasync def addqa(ctx, *, input)\nbecause i dont know how to do it outside of this function.')

@bot.command()
async def searchqa(ctx, *, input):
    reason = None
    input_explanation = None

    # check if input is correct
    if len(input.split('\n')) == 1:
        valid = True
    else:
        valid = False
        reason = 'input must be exactly 1 line'

    # formulate response
    if valid == True:
        # search qa and present findings
        findings = apply_searchterm(input)
        if findings == []:
            report = 'nothing found'
            response = f'search successful\n{report}'
        else:
            # doing the sections thing to deal with messages having to be shorter than 2000 chars
            sections = []

            # add beginning
            next_section = []
            next_section.append('search successful')
            next_section.append(f'number of results:{len(findings)}')
            next_section.append('-'*5 + ' start')

            # start new
            sections.append('\n'.join(next_section))
            next_section = []

            # add each qa as a seperate section
            qa = []
            for d in findings:
                lines = []
                for string in (
                    '**' + d['question'] + '**',
                    '```' + d['answer'] + '```'
                ):
                    lines.append(string)
                sections.append('\n'.join(lines))
            
            sections.append('-'*5 + ' end')
            full_response = '\n'.join(sections)
            if len(full_response) < 2000:
                response = full_response
            else:
                response = sections
    else:
        # say why search is incorrect
        response = f'search command is incorrect. reason:{reason}, input explanation:{input_explanation}'

    if type(response) is list:
        for message in response:
            await ctx.send(message)
    else:
        await ctx.send(response)

bot.run(bot_token)
