from config import groupID
from datetime import datetime
import pytz
import nonebot
from nonebot import on_command, CommandSession

imgURI = 'https://test.yxyy.top/%E8%8F%8A%E5%AE%9D.jpg'

@on_command('asup')
async def manual_up(session: CommandSession):
    await session.send('[CQ:image,file=' + imgURI + ']')

@nonebot.scheduler.scheduled_job('cron', hour='0,6,12,18')
async def auto_up():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    for group in groupID:
        await bot.send_group_msg(group_id=group, message=f'现在{now.hour}点整啦！[CQ:image,file=' + imgURI + ']')
