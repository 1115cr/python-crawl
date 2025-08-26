import time
import requests
from lxml import etree
import os
from os.path import exists
import random
from tqdm import tqdm

session = requests.session()

def get_prosy_userAgent():
    user_agent_list = [
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
    proxy_list = [
        {"http": "58.216.109.17:800"},
        {"http": "113.118.159.77:9000"},
        {"http": "39.105.27.30:3128"},
        {"http": "117.86.6.34:1080"},
        {"http": "8.146.209.239:3128"},
        {"http": "8.219.97.248:80"},
        {"http": "222.59.173.105:45108"},
        {"http": "47.96.42.36:80"},
        {"http": "222.59.173.105:45122"},
        {"http": "222.59.173.105:45023"},
        {"http": "180.103.19.163:1080"},
        {"http": "8.146.207.243:8888"},
        {"http": "120.26.123.95:8010"},
        {"http": "222.59.173.105:45085"},
        {"http": "119.3.113.150:9094"},
        {"http": "47.96.42.36:80"},
        {"http": "121.230.8.25:1080"},
        {"http": "222.59.173.105:45105"},
        {"http": "36.138.53.26:10017"},
        {"http": "103.115.20.71:8181"},
        {"http": "222.59.173.105:45250"},
        {"http": "58.216.109.14:800"},
        {"http": "222.59.173.105:45115"},
        {"http": "49.65.124.192:3128"},
        {"http": "123.128.12.93:9050"},
        {"http": "222.59.173.105:45090"},
        {"http": "121.43.150.231:3128"},
        {"http": "47.243.92.199:3128"},
        {"http": "222.59.173.105:45035"},
        {"http": "36.139.22.230:3128"},
        {"http": "120.26.123.95:8010"},
        {"http": "222.59.173.105:45088"},
        {"http": "222.59.173.105:45058"},
        {"http": "115.231.181.40:8128"},
        {"http": "222.59.173.105:45124"},
        {"http": "222.59.173.105:45026"},
    ]

    userAgent = random.choice(user_agent_list)
    proxy = random.choice(proxy_list)

    headers = {
        "referer": "https://www.bqg128.com/",
        "user-agent": userAgent
    }
    return headers, proxy

def get_content(url, title):
    for index in tqdm(range(len(url))):
        headers, proxy = get_prosy_userAgent()

        response2 = session.get(url[index], headers=headers, proxies=proxy)

        content_page = etree.HTML(response2.text)
        content = content_page.xpath('//*[@id="content"]/p/text()')
        if content and content[-1] and ('本小章还未完' in content[-1] or '请点击下一页继续阅读' in content[-1]):
            content.pop()

        # 新增逻辑：如果content的第二个元素中包含'－－－－'符号，删除第一和第二个元素
        if len(content) >= 2 and '－－' in content[1]:
            content = content[2:]  # 删除前两个元素，保留从第三个开始的所有元素

        with open('小说/蛊真人.txt', 'a', encoding='utf-8') as file1:
            file1.write(title[index])
            file1.write('\n')
            file1.write('\n'.join(content))
            file1.write('\n\n')


if __name__ == '__main__':
    if not exists('./小说'):
        os.mkdir('小说')

    headers, proxy = get_prosy_userAgent()

    basic_url = "https://www.biqugequ.org"
    first_url = "https://www.biqugequ.org/xs_1588/"

    response = session.get(first_url, headers=headers, proxies=proxy)
    print('抓取页面完成')

    page = etree.HTML(response.text)
    title = page.xpath('//*[@id="list"]/dl/dd/a/@title')
    url_list = page.xpath('//*[@id="list"]/dl/dd/a/@href')
    print('开始抓取小说标题和链接')

    url = []
    for index in range(len(url_list)):
        url.append(basic_url + url_list[index])
    print('开始抓取小说内容')

    get_content(url, title)
    print('小说抓取完成')
