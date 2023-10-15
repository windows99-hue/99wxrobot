#coding:utf-8
import pandas as pd
import numpy as np
from uiautomation import WindowControl, MenuControl
import requests
import keyboard
import sys
import random
import re
import time
import os
import json


#导入插件
plugin_path = "./plugin/"
from plugin import weather99
#import plugin.sentences99
from plugin.sentences99 import *
from plugin import sec60



wx = WindowControl(Name="微信")
print(wx)
exit_status = False
my_name = "jiu99"
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
没东西呢
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
            #sys.exit()
            os._exit(0)

#检查是不是群聊
def check_qun():
    wx2 = WindowControl(Name="聊天信息")
    lists = wx2.ListControl(Name="聊天成员").GetChildren()
    if len(lists) >= 3:
        return True
    else:
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
    o = 0
    for i in help_text_ok:
        wx.SendKeys(help_text_ok[o],waitTime=0) 
        wx.SendKeys("{Shift}{Enter}",waitTime=0)
        o += 1

def sender():#发送并返回文件传输助手
    wx.SendKeys("{Enter}",waitTime=0)
    hw.TextControl(Name="文件传输助手").Click(simulateMove=False)

#封装回车函数
def enter():
    wx.SendKeys("{Enter}",waitTime=0)
#封装换行函数
def shiftenter():
    wx.SendKeys("{Shift}{Enter}",waitTime=0)

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

print("Copyright: © 2023, windows99-hue. All rights reserved.")
print("欢迎使用99微信机器人, 运行过程中按下退格键(backspace)可以结束程序, 祝您使用愉快")
print("监听已开始。。。")
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
        
        else:
            reply = get_reply(last_msg)
        '''
        if not reply:
            print("没有需要回复的内容，跳过")
            continue
        '''

        #如果什么都没匹配，调用小机器人
        print("要回复的内容:",reply)
        wx.SendKeys(reply)
        wx.SendKeys("{Enter}",waitTime=0)
        #wx.TextControl(SubName=last_msg[:5]).RightClick()

    #点击文件传输助手，初始化
    hw.TextControl(Name="文件传输助手").Click(simulateMove=False)


        
sys.exit()
