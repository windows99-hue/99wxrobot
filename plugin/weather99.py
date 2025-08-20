import requests
import re

def show_weather(location):

    #声明变量
    api_key = "a4ad74ca6ccf4dd1985d34cae909e303"
    city_name = location

    find_weather = "https://geoapi.qweather.com/v2/city/lookup?location={}&key={}".format(city_name,api_key)

    #查找地方
    weather_name_raw = requests.get(find_weather)

    weather_name_json = weather_name_raw.json()
    if weather_name_json["code"] != "200":
        print(weather_name_json)
        return "请求状态码为：{}，如果为404，请确定您输入的城市没错，如果为其他，请给主人留言，谢谢".format(weather_name_json["code"])

    weather_name = weather_name_json["location"][0]["id"]



    weather_url = "https://devapi.qweather.com/v7/weather/now?location={}&key={}".format(weather_name,api_key)

    weather = requests.get(weather_url)

    # 检查响应状态码
    if weather.status_code == 200:
        data = weather.json()
        
        # 提取所需的天气信息
        if data['code'] == '200':
            weather_now = data['now']
            obs_time = weather_now['obsTime']
            temperature = weather_now['temp']
            feels_like = weather_now['feelsLike']
            weather_text = weather_now['text']
            wind_direction = weather_now['windDir']
            wind_speed = weather_now['windSpeed']
            humidity = weather_now['humidity']
            precipitation = weather_now['precip']
            pressure = weather_now['pressure']
            visibility = weather_now['vis']
            cloud_cover = weather_now['cloud']
            dew_point = weather_now['dew']
            

            '''print(f'观测时间：{obs_time}')
            print(f'温度：{temperature}°C')
            print(f'体感温度：{feels_like}°C')
            print(f'天气：{weather_text}')
            print(f'风向：{wind_direction}')
            print(f'风速：{wind_speed} m/s')
            print(f'湿度：{humidity}%')
            print(f'降水量：{precipitation} mm')
            print(f'气压：{pressure} hPa')
            print(f'能见度：{visibility} km')
            print(f'云量：{cloud_cover}')
            print(f'露点温度：{dew_point}°C')'''

            result = f'''
{location}天气：/n
观测时间：{obs_time} /n
温度：{temperature}°C /n
体感温度：{feels_like}°C /n
天气：{weather_text} /n
风向：{wind_direction} /n
风速：{wind_speed} m/s /n
湿度：{humidity}% /n
降水量：{precipitation} mm /n
气压：{pressure} hPa /n
能见度：{visibility} km /n
云量：{cloud_cover} /n
露点温度：{dew_point}°C /n
'''
            return result

        else:
            return 'SystemError:无法获取天气信息，请检查API密钥和城市ID是否正确。请尽快上报给主人。'
    else:
        return '请求失败，HTTP响应状态码不为200。为{}，请尽快上报给主人'.format(data["code"])

def main(last_msg):
    #调用天气插件
    city = extract_city_from_weather_request(last_msg)
    
    if city:
        if city == "今日":
            return show_weather("滨海新区")
        return show_weather(city)
    
def is_weather_request(message):
    """判断是否是天气请求"""
    if not message:
        return False
    
    # 支持的关键词（有空格和无空格）
    weather_patterns = [
        r'今日天气', r'天气', r'weather',
        r'.*天气$',   # 以"天气"结尾，如"天津天气"
        r'^天气.*',   # 以"天气"开头，如"天气天津"（不太常见但可能）
    ]
    
    return any(re.search(pattern, message) for pattern in weather_patterns)

def extract_city_from_weather_request(message):
    """
    从天气请求中提取城市名称
    支持格式：
    1. "今日天气 天津" -> 天津
    2. "天气 北京" -> 北京  
    3. "weather beijing" -> beijing
    4. "天津天气" -> 天津
    5. "北京今日天气" -> 北京
    6. "上海weather" -> 上海
    """
    # 移除首尾空格
    message = message.strip()

    if message == "天气" or message == "weather":
        return "滨海新区"
    
    # 方法1：有空格的情况（优先处理）
    if ' ' in message:
        parts = message.split()
        if len(parts) >= 2:
            # 格式: "关键词 城市"
            if parts[0] in ["今日天气", "天气", "weather"]:
                return parts[1]
            # 格式: "城市 关键词"  
            elif parts[1] in ["今日天气", "天气", "weather"]:
                return parts[0]
    
    # 方法2：无空格的情况（使用正则表达式）
    # 匹配模式：城市名称 + 天气关键词
    patterns = [
        r'^(.+?)今日天气$',    # 北京今日天气
        r'^(.+?)天气$',        # 天津天气
        r'^(.+?)weather$',     # beijingweather
        r'^今日天气(.+?)$',    # 今日天气北京（不太常见）
        r'^天气(.+?)$',        # 天气天津（不太常见）
        r'^weather(.+?)$',     # weatherbeijing（不太常见）
    ]
    
    for pattern in patterns:
        match = re.match(pattern, message)
        if match:
            return match.group(1).strip()
    
    # 方法3：尝试提取可能的中文城市名称
    # 假设城市名称是2-4个中文字符
    chinese_city_match = re.search(r'^([\u4e00-\u9fff]{2,4})', message)
    if chinese_city_match and any(kw in message for kw in ["天气", "今日天气"]):
        return chinese_city_match.group(1)
    
    return None

if __name__ == "__main__":
    print("此脚本为天气插件，需要与主程序配套使用")