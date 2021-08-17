"""
Author: moying
Date: 2021-08-16 19:37:56
LastEditTime: 2021-08-17 02:07:36
LastEditors: Please set LastEditors
Description: maimai muri detection
FilePath: \maimai无理检测\maiMuriDetect.py
"""
import json
import re
from slide_time import SLIDE_TIME

"""
maimai创作谱面无理配置检测
目前只检测两种情况：
1、多押
2、slide撞尾

对于多押检测，原理较简单，若某一时间点出现三个操作，则认为是无理。
但检测中有一些特殊情况需要说明：
1、slide在检测中会被认为需要全程跟随，也即锁手，或类似于hold的操作。换言之，一个时长非常长的slide中出现了双押则认为是无理；
2、hold、slide开始和结束的瞬间都会被认为是一次操作。也即，如果有某个瞬间，一个hold刚刚结束，而出现了另一对双押，则也认为是无理；
由于协宴和部分宴谱会出现多押，所以也可以关闭多押检测

对于slide撞尾，指的是slide在完成的时候，会触碰到tap、hold、slide-tap的情况。可以分为中途撞无理和尾撞无理。
slide有以下这些类型：
直线　：F-E[x:y],
v形　：FvE[x:y],
pq形　：FpE[x:y],FqE[x:y],
sz形　：FsE[x:y],FzE[x:y],
弧形　：F^E[x:y],F<E[x:y],F>E[x:y],
ppqq形：FppE[x:y],FqqE[x:y],
转折形：FVRE[x:y],
wifi　：FwE[x:y],

中途撞只会发生在: 弧形（^ < >）、部分ppqq型、转折型 中
弧形几乎全程都可能撞
部分ppqq型以及转折型可能在中途经过A区

尾撞会发生在所有slide中
slide完成时，最后一个判定区总是一个A区，若该A区有note则会导致该note被错误触发。

另外，未来还会加入蹭slide检测，若一个slide在应当完成前，其所有需要经过的判定区都被触碰过一次，就会被判为蹭slide无理
"""


def removeListCondition(iterObj, func):
    """根据func的返回值删除对象，func返回值为True时，删除该元素"""
    for i in range(len(iterObj) - 1, -1, -1):
        if func(iterObj[i]):
            iterObj.pop(i)


def notePos(pos, relative):
    """
    @params relative:bool  若为True 则pos应当是0到7的相对键位 反之则为1-8的绝对键位
    将传入的非正规的键位位置转化为正规的键位位置
    """
    if relative:
        if pos < 0:
            pos += 8
        if pos > 7:
            pos %= 8
    else:
        if pos <= 0:
            pos += 8
        if pos > 8:
            pos = (pos - 1) % 8 + 1
    return pos


class MaiMuriDetector:
    def __init__(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                temp = json.load(f)
            self.data = temp["timingList"]
            self.infos = {
                "level": temp["level"],
                "difficulty": temp["difficulty"],
                "title": temp["title"],
                "artist": temp["artist"],
                "designer": temp["designer"],
            }
            assert isinstance(self.data, list)
        except:
            raise RuntimeError(f"无法读取{path}, 错误的编码或文件格式.")

    def multNoteDetect(self, eps=5):
        """
        @params eps:float       操作时间结算的精度 单位为小数点后位
        根据原先操作序列生成操作表
        操作表有3种操作信号：单次操作、占用操作、解除占用操作
        在开始时，操作资源为2（也即两只手），占用操作会使资源-1，解除占用则会+1
        以下情况出现时，会给出多押警告：
        1、单次操作时，资源<=0
        2、占用操作时，资源<=0（此时会临时变为负数）

        同一瞬间，操作按照占用、单次、解除 排序

        opSequence  List<Dict>
        {
            'time': float # 操作时间
            'type': int # 操作类型 0-单次 1-占用 2-解除
        }
        """
        # TODO: 双手拍滑错位检测
        epsRound = lambda x: round(x, eps)

        errorCnt = 0

        opSequence = []
        for noteGroup in self.data:
            baseTime = noteGroup["time"]  # 这一组note的时间
            noteContent = noteGroup["notesContent"]
            position = noteGroup["rawTextPositionX"], noteGroup["rawTextPositionY"]

            for note in noteGroup["noteList"]:
                if note["noteType"] == 0:
                    # tap
                    opSequence.append(
                        {
                            "time": epsRound(baseTime),
                            "type": 0,
                            "noteContent": noteContent,
                            "position": position,
                        }
                    )
                elif note["noteType"] == 1:
                    # slide
                    opSequence.append(
                        {
                            "time": epsRound(baseTime),
                            "type": 0,
                            "noteContent": noteContent,
                            "position": position,
                        }
                    )  # slide-tap
                    opSequence.append(
                        {
                            "time": epsRound(note["slideStartTime"]),
                            "type": 1,
                            "noteContent": noteContent,
                            "position": position,
                        }
                    )  # slide-track-start
                    opSequence.append(
                        {
                            "time": epsRound(note["slideStartTime"]) + epsRound(note["slideTime"]),
                            "type": 2,
                            "noteContent": noteContent,
                            "position": position,
                        }
                    )  # slide-track-end
                elif note["noteType"] == 2:
                    # hold
                    opSequence.append(
                        {
                            "time": epsRound(baseTime),
                            "type": 1,
                            "noteContent": noteContent,
                            "position": position,
                        }
                    )
                    opSequence.append(
                        {
                            "time": epsRound(baseTime) + (note["holdTime"]),
                            "type": 2,
                            "noteContent": noteContent,
                            "position": position,
                        }
                    )

        # 按照时间顺序正向排序
        opSequence.sort(key=lambda x: (x["time"], (1, 2, 0)[x["type"]]))
        signal = 2  # 2个资源（信号量）
        for op in opSequence:
            if op["type"] == 0:
                if signal <= 0:
                    print(f"""[多押无理] {op['position'][1]+1}行的"{op['noteContent']}"可能出现了多押""")
                    errorCnt += 1
            elif op["type"] == 1:
                if signal <= 0:
                    print(f"""[多押无理] {op['position'][1]+1}行的"{op['noteContent']}"可能出现了多押""")
                    errorCnt += 1
                signal -= 1
            elif op["type"] == 2:
                signal += 1

        return errorCnt

    def slideDetect(self, judgementLength=0.15):
        """
        @params judgementLength:float   判定时长，指tap判定为good的时间界限

        SLIDE_TIME中数据通过MajView生成谱面预览并使用PR逐帧慢放计算得出，不代表官方数据，不保证正确性
        """

        """
        opSequence List<Dict>
        {
            'time': float,      # 操作时间
            'area': int,        # 操作区域（A区）
            'type': int         # 操作类型 0-tap 1-slideTrack
        }
        """

        prog = re.compile(r"(\d)(.+?)(\d{1,2})\[\d+?\:\d+?\]")

        opSequence = []
        for noteGroup in self.data:
            baseTime = noteGroup["time"]  # 这一组note的时间
            position = noteGroup["rawTextPositionX"], noteGroup["rawTextPositionY"]

            for note in noteGroup["noteList"]:
                if note["noteType"] == 0 or note["noteType"] == 2:
                    # tap or hold
                    # 这里无论是tap还是hold都是一样的 因为只是检测是否会蹭到开始的判定 所以hold可以视为tap
                    opSequence.append(
                        {
                            "time": baseTime,
                            "area": note["startPosition"],
                            "type": 0,
                            "noteContent": note["noteContent"],
                            "position": position,
                        }
                    )
                elif note["noteType"] == 1:
                    # slide
                    """
                    通过noteContent匹配出slide类型、起点、终点
                    在SLIDE_TIME中找到对应类型的slide时间数据
                    将终点减去起点，得到相对终点，带入上面的dict得到时间比例
                    将时间比例乘以slideTime得到对应进入A区的相对时间
                    将进入A区相对时间加上slideStartTime即可得到进入A区的真实时间
                    另外，经过的A区编号在SLIDE_TIME中也是相对位置，需要加上起点才能得到绝对位置
                    """
                    try:
                        slideInfos = prog.match(note["noteContent"])
                        sStart = int(slideInfos.group(1))
                        sType = slideInfos.group(2)
                        sEnd = slideInfos.group(3)
                    except:
                        print(f"[语法错误] {position[1]+1}行的\"{note['noteContent']}\"解析失败，可能存在语法错误")
                        continue
                    # 处理转折型（aVbc）特殊情况
                    if sType == "V":
                        sEnd = (notePos(int(sEnd[0]) - sStart, True), notePos(int(sEnd[1]) - sStart, True))
                    else:
                        sEnd = notePos(int(sEnd) - sStart, True)  # 相对终点

                    if sType == ">" and sStart in (3, 4, 5, 6):  # 数据中的>总是顺时针 若真实数据为逆时针 则需要反转
                        """
                        WARNING:
                        这其实是一个测定数据时的遗留问题
                        在测定数据的时候，对于每一种slide，都以1开头来测定，并存储相对的位置
                        在实际判定的时候，会根据实际的起点和相对位置计算绝对位置，也就是说，是在测定数据的基础上进行了旋转
                        但是>和<型的slide，其方向会受到起点位置的影响
                        以>为例，当起点是7812时，是顺时针，起点是3456时，则为逆时针
                        但是在测定时，因为起点总是1，所以>总是顺时针的，<总是逆时针的
                        --- 换言之，在SLIDE_TIME里，>不表示向右开始回旋的slide，而表示“总是顺时针的回旋slide” ---
                        所以此处选择对>和<slide进行特判，如果和测定时的方向相反，则人为反转操作符

                        请注意：这是目前的权宜之计，也许后续会更正这个问题
                        """
                        # 当起点为3456 slide类型为>时 和测定方向相反
                        sType = "<"
                    elif sType == "<" and sStart in (3, 4, 5, 6):
                        # 当起点为3456 slide类型为<时 和测定方向相反
                        sType = ">"

                    try:
                        sTimeInfo = SLIDE_TIME[sType][sEnd]
                    except:
                        print(f"[语法错误] {position[1]+1}行的\"{note['noteContent']}\"解析失败，可能存在语法错误")
                        continue

                    for each in sTimeInfo:
                        # print(note["noteContent"], sStart, sType, sEnd, notePos(each["area"] + sStart, False))
                        opSequence.append(
                            {
                                "time": each["time"] * note["slideTime"] + note["slideStartTime"],
                                "area": notePos(each["area"] + sStart, False),
                                "type": 1,
                                "noteContent": note["noteContent"],
                                "position": position,
                            }
                        )

        """
        生成操作序列后，需要开始判定无理
        无理满足以下情况：
        1、一个slideTrack操作与一个tap操作发生发生在同一个area中
        2、slideTrack操作先于tap操作    # 必须是slide撞上了未发生的tap(蹭只可能是fast) 如果反过来 则应该是判断是否为蹭
        3、二者时间间隔小于judgementLength
        """
        opSequence.sort(key=lambda x: (x["time"], -x["type"]))
        errorCnt = 0

        inJudgement = []  # 正在判定的slide操作
        for op in opSequence:
            curTime = op["time"]
            # 删除curTime-judgementLength之前的待判定操作 因为这些操作不再可能被判无理了
            removeListCondition(inJudgement, lambda x: x["time"] + judgementLength < curTime)

            if op["type"] == 1:
                # 将slide操作加入待判定操作列表中
                inJudgement.append(op)
            elif op["type"] == 0:
                # tap操作
                for e in inJudgement:
                    if e["area"] == op["area"] and op["time"] - judgementLength < e["time"] < op["time"]:
                        # 无理
                        print(
                            f"""[撞尾无理] {e['position'][1]+1}行的"{e['noteContent']}"可能会撞上 {op['position'][1]}行的"{op['noteContent']}\""""
                        )
                        errorCnt += 1

        return errorCnt

    def detectMuri(self, multNoteDetectEnable=True, slideDetectAccuracy=0.15):
        """检测"""
        print(
            f"""【谱面信息】
{self.infos['title']} - {self.infos['artist']}
{self.infos['difficulty']} lv.{self.infos['level']}
note designed by {self.infos['designer']}
"""
        )

        print("【开始检查谱面】\n")

        if multNoteDetectEnable:
            multNoteErrorCnt = self.multNoteDetect(5)
            if multNoteErrorCnt == 0:
                print("【未检测到多押无理配置】")
            print()

        slideErrorCnt = self.slideDetect(slideDetectAccuracy)
        if slideErrorCnt == 0:
            print("【未检测到撞尾无理配置】")
        print()

        if multNoteDetectEnable:
            print(f"检查完毕，共发现{multNoteErrorCnt}个多押无理错误，{slideErrorCnt}个撞尾无理错误")
        else:
            print(f"检查完毕，共发现{slideErrorCnt}个撞尾无理错误")
        print("\n>>>maimaiMuriDetector提供的警告与建议并不一定完全准确，结果仅供参考<<<")


if __name__ == "__main__":
    import sys
    import os
    import getopt

    def getOptByName(opts, opt):
        for optName, optValue in opts:
            if optName in opt:
                return optValue
        return None

    opts, args = getopt.getopt(
        sys.argv[1:],
        "hicm:s:",
        ["help", "interactive", "command-line", "mult-note-detection=", "slide-detection-accuracy="],
    )

    if len(opts) == 0 or getOptByName(opts, ("-h", "--help")) is not None:
        # 显示帮助信息并退出
        print(
            r"""帮助信息
maimaiMuriDetector [-h] [-i] [-c] [-m [-s]] [filepath]
-h --help               显示本帮助信息
-i --interactive        适合电脑苦手的方式 通过交互式的命令菜单来使用maimaiMuriDetector
-c --command-line       适合电脑老手的方式 通过命令行来使用maimaiMuriDetector
                            既不传入-i 也不传入-c时 默认工作在命令行模式下
-m --mult-note-detection
                        指定是否开启多押无理检测 默认为开 传入f/0/false可禁用多押无理检测
                            如果您的谱面是协宴 或存在多押的宴谱 建议您关闭多押无理检测
-s --slide-detection-accuracy
                        设置撞尾检测的时长 默认为150(good的判定区间) 单位为毫秒 该设置不建议低于默认值
                            如果您希望更严格的检测撞尾无理 可以适当提高该设置
filepath                指定需要检测的majdata.json路径 使用-c选项时 必须输入此参数
                            如果您的路径中含有空格 请您用半角引号(英文引号)将路径括起 或者您也可以直接将文件拖拽至shell窗口中自动生成路径

·如何获得majdata.json：
    使用MajdataEdit打开您的谱面文件，切换到需要检测的难度，单击播放或“录制模式”。此时MajdataEdit会在您的谱面文件夹中生成majdata.json
    请注意：
        majdata.json中只能存放一个难度的谱面信息。
        举例来说：如果您查看过MASTER谱面之后，又切换到EXPERT难度并点击播放或“录制模式”，那么谱面文件夹中的majdata.json中的内容就会变为EXPERT谱面的信息。这一点请您一定要多加注意

命令示例：
maimaiMuriDetector -h
maimaiMuriDetector -i
maimaiMuriDetector --interactive
maimaiMuriDetector -c D:\maimai自制谱\tempestissimo\majdata.json
maimaiMuriDetector -c -m false ".\[宴]Oshama Scramble\majdata.json"
maimaiMuriDetector --slide-detection-accuracy=200 majdata.json
maimaiMuriDetector majdata.json"""
        )
        sys.exit(0)
    else:
        interactive = False
        if getOptByName(opts, ("-i", "--interactive")) is not None:
            # 交互式
            interactive = True

        if getOptByName(opts, ("-c", "--command-line")) is not None:
            if interactive:
                print('错误的选项: 同时使用了-i和-c选项')
                sys.exit(1)
            interactive = False

        multNoteDetection = getOptByName(opts, ("-m", "--mult-note-detection"))
        if multNoteDetection is not None:
            if interactive:
                print('错误的选项: 同时使用了-i和-m选项')
                sys.exit(1)
            interactive = False
            multNoteDetection = (False if multNoteDetection in ('f','0','false') else True)
        else:
            multNoteDetection = True
        
        slideDetectionAccuracy = getOptByName(opts, ('-s', '--slide-detection-accuracy'))
        if slideDetectionAccuracy is not None:
            if interactive:
                print('错误的选项: 同时使用了-i和-s选项')
                sys.exit(1)
            interactive = False
            try:
                slideDetectionAccuracy = int(slideDetectionAccuracy)/1000
            except:
                print('错误的参数: -s的值必须是一个整数')
                sys.exit(2)
        else:
            slideDetectionAccuracy = 0.15
        
        if not interactive:
            if len(args) == 0:
                print('错误的参数: 使用命令行模式 但没有给出filepath')
                sys.exit(2)
            if len(args) != 1:
                print('错误的参数: 给出了多个filepath 或有参数输入有误')
                sys.exit(2)
            if not os.path.exists(args[0]):
                print('错误的参数: 给出的filepath不存在')
                sys.exit(2)
        
        if interactive:
            # 交互模式
            filepath = input('请输入majdata.json的路径(也可将文件拖拽至该窗口):')
            if not os.path.exists(filepath):
                print('majdata.json路径错误 请检查输入并重试')
                sys.exit(2)
            
            multNoteDetection = input('是否开启多押无理检测\n\t如果您的谱面是协宴或允许多押的宴谱 您可以禁用多押检测\n\t(y/n 默认y):') != 'n'
            slideDetectionAccuracy = input('撞尾检测精度\n\t单位ms 默认值150\n\t默认值是最低限度的撞尾检测 如果您想加大检测力度 可以适当提高此值\n\t(直接输入回车或输入非数字视为使用默认值):')
            try:
                slideDetectionAccuracy = int(slideDetectionAccuracy)/1000
            except:
                slideDetectionAccuracy = 0.15
            print('\n\n')
            mmd = MaiMuriDetector(filepath)
            mmd.detectMuri(multNoteDetection, slideDetectionAccuracy)
        else:
            # 命令行模式
            mmd = MaiMuriDetector(args[0])
            mmd.detectMuri(multNoteDetection, slideDetectionAccuracy)
        
        try:
            # 因为不知道是什么平台的，总之尝试pause一下，如果是linux的大概率是在shell里运行的，不pause也无所谓
            os.system('pause')
        except:
            pass
