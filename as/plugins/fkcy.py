from ..tools.generator import genImage
from nonebot import on_command, CommandSession

@on_command('fkcy', only_to_me=False)
async def fkcy(session: CommandSession):
    if len(session.current_arg_text) > 20:
        args = ['太长了', '打咩']
    else:
        args = session.current_arg_text.split(' ')
    if len(args) == 0:
        return
    elif len(args) == 1:
        word = args[0]
        word_a, word_b = word[:len(word) // 2], word[len(word) // 2:]
    else:
        word_a, word_b = args[0], args[1]
    genImage(word_a=word_a, word_b=word_b).save("/home/david/asbot/5kcy.jpg")
    await session.send('[CQ:image,file=file:///home/david/asbot/5kcy.jpg]')
