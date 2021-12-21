from nonebot import on_natural_language, NLPSession

msgDict = {}

@on_natural_language(only_to_me=False)
async def typecho(session: NLPSession):
    global msgDict
    try:
        group_id = session.event['group_id']
        message = session.event['message']
    except:
        return
    try:
        if msgDict[group_id][0] == message:
            msgDict[group_id][1] += 1
        else:
            msgDict[group_id][0] = message
            msgDict[group_id][1] = 1
        if msgDict[group_id][1] >= 3:
            await session.send(message)
            msgDict[group_id][1] = 0
    except:
        msgDict[group_id] = [message, 1]
