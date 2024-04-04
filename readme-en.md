# 99 WeChat Bot

This program can automatically detect user messages and provide responses, operating fully autonomously.

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

![image-20231015091909317](file:///E:/%5C99%E4%B9%8B%E6%B2%A1%E4%BA%8B%E5%86%99%E7%9A%84%E5%B0%8F%E7%A8%8B%E5%BA%8F%5C99%E5%BE%AE%E4%BF%A1%E6%9C%BA%E5%99%A8%E4%BA%BA%5C05-github%5Ccontent%5Cimage-20231015091909317.png)

```python
more_help_text = '''
Additional tips include: 
- "天气," "今日天气," or "weather" to check the current weather.
  You can specify a location by adding a space and the location.
- "60秒," "六十秒," "day60s," or "今日新闻" to get the "每日60秒" image.
'''
```

This is the content that will be displayed when a user sends the "help" command to the bot.

### Plugins

Place the plugins you want to write into the `plugin` folder. The file name is the plugin name, and the file type is `.py`.

Each plugin must have the **following parts**:

- `main` function, with arbitrary formal parameters, but there must be only one
- `if` statement to determine the content of the formal variable
- The return value of the `main` function, which is the content finally output to WeChat

Here is an example program:

```python
def main(msg):
    if msg == "插件测试":
        return "欢迎使用此插件"
```

The execution order of plugins is determined by the file name. If the detection words of two plugins overlap, the program will take the return value of the first imported (i.e., the plugin with the file name earlier).

Plugins can contain any number of functions, classes, variables, but must **have a `main` function and this function must have a return value**, otherwise the plugin you write will be invalid.

You can refer to the sample plugins in the `plugin` folder.

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

This project is licensed under the [MIT License](https://chat.openai.com/c/LICENSE).  I don't want this program to be commercial. If you want to use this code for commercial purposes, please contact me
3013907412@qq.com
thanks

# We hope this program continues to improve, and we look forward to your contributions! Thank you.