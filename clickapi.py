import time
import win32api
import win32gui
import win32con
from uiautomation import WindowControl

def leftClick(hwnd, x, y):
    lParam = win32api.MAKELONG(x, y)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam) 
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)
    time.sleep(0.1)

def rightClick(hwnd, x, y):
    lParam = win32api.MAKELONG(x, y)
    win32gui.SendMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lParam) 
    win32gui.SendMessage(hwnd, win32con.WM_RBUTTONUP, 0, lParam)
    time.sleep(0.1)

def GetInfo(wx, filer):
    wx_rect = wx.BoundingRectangle
    wx_left, wx_top, wx_right, wx_bottom = wx_rect.left, wx_rect.top, wx_rect.right, wx_rect.bottom

    # 获取文件传输助手控件的屏幕坐标
    filer_rect = filer.BoundingRectangle
    filer_left, filer_top, filer_right, filer_bottom = filer_rect.left, filer_rect.top, filer_rect.right, filer_rect.bottom

    # 计算控件相对于微信窗口的位置
    relative_left = filer_left - wx_left
    relative_top = filer_top - wx_top

    # 输出结果
    print(f"文件传输助手相对于微信窗口的位置: ({relative_left}, {relative_top})")

    # 发送点击消息
    hwnd = wx.NativeWindowHandle

    return hwnd,relative_left, relative_top

def LeftClick(wx, rect):
    hwnd, rl, rt = GetInfo(wx, rect)
    leftClick(hwnd,rl,rt)

def RightClick(wx, rect):
    hwnd, rl, rt = GetInfo(wx, rect)
    rightClick(hwnd,rl,rt)

# wx = WindowControl(Name="微信")
# hw = wx.ListControl(Name="会话")
# LeftClick(wx, hw.TextControl(Name="家"))
# bt = wx.ButtonControl(Name="聊天信息")
# print(bt)
# time.sleep(0.1)
# LeftClick(wx, bt)

#rightClick(hwnd,relative_left,relative_top)