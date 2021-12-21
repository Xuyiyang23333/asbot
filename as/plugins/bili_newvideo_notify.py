import nonebot
from bilibili_api import user, sync

async def videoInfo(u):
    info = await u.get_videos()
    return info['list']['vlist'][0]['bvid'], info['list']['vlist'][0]['title'], info['list']['vlist'][0]['description']

async def liveInfo(u):
	info = await u.get_live_info()
	return info['live_room']['liveStatus'], info['live_room']['title'], info['live_room']['url'], info['live_room']['cover']

userID = 349990299
nickname = f'听风'
groupList = [131211694, 783224265, 837491344]
previousVideo, title, desc = sync(videoInfo(user.User(userID)))
oldLiveStat, liveTitle, liveUrl, liveCover = sync(liveInfo(user.User(userID)))
@nonebot.scheduler.scheduled_job('interval', minutes=5)
async def biliUpStat():
    bot = nonebot.get_bot()
    global previousVideo, oldLiveStat
    latestVideo, title, desc = await videoInfo(user.User(userID))
    if latestVideo != previousVideo:
        for group in groupList:
            await bot.send_group_msg(group_id=group, message=nickname + f'发新视频啦！')
            await bot.send_group_msg(group_id=group, message=f'[CQ:share,url=https://www.bilibili.com/video/' + latestVideo + ',title=' + title + ',image=https://www.bilibili.com/favicon.ico,content=' + desc + ']')
        previousVideo = latestVideo
    liveStat, liveTitle, liveUrl, liveCover = await liveInfo(user.User(userID))
    if liveStat != oldLiveStat and liveStat == 1:
        for group in groupList:
            await bot.send_group_msg(group_id=group, message=nickname + f'开始直播啦！')
            await bot.send_group_msg(group_id=group, message=f'[CQ:share,url=' + liveUrl + ',title=' + liveTitle + ',image=' + liveCover + ']')
    oldLiveStat = liveStat
