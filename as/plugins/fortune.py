from nonebot import on_command, CommandSession
import random, datetime, sqlite3

def fortune_write(userID):
    con = sqlite3.connect('asbot.db')
    cur = con.cursor()
    percent = random.randint(0, 100)
    fDate = datetime.datetime.now().day
    if len(cur.execute('SELECT * FROM sqlite_master WHERE name="fortune";').fetchall()) == 0:
        cur.execute('CREATE TABLE fortune(id INTEGER PRIMARY KEY AUTOINCREMENT, qqNum INT, percent INT, date INT);')
    if len(cur.execute('select * from fortune where qqNum=?', (userID, )).fetchall()) == 0:
        cur.execute('insert into fortune (qqNum, percent, date) values (?, ?, ?)', (userID, percent, fDate))
    if cur.execute('select date from fortune where qqNum=?', (userID, )).fetchall()[0][0] != fDate:
        cur.execute('update fortune set percent=?, date=? where qqNum=?', (percent, fDate, userID))
    con.commit()
    con.close()

def fortune_read(userID):
    con = sqlite3.connect('asbot.db')
    cur = con.cursor()
    readout = cur.execute('select percent from fortune where qqNum=?', (userID, )).fetchall()
    con.close()
    return readout[0][0]

@on_command('fortune', only_to_me=False)
async def fortune(session: CommandSession):
    user_id = session.event['user_id']
    fortune_write(user_id)
    await session.send('[CQ:at,qq=' + str(user_id) + ']您今天有' + str(fortune_read(user_id)) + '%的概率遇到大啥B。')
