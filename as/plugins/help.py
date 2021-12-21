from nonebot import on_command, CommandSession

NICKNAME = '菊宝'

@on_command('help', only_to_me=False)
async def help(session: CommandSession):
    await session.send(NICKNAME + '功能说明：\u000d\
    1. 每天0、6、12、18点会提示群友们asup（用@' + NICKNAME + ' asup可以手动调起）。\u000d\
    2. 当群内有人说sb/傻逼时会加以附和并计入数据库。\u000d\
    3. 用sbtop指令可以获取该群内的sb排行榜前10名。\u000d\
    4. sbtopall指令将返回一个URI，包含了完整的排行榜。\u000d\
    5. 用fortune指令算一算您今天遇到大啥B的概率。\u000d\
    6. sign指令提供签到功能，分数从[1, 3, 5, 7, 9, 11, 13, 15, 114514]中随机抽取，除114514外权重相同，抽得114514的概率为1/801。\u000d\
    7. @' + NICKNAME + 'sleep + <数字>，' + NICKNAME + '会向你问好并给予你指定时间的禁言。\u000d\
    温馨提示：sb记录没有（写）归零功能。sleep功能单位为小时。复制的@无效！')
