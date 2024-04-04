import requests

def show_weather(location):

    #声明变量
    api_key = "a4ad74ca6ccf4dd1985d34cae909e303"
    city_name = location

    find_weather = "https://geoapi.qweather.com/v2/city/lookup?location={}&key={}".format(city_name,api_key)

    #查找地方
    weather_name_raw = requests.get(find_weather)

    weather_name_json = weather_name_raw.json()
    if weather_name_json["code"] != "200":
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

if __name__ == "__main__":
    print("此脚本为天气插件，需要与主程序配套使用")