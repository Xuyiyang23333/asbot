from nonebot import on_command, CommandSession
from config import new_line as nl
import requests

async def search_by_name(name, amount=1, offset=0):
    p = {'offset' : offset, 'amount' : amount, 'sort' : 'RECENT_DESC',\
        'query' : name, 'includeTags' : '', 'minDifficulty':'',\
        'maxDifficulty':'', 'minBpm':'', 'maxBpm':'', 'minTiles':'', 'maxTiles':''}
    r = requests.get('https://adofai.gg:9200/api/v1/levels', params=p)
    return r.json()['results']

async def search_by_id(songID):
    r = requests.get('https://adofai.gg:9200/api/v1/levels/' + str(songID))
    if len(r.text) == 0:
        return -1
    return r.json()

def fmt(s):
    ans = 'ID: ' + str(s['id']) + nl + \
    '标题: ' + s['title'] + nl + \
    '曲师: ' + '、'.join(s['artists']) + nl + \
    '谱师: ' + '、'.join(s['creators']) + nl + \
    '难度: ' + str(s['difficulty']) + nl + \
    'max BPM: ' + str(s['maxBpm']) + nl + \
    'Preview: https://adofai.gg/levels/' + str(s['id'])
    return ans

@on_command('adofai', only_to_me=False)
async def adofai(session: CommandSession):
    args = session.current_arg_text.split(' ')
    ext = 3 - len(args)
    if ext > 0:
        args = args + [-1] * ext 
    action = args[0]
    ans = '命令错误，请检查参数。'
    amount = 1
    num = 0
    if action == 'search':
        if args[2] == -1:
            num = 0
        elif args[2] == 'list':
            amount = 10
        else:
            num = int(args[2]) - 1
        s = await search_by_name(args[1].replace('_', ' '), amount, num)
        if len(s) == 0:
            ans = '无结果。'
        elif args[2] == 'list':
            ans = ''
            for i in range(len(s)):
                ans += str(i + 1) + '. 标题: ' + s[i]['title'] + \
                    ' 谱师: ' + '、'.join(s[i]['creators']) + nl
        else:
            s = s[0]
            ans = fmt(s)
    elif action == 'preview':
        songID = args[1]
        s = await search_by_id(songID)
        if s == -1:
            ans = '无结果。'
        else:
            ans = fmt(s)
    else:
        return
    await session.send(ans)
