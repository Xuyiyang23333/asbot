from nonebot import on_command, CommandSession
import nonebot, re, requests, os
from io import BytesIO
from PIL import Image
from nonebot.argparse import ArgumentParser

bot = nonebot.get_bot()

async def save_pic(uri, name):
    global mkdirFlag
    #print(uri)
    r = requests.get(uri)
    fmt = Image.open(BytesIO(r.content)).format
    if mkdirFlag:
        os.mkdir('./pic/saved/' + name)
        mkdirFlag = False
    pic = open('./pic/saved/' + name + '/' + uri[-52:-9] + '.' + fmt, 'wb')
    pic.write(r.content)
    pic.close()
    #print('Saved!')

@on_command('mutectl', only_to_me=False, shell_like=True, permission=lambda sender: sender.is_superuser)
async def _(session: CommandSession):
    parser = ArgumentParser(session=session)
    parser.add_argument('-g', '--group')
    parser.add_argument('-i', '--id', required=True)
    parser.add_argument('-t', '--time', required=True)
    args = parser.parse_args(session.argv)
    group_id = args.group
    if group_id == None:
        group_id = session.event['group_id']
    await bot.set_group_ban(group_id=group_id, user_id=args.id, duration=args.time)

@on_command('getpics', shell_like=True, permission=lambda sender: sender.is_superuser)
async def _(session: CommandSession):
    global mkdirFlag
    parser = ArgumentParser(session=session)
    parser.add_argument('-i', '--id',)
    args = parser.parse_args(session.argv)
    if args.id == None:
        forwardId = (await session.aget(prompt='请将聊天记录转发给我！'))
        while 'CQ:forward' not in forwardId:
            forwardId = (await session.aget(prompt='请转发聊天记录！如希望退出请发送"q"。'))
            if forwardId == 'q':
                return
        forwardId = forwardId.strip(']').strip('[CQ:forward,id=')
    else:
        forwardId = args.id
    print('Forward ID:', forwardId)
    ans = ''
    msgs = await bot.get_forward_msg(id=forwardId)
    msgs = msgs['messages']
    #print(msgs)
    mkdirFlag = True
    name = forwardId[-10:]
    for msg in msgs:
        if 'CQ:image' in msg['content']:
            for uri in re.findall('url=\S*]', msg['content']):
                await save_pic(uri.strip('url=').strip(']'), name)
    await session.send('已保存！')
    #print(ans)