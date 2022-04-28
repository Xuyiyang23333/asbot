import sqlite3, random
from nonebot import on_command, CommandSession

def wager(userID, count=1):
    con = sqlite3.connect('asbot.db')
    cur = con.cursor()
    if len(cur.execute('SELECT * FROM sqlite_master WHERE name="scoreTable";').fetchall()) == 0:
        cur.execute('CREATE TABLE scoreTable(id INTEGER PRIMARY KEY AUTOINCREMENT, qqNum INT, score INT, date INT);')
    if len(cur.execute('SELECT * FROM sqlite_master WHERE name="dataTable";').fetchall()) == 0:
        cur.execute('CREATE TABLE dataTable(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, data INT);')
    if len(cur.execute('select * from dataTable where name=?', ('wager', )).fetchall()) == 0:
        cur.execute('insert into dataTable (name, data) values (?, ?)', ('wager', 0))
    if len(cur.execute('select * from scoreTable where qqNum=?', (userID, )).fetchall()) == 0:
        ans = '您还未签到过，请尝试sign指令。'
    else:
        oldScore = cur.execute('select score from scoreTable where qqNum=?', (userID, )).fetchall()[0][0]
        if count > oldScore:
            ans = '经验不足！'
        else:
            history = cur.execute('select data from dataTable where name=?', ('wager', )).fetchall()[0][0]
            if history == 0:
                win = False
            else:
                win = random.choices([True, False], [count, history])[0]
            if win:
                addScore = history
                cur.execute('update dataTable set data=? where name=?', (0, 'wager'))
            else:
                addScore = -count
                cur.execute('update dataTable set data=? where name=?', (history + count, 'wager'))
            cur.execute('update scoreTable set score=? where qqNum=?', (oldScore + addScore, userID))
            if addScore > 0:
                sym = '加'
            else:
                sym = '减'
                addScore = -addScore
            ans = '经验' + sym + str(addScore) + '！'
    con.commit()
    con.close()
    return ans

def score_read(userID):
    con = sqlite3.connect('asbot.db')
    cur = con.cursor()
    readout = cur.execute('select score from scoreTable where qqNum=?', (userID, )).fetchall()
    con.close()
    return '您目前的经验是' + str(readout[0][0]) + '点。'

def wager_read():
    con = sqlite3.connect('asbot.db')
    cur = con.cursor()
    readout = cur.execute('select data from dataTable where name=?', ('wager', )).fetchall()
    con.close()
    return '目前奖池中的的经验数为' + str(readout[0][0]) + '点。'

@on_command('wager', only_to_me=False)
async def fortune(session: CommandSession):
    user_id = session.event['user_id']
    if session.current_arg == '':
        count = 1
    else:
        count = session.current_arg
    await session.send('[CQ:at,qq=' + str(user_id) + ']' + wager(user_id, int(count)) + '\u000d' + score_read(user_id) + '\u000d' + wager_read())
