from nonebot import on_command, CommandSession
import time

@on_command('ping', only_to_me=False)
async def ping(session: CommandSession):
    sendTime = session.event['time']
    receiveTime = time.time_ns() // 1000000000
    await session.send('Pong! (Delay: ' + str(receiveTime - sendTime) + 's)')