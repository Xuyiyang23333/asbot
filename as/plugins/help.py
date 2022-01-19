from nonebot import on_command, CommandSession
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

NICKNAME = '菊宝'

TEXT = NICKNAME + '功能说明：\n\
1. 用adofai search + 曲名 + <1~10>/list查询adofai.gg上的曲谱。\n\
2. 当群内有人说sb/傻逼时会加以附和并计入数据库。\n\
3. 用sbtop指令可以获取该群内的sb排行榜前10名。\n\
4. sbtopall指令将返回一个URI，包含了完整的排行榜。\n\
5. 用fortune指令算一算您今天遇到大啥B的概率。\n\
6. sign指令提供签到功能，分数从[1, 3, 5, 7, 9, 11, 13, 15, 114514]中随机抽取，除114514外权重相同，抽得114514的概率为1/801。\n\
7. ' + NICKNAME + 'sleep + <数字>，' + NICKNAME + '会向你问好并给予你指定时间的禁言。\n\
8. ' + NICKNAME + '晚安，功能同上。\n\
9. 试一试' + NICKNAME + '禅定，会给予你0~60分钟的随机禁言。\n\
10. 用heat/heihei指令一键**。\n\
11. fkcy + <上文> + <下文>可以自动生成“5000兆元”风格的图片。\n\
12. poketop会返回群内菊宝被“戳一戳”次数的排名。\n\
温馨提示：sb附和功能有频率限制，连续6次或是15秒内2次即可触发。\
sb记录没有（写）归零功能。sleep功能单位为小时，不指定参数则默认8小时。\
**指令可以接受参数，无参数则默认使用调用者昵称。\
曲名中有空格时请用_替代之。'

def new_line_show_txt(img, text, size, x, y, line=320):
    '''
    #根据字数换行
    newText = text[:line]
    lineCnt = 1
    for i in range(1, len(text)):
        if i % line == 0:
            newText = newText + '\n' + text[i:i + line]
            lineCnt += 1
    '''
    AA = 4 #抗锯齿
    font = ImageFont.truetype("LXGWWenKai-Regular.ttf", size * AA)
    lineCnt, width, nlFlag = 1, 0, 0
    newText = ''
    for i in range(len(text)): #根据像素数判断是否换行
        if text[i] == '\n':
            newText = newText + text[nlFlag:i]
            nlFlag = i
            width = 0
            lineCnt += 1
            continue
        w, h = font.getsize(text[i])
        x_offset, y_offset = font.getoffset(text[nlFlag * lineCnt:nlFlag * lineCnt + lineCnt])
        width += w - x_offset
        if width >= line * AA - x_offset:
            newText = newText + text[nlFlag:i] + '\n'
            nlFlag = i
            width = 0
            lineCnt += 1
    newText = newText + text[nlFlag:]
    x_offset, y_offset = font.getoffset(newText)
    w, h = line, lineCnt * size
    textImg = Image.new('RGBA', (w * AA, h * AA), (255, 255, 255, 0))
    drawText = ImageDraw.Draw(textImg)
    drawText.text([0, 0], newText, (255, 255, 255, 255), font)
    textImg = textImg.resize((w, h), resample=Image.ANTIALIAS)
    img.alpha_composite(textImg, (x - (x_offset // AA), y - (y_offset // AA)))

img = Image.open('bg.jpg')
img = img.filter(ImageFilter.GaussianBlur(20))
img = ImageEnhance.Brightness(img).enhance(0.75)
img = img.convert('RGBA')
#draw.rectangle([20, 20, 880, 200], None, (0, 0, 0, 255), 5)
new_line_show_txt(img, TEXT, 50, 20, 20, 1900)
img = img.convert('RGB')
img.save('help.jpg')

@on_command('help', only_to_me=False)
async def help(session: CommandSession):
    await session.send('[CQ:image,file=file:///home/david/asbot/help.jpg]')
