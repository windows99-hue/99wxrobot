#coding:utf-8
from uiautomation import WindowControl, MenuControl
import requests
import keyboard
import sys
import random
import os
import importlib.util
from plugin.sentences99 import *
from clc99 import print_status as ps
from clc99 import *
import re

print_notrun("Copyright: © 2025, windows99-hue. All rights reserved.")

#导入插件
plugin_path = "./plugin/"

exit_status = False
my_name = "jy9999999999" #请修改为您的微信名称
#创建教程完毕的字典，防止重复教程
help_finished = {}
close_robot = []
#初始提示
help_text = ''' 
你好呀，主人现在不在，由我接管啦~/n
在您要说的话前面输入  留言:  或  yly /n
就可以给主人留言啦，信息会直接发送到主人手机 /n
输入 关闭/打开机器人 可以关开我 /n
输入 帮助 或 help 可以查看更多使用教程哦 /n
直接跟我说话就可以和我聊天啦/n
祝你天天开心~[呲牙]
    '''

#更多教程提示
more_help_text = '''
更多提示如下：/n
天气/今日天气/weather 可以查看今日天气 /n
用空格分隔加地点可以指定地点 /n
/n
/n
输入 60秒/六十秒 或 day60s 或 今日新闻 可以获取 每日60秒图片
'''

#非用户列表
unuser = ["公众号","微信运动","微信团队","微信支付","服务号","微信游戏","服务通知"]

unread_pattern = r'\s\d+条未读\s'
unnotice_pattern = r'\s\d{2}:\d{2}消息免打扰'

def start_wx():
    global wx
    try:
        wx = WindowControl(Name="微信")
        wx.SetFocus()
    except:
        print_error("没有成功获取到微信窗口，请确定窗口已打开且没有被最小化，按Y重试")
        keyboard.wait("Y")
        ps("try again!")
        start_wx()
    else:
        print_good("成功获取:",wx)

start_wx()


#小机器人
def get_reply(keyword):
    try:
        url = f"https://open.drea.cc/bbsapi/chat/get?keyWord={keyword}&userName=type%3Dbbs"
        res = requests.get(url)
        data = res.json()
        return data['data']['reply']
    except:
        return "opps, 我还很笨，不造你在说啥"
    
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
    ps("执行插件")
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
            print_warning("收到f8信号，程序退出。。")
            keyboard.unhook_all()
            exit_status = True
            #sys.exit()
            os._exit(0)

#检查是不是群聊
def check_qun():
    time.sleep(0.1)
    try:
        chat_infomation = wx.GetChildren()[0].GetChildren()[0].GetChildren()[0]\
        .GetChildren()[2].GetChildren()[1].GetChildren()[0].\
        GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[1].GetChildren()[1].GetChildren()[0].\
        GetChildren()[0].GetChildren()[0].GetChildren()[0]
    except IndexError:
        return True
    return False
    
    
    
#检测会话控件内是否存在被at的提示
def check_at():
    check_at_list = hw.GetChildren()
    for at_text in check_at_list:
        if "[有人@我]" in at_text.Name.split():
            return at_text
        
def split_enter(context):#切分/n并逐步手动换行
    help_text_ok = context.split("/n")
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
    filehelper.Click(simulateMove=False)
    
#切换窗口(置顶)
#wx.SwitchToThisWindow()
#寻找会话控件绑定
hw = wx.ListControl(Name="会话")
print_good("查找到‘会话’控件：",hw)

get_filehelper = False
for filehelper in hw.GetChildren():
    name = filehelper.Name.split(" ")[0]
    if name == "文件传输助手":
        get_filehelper = True
        print_good("找到文件传输助手:",filehelper)
        break

if not get_filehelper:
    print_error("没有找到文件传输助手，请确定它显示在左侧会话框中，我建议您把它置顶。")
    sys.exit(1)

try:
    filehelper.Click(simulateMove=False)
except:
    print_error("无法切换至文件传输助手，请确定它显示在左侧会话框中，我建议您把它置顶。")
    sys.exit()

keyboard.on_press(exit_for_keyboard)#监听是否按下f8

#加载插件
plugins = load_plugins()
print_good("插件加载完成！")

print_ok("欢迎使用99微信机器人, 运行过程中按下f8可以结束程序, 祝您使用愉快")
print_good("监听已开始。。。")

#死循环查找消息
while not exit_status:
    ated = False
    newmessage = None

    while True:
        #查找未读消息
        we = hw.GetChildren()
        get_new_message = False
        for i in we:
            if re.search(unread_pattern, i.Name):
                get_new_message = True
                newmessage = i
                at_text = check_at()
                if at_text:
                    ated = True
                break
        if get_new_message: break
    #存在未读消息
    if ated or newmessage:
        #ps(ated)
        #点击未读消息
        if ated:
            we = at_text
        else:
            we = newmessage
        ps("发现未读消息:",we.Name)
        we.Click(simulateMove=False)
        #读取当前聊天人的名字（扒控件累死我了）
        try:
            user_name = wx.GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[2].GetChildren()[1].GetChildren()[0].\
            GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[1].GetChildren()[1].GetChildren()[0].GetChildren()[0].\
            GetChildren()[0].GetChildren()[0].Name
        except:
            ps("非正常用户，跳过")
            filehelper.Click(simulateMove=False)
            continue

        if re.search(unnotice_pattern, we.Name):
            ps("免打扰用户")
            if we.Name not in close_robot:
                ps("加入黑名单")
                close_robot.append(user_name)
                filehelper.Click(simulateMove=False)
                continue

        chat_info_button = wx.ButtonControl(Name="聊天信息")
        chat_info_button.Click(simulateMove=False)
        #读取最后一条消息
        last_msg = wx.ListControl(Name="消息").GetChildren()[-1].Name
        last_msg = last_msg[:-2] #去除微信4.0的末尾换行符
        ps("读取最后一条消息:",last_msg)
        #判断是否来自于群聊
        qun = check_qun()
        chat_info_button.Click(simulateMove=False)
        #如果是群聊
        if qun:
            if not ated:
                ps("没at我，没我事")
                filehelper.Click(simulateMove=False)
                continue
            elif ated:
                try:
                    # 使用正则表达式移除所有@jiu99（可以根据实际机器人ID调整）
                    cleaned_msg = re.sub(r'@{}\s*'.format(my_name), '', last_msg).strip()
                    
                    if len(cleaned_msg) == 0:
                        reply = "别光at我呀，如果有不会使用的地方，请您看一下教程提示哦~"
                    else:
                        last_msg = cleaned_msg
                except Exception as e:
                    reply = "别光at我呀，如果有不会使用的地方，请您看一下教程提示哦~"            

        #判断关键字
        #先判断是否关闭
        reply = None

        input_area = wx.EditControl(Name=user_name)
        input_area.Click(simulateMove=False)

        try: #防止没关先开
            if last_msg == "开启机器人" or last_msg == "打开机器人":
                close_robot.remove(user_name)
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
            filehelper.Click(simulateMove=False)
            continue
            
        #教程被触发
        elif user_name not in help_finished.keys():
            print_good("教程机制启动")
            split_enter(help_text)
            wx.SendKeys("{Enter}",waitTime=0)
            help_finished[user_name] = True
            wx.SendKeys("九九每日金句：{}".format(day_sentence))
            enter()
            wx.SendKeys("主人干什么去了：{}".format(master_doing))
            sender()
            continue

        #留言系统
        elif last_msg[:3] == "留言：" or last_msg[:3] == "留言:" or last_msg[:3] == "yly" or last_msg[:2] == "留言":
            print_good("留言机制启动")
            reply = random.choice(["好的，主人会收到的","直接一手传达给主人"])
            wx.SendKeys(reply)
            wx.SendKeys("{Enter}",waitTime=0)
            filehelper.Click(simulateMove=False)
            wx.SendKeys(str(user_name)+" 给您留言了: "+str(last_msg[3:]))
            wx.SendKeys("{Enter}",waitTime=0)
            continue

        elif last_msg == "help" or last_msg == "帮助" or last_msg == "更多帮助":
            print_good("更多教程模块启动")
            split_enter(more_help_text)
            wx.SendKeys("{Enter}",waitTime=0)
            filehelper.Click(simulateMove=False)
            continue
    

        elif last_msg == "动画表":
            reply = "就目前来讲，我还不能看懂表情"


        elif last_msg == "图片":
            reply = "就目前来讲，我还不能看懂图片"

        elif "语音" in last_msg:
            reply = "语音？完全听不懂的耶"
        
        else:
            reply = get_reply(last_msg)

        #最后判断插件
        plugin_msg = run_plugins(plugins, last_msg)
        if plugin_msg:
            reply = plugin_msg[0]
            if "/n" in reply:#如果有需要换行的内容
                split_enter(reply)
            elif reply == "%Ctrl+V":
                wx.SendKeys("{Ctrl}{V}")
            else:
                wx.SendKeys(reply)
        else:
            if "/n" in reply:#如果有需要换行的内容
                split_enter(reply)
            elif reply == "%Ctrl+V":
                wx.SendKeys("{Ctrl}{V}")
            else:
                wx.SendKeys(reply)
        
        wx.SendKeys("{Enter}",waitTime=0)

        #如果什么都没匹配，调用小机器人
        ps("要回复的内容:",reply)

    #点击文件传输助手，初始化
    filehelper.Click(simulateMove=False)


        
sys.exit()