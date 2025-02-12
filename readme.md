# 99微信机器人

这个程序可以自动查找用户的消息并且做出回答，全自动操作。

[视频演示](https://www.bilibili.com/video/BV1zH4y1R73R/)

## 安装

将源代码下载下来或者clone这个仓库

然后安装必要的库

~~~bash
pip install -r requirements.txt
~~~

<span style="color: red;">注意：</span>如果您觉得这次安装可能会与您已经安装过的库冲突，我建议您创建一个虚拟环境 

虚拟环境教程：[点我](venv.md)

## 使用

### 运行项目：

~~~bash
python main-normal.py
~~~

请在终端执行这行代码，99微信机器人是一个命令行程序，因此建议您在终端执行这行代码

请根据程序配置您的机器人，按下 退格键 关闭机器人

### 自定义机器人

~~~python
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
~~~

help_text变量是机器人收到第一次发送的消息是回复的话

<span style="color: red;">注意：</span>请在换行处输入`/n` 这并不是一个错误的换行符，而是程序特有的换行操作的解析符号

![image-20231015091909317](https://github.com/windows99-hue/99wxrobot/blob/master/content/image-20231015091909317.png?raw=true)

~~~python
#更多教程提示
more_help_text = '''
更多提示如下：/n
天气/今日天气/weather 可以查看今日天气 /n
用空格分隔加地点可以指定地点 /n
/n
/n
输入 60秒/六十秒 或 day60s 或 今日新闻 可以获取 每日60秒图片
'''
~~~

这个是用户向机器人发送help时输出的内容

~~~python
#小机器人
def get_reply(keyword):
    try:
        url = f"https://open.drea.cc/bbsapi/chat/get?keyWord={keyword}&userName=type%3Dbbs"
        res = requests.get(url)
        data = res.json()
        return data['data']['reply']
    except:
        return "opps, 我还很笨，不造你在说啥"
~~~

这个函数是AI机器人的对话生成，你可以自己重新定义，只要最后返回要说的话

`reply`变量是要回答的内容，在程序的主循环里可以更改

### 插件

请把您要编写的插件放入plugin文件夹，文件名称就是插件名称，文件类型为.py

每个插件都必须**以下部分**

- `main`函数，形式参数任意，但是必须有且只有一个
- `if`判断，来判断形式变量的内容
- `main`函数的**返回值**，这是最后程序输出到微信的内容

下面是一个程序示例

~~~python
def main(msg):
    if msg == "插件测试":
        return "欢迎使用此插件"
~~~

插件的执行顺序由文件的名称先后决定，如果两个插件的判断词重复，程序会取第一个被导入（也就是文件名在前面的）的插件返回值

插件可以包含任意数量的函数，类，变量，但是必须要**存在main函数且次函数必须有返回值**，否则您编写的插件无效

您可以参考plugin文件夹中的示例插件

### 版本介绍

`main-v0.5.py` 是我最初创建的机器人，但是它bug很多，我不建议您更改或使用这个版本

`main-low.py` 是一个记录版本，它没有正确处理被at的请求

`main-v1.5.py` 是一个记录版本，这个版本正常处理了at请求，并且很轻量化，您可以自定义这个版本

`main-normal.py` 是我现在正在使用的版本，非常好用

`main-local-model.py` 可以从本地`ollama`接入deepseek(理论上任何ai都可以)

`main-api-model.py`可以从阿里云百炼接入deepseek的api(理论上任何ai都可以)

`main-api-model.py`可以从阿里云百炼接入deepseek的api(理论上任何ai都可以)，修改内容传输方式为流式传输，提升响应速度，可转换emoji为微信表情

## 特性

### 优点

- 全自动处理微信消息
- 使用了微软的gui控制库，大大降低了被封号风险
- 处理速度极快，没有图片识别，悄无声息的获取用户信息
- 可以附加插件

### 缺点

- 在使用过程中不能操控鼠标键盘
- 没有上下文功能（可自行编写）

## 许可证

该项目采用 [MIT 许可证](LICENSE)。 我并不想让这个程序商业，如果您想使用这个代码商业，请联系我

3013907412@qq.com

谢谢

# 我们希望这个程序能越来越好，我们期待你完善这个程序！谢谢