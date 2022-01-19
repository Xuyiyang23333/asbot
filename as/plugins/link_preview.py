from io import BytesIO
from PIL import Image
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from config import groupID, new_line
import nonebot, requests
import pyzbar.pyzbar as pyzbar
from bs4 import BeautifulSoup as bs

def short(txt, l=20):
    if len(txt) <= l:
        return txt
    return txt[:l] + '...'

def qr_scan(uri):
    r = requests.get(uri)
    img = Image.open(BytesIO(r.content))
    readout = pyzbar.decode(img)
    ans = ''
    for t in readout:
        ans += t.data.decode() + new_line
    return ans

def preview(uri):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}
    r = requests.head(uri, headers=headers)
    if 'text/html' not in r.headers['Content-Type']:
        return -1
    r = requests.get(uri, headers=headers)
    s = bs(r.text)
    if s.find('title') != None:
        title = s.find('title').text
    else:
        return -1
    if s.find(attrs={"name":"description"}) != None:
        description = s.find(attrs={"name":"description"})['content']
    else:
        description = '无'
    return {'title': title, \
        'description': description}

@on_command('qrscan')
async def qrscan_manual(session: CommandSession):
    message_id = session.event['message_id']
    ans = ''
    #print(session.current_arg)
    for uri in session.current_arg_images:
        ans += qr_scan(uri)
    ans = ans.strip(new_line)
    if ans != '':
        await session.send('[CQ:reply,id=' + str(message_id) + ']以下是二维码中的内容。' + \
        new_line + ans)

@on_command('preview')
async def preview_manual(session: CommandSession):
    message_id = session.event['message_id']
    uri = session.current_arg
    pv = preview(uri)
    if pv == -1:
        return
    await session.send('[CQ:reply,id=' + str(message_id) + ']标题: ' + short(pv['title']) +\
        new_line + '简介: ' + short(pv['description']))

@on_natural_language(only_to_me=False, only_short_message=False)
async def qrscan(session: NLPSession):
    if session.event['message_type'] == 'group' and \
            session.event['group_id'] in groupID:
        if len(session.msg_images) > 0:
            return IntentCommand(100.0, 'qrscan', current_arg=session.msg)
        if session.msg_text[:4] == 'http':
            return IntentCommand(100.0, 'preview', current_arg=session.msg_text)