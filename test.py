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
def start_wx():
    global wx
    try:
        wx = WindowControl(Name="微信")
    except:
        print_error("没有成功获取到微信窗口，请确定窗口已打开且没有被最小化，按Y重试")
        keyboard.wait("Y")
        ps("try again!")
        start_wx()
    else:
        print_good("成功获取:",wx)

start_wx()

user_name = wx.GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[2].GetChildren()[1].GetChildren()[0].\
        GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[1].GetChildren()[1].GetChildren()[0].GetChildren()[0].\
        GetChildren()[0].GetChildren()[0].Name
ps(user_name)