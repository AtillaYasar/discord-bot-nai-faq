from backend_storage import QaHandler
from discord.ext import commands

path = 'data/qa.json'
qa_handler = QaHandler(path)
qa_handler.storage.load()

def clean_edges(string):
    """Removes whitespaces at the edges."""
    
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

def addqa_parser(input):
    """Helper function for `async def addqa`."""
    
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

@commands.command()
async def searchqa(ctx, *, inp):
    """Search the Q&A database and return matching questions and answers, is case-insensitive.
    If the total response is longer than 2000 chars, responds in multiple parts."""

    res = qa_handler.search(inp)
    match_count = len(res)
    if match_count == 0:
        response = 'search successful.\nnothing found.'
    else:
        sections = []
        sections.append(f'search successful.\n{match_count} matches found.')

        for match in res:
            lines = []
            q = match['question']
            a = match['answer']
            for string in ('**question**', q, '**answer**', a):
                lines.append(string)
            lines.append('='*10)
            sections.append('\n'.join(lines))
        
        char_limit = 2000
        total_chars = len('\n'.join(sections))
        print(f'total_chars:{total_chars}')
        if total_chars > 2000-100:
            response = sections
        else:
            response = '\n'.join(sections)
    print(f'type response:{type(response)}')
    if type(response) is str:
        await ctx.send(response)
    elif type(response) is list:
        for item in response:
            await ctx.send(item)

@commands.command()
async def addqa(ctx, *, inp):
    """Add a question-answer pair to the database."""

    q, a = inp.split('&')
    response = qa_handler.add_qa(q, a)
    await ctx.send(response)

@commands.command()
async def deleteq(ctx, *, inp):
    """Delete questions from the Q&A database that are an exact match to the input.
    
    Example:
    (to add)
        -addqa ping?
    
        pong.
    
    (to delete)
        -deleteq ping?
    """

    removed_pairs = qa_handler.delete_q(inp)
    response = f'removed {len(removed_pairs)} pairs.'
    await ctx.send(response)

# load this module
async def setup(bot):
    """When await bot.load_extension('frontend_qa') is called, this function will add discord commands.
    
    bot is discord.ext.commands.Bot"""
    
    for f in (addqa, deleteq, searchqa):
        bot.add_command(f)