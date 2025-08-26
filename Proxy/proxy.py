"""
代理IP获取和验证模块

该模块用于从快代理网站获取免费代理IP，并通过ping测试验证其可用性。
提供对外接口供其他模块调用有效的代理IP列表。
"""

import requests
import re
import os
import time
import json
import random
import subprocess as sp
from tqdm import tqdm
from datetime import datetime


# 用户代理列表，用于模拟不同浏览器访问
USER_AGENT_LIST = [
    # Mac
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',

    # Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.2739.54',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.2739.63',
    # 2024.09
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.2739.67',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.2739.79',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.2792.52',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.2792.65',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.2792.79',
    # 2024.10
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.2792.89',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.2849.46',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.2849.52',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.225 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.86 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.161 Safari/537.36',
    # 2024.02
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.185 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.58 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.70 Safari/537.36',
]


def check_ip_connectivity(ip_address, lose_pattern, time_pattern):
    """
    检查IP地址的网络连通性

    Args:
        ip_address (str): 要测试的IP地址
        lose_pattern: 用于匹配丢包数的正则表达式对象
        time_pattern: 用于匹配平均响应时间的正则表达式对象

    Returns:
        int: 平均响应时间(毫秒)，如果超时返回1000
    """
    # 命令 -n 要发送的回显请求数 -w 等待每次回复的超时时间(毫秒)
    cmd = "ping -n 3 -w 3 %s"
    # 执行命令
    process = sp.Popen(cmd % ip_address, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    # 获得返回结果并解码
    output = process.stdout.read().decode("gbk")
    # 丢包数
    lose_matches = lose_pattern.findall(output)
    # 当匹配到丢失包信息失败,默认为三次请求全部丢包,丢包数lose赋值为3
    if len(lose_matches) == 0:
        lose_count = 3
    else:
        lose_count = int(lose_matches[0])
    # 如果丢包数目大于2个,则认为连接超时,返回平均耗时1000ms
    if lose_count > 2:
        # 返回False
        return 1000
    # 如果丢包数目小于等于2个,获取平均耗时的时间
    else:
        # 平均时间
        time_matches = time_pattern.findall(output)
        # 当匹配耗时时间信息失败,默认三次请求严重超时,返回平均好使1000ms
        if len(time_matches) == 0:
            return 1000
        else:
            #
            average_time = int(time_matches[0])
            # 返回平均耗时
            return average_time


def init_regex_patterns():
    """
    初始化正则表达式模式

    Returns:
        tuple: (丢包数匹配模式, 平均时间匹配模式)
    """
    # 匹配丢包数
    lose_time_pattern = re.compile(u"丢失 = (\d+)", re.IGNORECASE)
    # 匹配平均时间
    waste_time_pattern = re.compile(u"平均 = (\d+)ms", re.IGNORECASE)
    return lose_time_pattern, waste_time_pattern


def fetch_proxy_data():
    """
    从快代理网站获取代理IP数据

    Returns:
        list: 代理IP字典列表，格式如 [{'http': 'ip:port'}, ...]
    """
    # 随机选择用户代理
    selected_user_agent = random.choice(USER_AGENT_LIST)

    session = requests.session()

    headers = {
        'user-agent': selected_user_agent,
    }

    # 初始化返回数据列表
    proxy_data = []

    try:
        for page_num in tqdm(range(1, 5), desc="获取代理IP"):
            # 发送请求并解析数据 - 修正URL格式并添加延时避免反爬
            url = f'https://www.kuaidaili.com/free/inha/{page_num}/'  # 更正为正确的URL格式

            response = session.get(url, headers=headers)
            page_content = response.text

            # 更新正则表达式以匹配实际页面结构
            data_list = re.findall('const fpsList = (.*?);', page_content, re.S)

            if data_list:
                proxy_ip_list = re.findall('"ip": "(.*?)"', data_list[0], re.S)
                proxy_port_list = re.findall('"port": "(.*?)"', data_list[0], re.S)

                # 组装代理数据
                if len(proxy_ip_list) == len(proxy_port_list):
                    for index in range(len(proxy_ip_list)):
                        proxy_dict = {
                            'http': proxy_ip_list[index] + ':' + proxy_port_list[index]
                        }
                        proxy_data.append(proxy_dict)

            # 添加延时避免请求过快被封
            time.sleep(1)

        return proxy_data

    except Exception as e:
        print(f"获取代理数据时出错: {e}")
        return proxy_data


def get_valid_proxies():
    """
    获取有效的代理IP列表

    Returns:
        list: 可用的代理IP列表，格式如 [{'http': 'ip:port'}, ...]
    """
    # 初始化正则表达式
    lose_time_pattern, waste_time_pattern = init_regex_patterns()
    proxy_data = fetch_proxy_data()

    # 创建一个新的列表存储有效IP，避免在迭代时修改原列表
    valid_proxies = []

    print("正在检测代理IP可用性...")
    for proxy_item in proxy_data:
        # 从代理字典中提取IP地址进行测试
        ip_address = list(proxy_item.values())[0].split(':')[0]
        average_time = check_ip_connectivity(ip_address, lose_time_pattern, waste_time_pattern)

        if average_time <= 200:
            valid_proxies.append(proxy_item)
            print(f"{proxy_item} 连接正常!")
        else:
            print(f"{proxy_item} 连接超时, 已移除!")

    # 将有效的代理IP写入代理目录下以当天日期命名的文件中
    if valid_proxies:
        # 确保代理目录存在
        proxy_dir = "代理"
        if not os.path.exists(proxy_dir):
            os.makedirs(proxy_dir)

        # 获取当前日期作为文件名
        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f"{current_date}.py"
        full_path = os.path.join(proxy_dir, filename)

        # 写入文件
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write("proxy_list = [\n")
            for proxy in valid_proxies:
                f.write(f"    {json.dumps(proxy, ensure_ascii=False)},\n")
            f.write("]\n")

        print(f"有效代理IP已保存到 {full_path}")

    return valid_proxies


if __name__ == "__main__":
    # 当直接运行此脚本时执行
    valid_proxies = get_valid_proxies()
    print("\n可用的代理IP:")
    for proxy in valid_proxies:
        print(proxy)
