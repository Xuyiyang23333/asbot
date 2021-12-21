from nonebot import on_command, CommandSession

@on_command('httpcats', only_to_me=False)
async def http_cat(session: CommandSession):
    status = session.current_arg
    await session.send('[CQ:image,file=https://http.cat/' + status + '.jpg]')