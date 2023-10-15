# 99 WeChat Bot
## [中文版](https://github.com/windows99-hue/99wxrobot/blob/main/readme.md)

This program can automatically detect user messages and provide responses, operating fully autonomously.
[Video](https://www.bilibili.com/video/BV1zH4y1R73R/)

## Installation

Download the source code or clone this repository.

Then, install the required libraries:

```bash
pip install -r requirements.txt
```

<span style="color: red;">Attention：</span>If you believe this installation might conflict with libraries you already have installed, I recommend creating a virtual environment. [Tutorial here](https://chat.openai.com/c/venv.md).

## Usage

### Running the Project:

```
bashCopy code
python main-normal.py
```

Please execute this command in your terminal. 99 WeChat Bot is a command-line program, so it's recommended to run it in a terminal. Configure your bot according to your preferences, and press the Backspace key to close the bot.
### Please make sure to keep WeChat at the top when using it. When using it, you need to have the file transfer assistant display in the conversation box. I suggest you set it to the top.

### Customizing the Bot

```python
help_text = ''' 
Hello there! The master is currently away, and I'm here to take over. 😊
To leave a message for the master, simply prefix your message with "留言:" or "yly".
Your message will be sent directly to the master's phone.
To turn the bot on or off, simply type "关闭" or "打开" (close/open).
You can also type "帮助" or "help" to access more usage instructions.
Feel free to chat with me directly!
Wishing you a wonderful day! 😄
'''
```

The `help_text` variable is the response when the bot receives its first message.
<span style="color: red;">Note:</span>Please enter `/n` at the line break. This is not an incorrect line break, but a parsing symbol for program specific line breaks.

![img01](https://github.com/windows99-hue/99wxrobot/blob/main/content/image-20231015091909317.png)

```python
more_help_text = '''
Additional tips include: 
- "天气," "今日天气," or "weather" to check the current weather.
  You can specify a location by adding a space and the location.
- "60秒," "六十秒," "day60s," or "今日新闻" to get the "每日60秒" image.
'''
```

This is the content that will be displayed when a user sends the "help" command to the bot.


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

This function is the dialogue generation of AI robots, and you can redefine it yourself as long as you return the desired message in the end
The `reply` variable is the content to be answered and can be changed in the main loop of the program

### Plugins

To add your own plugins, place them in the "plugin" folder and import them into the main file. In the loop where unread messages are checked, add `elif` statements to handle different messages. The `last_msg` variable holds the user's last message, which you can use to formulate responses.

### Version Information

- `main-v0.5.py` is the initial version of the bot but contains numerous bugs. It is not recommended for modification or use.
- `main-low.py` is a historical version that did not handle `@` requests correctly.
- `main-v1.5.py` is a historical version that correctly handled `@` requests and is lightweight and customizable.
- `main-normal.py` is the current and highly functional version of the bot.

## Features

### Advantages

- Fully automated handling of WeChat messages.
- Uses Microsoft's GUI control library, reducing the risk of being banned.
- Extremely fast message processing without image recognition, ensuring stealthy user information retrieval.
- Supports the attachment of plugins.

### Disadvantages

- Does not support mouse and keyboard control during use.
- Lacks context awareness.

## License

This project is licensed under the [MIT License](https://chat.openai.com/c/LICENSE). 
I don't want this program to be commercial. If you want to use this code for commercial purposes, please contact me
3013907412@qq.com
thanks

# We hope this program continues to improve, and we look forward to your contributions! Thank you.
