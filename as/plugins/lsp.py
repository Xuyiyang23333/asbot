from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from aliyunsdkcore.client import AcsClient
from aliyunsdkimageaudit.request.v20191230 import ScanImageRequest
import requests, random, sqlite3
from config import AK, AKS
'''
async def nsfw(uri):
    image = requests.get(uri)
    pic = {'content': image.content}
    nsfw_api=requests.post('http://127.0.0.1:3333/single/multipart-form', files=pic)
    ans = eval(nsfw_api.text)["prediction"]
    return ans
'''
def is_porn(uri):
    client = AcsClient(AK, AKS, "cn-shanghai")
    request = ScanImageRequest.ScanImageRequest()
    scenes = []
    scenes.append("porn")
    request.set_Scenes(scenes)
    tasks = []
    ## 如下url替换为自有的上海region的oss文件地址
    tasks.append({"DataId":"tegfkhNSMsdfbA0c5mwxpx", "ImageURL":uri})
    request.set_Tasks(tasks)
    response = eval(client.do_action_with_exception(request).decode())
    return response

def db_read(userID):
    con = sqlite3.connect('asbot.db')
    cur = con.cursor()
    readout = cur.execute('select weight from lspTop where qqNum=?', (userID, )).fetchall()
    con.close()
    return readout

def db_write(userID, addCount=1, addWeight=1):
    con = sqlite3.connect('asbot.db')
    cur = con.cursor()
    if len(cur.execute('SELECT * FROM sqlite_master WHERE name="lspTop";').fetchall()) == 0:
        cur.execute('CREATE TABLE lspTop(id INTEGER PRIMARY KEY AUTOINCREMENT, qqNum INT, weight INT, count INT);')
    if len(cur.execute('select * from lspTop where qqNum=?', (userID, )).fetchall()) == 0:
        cur.execute('insert into lspTop (qqNum, weight, count) values (?, ?, ?)', (userID, 10, 0))
    else:
        old = cur.execute('select count, weight from lspTop where qqNum=?', (userID, )).fetchall()[0]
        if old[1] + addWeight <= 0:
            addWeight = 0
        cur.execute('update lspTop set count=?, weight=? where qqNum=?', (old[0] + addCount, old[1] + addWeight, userID))
    con.commit()
    con.close()

ans = '暂时还没有色色！'
reply = ''

@on_command('lastsex')
async def dont_sex(session: CommandSession):
    global ans, reply
    await session.send(reply + ans)

@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    global ans, reply
    user_id = session.event['user_id']
    allPic = session.msg_images
    db_write(user_id, 0, 0)
    weight = db_read(user_id)[0][0]
    choice = random.choices([True, False], [weight, 10])[0]
    if weight >= 20:
        choice = True
    if allPic != [] and choice:
        for uri in allPic:
            response = is_porn(uri)
            if response['Data']['Results'][0]['SubResults'][0]['Label'] != 'normal':
                db_write(user_id)
                label = response['Data']['Results'][0]['SubResults'][0]['Label']
                rate = response['Data']['Results'][0]['SubResults'][0]['Rate']
                ans = '检测到色情信息……\u000d类型：' + label +'\u000d可信度：' + str(rate) + '%\u000d处理方案：不可以色色！'
                try:
                    message_id = session.event['message_id']
                    reply = '[CQ:reply,id=' + str(message_id) + ']'
                except:
                    reply = ''
                return IntentCommand(100.0, '/muteme 600')
            else:
                db_write(user_id, 0, -1)
'''
@on_natural_language(keywords={'sese'}, only_to_me=False)
async def _(session: NLPSession):
    global ans
    allPic = session.msg_images
    if allPic != []:
        for uri in allPic:
            readout = await nsfw(uri)
            probList = []
            for item in readout:
                #print(item['className'] + ' : ' + str(item['probability']))
                if item['probability'] >= 0.7:
                    probList.append([item['className'], item['probability']])
                    ans = ''
                    for prob in probList:
                        ans += prob[0] + ' : ' + str(((prob[1] * (10 ** 4) // (10 ** 2) / (10 ** 2)) * 100)) + '%\u000d'
                    return IntentCommand(100.0, 'lastsex')
'''