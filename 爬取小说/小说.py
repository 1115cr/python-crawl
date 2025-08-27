import time
import requests
from lxml import etree
import os
from os.path import exists
import random
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

session = requests.session()

# 添加线程锁，确保文件写入顺序
file_lock = threading.Lock()

def get_proxy_user_agent():
    user_agents = [
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
    proxies = [
        {"http": "8.140.235.207:9001"},
        {"http": "103.85.53.62:8080"},
        {"http": "103.85.53.62:8080"},
        {"http": "8.140.235.207:9001"},
        {"http": "121.230.8.229:1080"},
        {"http": "103.158.62.186:8088"},
        {"http": "101.132.222.120:80"},
        {"http": "183.60.141.41:443"},
        {"http": "58.216.109.14:800"},
        {"http": "118.113.133.135:9999"},
        {"http": "119.3.113.150:9094"},
        {"http": "119.3.113.152:9094"},
        {"http": "39.172.97.192:8060"},
        {"http": "123.128.12.93:9055"},
        {"http": "39.105.27.30:3128"},
        {"http": "116.62.230.32:3128"},
        {"http": "60.171.194.50:9300"},
        {"http": "39.172.97.192:8060"},
        {"http": "58.216.109.14:800"},
        {"http": "119.3.113.150:9094"},
        {"http": "8.219.97.248:80"},
        {"http": "118.178.197.213:3128"},
        {"http": "111.3.102.207:30001"},
        {"http": "47.98.123.255:8035"},
        {"http": "58.242.190.79:8095"},
        {"http": "119.3.113.151:9094"},
        {"http": "58.216.109.14:800"},
        {"http": "118.178.197.213:3128"},
        {"http": "58.216.109.17:800"},
        {"http": "101.132.222.120:80"},
        {"http": "103.85.53.62:8080"},
        {"http": "110.80.140.213:443"},
        {"http": "58.216.109.17:800"},
        {"http": "61.158.175.38:9002"},
        {"http": "119.3.113.152:9094"},
        {"http": "115.190.24.138:8080"},
        {"http": "116.62.230.32:3128"},
        {"http": "116.62.230.32:3128"},
    ]

    return {
        "headers": {
            "Referer": "https://www.bqg128.com/",
            "user-agent": random.choice(user_agents)
        },
        "proxy": random.choice(proxies)
    }

def fetch_single_chapter(chapter_info):
    """抓取单个章节内容，包括分页处理"""
    index, chapter_url, title = chapter_info
    basic_url = "https://www.biqugequ.org"
    config = get_proxy_user_agent()

    try:
        response = session.get(chapter_url, headers=config["headers"], proxies=config["proxy"], timeout=10)
        content_tree = etree.HTML(response.text)

        # 提取当前页面内容
        content = content_tree.xpath('//*[@id="content"]/p/text()')
        next_page_text = content_tree.xpath('//div[@class="bottem1"]/a[@id="pager_next"]/text()')
        next_page_href = content_tree.xpath('//div[@class="bottem1"]/a[@id="pager_next"]/@href')

        # 清理无效内容
        if content and '下一页' in content[-1]:
            content.pop()

        # 处理分页请求
        while next_page_text and '下一页' in next_page_text[0]:
            # 构建下一页URL
            if next_page_href:
                next_page_url = f"{basic_url}{next_page_href[0]}"

                # 发起分页请求
                response = session.get(next_page_url, headers=config["headers"], proxies=config["proxy"],
                                       timeout=10)
                content_tree = etree.HTML(response.text)

                # 提取分页内容
                page_content = content_tree.xpath('//*[@id="content"]/p/text()')
                if page_content and '下一页' in page_content[-1]:
                    page_content.pop()

                content.extend(page_content)
                # 更新分页信息
                next_page_text = content_tree.xpath('//div[@class="bottem1"]/a[@id="pager_next"]/text()')
                next_page_href = content_tree.xpath('//div[@class="bottem1"]/a[@id="pager_next"]/@href')
            else:
                break

        # 返回章节内容，保持索引以确保顺序
        filtered_content = [line.strip() for line in content if line.strip()]
        return index, title, filtered_content

    except Exception as e:
        print(f"章节 {title} 抓取失败: {e}")
        return index, title, []

def write_chapter_to_file(chapter_data, filename):
    """将章节内容写入文件，使用锁确保顺序写入"""
    index, title, content = chapter_data

    with file_lock:
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(title + '\n')
            file.write('\n'.join(content) + '\n\n')

def fetch_chapter_content(chapter_urls, titles):
    """使用并发方式抓取章节内容，同时保证写入顺序"""
    basic_url = "https://www.biqugequ.org"

    # 创建章节信息列表，包含索引以保持顺序
    chapter_info_list = [(i, chapter_urls[i], titles[i]) for i in range(len(chapter_urls))]

    # 使用线程池并发抓取章节内容
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 提交所有任务
        future_to_chapter = {executor.submit(fetch_single_chapter, info): info
                             for info in chapter_info_list}

        # 收集结果并按顺序存储
        results = {}
        with tqdm(total=len(chapter_urls), desc="章节进度", unit="章") as pbar:
            for future in as_completed(future_to_chapter):
                index, title, content = future.result()
                results[index] = (title, content)
                pbar.update(1)

                # 检查是否可以按顺序写入文件
                write_chapters_in_order(results, len(chapter_urls), '小说/仙逆.txt')

    # 确保所有章节都已写入
    write_chapters_in_order(results, len(chapter_urls), '小说/仙逆.txt')

def write_chapters_in_order(results, total_chapters, filename):
    """按顺序将已抓取的章节写入文件"""
    next_index = getattr(write_chapters_in_order, 'next_index', 0)

    while next_index < total_chapters and next_index in results:
        title, content = results[next_index]
        with file_lock:
            with open(filename, 'a', encoding='utf-8') as file:
                file.write(title + '\n')
                file.write('\n'.join(content) + '\n\n')
        next_index += 1

    # 更新下次开始写入的索引
    write_chapters_in_order.next_index = next_index

if __name__ == '__main__':
    # 创建存储目录
    if not exists('./小说'):
        os.mkdir('小说')

    # 初始化请求
    basic_url = "https://www.biqugequ.org"
    first_url = "https://www.biqugequ.org/xs_339/"

    config = get_proxy_user_agent()
    response = session.get(first_url, headers=config["headers"], proxies=config["proxy"], timeout=10)
    print('抓取页面完成')

    # 解析目录页
    page_tree = etree.HTML(response.text)
    titles = page_tree.xpath('//*[@id="list"]/dl/dd/a/@title')
    url_suffixes = page_tree.xpath('//*[@id="list"]/dl/dd/a/@href')
    chapter_urls = [basic_url + suffix for suffix in url_suffixes]

    print('开始抓取小说内容')
    fetch_chapter_content(chapter_urls, titles)
    print('小说抓取完成')
