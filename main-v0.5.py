#coding:utf-8
from uiautomation import WindowControl, MenuControl
import requests
import keyboard
import sys
import random
import re

print("Copyright: © 2024, windows99-hue. All rights reserved.")

wx = WindowControl(Name="微信")
print(wx)
exit_status = False
my_name = "jiu99"
#创建教程完毕的字典，防止重复教程
help_finished = {}
close_robot = []
help_text = \
    '''
你好呀，主人现在不在，由我接管啦~/n
在您要说的话前面输入  留言:  或  yly /n
就可以给主人留言啦，信息会直接发送到主人手机 /n
输入 关闭/打开机器人 可以关开我 /n
直接跟我说话就可以和我聊天啦/n
祝你天天开心~[呲牙]
    '''

#小机器人
def get_reply(keyword):
    try:
        url = f"https://open.drea.cc/bbsapi/chat/get?keyWord={keyword}&userName=type%3Dbbs"
        res = requests.get(url)
        data = res.json()
        return data['data']['reply']
    except:
        return "opps, 我还很笨，不造你在说啥"
    
def exit_for_keyboard(event):#退出程序事件
    global exit_status
    if event.event_type == keyboard.KEY_DOWN:
        if keyboard.is_pressed('backspace'):
            print("收到退格键信号，程序退出。。")
            keyboard.unhook_all()
            exit_status = True

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
    
    
#切换窗口(置顶)
wx.SwitchToThisWindow()
#寻找会话控件绑定
hw = wx.ListControl(Name="会话")
print("查找到‘会话’控件：",hw)
hw.TextControl(Name="文件传输助手").Click(simulateMove=False)

keyboard.on_press(exit_for_keyboard)#监听是否按下退格键
#死循环查找消息
while not exit_status:
    #查找未读消息
    we = hw.TextControl(searchDepth=4)
    while not we.Exists(0):
        pass
    print("查找未读消息:",we)
    #存在未读消息
    if we.Name:
        #点击未读消息
        we.Click(simulateMove=False)
        wx.ButtonControl(Name="聊天信息").Click(simulateMove=False)
        #读取当前聊天人的名字（扒控件累死我了）
        user_name = wx.ListControl(Name="消息").GetParentControl().GetParentControl().GetParentControl()\
            .GetParentControl().GetChildren()[0].GetChildren()[0].GetChildren()[1].GetChildren()[0].GetChildren()[0]\
                .GetChildren()[0].GetChildren()[0].Name
        #print("fdsjkahfjdeksaghcfjdsa",user_name.Name)
        #读取最后一条消息
        last_msg = wx.ListControl(Name="消息").GetChildren()[-1].Name
        print("读取最后一条消息:",last_msg)
        #判断是否来自于群聊
        qun = check_qun()
        wx.ButtonControl(Name="聊天信息").Click(simulateMove=False)
        if qun:
            if "@" + my_name not in last_msg:
                print("没艾特我，没我事")
                continue
            else:
                #re.sub("\@{}".format(my_name),"",last_msg)
                temp = "@" + my_name
                last_msg = last_msg.replace(temp, "")
                last_msg = re.sub("\W+","",last_msg)
                print(last_msg)

            #time.sleep(0.7)
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
        print(close_robot)
        if user_name in close_robot:
            continue
            

        elif user_name not in help_finished.keys():
            print("教程机制启动")
            help_text_ok = help_text.split("/n")
            o = 0
            for i in help_text_ok:
                wx.SendKeys(help_text_ok[o]) 
                wx.SendKeys("{Shift}{Enter}",waitTime=0)
                o += 1
            wx.SendKeys("{Enter}",waitTime=0)
            help_finished[user_name] = True
            continue
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

        elif last_msg == "[动画表情]":
            reply = "就目前来讲，我还不能看懂表情"


        elif last_msg == "[图片]":
            reply = "就目前来讲，我还不能看懂图片"
        else:
            reply = get_reply(last_msg)
        '''
        if not reply:
            print("没有需要回复的内容，跳过")
            continue
        '''
        print("要回复的内容:",reply)
        wx.SendKeys(reply)
        wx.SendKeys("{Enter}",waitTime=0)
        #wx.TextControl(SubName=last_msg[:5]).RightClick()

    hw.TextControl(Name="文件传输助手").Click(simulateMove=False)


        
sys.exit()