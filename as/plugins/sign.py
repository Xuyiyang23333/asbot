import sqlite3, random, datetime
from nonebot import on_command, CommandSession

def score_write(userID):
    con = sqlite3.connect('asbot.db')
    cur = con.cursor()
    addScore = random.choices([1, 3, 5, 7, 9, 11, 13, 15, 114514], [100, 100, 100, 100, 100, 100, 100, 100, 1])[0]
    sDate = datetime.datetime.now().day
    if len(cur.execute('SELECT * FROM sqlite_master WHERE name="scoreTable";').fetchall()) == 0:
        cur.execute('CREATE TABLE scoreTable(id INTEGER PRIMARY KEY AUTOINCREMENT, qqNum INT, score INT, date INT);')
    if len(cur.execute('select * from scoreTable where qqNum=?', (userID, )).fetchall()) == 0:
        cur.execute('insert into scoreTable (qqNum, score, date) values (?, ?, ?)', (userID, addScore, sDate))
        ans = '经验加' + str(addScore) + '！'
    elif cur.execute('select date from scoreTable where qqNum=?', (userID, )).fetchall()[0][0] == sDate:
        ans = '您已经签到过了！'
    else:
        oldScore = cur.execute('select score from scoreTable where qqNum=?', (userID, )).fetchall()[0][0]
        cur.execute('update scoreTable set score=?, date=? where qqNum=?', (oldScore + addScore, sDate, userID))
        ans = '经验加' + str(addScore) + '！'
    con.commit()
    con.close()
    return ans

def score_read(userID):
    con = sqlite3.connect('asbot.db')
    cur = con.cursor()
    readout = cur.execute('select score from scoreTable where qqNum=?', (userID, )).fetchall()
    con.close()
    return '您目前的经验是' + str(readout[0][0]) + '点。'

@on_command('sign', only_to_me=False)
async def fortune(session: CommandSession):
    user_id = session.event['user_id']
    await session.send('[CQ:at,qq=' + str(user_id) + ']' + score_write(user_id) + '\u000d' + score_read(user_id))
