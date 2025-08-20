# 99 WeChat Bot

This program can automatically detect user messages and provide responses, operating fully autonomously.

[Video Demo](https://www.bilibili.com/video/BV1zH4y1R73R/)

## Installation

Download the source code or clone this repository.

Then, install the required libraries:

```bash
pip install -r requirements.txt
```

<span style="color: red;">Attention：</span>If you believe this installation might conflict with libraries you already have installed, I recommend creating a virtual environment. [Tutorial here](https://chat.openai.com/c/venv.md).

## Usage

### Running the Project:

```bash
python main-normal.py
```

Please execute this command in your terminal. 99 WeChat Bot is a command-line program, so it's recommended to run it in a terminal. Configure your bot according to your preferences, and press the Backspace key to close the bot.

### About `main-api-model-stream.py`

This version implements streaming transmission of AI-generated text from the LLM API to WeChat. For security, 99wxrobot2.0 uses environment variables to store the `apikey`.

Before use, please follow these steps:

1. In Windows systems, run the following command in `CMD`, replacing `YOUR_API_KEY` with your actual API key (usually starting with `sk-`):

shell

```
setx API_API_KEY "YOUR_API_KEY"
```

1. Open a new `CMD` or restart your editor for the environment variables to take effect.
2. Run:

shell

```
python main-api-model-stream.py
```

The program should work automatically.

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

![image-20231015091909317](https://github.com/windows99-hue/99wxrobot/blob/master/content/image-20231015091909317.png?raw=true)

```python
more_help_text = '''
Additional tips include: 
- "天气," "今日天气," or "weather" to check the current weather.
  You can specify a location by adding a space and the location.
- "60秒," "六十秒," "day60s," or "今日新闻" to get the "每日60秒" image.
'''
```

This is the content that will be displayed when a user sends the "help" command to the bot.

```python
def get_reply(keyword):
    try:
        url = f"https://open.drea.cc/bbsapi/chat/get?keyWord={keyword}&userName=type%3Dbbs"
        res = requests.get(url)
        data = res.json()
        return data['data']['reply']
    except:
        return "Oops, I'm still quite笨 (dumb), not sure what you're saying"
```

This function generates the dialogue for the AI robot. You can redefine it yourself, as long as it returns what to say at the end.

The `reply` variable is the content to respond with, which can be modified in the main loop of the program.

Please **change** the `my_name` variable in the program to your WeChat name, **not** your WeChat ID.

In the **streaming transmission version**, the variable `TIAOJIAO` is the identity setting of the LLM, which you can change as needed.

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

`main-normal.py` is the normal version.

`main-api-model-stream.py` can access deepseek's API from Alibaba Cloud Bailian (theoretically any AI can be used), modify the content transmission method to streaming transmission, improve response speed, and convert emojis to WeChat expressions. The `NEED_THINK` constant determines whether the model you are using requires deep thinking. This is the version I am currently using.

## Features

### Advantages

- Fully automated handling of WeChat messages.
- Uses Microsoft's GUI control library, reducing the risk of being banned.
- Extremely fast message processing without image recognition, ensuring stealthy user information retrieval.
- Supports the attachment of plugins.

### Disadvantages

- Does not support mouse and keyboard control during use.You can try using a virtual machine.

## License

This project is licensed under the [GPLv3 License](LICENSE).  I don't want this program to be commercial. If you want to use this code for commercial purposes, please contact me
3013907412@qq.com
thanks

# We hope this program continues to improve, and we look forward to your contributions! Thank you.
