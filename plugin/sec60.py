import requests

from PIL import Image
#from cStringIO import StringIO
from io import BytesIO
from ctypes import *
from ctypes.wintypes import *

###感谢这位大佬的解答，谢谢！###
#https://www.coder.work/article/2418399

# 使用Pillow库打开图像
HGLOBAL = HANDLE
SIZE_T = c_size_t
GHND = 0x0042
GMEM_SHARE = 0x2000

GlobalAlloc = windll.kernel32.GlobalAlloc
GlobalAlloc.restype = HGLOBAL
GlobalAlloc.argtypes = [UINT, SIZE_T]

GlobalLock = windll.kernel32.GlobalLock
GlobalLock.restype = LPVOID
GlobalLock.argtypes = [HGLOBAL]

GlobalUnlock = windll.kernel32.GlobalUnlock
GlobalUnlock.restype = BOOL
GlobalUnlock.argtypes = [HGLOBAL]

CF_DIB = 8

OpenClipboard = windll.user32.OpenClipboard
OpenClipboard.restype = BOOL 
OpenClipboard.argtypes = [HWND]

EmptyClipboard = windll.user32.EmptyClipboard
EmptyClipboard.restype = BOOL
EmptyClipboard.argtypes = None

SetClipboardData = windll.user32.SetClipboardData
SetClipboardData.restype = HANDLE
SetClipboardData.argtypes = [UINT, HANDLE]

CloseClipboard = windll.user32.CloseClipboard
CloseClipboard.restype = BOOL
CloseClipboard.argtypes = None

#################################################

def write_image_to_clip():


    response = requests.get("https://api.03c3.cn/api/zb")
    if response.status_code == 200:
        # 读取图片数据
        image_data = response.content


        image = Image.open(BytesIO(image_data))

        #output = StringIO()
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()

        hData = GlobalAlloc(GHND | GMEM_SHARE, len(data))
        pData = GlobalLock(hData)
        memmove(pData, data, len(data))
        GlobalUnlock(hData)

        OpenClipboard(None)
        EmptyClipboard() #这一句话是清除剪切板
        SetClipboardData(CF_DIB, pData)
        CloseClipboard()

        # 关闭响应以释放资源
        response.close()

        print('图片已复制到剪贴板')
    else:
        print('请求失败，状态码：', response.status_code)




if __name__ == "__main__":
    print("此脚本为每日60秒插件，需要与主程序配套使用")
