from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import nonebot, re

bot = nonebot.get_bot()
fetchList = ['perfect', 'great', 'good', 'bad', 'miss',\
    '稍快', '稍慢', '完美', '提前', '太快', '太慢', '错过', '按太快',\
    'combo', 'accuracy', 'early', 'late',\
    'pure', 'far', 'lost', 'score', '残片', 'recall',
    'beatmap', 'played', 'ranking',
    'best', 'cool'] 

@on_command('dad')
async def dad(session: CommandSession):
    message_id = session.event['message_id']
    await session.send('[CQ:reply,id=' + str(message_id) + ']您！')

@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    pic_id = re.findall('file.*image', session.event.raw_message)
    if len(pic_id) == 0:
        return
    pic_id = pic_id[0].lstrip('file=')
    #print(pic_id)
    ocr = await bot.ocr_image(image = pic_id)
    #print(ocr)
    confidence = 0
    for t in ocr['texts']:
        for f in fetchList:
            if f in t['text'].lower():
                print('fetch!')
                confidence += 1
    if confidence >= 3:
        #print('神!')
        return IntentCommand(100.0, 'dad')