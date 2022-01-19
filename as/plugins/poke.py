from nonebot import on_notice, NoticeSession
from nonebot import on_command, CommandSession
import random, sqlite3, nonebot

bot = nonebot.get_bot()

def db_write(addCount, groupID, userID):
    con = sqlite3.connect('asbot.db')
    cur = con.cursor()
    if len(cur.execute('SELECT * FROM sqlite_master WHERE name="pokeTop";').fetchall()) == 0:
        cur.execute('CREATE TABLE pokeTop(id INTEGER PRIMARY KEY AUTOINCREMENT, qqNum INT, grpNum INT, count INT);')
    if len(cur.execute('select * from pokeTop where grpNum=? and qqNum=?', (groupID, userID)).fetchall()) == 0:
        cur.execute('insert into pokeTop (qqNum, grpNum, count) values (?, ?, ?)', (userID, groupID, addCount))
    else:
        oldCount = cur.execute('select count from pokeTop where grpNum=? and qqNum=?', (groupID, userID)).fetchall()[0][0]
        cur.execute('update pokeTop set count=? where grpNum=? and qqNum=?', (oldCount + addCount, groupID, userID))
    con.commit()
    con.close()

def db_read(groupID, limit):
    con = sqlite3.connect('asbot.db')
    cur = con.cursor()
    readout = cur.execute('select qqNum, count from pokeTop where grpNum=? order by count desc limit ?', (groupID, limit)).fetchall()
    con.close()
    return readout

qqNum = 2557184662
'''
wordList = ['谢谢你。', '我只是机器。', \
    '不用在意我的存在。', '这样就好。', '我能感受到你。', \
        '继续你未完成的工作吧。', '这样会使你感到快乐吗？']
'''
@on_notice('notify')
async def _(session: NoticeSession):
    if session.event['target_id'] == qqNum and session.event['sub_type'] == 'poke':
        try:
            group_id = session.event['group_id']
        except:
            return
        user_id = session.event['user_id']
        db_write(1, group_id, user_id)

@on_command('poketop', only_to_me=False)
async def poke_top(session: CommandSession):
    sendFlag = True
    try:
        group_id = session.event['group_id']
    except:
        sendFlag = False
    if sendFlag == True:
        readout = db_read(group_id, 10)
        ans = '戳一戳排行榜Top10：\u000d'
        for i in range(len(readout)):
            try:
                info = await bot.get_group_member_info(group_id=group_id, user_id=readout[i][0])
                name = info['nickname']
            except:
                name = 'Undefind'
            ans += str(i + 1) + '. ' + name + '戳了' + str(readout[i][1]) + '次。\u000d'
        await session.send(ans)
