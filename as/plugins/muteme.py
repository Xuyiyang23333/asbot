from nonebot import on_command, CommandSession
import nonebot, random

bot = nonebot.get_bot()

@on_command('mute_me', aliases=('晚安', 'sleep', '禅定', '馋腚'))
async def mute_me(session: CommandSession):
    sendFlag = True
    my_id = await bot.get_login_info()
    message_id = session.event['message_id']
    user_id = session.event['user_id']
    group_id = session.event['group_id']
    msg = session.event['raw_message']
    my_info = await bot.get_group_member_info(group_id=group_id, user_id=my_id['user_id'])
    sb_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    i_am_admin = my_info['role'] in ['admin', 'owner']
    is_admin = sb_info['role'] not in ['admin', 'owner']
    if session.current_arg == '' or not '0' <= session.current_arg <= '8':
        length = '10'
    else:
        length = session.current_arg
    try:
        length = eval(length)
        if '晚安' in msg or 'sleep' in msg:
            if session.current_arg == '':
                length = 8
            elif not 0 <= length <= 8:
                await session.send('[CQ:reply,id=' + str(message_id) + ']' + '8小时的睡眠就足够了！')
                sendFlag = False
            length = length * 60
            if sendFlag:
                await session.send('[CQ:reply,id=' + str(message_id) + ']' + '晚安！')
        elif '禅定' in msg or '馋腚' in msg:
            if session.current_arg == '':
                length = random.randint(1, 60)
            elif not 0 <= length <= 3600:
                await session.send('[CQ:reply,id=' + str(message_id) + ']' + '时间太长了！')
                sendFlag = False
            if sendFlag:
                await session.send('[CQ:reply,id=' + str(message_id) + ']' + '禅定' + str(length) + '分钟！')
    except:
        sendFlag = False
    length = length * 60
    if i_am_admin and is_admin and sendFlag:
        await bot.set_group_ban(group_id=group_id, user_id=user_id, duration=length)
