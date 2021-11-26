from nonebot import on_command, CommandSession
import random, sqlite3, nonebot
from config import GoodAnsList, badAnsList, blockedGroupID, allowMsgList, blockMsgList

bot = nonebot.get_bot()

def db_write(addCount, groupID, userID):
    con = sqlite3.connect('asbot.db')
    cur = con.cursor()
    if len(cur.execute('SELECT * FROM sqlite_master WHERE name="sbTop";').fetchall()) == 0:
        cur.execute('CREATE TABLE sbTop(id INTEGER PRIMARY KEY AUTOINCREMENT, qqNum INT, grpNum INT, count INT);')
    if len(cur.execute('select * from sbTop where grpNum=? and qqNum=?', (groupID, userID)).fetchall()) == 0:
        cur.execute('insert into sbTop (qqNum, grpNum, count) values (?, ?, ?)', (userID, groupID, addCount))
    else:
        oldCount = cur.execute('select count from sbTop where grpNum=? and qqNum=?', (groupID, userID)).fetchall()[0][0]
        cur.execute('update sbTop set count=? where grpNum=? and qqNum=?', (oldCount + addCount, groupID, userID))
    con.commit()
    con.close()

def db_read(groupID, limit):
    con = sqlite3.connect('asbot.db')
    cur = con.cursor()
    readout = cur.execute('select qqNum, count from sbTop where grpNum=? order by count desc limit ?', (groupID, limit)).fetchall()
    con.close()
    return readout

def un_cap(raw):
    out = ''
    for c in raw:
        if 'A' <= c <= 'Z':
            out += chr(ord(c) + 32)
        else:
            out += c
    return out

@on_command('sb', only_to_me=False, patterns='傻逼|[sS][bB]|啥[bB]')
async def sb(session: CommandSession):
    message_id = session.event['message_id']
    user_id = session.event['user_id']
    rawMessage = session.event['raw_message']
    writeFlag, sendFlag = True, True
    ansList = GoodAnsList
    for word in blockMsgList:
        if '菊宝' in rawMessage or word in rawMessage:
            ansList = badAnsList
    try:
        group_id = session.event['group_id']
        if group_id in blockedGroupID:
            sendFlag = False
    except:
        writeFlag = False
    for allowMsg in allowMsgList:
        if allowMsg in un_cap(rawMessage):
            writeFlag = False
            sendFlag = False
    if writeFlag == True:
        db_write(1, group_id, user_id)
    if sendFlag == True:
        await session.send('[CQ:reply,id=' + str(message_id) + ']' + ansList[random.randint(0, len(ansList) - 1)])

@on_command('sbtop', only_to_me=False)
async def sb_top(session: CommandSession):
    sendFlag = True
    try:
        group_id = session.event['group_id']
    except:
        sendFlag = False
    if sendFlag == True:
        readout = db_read(group_id, 10)
        ans = 'SB排行榜Top10：\u000d'
        for i in range(len(readout)):
            try:
                info = await bot.get_group_member_info(group_id=group_id, user_id=readout[i][0])
                name = info['nickname']
            except:
                name = 'Undefind'
            ans += str(i + 1) + '. ' + name + '说了' + str(readout[i][1]) + '次SB。\u000d'
        await session.send(ans)

@on_command('sbtopall', only_to_me=False)
async def sb_top(session: CommandSession):
    sendFlag = True
    try:
        group_id = session.event['group_id']
    except:
        sendFlag = False
    if sendFlag:
        await session.send('[CQ:share,url=https://sbtop.yxyy.top/' + str(group_id) + ',title=本群的SB排行榜]')

@bot.server_app.route("/sbtop/")
async def usage():
    return '<h1 align="center">请在URI后加上群号以查询SB列表！</h1>'

@bot.server_app.route("/sbtop/<name>")
async def sbtop(name):
    readout = db_read(int(name), -1)
    ans = '<h2 align="center">这是' + name + '中的SB排行榜。</h2>'
    ans += '<table border="1" align="center">'
    for info in readout:
        try:
            memberInfo = await bot.get_group_member_info(group_id=name, user_id=info[0])
            memberName = memberInfo['nickname']
        except:
            memberName = 'Undefind'
        ans += '<tr> <th>' + memberName + '</th> <th>' + str(info[1]) + '</th> </tr>'
    ans += '</table>'
    return ans
