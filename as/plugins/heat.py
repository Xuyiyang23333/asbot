from nonebot import on_command, CommandSession
from config import heatMsgList, hateMsgList
import random, nonebot, time

heatCount = {}

def ans(grpID, name, is_group = True):
    #print(heatCount)
    day = time.localtime().tm_mday
    if is_group == False:
        ans = random.choice(heatMsgList).replace('NAME', name)
        return ans
    try:
        if heatCount[grpID][0] == day:
            if heatCount[grpID][1] <= 20:
                ans = random.choice(heatMsgList).replace('NAME', name)
            else:
                ans = random.choice(hateMsgList).replace('NAME', name)
        else:
            heatCount[grpID][0] = day
            heatCount[grpID][1] = 0
    except:
        heatCount[grpID] = [day, 0]
        ans = random.choice(heatMsgList).replace('NAME', name)
    heatCount[grpID][1] += 1
    return ans

@on_command('heat', only_to_me=False)
async def heat(session: CommandSession):
    name = session.current_arg
    message_id = session.event['message_id']
    try:
        group_id = session.event['group_id']
        is_group = True
    except:
        group_id = 0
        is_group = False
    if not 1 <= len(name) <= 10:
        name = session.event.sender['nickname']
    await session.send('[CQ:reply,id=' + str(message_id) + ']' + ans(group_id, name, is_group))

@on_command('heihei', only_to_me=False)
async def heihei(session: CommandSession):
    name = session.current_arg
    message_id = session.event['message_id']
    if not 1 <= len(name) <= 10:
        name = session.event.sender['nickname']
    await session.send('[CQ:reply,id=' + str(message_id) + ']嘿嘿, NAME🤤🤤🤤…嘿嘿嘿, 我的NAME🤤🤤🤤…'.replace('NAME', name))
'''
@on_command('骂我', only_to_me=False)
async def scold_me(session: CommandSession):
    name = session.current_arg
    message_id = session.event['message_id']
    if not 1 <= len(name) <= 10:
        name = session.event.sender['nickname']
    await session.send('[CQ:reply,id=' + str(message_id) + ']')
'''