from nonebot import on_command, CommandSession
import random, sqlite3, nonebot, time
from config import groupID, GoodAnsList, badAnsList, blockedGroupID, allowMsgList, blockMsgList

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

def db_read_count(groupID, qqNum):
    con = sqlite3.connect('asbot.db')
    cur = con.cursor()
    readout = cur.execute('select count from sbTop where grpNum=? and qqNum=?', (groupID, qqNum)).fetchall()
    con.close()
    return readout[0][0]

def un_cap(raw):
    out = ''
    for c in raw:
        if 'A' <= c <= 'Z':
            out += chr(ord(c) + 32)
        else:
            out += c
    return out

lastSb = {}
sbTime = {}

#----main----
'''
@nonebot.scheduler.scheduled_job('cron', hour='20')
async def auto_mute():
    my_id = await bot.get_login_info()
    for group in groupID:
        con = sqlite3.connect('asbot.db')
        cur = con.cursor()
        user_id = cur.execute('select qqNum from sbTop where grpNum=? order by count desc limit 1', (group, )).fetchall()[0][0]
        con.close()
        my_info = await bot.get_group_member_info(group_id=group, user_id=my_id['user_id'])
        sb_info = await bot.get_group_member_info(group_id=group, user_id=user_id)
        i_am_admin = my_info['role'] in ['admin', 'owner']
        is_admin = sb_info['role'] not in ['admin', 'owner']
        if i_am_admin and is_admin:
            await bot.send_group_msg(group_id=group, message='[CQ:at,qq=' + str(user_id) + ']????????????sbTop???????????????????????????????????????????????????????????????????????????????????????????????????')
            #await bot.set_group_ban(group_id=group, user_id=user_id, duration=600)
'''
@on_command('sb', only_to_me=False, patterns='??????|[sS][bB]|???[bB]')
async def sb(session: CommandSession):
    message_id = session.event['message_id']
    user_id = session.event['user_id']
    rawMessage = session.event['raw_message']
    writeFlag, sendFlag, muteFlag = True, True, False
    ansList = GoodAnsList
    for word in blockMsgList:
        if '??????' in rawMessage or word in rawMessage:
            ansList = badAnsList
    try:
        group_id = session.event['group_id']
        if group_id in blockedGroupID:
            sendFlag = False
        my_id = await bot.get_login_info()
        my_info = await bot.get_group_member_info(group_id=group_id, user_id=my_id['user_id'])
        sb_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
        i_am_admin = my_info['role'] in ['admin', 'owner']
        is_admin = sb_info['role'] not in ['admin', 'owner']
        '''
        if db_read_count(group_id, user_id) >= 400:
            writeFlag = False
            sendFlag = False
        '''
    except:
        writeFlag = False
        i_am_admin = False
        is_admin = False
    for allowMsg in allowMsgList:
        if allowMsg in un_cap(rawMessage):
            writeFlag = False
            sendFlag = False
    try:
        if time.time_ns() // 1000000000 <= sbTime[user_id] + 15:
            writeFlag = False
            sendFlag = False
            muteFlag = True
        else:
            sbTime[user_id] = time.time_ns() // 1000000000
    except:
        sbTime[user_id] = time.time_ns() // 1000000000
    if writeFlag == True:
        if i_am_admin and is_admin:
            try:
                if lastSb[group_id][0] == user_id:
                    lastSb[group_id][1] += 1
                else:
                    lastSb[group_id][0] = user_id
                    lastSb[group_id][1] = 1
            except:
                lastSb[group_id] = []
                lastSb[group_id].append(user_id)
                lastSb[group_id].append(1)
            if lastSb[group_id][1] >= 6:
                muteFlag = True
                sendFlag = False
                lastSb[group_id][0] = 0
                lastSb[group_id][1] = 0
        db_write(1, group_id, user_id)
    #print(lastSb, sbTime)
    if muteFlag == True:
        if i_am_admin and is_admin:
            await bot.set_group_ban(group_id=group_id, user_id=user_id, duration=600)
            await session.send('[CQ:reply,id=' + str(message_id) + ']sb?????????????????????10?????????')
        else:
            sendFlag = False
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
        ans = 'SB?????????Top10???\u000d'
        for i in range(len(readout)):
            try:
                info = await bot.get_group_member_info(group_id=group_id, user_id=readout[i][0])
                name = info['nickname']
            except:
                name = 'Undefind'
            ans += str(i + 1) + '. ' + name + '??????' + str(readout[i][1]) + '???SB???\u000d'
        await session.send(ans)

@on_command('sbtopall', only_to_me=False)
async def sb_top(session: CommandSession):
    sendFlag = True
    try:
        group_id = session.event['group_id']
    except:
        sendFlag = False
    if sendFlag:
        await session.send('[CQ:share,url=https://sbtop.yxyy.top/' + str(group_id) + ',title=?????????SB?????????]')

@bot.server_app.route("/sbtop/")
async def usage():
    return '<h1 align="center">??????URI????????????????????????SB?????????</h1>'

@bot.server_app.route("/sbtop/<name>")
async def sbtop(name):
    readout = db_read(int(name), -1)
    ans = '<h2 align="center">??????' + name + '??????SB????????????</h2>'
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
