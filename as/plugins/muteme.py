from nonebot import on_command, CommandSession
import nonebot

bot = nonebot.get_bot()

@on_command('muteme')
async def mute_me(session: CommandSession):
    my_id = await bot.get_login_info()
    user_id = session.event['user_id']
    group_id = session.event['group_id']
    my_info = await bot.get_group_member_info(group_id=group_id, user_id=my_id['user_id'])
    sb_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    i_am__admin = my_info['role'] in ['admin', 'owner']
    is_admin = sb_info['role'] not in ['admin', 'owner']
    length = session.current_arg
    print(i_am__admin, is_admin)
    if i_am__admin and is_admin:
        await bot.set_group_ban(group_id=group_id, user_id=user_id, duration=length)
