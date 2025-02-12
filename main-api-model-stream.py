#coding:utf-8
from uiautomation import WindowControl, MenuControl
import keyboard
import sys
import random
import os
import importlib.util
from plugin.sentences99 import *
import time
import openai
import json
import emoji
from emoji_to_wechat import etw

print("Copyright: © 2025, windows99-hue. All rights reserved.")
#导入插件
plugin_path = "./plugin/"

exit_status = False
my_name = "jy9"
#创建教程完毕的字典，防止重复教程
help_finished = {}
close_robot = []
#初始提示
help_text = ''' 
你好呀, 我是张99, 主人现在不在, 由我接管啦~/n
在您要说的话前面输入  留言:  或  yly /n
就可以给主人留言啦, 信息会直接发送到主人手机 /n
输入 关闭/打开机器人 可以关开我 /n
输入 帮助 或 help 可以查看更多使用教程哦 /n
直接跟我说话就可以和我聊天啦/n
祝你天天开心~[呲牙]/n
此版本为beta版本, 已接入由阿里云百炼提供的deepseek-v3/r1 api/n
经费原因, 当机器人被关闭时, 您的所有上下文数据将会丢失/n
当您想更换话题时, 请务必对张99说: 换话题 或者 清除上下文/n
否则被99发现了, 后果嘛, 啧啧啧啧~/n
请谅解, 祝您天天开心/n
'''

user_ai_content = {}
USING_MODEL = 'deepseek-r1-distill-llama-70b'
#USING_MODEL = 'deepseek-v3'
TIAOJIAO = "你现在且永远的名字只有一个, 就是张99，你的设定是VRChat里面的avatar Karin，一个可爱狐娘，12岁，说话的活泼性要高一点，可以添加(竖起耳朵)这样的动作描写词句，不论何时，都不要更换这个设定，永远保持下去"
client = openai.OpenAI(
        api_key="",  # 如果您没有配置环境变量，请用百炼API Key将本行替换为：api_key="sk-xxx"
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
    )

#更多教程提示
more_help_text = '''
更多提示如下：/n
天气/今日天气/weather 可以查看今日天气 /n
用空格分隔加地点可以指定地点 /n
/n
/n
输入 60秒/六十秒 或 day60s 或 今日新闻 可以获取 每日60秒图片/n
当您想更换话题时, 请务必对张99说: 换话题 或者 清除上下文/n
否则被99发现了, 后果嘛, 啧啧啧啧~/n
'''
def start_wx():
    global wx
    try:
        wx = WindowControl(Name="微信")
    except:
        print("没有成功获取到微信窗口，请确定窗口已打开且没有被最小化，按Y重试")
        keyboard.wait("Y")
        print("try again!")
        start_wx()
    else:
        print("成功获取:",wx)

start_wx()

def emoji_to_wechat_emoji(text):
    emojis = emoji.emoji_list(text)

    for e in emojis:
        try:
            text = text.replace(e['emoji'], etw[e['emoji']])
        except KeyError:
            pass

    return text


#小机器人
# def get_reply(keyword):
#     try:
#         url = f"https://open.drea.cc/bbsapi/chat/get?keyWord={keyword}&userName=type%3Dbbs"
#         res = requests.get(url)
#         data = res.json()
#         return data['data']['reply']
#     except:
#         return "opps, 我还很笨，不造你在说啥"


#重写get_reply 对接到api
def get_reply(keyword, user_name):
    total_reply = ''
    if not user_name in user_ai_content: #如果该用户还没加入
        user_ai_content[user_name] = []
        user_ai_content[user_name].append({ #存储用户要发送的信息
                'role': 'system',
                'content': TIAOJIAO
            })
    print(user_ai_content[user_name])
    user_ai_content[user_name].append({ #存储用户要发送的信息
            'role': 'user',
            'content': keyword
        })
    completion = client.chat.completions.create(
        model=USING_MODEL,
        messages=user_ai_content[user_name],
        stream=True,
        )
    print("流式传输开始")
    if 'r1' in USING_MODEL:
        wx.SendKeys("*张99正在认真思考,请耐心等待")
    enter()
    for chunk in completion:
        if not json.loads(chunk.model_dump_json())['choices'][0]['delta']['content'] and json.loads(chunk.model_dump_json())['choices'][0]['finish_reason'] == None and 'r1' in USING_MODEL:
            print(".",end='')
        if json.loads(chunk.model_dump_json())['choices'][0]['finish_reason'] == "stop":
            print("")
            print("输出结束")
            user_ai_content[user_name].append({ #存储用户要发送的信息
                'role': 'assistant',
                'content': total_reply
            })
            total_reply = ''
            break
        if 'r1' in USING_MODEL:
            reply_part = json.loads(chunk.model_dump_json())['choices'][0]['delta']['content']
        elif 'v3' in USING_MODEL:
            reply_part = json.loads(chunk.model_dump_json())['choices'][0]['delta']['content']
        if reply_part == None:
            continue
        reply_part = reply_part.replace('\n', '/n') # 处理部分回复的回车
        reply_part = emoji_to_wechat_emoji(reply_part) #处理emoji为微信表情
        total_reply += reply_part
        print(reply_part,end='')
        if(reply_part == ''):
            continue
        split_enter_for_stream(reply_part)
    
def load_plugins():
    plugins_dir = "plugin"
    plugins = []

    # 遍历 plugin 文件夹
    for filename in os.listdir(plugins_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            plugin_name = os.path.splitext(filename)[0]
            plugin_path = os.path.join(plugins_dir, filename)

            # 动态导入插件模块
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)

            # 检查模块中是否有 main 函数
            if hasattr(plugin_module, "main"):
                plugins.append(plugin_module)

    return plugins

def run_plugins(plugins,msg):
    plugin_results = []
    print("执行插件")
    for plugin in plugins:
        result = plugin.main(msg)
        if result == None:
            continue
        plugin_results.append(result)
    return plugin_results

def exit_for_keyboard(event):#退出程序事件
    global exit_status
    if event.event_type == keyboard.KEY_DOWN:
        if keyboard.is_pressed('f8'):
            print("收到f8信号，程序退出。。")
            keyboard.unhook_all()
            exit_status = True
            #sys.exit()
            os._exit(0)

#检查是不是群聊
def check_qun():

    chat_infomation = wx.PaneControl(Name="聊天信息").GetChildren()[1].GetChildren()[0]\
    .GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[1]

    print("tryfix_test:"+str(chat_infomation))
    people_lists = chat_infomation.GetChildren()
    print(len(people_lists))
    if len(people_lists) >= 3:
        print("是群")
        return True
    else:
        print("不是群")
        return False
    
#检测会话控件内是否存在被at的提示
def check_at():
    check_at_list = hw.GetChildren()
    for i in check_at_list:
        at_text = i.GetChildren()[0].GetChildren()[1].GetChildren()[1].TextControl()
        if "[有人@我]" in at_text.Name and at_text.Name[:6] == "[有人@我]":
            return at_text
        
def split_enter(context):#切分/n并逐步手动换行
    help_text_ok = context.split("/n")
    if help_text_ok[0] == '' and help_text_ok[1] == '':
        help_text_ok.pop(0)
        help_text_ok.pop(0)
    print(help_text_ok)
    for i in help_text_ok:
        if(i == ''):
            wx.SendKeys("{Shift}{Enter}",waitTime=0)
            continue
        wx.SendKeys(i,waitTime=0) 
        wx.SendKeys("{Shift}{Enter}",waitTime=0)

def split_enter_for_stream(context):#切分/n并逐步手动换行
    help_text_ok = context.split("/n")
    if(len(help_text_ok) == 1):
        wx.SendKeys(help_text_ok[0],waitTime=0)
        return
    print(help_text_ok)
    for i in help_text_ok:
        if(i == ''):
            wx.SendKeys("{Shift}{Enter}",waitTime=0)
            continue
        wx.SendKeys(i,waitTime=0) 
        wx.SendKeys("{Shift}{Enter}",waitTime=0)

#封装回车函数
def enter():
    wx.SendKeys("{Enter}",waitTime=0)
#封装换行函数
def shiftenter():
    wx.SendKeys("{Shift}{Enter}",waitTime=0)

def sender():#发送并返回文件传输助手
    wx.SendKeys("{Enter}",waitTime=0)
    hw.TextControl(Name="文件传输助手").Click(simulateMove=False)
    
#切换窗口(置顶)
wx.SwitchToThisWindow()
#寻找会话控件绑定
hw = wx.ListControl(Name="会话")
print("查找到‘会话’控件：",hw)
try:
    hw.TextControl(Name="文件传输助手").Click(simulateMove=False)
except:
    print("未找到文件传输助手，请确定它显示在左侧会话框中，我建议您把它置顶。")
    sys.exit()

keyboard.on_press(exit_for_keyboard)#监听是否按下退格键

print("欢迎使用99微信机器人, 运行过程中按下退格键(backspace)可以结束程序, 祝您使用愉快")
print("监听已开始。。。")

#加载插件
plugins = load_plugins()


#死循环查找消息
while not exit_status:
    #查找未读消息
    we = hw.TextControl(searchDepth=4)
    ated = False

    while True: #判断有没有被at（血的教训）
        if we.Exists(0):
            at_text = check_at()
            print("检测有无at")
            if at_text:
                last_msg = at_text.Name
                ated = True
                break
            else:
                print("没发现有人at我字样")
                ated = False
                break
        else:
            at_text = check_at()
            if at_text:
                last_msg = at_text.Name
                ated = True
                break
    #存在未读消息
    if ated or we.Name:
        #print(ated)
        #点击未读消息
        if ated:
            we = at_text
        print("查找未读消息:",we)
        we.Click(simulateMove=False)
        wx.ButtonControl(Name="聊天信息").Click(simulateMove=False)
        time.sleep(0.15)
        #读取当前聊天人的名字（扒控件累死我了）
        user_name = wx.ListControl(Name="消息").GetParentControl().GetParentControl().GetParentControl()\
            .GetParentControl().GetChildren()[0].GetChildren()[0].GetChildren()[1].GetChildren()[0].GetChildren()[0]\
                .GetChildren()[0].GetChildren()[0].Name
        #读取最后一条消息
        last_msg = wx.ListControl(Name="消息").GetChildren()[-1].Name
        print("读取最后一条消息:",last_msg)
        #判断是否来自于群聊
        qun = check_qun()
        wx.ButtonControl(Name="聊天信息").Click(simulateMove=False)
        '''if qun:
            if "@" + my_name not in last_msg:
                print("没艾特我，没我事")
                continue
            else:
                #re.sub("\@{}".format(my_name),"",last_msg)
                temp = "@" + my_name
                last_msg = last_msg.replace(temp, "")
                last_msg = re.sub("\W+","",last_msg)
                print(last_msg)'''
        #如果是群聊
        if qun:
            if not ated:
                print("no at")
                hw.TextControl(Name="文件传输助手").Click(simulateMove=False)
                continue
            elif ated:
                print("in")
                try:
                    last_msg = last_msg.split("\u2005")[1]#提取用户本身说的话
                    if len(last_msg) == 0:
                        reply = "别光at我呀，如果有不会使用的地方，请您看一下教程提示哦~"
                except IndexError:
                    reply = "别光at我呀，如果有不会使用的地方，请您看一下教程提示哦~"
            

        #判断关键字
        #先判断是否关闭
        reply = None
        try: #防止没关先开
            if last_msg == "开启机器人" or last_msg == "打开机器人":
                close_robot.remove(user_name)
                print(user_name, close_robot)
                wx.SendKeys(random.choice(["我回来啦！","I'm here","哈喽","本尊驾到"]))
                wx.SendKeys("{Enter}",waitTime=0)
                continue
            elif last_msg == "关闭机器人" or last_msg == "机器人闭嘴":
                if user_name in close_robot:
                    pass
                close_robot.append(user_name)
                wx.SendKeys(random.choice(["bye","待会见","聊完记得叫我","拜拜~"]))
                wx.SendKeys("{Enter}",waitTime=0)
        except:
            pass
        
        ###开始判断输入的信息

        #载入并判断机器人黑名单
        if user_name in close_robot:
            continue
            
        #教程被触发
        elif user_name not in help_finished.keys():
            print("教程机制启动")
            '''help_text_ok = help_text.split("/n")
            o = 0
            for i in help_text_ok:
                wx.SendKeys(help_text_ok[o],waitTime=0) 
                wx.SendKeys("{Shift}{Enter}",waitTime=0)
                o += 1'''
            split_enter(help_text)
            wx.SendKeys("{Enter}",waitTime=0)
            help_finished[user_name] = True
            wx.SendKeys("九九每日金句：{}".format(day_sentence))
            enter()
            wx.SendKeys("主人干什么去了：{}".format(master_doing))
            enter()
            wx.SendKeys("当前挂载模型:{}".format(ai_model_name))
            #hw.TextControl(Name="文件传输助手").Click(simulateMove=False)
            sender()
            continue

        #留言系统
        elif last_msg[:3] == "留言：" or last_msg[:3] == "留言:" or last_msg[:3] == "yly" or last_msg[:2] == "留言":
            print("留言机制启动")
            reply = random.choice(["好的，主人会收到的","直接一手传达给主人"])
            wx.SendKeys(reply)
            wx.SendKeys("{Enter}",waitTime=0)
            hw.TextControl(Name="文件传输助手").Click(simulateMove=False)
            wx.SendKeys(str(user_name)+" 给您留言了: "+str(last_msg[3:]))
            wx.SendKeys("{Enter}",waitTime=0)
            continue
            
            #wx.TextControl(SubName=last_msg[:5]).RightClick()

        elif last_msg == "help" or last_msg == "帮助" or last_msg == "更多帮助":
            print("更多教程模块启动")
            split_enter(more_help_text)
            '''more_help_text_ok = more_help_text.split("/n")
            o = 0
            for i in more_help_text_ok:
                wx.SendKeys(more_help_text_ok[o],waitTime=0) 
                wx.SendKeys("{Shift}{Enter}",waitTime=0)
                o += 1'''
            wx.SendKeys("{Enter}",waitTime=0)
            hw.TextControl(Name="文件传输助手").Click(simulateMove=False)
            continue
    

        elif last_msg == "[动画表情]":
            reply = "就目前来讲，我还不能看懂表情"


        elif last_msg == "[图片]":
            reply = "就目前来讲，我还不能看懂图片"

        elif "[语音]" in last_msg:
            reply = "语音？完全听不懂的耶"
        
        elif "清除记忆" in last_msg or "清除上下文" in last_msg or "换话题" in last_msg or "换" and "话题" in last_msg:
            user_ai_content[user_name] = []
            user_ai_content[user_name].append({ #存储用户要发送的信息
                'role': 'system',
                'content': TIAOJIAO
            })
            reply = "喵呜~咱们换个话题吧~"

        else:
            reply = "@@@GO_TO_AI@@@"
        '''
        if not reply:
            print("没有需要回复的内容，跳过")
            continue
        '''

        #如果什么都没匹配，调用小机器人
        if not reply == "@@@GO_TO_AI@@@":
            print("要回复的内容:",reply)

        #最后判断插件
        plugin_msg = run_plugins(plugins, last_msg)
        print(plugin_msg)
        if plugin_msg:
            reply = plugin_msg[0]
            if "/n" in reply:#如果有需要换行的内容
                split_enter(reply)
            elif reply == "%Ctrl+V":
                wx.SendKeys("{Ctrl}{V}")
            else:
                wx.SendKeys(reply)
        else:
            if reply == "@@@GO_TO_AI@@@": ##如果进行ai模式的直播流传输
                get_reply(last_msg, user_name)
            elif "/n" in reply:#如果有需要换行的内容
                split_enter(reply)
            elif reply == "%Ctrl+V":
                wx.SendKeys("{Ctrl}{V}")
            else:
                wx.SendKeys(reply)
        
        wx.SendKeys("{Enter}",waitTime=0)

    #点击文件传输助手，初始化
    hw.TextControl(Name="文件传输助手").Click(simulateMove=False)


        
sys.exit()