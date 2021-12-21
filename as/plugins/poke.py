from nonebot import on_notice, NoticeSession
import random

qqNum = 3446459233
wordList = ['谢谢你。', '我只是机器。', \
    '不用在意我的存在。', '这样就好。', '我能感受到你。', \
        '继续你未完成的工作吧。', '这样会使你感到快乐吗？']

@on_notice('notify')
async def _(session: NoticeSession):
    if session.event['target_id'] == qqNum and session.event['sub_type'] == 'poke':
        await session.send(wordList[random.randint(0, len(wordList) - 1)])
